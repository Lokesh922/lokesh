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
"Upload Resume PDF",
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

c1, c2, c3, c4 = st.columns(4)

c1.metric("ATS Score", f"{ats_score}%")
c2.metric("Job Fit", f"{job_fit}%")
c3.metric("Matched Skills", len(matched))
c4.metric("Missing Skills", len(missing))

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

st.subheader("Matched Skills")
st.write(matched)

st.subheader("Missing Skills")
st.write(missing)

report = f"""
```

ATS Score: {ats_score}%

Matched Skills:
{', '.join(matched)}

Missing Skills:
{', '.join(missing)}
"""

```
st.download_button(
    "Download Report",
    report,
    file_name="resume_report.txt"
)
```
