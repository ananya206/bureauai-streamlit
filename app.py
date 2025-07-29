import streamlit as st
import openai
from fpdf import FPDF
import tempfile
import os

# Title
st.set_page_config(page_title="BureauAI", layout="centered")
st.title("📊 BureauAI – AI-powered Deal Memo Generator")

# User Input
company_name = st.text_input("Enter the name of the company:")

# Load OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_memo(company):
    prompt = f"""
You are an AI investment analyst writing a short but sharp 1-page deal memo on the company "{company}". Include the following sections:

1. Company Overview
2. Product & Market Fit
3. Moat Analysis
4. Financial Snapshot (mocked if real data is unknown)
5. Red Flags
6. Exit Potential
7. Why We Like This Deal (make it investor-persuasive)

Keep it crisp, professional, and investor-focused. Avoid fluff. Return the memo in markdown-style bullet points and short paragraphs.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response['choices'][0]['message']['content']

def save_pdf(memo, company):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for line in memo.split('\n'):
        pdf.multi_cell(0, 10, line)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(tmp_file.name)
    return tmp_file.name

# Generate Button
if st.button("Generate Deal Memo"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Generating deal memo..."):
            memo = generate_memo(company_name)
            pdf_path = save_pdf(memo, company_name)

            st.success("✅ Deal memo generated!")
            st.download_button(
                label="📄 Download PDF",
                data=open(pdf_path, "rb"),
                file_name=f"{company_name}_deal_memo.pdf",
                mime="application/pdf"
            )

        st.subheader("🔍 Memo Preview")
        st.markdown(memo)
