from PyPDF2 import PdfReader
import streamlit as st

uploaded_file = st.file_uploader(
    "Upload your resume",
    type=["pdf"]
)

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        resume_text += page.extract_text() or ""

    if resume_text.strip():
        st.success("PDF read successfully!")
        st.text_area("Extracted Resume Text", resume_text, height=250)
    else:
        st.warning("No readable text found in this PDF.")
