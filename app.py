import re
from collections import Counter

import pandas as pd
import plotly.express as px
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(
page_title="Resume Analyzer Pro",
page_icon="📄",
layout="wide"
)

SKILLS_DB = [
"python","java","c++","sql","aws","azure","gcp",
"machine learning","deep learning","tensorflow",
"pytorch","docker","kubernetes","git","github",
"linux","data analysis","pandas","numpy",
"power bi","tableau","excel","flask","django",
"streamlit","nlp","computer vision"
]

def extract_pdf_text(uploaded_file):
reader = PdfReader(uploaded_file)
text = ""

```
for page in reader.pages:
    page_text = page.extract_text()
    if page_text:
        text += page_text + " "

return text.lower()
```

def extract_skills(text):
found = []

```
for skill in SKILLS_DB:
    if skill.lower() in text.lower():
        found.append(skill)

return sorted(list(set(found)))
```

def calculate_ats(resume_skills, jd_skills):
if len(jd_skills) == 0:
return 0

```
matched = set(resume_skills).intersection(set(jd_skills))

score = int((len(matched) / len(jd_skills)) * 100)

return score
```

st.title("📄 Resume Analyzer Pro")
st.caption("ATS Score • Skill Gap Analysis • Recruiter Feedback")

uploaded_resume = st.file_uploader(
"Upload Resume (PDF)",
type=["pdf"]
)

job_description = st.text_area(
"Paste Job Description",
height=250
)

if uploaded_resume and job_description:

```
resume_text = extract_pdf_text(uploaded_resume)

resume_skills = extract_skills(resume_text)

jd_skills = extract_skills(job_description)

matched = sorted(
    list(set(resume_skills).intersection(set(jd_skills)))
)

missing = sorted(
    list(set(jd_skills) - set(resume_skills))
)

ats_score = calculate_ats(
    resume_skills,
    jd_skills
)

job_fit = min(100, ats_score + 5)

st.divider()

c1, c2, c3, c4 = st.columns(4)

c1.metric("ATS Score", f"{ats_score}%")
c2.metric("Job Fit", f"{job_fit}%")
c3.metric("Matched Skills", len(matched))
c4.metric("Missing Skills", len(missing))

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("✅ Matched Skills")

    if matched:
        st.success(", ".join(matched))
    else:
        st.warning("No matching skills found.")

with col2:
    st.subheader("❌ Missing Skills")

    if missing:
        st.error(", ".join(missing))
    else:
        st.success("No missing skills detected.")

chart_df = pd.DataFrame({
    "Category": ["Matched", "Missing"],
    "Count": [len(matched), len(missing)]
})

fig = px.bar(
    chart_df,
    x="Category",
    y="Count",
    title="Skill Gap Analysis"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.subheader("📊 Resume Strengths")

strengths = []

if ats_score >= 70:
    strengths.append(
        "Strong keyword alignment with job description."
    )

if len(matched) >= 5:
    strengths.append(
        "Good skill coverage."
    )

if not strengths:
    strengths.append(
        "Resume contains relevant experience."
    )

for item in strengths:
    st.write("•", item)

st.subheader("⚠️ Resume Weaknesses")

weaknesses = []

if ats_score < 60:
    weaknesses.append(
        "Low ATS score."
    )

if len(missing) > 0:
    weaknesses.append(
        "Important skills are missing."
    )

if not weaknesses:
    weaknesses.append(
        "No major weaknesses detected."
    )

for item in weaknesses:
    st.write("•", item)

st.subheader("💡 Recommendations")

if missing:
    for skill in missing:
        st.write(
            f"• Add experience or keywords related to {skill}"
        )
else:
    st.write(
        "Resume is well aligned with the job description."
    )

st.subheader("👨‍💼 Recruiter Feedback")

if ats_score >= 80:
    st.success(
        "Likely to pass initial ATS screening."
    )
elif ats_score >= 60:
    st.warning(
        "Moderate fit. Improve missing skills."
    )
else:
    st.error(
        "Low compatibility for this role."
    )

st.subheader("🎯 Interview Questions")

for skill in matched[:5]:
    st.write(
        f"• Explain your experience with {skill}."
    )

report = f"""
```

Resume Analyzer Report

ATS Score: {ats_score}%
Job Fit: {job_fit}%

Matched Skills:
{", ".join(matched)}

Missing Skills:
{", ".join(missing)}

Recommendations:
{chr(10).join([f"- Add {s}" for s in missing])}
"""

```
st.download_button(
    "📥 Download Report",
    report,
    file_name="resume_report.txt"
)
```
