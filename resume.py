import streamlit as st
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader

st.set_page_config(
    page_title="Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

SKILLS_DB = [
    "python",
    "java",
    "c++",
    "sql",
    "aws",
    "docker",
    "git",
    "github",
    "machine learning",
    "deep learning",
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",
    "excel",
    "power bi",
    "tableau",
    "streamlit",
    "flask",
    "django"
]

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text is not None:
            text += page_text + " "

    return text.lower()

def find_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill.lower() in text:
            found_skills.append(skill)

    return found_skills

st.title("📄 Resume Analyzer")
st.write("Upload a resume and paste a job description.")

uploaded_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=200
)

if uploaded_file is not None and job_description:

    resume_text = extract_text_from_pdf(uploaded_file)

    resume_skills = find_skills(resume_text)

    jd_skills = find_skills(job_description.lower())

    matched_skills = []

    for skill in jd_skills:
        if skill in resume_skills:
            matched_skills.append(skill)

    missing_skills = []

    for skill in jd_skills:
        if skill not in resume_skills:
            missing_skills.append(skill)

    if len(jd_skills) > 0:
        ats_score = int(
            (len(matched_skills) / len(jd_skills)) * 100
        )
    else:
        ats_score = 0

    col1, col2, col3 = st.columns(3)

    col1.metric("ATS Score", f"{ats_score}%")
    col2.metric("Matched Skills", len(matched_skills))
    col3.metric("Missing Skills", len(missing_skills))

    chart_data = pd.DataFrame(
        {
            "Type": ["Matched", "Missing"],
            "Count": [
                len(matched_skills),
                len(missing_skills)
            ]
        }
    )

    fig = px.bar(
        chart_data,
        x="Type",
        y="Count",
        title="Skill Gap Analysis"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.subheader("Matched Skills")

    if len(matched_skills) > 0:
        st.success(", ".join(matched_skills))
    else:
        st.warning("No matched skills found.")

    st.subheader("Missing Skills")

    if len(missing_skills) > 0:
        st.error(", ".join(missing_skills))
    else:
        st.success("No missing skills.")

    st.subheader("Resume Feedback")

    if ats_score >= 80:
        st.success(
            "Excellent match for the role."
        )
    elif ats_score >= 60:
        st.warning(
            "Good match but can be improved."
        )
    else:
        st.error(
            "Low ATS score. Add more relevant skills."
        )

    report = f"""
Resume Analyzer Report

ATS Score: {ats_score}%

Matched Skills:
{", ".join(matched_skills)}

Missing Skills:
{", ".join(missing_skills)}
"""

    st.download_button(
        label="Download Report",
        data=report,
        file_name="resume_report.txt",
        mime="text/plain"
    )