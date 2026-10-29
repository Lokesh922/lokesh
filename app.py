
import streamlit as st
import pandas as pd
import plotly.express as px
from PyPDF2 import PdfReader

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="ResumeAI | Resume Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
    .stApp {
        background-color: #f4f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(120deg, #101c3a, #244b91);
        padding: 35px;
        border-radius: 18px;
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
    }

    .hero p {
        color: #dce7ff;
        font-size: 16px;
    }

    .section-card {
        background: white;
        padding: 24px;
        border-radius: 15px;
        border: 1px solid #e3e9f2;
        margin-bottom: 20px;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 20px;
        border-radius: 14px;
        border: 1px solid #e3e9f2;
    }

    div.stButton > button {
        background: linear-gradient(90deg, #2563eb, #4f46e5);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 25px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        min-height: 48px;
    }

    div.stButton > button:hover {
        background: #1d4ed8;
        color: white;
        border: none;
    }

    h2, h3 {
        color: #172554;
    }

    .footer {
        text-align: center;
        color: #718096;
        padding: 25px 0 5px 0;
        font-size: 13px;
    }

    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 12px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SKILLS DATABASE ----------------

SKILLS_DB = [
    "python", "java", "c++", "sql", "aws",
    "docker", "git", "github", "machine learning",
    "deep learning", "tensorflow", "pytorch",
    "pandas", "numpy", "excel", "power bi",
    "tableau", "streamlit", "flask", "django",
    "scikit-learn", "html", "css", "javascript",
    "react", "node.js", "mongodb", "mysql",
    "postgresql", "data analysis", "data science",
    "artificial intelligence", "nlp", "computer vision",
    "rest api", "linux", "fastapi", "azure",
    "google cloud", "communication", "problem solving"
]


# ---------------- FUNCTIONS ----------------

def extract_text_from_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + " "

    return text.lower()


def find_skills(text):
    found_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            found_skills.append(skill)

    return found_skills


def analyze_resume(resume_text, job_description):
    resume_skills = find_skills(resume_text)
    jd_skills = find_skills(job_description.lower())

    matched_skills = [
        skill for skill in jd_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in jd_skills
        if skill not in resume_skills
    ]

    if jd_skills:
        ats_score = round(
            len(matched_skills) / len(jd_skills) * 100
        )
    else:
        ats_score = 0

    return (
        ats_score,
        resume_skills,
        jd_skills,
        matched_skills,
        missing_skills
    )


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <h1>📄 ResumeAI</h1>
    <p>Smart Resume Analyzer &nbsp; | &nbsp;
    Skill Gap Analysis &nbsp; | &nbsp;
    Career Readiness</p>
    <p>Discover how well your resume matches your target job.
    Identify missing skills and improve your application.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- INPUT SECTION ----------------

st.markdown("## Analyze Your Resume")
st.write(
    "Upload your resume, provide the job description, "
    "and click Analyze Resume to generate your report."
)

left, right = st.columns(2, gap="large")

with left:
    st.markdown("### 📎 Upload Resume")

    uploaded_file = st.file_uploader(
        "Choose your resume in PDF format",
        type=["pdf"],
        help="Upload a text-based PDF resume."
    )

    if uploaded_file:
        st.success(f"Uploaded: {uploaded_file.name}")

with right:
    st.markdown("### 💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=180,
        placeholder=(
            "Example: We are looking for a Python developer "
            "with SQL, machine learning, pandas and Git skills..."
        ),
        label_visibility="collapsed"
    )

st.markdown("")

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)


# ---------------- ANALYSIS ----------------

