import streamlit as st
from PyPDF2 import PdfReader
from skills import skills

st.title("AI Resume Analyzer")

uploaded_file = st.file_uploader(
    "Upload Resume (PDF)",
    type="pdf"
)

job_description = st.text_area(
    "Paste Job Description Here"
)

def extract_text(pdf):
    reader = PdfReader(pdf)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text.lower()

if uploaded_file and job_description:

    resume_text = extract_text(uploaded_file)

    resume_skills = []
    jd_skills = []

    for skill in skills:
        if skill in resume_text:
            resume_skills.append(skill)

        if skill in job_description.lower():
            jd_skills.append(skill)

    matched = list(set(resume_skills) & set(jd_skills))
    missing = list(set(jd_skills) - set(resume_skills))

    if len(jd_skills) > 0:
        score = (len(matched) / len(jd_skills)) * 100
    else:
        score = 0

    st.subheader("Resume Score")
    st.write(f"{score:.2f}%")

    st.subheader("Matched Skills")
    st.write(matched)

    st.subheader("Missing Skills")
    st.write(missing)

    st.subheader("Suggestions")

    if missing:
        for skill in missing:
            st.write(f"Learn or highlight: {skill}")
    else:
        st.success("Great! Your resume matches the job description.")