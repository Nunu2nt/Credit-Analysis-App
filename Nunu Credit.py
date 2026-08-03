# Path: credit-analysis-app/app.py

import streamlit as st

# 1. Page Configuration (MUST be the first Streamlit command)
st.set_page_config(
    page_title="Professional Credit Analysis Platform",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Custom CSS Injection for Professional Financial Styling
st.markdown("""
    <style>
        /* Main background and clean text styling */
        .main {
            background-color: #F8F9FA;
        }
        /* Sidebar custom branding */
        [data-testid="stSidebar"] {
            background-color: #FFFFFF;
            border-right: 1px solid #E2E8F0;
        }
        /* Title color styling */
        h1, h2, h3 {
            color: #1E293B;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Dynamic Imports of Page Modules
try:
    from modules.personal_loan import render_personal_loan_dashboard
    from modules.corporate_loan import render_corporate_loan_dashboard
    from modules.report_generator import render_report_dashboard
except ModuleNotFoundError as e:
    st.error(f"❌ Module Import Error: Check if your 'modules/' folder contains '__init__.py'. Details: {e}")
    st.stop()

# 4. Sidebar Navigation Header
st.sidebar.markdown("## 🏦 ระบบวิเคราะห์สินเชื่อ")
st.sidebar.caption("Financial Analysis & Credit Scoring Engine")
st.sidebar.markdown("---")

# 5. Radio Menu Navigation
selected_menu = st.sidebar.radio(
    "เลือกประเภทการวิเคราะห์ (Select Analysis):",
    [
        "วิเคราะห์สินเชื่อบุคคล (Personal Loan)",
        "วิเคราะห์สินเชื่อนิติบุคคล/ธุรกิจ (Corporate Loan)",
        "สรุปรายงานการอนุมัติ (Credit Memo & PDF)"
    ],
    index=0
)

st.sidebar.markdown("---")

# 6. Sidebar System Status Indicator
st.sidebar.markdown("### ⚙️ System Status")
st.sidebar.success("Engine: Active (v1.0.0 Pro)")
st.sidebar.info("PDF Engine: ReportLab Ready")

# 7. Router: Render pages based on user selection
if selected_menu == "วิเคราะห์สินเชื่อบุคคล (Personal Loan)":
    render_personal_loan_dashboard()

elif selected_menu == "วิเคราะห์สินเชื่อนิติบุคคล/ธุรกิจ (Corporate Loan)":
    render_corporate_loan_dashboard()

elif selected_menu == "สรุปรายงานการอนุมัติ (Credit Memo & PDF)":
    render_report_dashboard()
    