if analyze_button:

    if uploaded_file is None:
        st.warning("Please upload your resume PDF first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_text_from_pdf(uploaded_file)

                if not resume_text.strip():
                    st.error(
                        "No readable text found in the PDF. "
                        "Try a text-based PDF instead of a scanned image."
                    )
                    st.stop()

                (
                    ats_score,
                    resume_skills,
                    jd_skills,
                    matched_skills,
                    missing_skills
                ) = analyze_resume(resume_text, job_description)

            # ---------------- RESULTS ----------------

            st.divider()
            st.markdown("## 📊 Analysis Dashboard")

            if not jd_skills:
                st.warning(
                    "No supported skills were detected in the job "
                    "description. Try including specific technical skills."
                )

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("ATS Match Score", f"{ats_score}%")
            col2.metric("Matched Skills", len(matched_skills))
            col3.metric("Missing Skills", len(missing_skills))
            col4.metric("Resume Skills", len(resume_skills))

            # Progress bar

            st.markdown("### Resume Match Progress")
            st.progress(ats_score / 100)

            # ---------------- CHART ----------------

            chart_col, info_col = st.columns(
                [1.2, 1],
                gap="large"
            )

            with chart_col:
                st.markdown("### Skill Gap Overview")

                chart_data = pd.DataFrame({
                    "Skill Category": ["Matched Skills", "Missing Skills"],
                    "Count": [
                        len(matched_skills),
                        len(missing_skills)
                    ]
                })

                fig = px.pie(
                    chart_data,
                    names="Skill Category",
                    values="Count",
                    hole=0.60,
                    color="Skill Category",
                    color_discrete_map={
                        "Matched Skills": "#2563eb",
                        "Missing Skills": "#f97316"
                    }
                )

                fig.update_layout(
                    margin=dict(t=20, b=20, l=10, r=10),
                    legend_title_text="",
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(
                        family="Arial",
                        size=13,
                        color="#334155"
                    )
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True
                )

            with info_col:
                st.markdown("### 🎯 Match Assessment")

                if ats_score >= 80:
                    st.success(
                        "Strong skill match! Your resume contains "
                        "most of the detected job skills."
                    )
                elif ats_score >= 60:
                    st.warning(
                        "Moderate skill match. Review the missing "
                        "skills and improve relevant resume sections."
                    )
                else:
                    st.error(
                        "Low skill match. Compare your experience "
                        "with the job requirements before applying."
                    )

                st.info(
                    "This score measures detected skill overlap only. "
                    "It is not an official ATS score or a prediction "
                    "of interview selection."
                )

            # ---------------- SKILL DETAILS ----------------

            st.divider()
            st.markdown("## 🧠 Skill Gap Analysis")

            matched_tab, missing_tab, all_tab = st.tabs([
                "✅ Matched Skills",
                "⚠️ Missing Skills",
                "📚 All Detected Skills"
            ])

            with matched_tab:
                if matched_skills:
                    st.success(
                        "Skills found in both your resume and the job "
                        "description:"
                    )
                    st.write(", ".join(matched_skills))
                else:
                    st.write("No matching skills detected.")

            with missing_tab:
                if missing_skills:
                    st.warning(
                        "These job-description skills were not detected "
                        "in your resume:"
                    )
                    st.write(", ".join(missing_skills))
                    st.caption(
                        "Only add skills you genuinely possess. "
                        "Consider learning the others."
                    )
                else:
                    st.success("No missing skills detected.")

            with all_tab:
                st.write("**Skills found in your resume:**")
                st.write(
                    ", ".join(resume_skills)
                    if resume_skills else "No supported skills detected."
                )

                st.write("**Skills detected in the job description:**")
                st.write(
                    ", ".join(jd_skills)
                    if jd_skills else "No supported skills detected."
                )

            # ---------------- RECOMMENDATIONS ----------------

            st.divider()
            st.markdown("## 💡 Recommendations")

            if missing_skills:
                for skill in missing_skills:
                    st.markdown(f"- Improve or learn **{skill}** if relevant.")
            else:
                st.write(
                    "Your resume covers all skills detected by this "
                    "basic analyzer. Review experience, projects and "
                    "achievements for further improvements."
                )

            st.markdown(
                "- Add relevant projects that demonstrate your skills."
            )
            st.markdown(
                "- Use clear headings such as Skills, Projects, "
                "Education and Experience."
            )
            st.markdown(
                "- Include measurable achievements where appropriate."
            )

            # ---------------- DOWNLOAD REPORT ----------------

            report = f"""
RESUMEAI - RESUME ANALYSIS REPORT
=================================

Resume: {uploaded_file.name}

ATS SKILL MATCH SCORE: {ats_score}%

RESUME SKILLS:
{", ".join(resume_skills) if resume_skills else "None detected"}

JOB DESCRIPTION SKILLS:
{", ".join(jd_skills) if jd_skills else "None detected"}

MATCHED SKILLS:
{", ".join(matched_skills) if matched_skills else "None"}

MISSING SKILLS:
{", ".join(missing_skills) if missing_skills else "None"}

RECOMMENDATIONS:
Review missing skills, improve relevant projects,
and tailor your resume to the job description.

NOTE:
This score represents detected skill overlap only.
It is not an official ATS score or a hiring prediction.
"""

            st.divider()
            st.markdown("## 📥 Download Your Report")

            st.download_button(
                label="⬇️ Download Analysis Report",
                data=report,
                file_name="resume_analysis_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:
            st.error(
                "Unable to analyze this PDF. Please check whether "
                "the file is valid and try again."
            )
            st.caption(f"Technical details: {e}")


# ---------------- FOOTER ----------------

st.markdown("""
<div class="footer">
    ResumeAI · Smart Resume Analysis Tool<br>
    Built with Streamlit, Python, Pandas and Plotly
</div>
""", unsafe_allow_html=True)
