import streamlit as st
from fpdf import FPDF
from openai import OpenAI
import os
import tempfile

# Initialize the OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="📄 BureauAI - Deal Memo Generator", layout="centered")
st.title("📄 BureauAI - Deal Memo Generator")
st.caption("Generate a 1-page AI-powered deal memo based on a startup or company name.")

# Function to generate investment memo using OpenAI
def generate_memo(company):
    prompt = f"""
You are an AI investment analyst writing a sharp 1-page deal memo on the company "{company}". Include these sections:

1. Company Overview
2. Product & Market Fit
3. Moat Analysis
4. Financial Snapshot (mock if unknown)
5. Red Flags
6. Exit Potential
7. Why We Like This Deal

Make it crisp, insightful, and persuasive.
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content

# Function to convert memo text to PDF
def generate_pdf(company, memo_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, f"Deal Memo: {company}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    for line in memo_text.split("\n"):
        pdf.multi_cell(0, 10, line)

    tmp_dir = tempfile.gettempdir()
    file_path = os.path.join(tmp_dir, f"{company}_memo.pdf")
    pdf.output(file_path)
    return file_path

# Streamlit UI
company_name = st.text_input("Enter company/startup name")

if st.button("Generate Memo"):
    if company_name:
        with st.spinner("Generating memo..."):
            memo = generate_memo(company_name)
            pdf_path = generate_pdf(company_name, memo)
        st.success("✅ Deal memo generated!")

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Memo as PDF",
                data=f,
                file_name=f"{company_name}_memo.pdf",
                mime="application/pdf"
            )

        st.markdown("---")
        st.subheader("📄 Memo Preview")
        st.text_area("Generated Deal Memo", memo, height=400)

    else:
        st.warning("Please enter a company name.")
