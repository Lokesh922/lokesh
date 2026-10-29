import streamlit as st

st.set_page_config(
    page_title="ResumeAI Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
.stApp {
    background: #0b0d12;
    color: #f5f7fb;
}
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}
[data-testid="stFileUploader"] {
    background: #171b26;
    border: 1px dashed #454c60;
    border-radius: 14px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

st.title("ResumeAI")
st.caption("AI-powered resume analysis and ATS optimization")

left, right = st.columns([1, 1])

with left:
    st.subheader("Upload your resume")
    resume = st.file_uploader(
        "Upload PDF or DOCX",
        type=["pdf", "docx"]
    )

with right:
    st.subheader("Job description")
    job_description = st.text_area(
        "Paste the job description here",
        height=180,
        placeholder="Paste the target role's job description..."
    )

if st.button("Analyze Resume", type="primary", use_container_width=True):
    if resume is None:
        st.warning("Please upload your resume first.")
    elif not job_description.strip():
        st.warning("Please enter the job description.")
    else:
        st.success("Inputs received. Connect your resume analysis logic here.")

st.divider()

st.subheader("Analysis dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("ATS Match Score", "—", help="Calculated after analysis")

with col2:
    st.metric("Matched Skills", "—")

with col3:
    st.metric("Missing Skills", "—")

st.info("Upload a resume and enter a job description to begin.")
