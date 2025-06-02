import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Set page configuration
st.set_page_config(page_title="TikTok Ads Performance Analyzer", layout="wide")

# Translation dictionaries
translations = {
    "en": {
        "title": "TikTok Ads Performance Analyzer",
        "instructions": """
        Upload an Excel file containing TikTok Ads data. Required columns:
        - Date Created
        - Ad name
        - Impressions
        - Clicks (destination)
        - Cost
        - Conversions
        Optional columns (for enhanced insights):
        - Video views
        - 2-second video views
        - 6-second video views
        - Video views at 100%
        - Average play time per video view
        - Landing page views (website)
        - Landing page view rate (website)
        """,
        "upload_label": "Upload Excel file",
        "columns_found": "Columns found",
        "missing_columns": "Missing required columns: {columns}",
        "invalid_dates": "Some dates in 'Date Created' could not be parsed. Please ensure all dates are valid (e.g., YYYY-MM-DD).",
        "invalid_rows": "Sample invalid rows:",
        "empty_data": "No valid data remains after filtering invalid dates.",
        "processing_error": "Error processing file: {error}",
        "processing_check": "Please check the file format and data, then try again.",
        "summary_header": "Performance Summary",
        "ad_performance_header": "Ad Performance",
        "visual_insights_header": "Visual Insights",
        "suggestions_header": "Optimization Suggestions",
        "no_suggestions": "No specific optimization suggestions at this time.",
        "metrics": {
            "total_impressions": "Total Impressions",
            "total_clicks": "Total Clicks",
            "total_cost": "Total Cost",
            "total_conversions": "Total Conversions",
            "total_video_views": "Total Video Views",
            "total_landing_page_views": "Total Landing Page Views",
            "avg_ctr": "Average CTR",
            "avg_cpm": "Average CPM",
            "avg_conversion_rate": "Average Conversion Rate",
            "avg_cost_per_conversion": "Average Cost per Conversion",
            "avg_6s_view_rate": "Average 6s Video View Rate",
            "avg_landing_page_view_rate": "Average Landing Page View Rate"
        },
        "chart_titles": {
            "impressions_clicks": "Impressions and Clicks Over Time",
            "performance_metrics": "Performance Metrics by Ad",
            "cost_distribution": "Cost Distribution by Ad",
            "video_engagement": "Video Engagement by Ad"
        },
        "chart_labels": {
            "date": "Date",
            "impressions": "Impressions",
            "clicks": "Clicks",
            "ad_name": "Ad Name",
            "percentage": "Percentage (%)",
            "cost": "Cost",
            "count": "Count",
            "ctr": "CTR (%)",
            "conversion_rate": "Conversion Rate (%)",
            "6s_view_rate": "6s Video View Rate (%)",
            "landing_page_view_rate": "Landing Page View Rate (%)",
            "video_views": "Video Views",
            "6s_video_views": "6s Video Views"
        },
        "suggestions": {
            "low_ctr": {"issue": "Low campaign CTR", "text": "Average CTR is below 1%. Test TikTok-native formats like Spark Ads or refine audience targeting."},
            "high_cpm": {"issue": "High CPM", "text": "Average CPM exceeds $10. Consider CPC or oCPM bidding strategies."},
            "low_conversion_rate": {"issue": "Low conversion rate", "text": "Conversion rate is below 2%. Optimize landing pages for mobile and ensure clear CTAs."},
            "high_cost_per_conversion": {"issue": "High cost per conversion", "text": "Cost per conversion is high. Pause low-performing ads and reallocate budget."},
            "low_6s_view_rate": {"issue": "Low 6-second video view rate", "text": "Average 6-second video view rate is below 10%. Improve video hooks in the first 3 seconds."},
            "low_landing_page_view_rate": {"issue": "Low landing page view rate", "text": "Average landing page view rate is below 20%. Enhance ad creatives or landing page relevance."},
            "ad_low_ctr": {"issue": "Low ad CTR", "text": "Ad '{ad_name}': Low CTR ({ctr}%). Test new visuals or ad copy."},
            "ad_low_6s_view_rate": {"issue": "Low ad 6-second view rate", "text": "Ad '{ad_name}': Low 6-second view rate ({rate}%). Shorten intros or add engaging hooks."},
            "ad_low_landing_page_view_rate": {"issue": "Low ad landing page view rate", "text": "Ad '{ad_name}': Low landing page view rate ({rate}%). Ensure ad and landing page alignment."}
        },
        "suggestions_table": {
            "ad_name": "Ad Name",
            "issue": "Issue",
            "suggestion": "Suggestion",
            "priority": "Priority",
            "general": "General",
            "high": "High",
            "medium": "Medium",
            "low": "Low"
        },
        "language_label": "Language",
        "english": "English",
        "arabic": "Arabic"
    },
    "ar": {
        "title": "محلل أداء إعلانات تيك توك",
        "instructions": """
        قم برفع ملف إكسل يحتوي على بيانات إعلانات تيك توك. الأعمدة المطلوبة:
        - تاريخ الإنشاء
        - اسم الإعلان
        - الانطباعات
        - النقرات (الوجهة)
        - التكلفة
        - التحويلات
        الأعمدة الاختيارية (لرؤى محسنة):
        - مشاهدات الفيديو
        - مشاهدات الفيديو لمدة ثانيتين
        - مشاهدات الفيديو لمدة 6 ثوانٍ
        - مشاهدات الفيديو بنسبة 100%
        - متوسط وقت التشغيل لكل مشاهدة فيديو
        - مشاهدات صفحة الهبوط (الموقع)
        - معدل مشاهدة صفحة الهبوط (الموقع)
        """,
        "upload_label": "رفع ملف إكسل",
        "columns_found": "الأعمدة الموجودة",
        "missing_columns": "الأعمدة المطلوبة المفقودة: {columns}",
        "invalid_dates": "تعذر تحليل بعض التواريخ في 'تاريخ الإنشاء'. يرجى التأكد من أن جميع التواريخ صالحة (مثل، YYYY-MM-DD).",
        "invalid_rows": "عينة من الصفوف غير الصالحة:",
        "empty_data": "لا توجد بيانات صالحة متبقية بعد تصفية التواريخ غير الصالحة.",
        "processing_error": "خطأ في معالجة الملف: {error}",
        "processing_check": "يرجى التحقق من تنسيق الملف والبيانات، ثم حاول مرة أخرى.",
        "summary_header": "ملخص الأداء",
        "ad_performance_header": "أداء الإعلان",
        "visual_insights_header": "رؤى بصرية",
        "suggestions_header": "اقتراحات التحسين",
        "no_suggestions": "لا توجد اقتراحات تحسين محددة في الوقت الحالي.",
        "metrics": {
            "total_impressions": "إجمالي الانطباعات",
            "total_clicks": "إجمالي النقرات",
            "total_cost": "إجمالي التكلفة",
            "total_conversions": "إجمالي التحويلات",
            "total_video_views": "إجمالي مشاهدات الفيديو",
            "total_landing_page_views": "إجمالي مشاهدات صفحة الهبوط",
            "avg_ctr": "متوسط نسبة النقر إلى الظهور",
            "avg_cpm": "متوسط التكلفة لكل ألف ظهور",
            "avg_conversion_rate": "متوسط معدل التحويل",
            "avg_cost_per_conversion": "متوسط التكلفة لكل تحويل",
            "avg_6s_view_rate": "متوسط معدل مشاهدة الفيديو لمدة 6 ثوانٍ",
            "avg_landing_page_view_rate": "متوسط معدل مشاهدة صفحة الهبوط"
        },
        "chart_titles": {
            "impressions_clicks": "الانطباعات والنقرات عبر الزمن",
            "performance_metrics": "مقاييس الأداء حسب الإعلان",
            "cost_distribution": "توزيع التكلفة حسب الإعلان",
            "video_engagement": "تفاعل الفيديو حسب الإعلان"
        },
        "chart_labels": {
            "date": "التاريخ",
            "impressions": "الانطباعات",
            "clicks": "النقرات",
            "ad_name": "اسم الإعلان",
            "percentage": "النسبة المئوية (%)",
            "cost": "التكلفة",
            "count": "العدد",
            "ctr": "نسبة النقر إلى الظهور (%)",
            "conversion_rate": "معدل التحويل (%)",
            "6s_view_rate": "معدل مشاهدة الفيديو لمدة 6 ثوانٍ (%)",
            "landing_page_view_rate": "معدل مشاهدة صفحة الهبوط (%)",
            "video_views": "مشاهدات الفيديو",
            "6s_video_views": "مشاهدات الفيديو لمدة 6 ثوانٍ"
        },
        "suggestions": {
            "low_ctr": {"issue": "نسبة نقر إلى ظهور منخفضة للحملة", "text": "متوسط نسبة النقر إلى الظهور أقل من 1%. جرب تنسيقات تيك توك الأصلية مثل Spark Ads أو قم بتحسين استهداف الجمهور."},
            "high_cpm": {"issue": "تكلفة مرتفعة لكل ألف ظهور", "text": "متوسط التكلفة لكل ألف ظهور يتجاوز 10 دولارات. فكر في استراتيجيات العطاء بناءً على التكلفة لكل نقرة أو التكلفة المثلى لكل ألف ظهور."},
            "low_conversion_rate": {"issue": "معدل تحويل منخفض", "text": "معدل التحويل أقل من 2%. قم بتحسين صفحات الهبوط للأجهزة المحمولة وتأكد من وضوح دعوات الإجراء."},
            "high_cost_per_conversion": {"issue": "تكلفة مرتفعة لكل تحويل", "text": "تكلفة التحويل مرتفعة. أوقف الإعلانات ذات الأداء المنخفض وأعد تخصيص الميزانية."},
            "low_6s_view_rate": {"issue": "معدل مشاهدة فيديو منخفض لمدة 6 ثوانٍ", "text": "متوسط معدل مشاهدة الفيديو لمدة 6 ثوانٍ أقل من 10%. حسّن خطافات الفيديو في أول 3 ثوانٍ."},
            "low_landing_page_view_rate": {"issue": "معدل مشاهدة صفحة هبوط منخفض", "text": "متوسط معدل مشاهدة صفحة الهبوط أقل من 20%. عزز الإبداعات الإعلانية أو صلة صفحة الهبوط."},
            "ad_low_ctr": {"issue": "نسبة نقر إلى ظهور منخفضة للإعلان", "text": "الإعلان '{ad_name}': نسبة نقر إلى ظهور منخفضة ({ctr}%). جرب صورًا بصرية أو نصوص إعلانية جديدة."},
            "ad_low_6s_view_rate": {"issue": "معدل مشاهدة فيديو منخفض للإعلان لمدة 6 ثوانٍ", "text": "الإعلان '{ad_name}': معدل مشاهدة الفيديو لمدة 6 ثوانٍ منخفض ({rate}%). قم بتقصير المقدمات أو أضف خطافات جذابة."},
            "ad_low_landing_page_view_rate": {"issue": "معدل مشاهدة صفحة هبوط منخفض للإعلان", "text": "الإعلان '{ad_name}': معدل مشاهدة صفحة الهبوط منخفض ({rate}%). تأكد من توافق الإعلان وصفحة الهبوط."}
        },
        "suggestions_table": {
            "ad_name": "اسم الإعلان",
            "issue": "المشكلة",
            "suggestion": "الاقتراح",
            "priority": "الأولوية",
            "general": "عام",
            "high": "عالية",
            "medium": "متوسطة",
            "low": "منخفضة"
        },
        "language_label": "اللغة",
        "english": "الإنجليزية",
        "arabic": "العربية"
    }
}

def main():
    # Mobile-friendly CSS
    st.markdown("""
    <style>
    /* General responsive styles */
    body, .stApp {
        font-size: 16px;
    }
    @media (max-width: 600px) {
        body, .stApp, .stMarkdown, .stText, .stHeader, .stSubheader, .stMetric, .stDataFrame {
            font-size: 14px;
        }
        .stMetric label {
            font-size: 12px;
        }
        .stPlotlyChart {
            width: 100% !important;
            height: 300px !important;
        }
        .stDataFrame {
            font-size: 12px;
        }
        .stRadio > div {
            flex-wrap: wrap;
        }
    }
    /* Arabic RTL styles */
    [dir="rtl"] body, [dir="rtl"] .stApp, [dir="rtl"] .stMarkdown, [dir="rtl"] .stText, [dir="rtl"] .stHeader, [dir="rtl"] .stSubheader, [dir="rtl"] .stMetric, [dir="rtl"] .stDataFrame {
        direction: rtl;
        text-align: right;
        font-family: 'Amiri', serif;
    }
    [dir="rtl"] .stRadio > div {
        flex-direction: row-reverse;
    }
    [dir="rtl"] .stRadio > div > label {
        margin-left: 10px;
        margin-right: 5px;
    }
    /* Ensure columns stack on mobile */
    .css-1l02zno { /* Streamlit column container */
        flex-direction: column !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Language selection
    language = st.sidebar.radio(
        translations["en"]["language_label"],
        (translations["en"]["english"], translations["en"]["arabic"]),
        format_func=lambda x: translations["ar"]["arabic"] if x == translations["en"]["arabic"] else x
    )
    lang_code = "ar" if language == translations["en"]["arabic"] else "en"
    t = translations[lang_code]

    # Set RTL for Arabic
    if lang_code == "ar":
        st.markdown('<div dir="rtl">', unsafe_allow_html=True)

    # Main content
    st.title(t["title"])
    st.markdown(t["instructions"])

    uploaded_file = st.file_uploader(t["upload_label"], type=["xls", "xlsx"])

    if uploaded_file:
        try:
            with st.spinner("Processing file..." if lang_code == "en" else "جارٍ معالجة الملف..."):
                df = pd.read_excel(uploaded_file)

                # Remove total row if present
                df = df[df['Ad name'] != 'Total of 51 results'].copy()

                # Log columns for debugging
                original_columns = df.columns.tolist()
                st.write(f"**{t['columns_found']}**: {', '.join(original_columns)}")

                # Normalize column names
                df.columns = df.columns.str.strip().str.lower()
                column_map = {col.lower(): col for col in original_columns}

                # Check required columns
                required_columns = ['date created', 'ad name', 'impressions', 'clicks (destination)', 'cost', 'conversions']
                missing_columns = [column_map.get(col, col) for col in required_columns if col not in df.columns]
                if missing_columns:
                    st.error(t["missing_columns"].format(columns=', '.join(missing_columns)))
                    return

                # Check optional columns
                optional_columns = [
                    'video views', '2-second video views', '6-second video views', 'video views at 100%',
                    'average play time per video view', 'landing page views (website)', 'landing page view rate (website)'
                ]
                available_optional = [col for col in optional_columns if col in df.columns]

                # Restore original column names
                df.columns = [column_map[col.lower()] for col in df.columns]

                # Clean and parse dates
                df = df[df['Date Created'].notna() & (df['Date Created'] != '-')].copy()
                df['Date Created'] = pd.to_datetime(df['Date Created'], format='mixed', errors='coerce', dayfirst=True)
                if df['Date Created'].isna().any():
                    st.error(t["invalid_dates"])
                    invalid_rows = df[df['Date Created'].isna()][['Ad name', 'Date Created']].head()
                    st.write(t["invalid_rows"], invalid_rows)
                    return

                if df.empty:
                    st.error(t["empty_data"])
                    return

                # Convert numeric columns
                numeric_cols = [
                    'Impressions', 'Clicks (destination)', 'Cost', 'Conversions',
                    'Video views', '2-second video views', '6-second video views', 'Video views at 100%',
                    'Average play time per video view', 'Landing page views (website)', 'Landing page view rate (website)'
                ]
                for col in numeric_cols:
                    if col in df.columns:
                        df[col] = pd.to_numeric(df[col], errors='coerce')

                # Calculate KPIs
                df['CTR (destination)'] = (df['Clicks (destination)'] / df['Impressions'] * 100).round(2)
                df['CPM'] = (df['Cost'] / (df['Impressions'] / 1000)).round(2)
                df['Conversion rate (CVR)'] = (df['Conversions'] / df['Clicks (destination)'] * 100).round(2)
                df['Cost per conversion'] = (df['Cost'] / df['Conversions']).where(df['Conversions'] > 0, np.inf).round(2)
                if 'Video views' in df.columns and '6-second video views' in df.columns:
                    df['6-second view rate'] = (df['6-second video views'] / df['Video views'] * 100).round(2)
                if 'Landing page views (website)' in df.columns:
                    df['Cost per landing page view'] = (df['Cost'] / df['Landing page views (website)']).where(df['Landing page views (website)'] > 0, np.inf).round(2)

                # Summary metrics
                summary = {
                    'total_impressions': int(df['Impressions'].sum() or 0),
                    'total_clicks': int(df['Clicks (destination)'].sum() or 0),
                    'total_cost': round(float(df['Cost'].sum() or 0), 2),
                    'total_conversions': int(df['Conversions'].sum() or 0),
                    'avg_ctr': round(float(df['CTR (destination)'].mean() or 0), 2),
                    'avg_cpm': round(float(df['CPM'].mean() or 0), 2),
                    'avg_conversion_rate': round(float(df['Conversion rate (CVR)'].mean() or 0), 2),
                    'avg_cost_per_conversion': round(float(df['Cost per conversion'].replace(np.inf, 0).mean()), 2),
                }
                if 'Video views' in df.columns:
                    summary['total_video_views'] = int(df['Video views'].sum() or 0)
                    summary['avg_6s_view_rate'] = round(float(df['6-second view rate'].mean() or 0), 2) if '6-second view rate' in df.columns else 0
                if 'Average play time per video view' in df.columns:
                    summary['avg_play_time'] = round(float(df['Average play time per video view'].mean() or 0), 2)
                if 'Landing page views (website)' in df.columns:
                    summary['total_landing_page_views'] = int(df['Landing page views (website)'].sum() or 0)
                    summary['avg_landing_page_view_rate'] = round(float(df['Landing page view rate (website)'].mean() or 0), 2)
                    summary['avg_cost_per_landing_page_view'] = round(float(df['Cost per landing page view'].replace(np.inf, 0).mean()), 2)

                # Ad summary table
                agg_dict = {
                    'Impressions': 'sum',
                    'Clicks (destination)': 'sum',
                    'Cost': 'sum',
                    'Conversions': 'sum',
                    'CTR (destination)': 'mean',
                    'CPM': 'mean',
                    'Conversion rate (CVR)': 'mean',
                    'Cost per conversion': lambda x: round(float(x.replace(np.inf, 0).mean()), 2),
                }
                if 'Video views' in df.columns:
                    agg_dict['Video views'] = 'sum'
                    agg_dict['6-second video views'] = 'sum'
                    agg_dict['6-second view rate'] = 'mean'
                if 'Average play time per video view' in df.columns:
                    agg_dict['Average play time per video view'] = 'mean'
                if 'Landing page views (website)' in df.columns:
                    agg_dict['Landing page views (website)'] = 'sum'
                    agg_dict['Landing page view rate (website)'] = 'mean'
                    agg_dict['Cost per landing page view'] = lambda x: round(float(x.replace(np.inf, 0).mean()), 2)

                ad_summary = df.groupby('Ad name').agg(agg_dict).reset_index().round(2)

                # Display Summary
                st.header(t["summary_header"])
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.metric(t["metrics"]["total_impressions"], f"{summary['total_impressions']:,}")
                    st.metric(t["metrics"]["total_clicks"], f"{summary['total_clicks']:,}")
                    st.metric(t["metrics"]["total_cost"], f"${summary['total_cost']:,}")
                    st.metric(t["metrics"]["total_conversions"], f"{summary['total_conversions']:,}")
                    if 'total_video_views' in summary:
                        st.metric(t["metrics"]["total_video_views"], f"{summary['total_video_views']:,}")
                    if 'total_landing_page_views' in summary:
                        st.metric(t["metrics"]["total_landing_page_views"], f"{summary['total_landing_page_views']:,}")
                with col2:
                    st.metric(t["metrics"]["avg_ctr"], f"{summary['avg_ctr']}%")
                    st.metric(t["metrics"]["avg_cpm"], f"${summary['avg_cpm']}")
                    st.metric(t["metrics"]["avg_conversion_rate"], f"{summary['avg_conversion_rate']}%")
                    st.metric(t["metrics"]["avg_cost_per_conversion"], f"${summary['avg_cost_per_conversion']}")
                    if 'avg_6s_view_rate' in summary:
                        st.metric(t["metrics"]["avg_6s_view_rate"], f"{summary['avg_6s_view_rate']}%")
                    if 'avg_landing_page_view_rate' in summary:
                        st.metric(t["metrics"]["avg_landing_page_view_rate"], f"{summary['avg_landing_page_view_rate']}%")

                # Display Ad Summary Table
                st.header(t["ad_performance_header"])
                st.dataframe(ad_summary, use_container_width=True)

                # Generate Charts
                st.header(t["visual_insights_header"])
                # 1. Impressions and Clicks over Time
                time_data = df.groupby('Date Created').agg({
                    'Impressions': 'sum',
                    'Clicks (destination)': 'sum'
                }).reset_index()
                if not time_data.empty:
                    fig1 = go.Figure()
                    fig1.add_trace(go.Scatter(x=time_data['Date Created'], y=time_data['Impressions'], name=t["chart_labels"]["impressions"], mode='lines+markers'))
                    fig1.add_trace(go.Scatter(x=time_data['Date Created'], y=time_data['Clicks (destination)'], name=t["chart_labels"]["clicks"], mode='lines+markers', yaxis='y2'))
                    fig1.update_layout(
                        title=t["chart_titles"]["impressions_clicks"],
                        xaxis_title=t["chart_labels"]["date"],
                        yaxis_title=t["chart_labels"]["impressions"],
                        yaxis2=dict(title=t["chart_labels"]["clicks"], overlaying='y', side='right'),
                        height=400
                    )
                    st.plotly_chart(fig1, use_container_width=True)

                # 2. Performance Metrics by Ad
                ad_metrics = df.groupby('Ad name')[['CTR (destination)', 'Conversion rate (CVR)']].mean().reset_index()
                if '6-second view rate' in df.columns:
                    ad_metrics['6-second view rate'] = df.groupby('Ad name')['6-second view rate'].mean().values
                if 'Landing page view rate (website)' in df.columns:
                    ad_metrics['Landing page view rate (website)'] = df.groupby('Ad name')['Landing page view rate (website)'].mean().values
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(x=ad_metrics['Ad name'], y=ad_metrics['CTR (destination)'], name=t["chart_labels"]["ctr"]))
                fig2.add_trace(go.Bar(x=ad_metrics['Ad name'], y=ad_metrics['Conversion rate (CVR)'], name=t["chart_labels"]["conversion_rate"]))
                if '6-second view rate' in ad_metrics.columns:
                    fig2.add_trace(go.Bar(x=ad_metrics['Ad name'], y=ad_metrics['6-second view rate'], name=t["chart_labels"]["6s_view_rate"]))
                if 'Landing page view rate (website)' in ad_metrics.columns:
                    fig2.add_trace(go.Bar(x=ad_metrics['Ad name'], y=ad_metrics['Landing page view rate (website)'], name=t["chart_labels"]["landing_page_view_rate"]))
                fig2.update_layout(
                    title=t["chart_titles"]["performance_metrics"],
                    xaxis_title=t["chart_labels"]["ad_name"],
                    yaxis_title=t["chart_labels"]["percentage"],
                    barmode='group',
                    height=400
                )
                st.plotly_chart(fig2, use_container_width=True)

                # 3. Cost Distribution by Ad
                cost_data = df.groupby('Ad name')['Cost'].sum().reset_index()
                if not cost_data.empty:
                    fig3 = px.pie(cost_data, values='Cost', names='Ad name', title=t["chart_titles"]["cost_distribution"])
                    fig3.update_layout(height=400)
                    st.plotly_chart(fig3, use_container_width=True)

                # 4. Video Engagement by Ad
                if 'Video views' in df.columns and '6-second video views' in df.columns:
                    video_data = df.groupby('Ad name')[['Video views', '6-second video views']].sum().reset_index()
                    fig4 = go.Figure()
                    fig4.add_trace(go.Bar(x=video_data['Ad name'], y=video_data['Video views'], name=t["chart_labels"]["video_views"]))
                    fig4.add_trace(go.Bar(x=video_data['Ad name'], y=video_data['6-second video views'], name=t["chart_labels"]["6s_video_views"]))
                    fig4.update_layout(
                        title=t["chart_titles"]["video_engagement"],
                        xaxis_title=t["chart_labels"]["ad_name"],
                        yaxis_title=t["chart_labels"]["count"],
                        barmode='group',
                        height=400
                    )
                    st.plotly_chart(fig4, use_container_width=True)

                # Optimization Suggestions Table
                st.header(t["suggestions_header"])
                suggestions = []
                if summary['avg_ctr'] < 1:
                    priority = t["suggestions_table"]["high"] if summary['avg_ctr'] < 0.5 else t["suggestions_table"]["medium"]
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["low_ctr"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["low_ctr"]["text"],
                        t["suggestions_table"]["priority"]: priority
                    })
                if summary['avg_cpm'] > 10:
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["high_cpm"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["high_cpm"]["text"],
                        t["suggestions_table"]["priority"]: t["suggestions_table"]["medium"]
                    })
                if summary['avg_conversion_rate'] < 2:
                    priority = t["suggestions_table"]["high"] if summary['avg_conversion_rate'] < 1 else t["suggestions_table"]["medium"]
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["low_conversion_rate"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["low_conversion_rate"]["text"],
                        t["suggestions_table"]["priority"]: priority
                    })
                if summary['avg_cost_per_conversion'] > 50:
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["high_cost_per_conversion"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["high_cost_per_conversion"]["text"],
                        t["suggestions_table"]["priority"]: t["suggestions_table"]["high"]
                    })
                if 'avg_6s_view_rate' in summary and summary['avg_6s_view_rate'] < 10:
                    priority = t["suggestions_table"]["high"] if summary['avg_6s_view_rate'] < 5 else t["suggestions_table"]["medium"]
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["low_6s_view_rate"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["low_6s_view_rate"]["text"],
                        t["suggestions_table"]["priority"]: priority
                    })
                if 'avg_landing_page_view_rate' in summary and summary['avg_landing_page_view_rate'] < 20:
                    suggestions.append({
                        t["suggestions_table"]["ad_name"]: t["suggestions_table"]["general"],
                        t["suggestions_table"]["issue"]: t["suggestions"]["low_landing_page_view_rate"]["issue"],
                        t["suggestions_table"]["suggestion"]: t["suggestions"]["low_landing_page_view_rate"]["text"],
                        t["suggestions_table"]["priority"]: t["suggestions_table"]["high"]
                    })
                for _, ad in ad_summary.iterrows():
                    if ad['CTR (destination)'] < 1:
                        priority = t["suggestions_table"]["high"] if ad['CTR (destination)'] < 0.5 else t["suggestions_table"]["medium"]
                        suggestions.append({
                            t["suggestions_table"]["ad_name"]: ad['Ad name'],
                            t["suggestions_table"]["issue"]: t["suggestions"]["ad_low_ctr"]["issue"],
                            t["suggestions_table"]["suggestion"]: t["suggestions"]["ad_low_ctr"]["text"].format(ad_name=ad['Ad name'], ctr=ad['CTR (destination)']),
                            t["suggestions_table"]["priority"]: priority
                        })
                    if '6-second view rate' in ad and ad['6-second view rate'] < 10:
                        priority = t["suggestions_table"]["high"] if ad['6-second view rate'] < 5 else t["suggestions_table"]["medium"]
                        suggestions.append({
                            t["suggestions_table"]["ad_name"]: ad['Ad name'],
                            t["suggestions_table"]["issue"]: t["suggestions"]["ad_low_6s_view_rate"]["issue"],
                            t["suggestions_table"]["suggestion"]: t["suggestions"]["ad_low_6s_view_rate"]["text"].format(ad_name=ad['Ad name'], rate=ad['6-second view rate']),
                            t["suggestions_table"]["priority"]: priority
                        })
                    if 'Landing page views (website)' in ad and ad['Landing page view rate (website)'] < 20:
                        suggestions.append({
                            t["suggestions_table"]["ad_name"]: ad['Ad name'],
                            t["suggestions_table"]["issue"]: t["suggestions"]["ad_low_landing_page_view_rate"]["issue"],
                            t["suggestions_table"]["suggestion"]: t["suggestions"]["ad_low_landing_page_view_rate"]["text"].format(ad_name=ad['Ad name'], rate=ad['Landing page view rate (website)']),
                            t["suggestions_table"]["priority"]: t["suggestions_table"]["high"]
                        })

                if suggestions:
                    suggestions_df = pd.DataFrame(suggestions)
                    st.dataframe(suggestions_df, use_container_width=True)
                else:
                    st.markdown(t["no_suggestions"])

        except Exception as e:
            st.error(t["processing_error"].format(error=str(e)))
            st.markdown(t["processing_check"])

    # Close RTL div for Arabic
    if lang_code == "ar":
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()