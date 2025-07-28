import streamlit as st
from fpdf import FPDF
import datetime
import os

def generate_pdf(company_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=f"BureauAI Deal Memo: {company_name}", ln=True, align="C")
    pdf.set_font("Arial", size=12)
    pdf.ln(10)

    sections = {
        "Company Overview": f"{company_name} is a startup operating in the consumer sector with a unique positioning and market-driven offerings.",
        "Why We Like This Deal": "Strong founding team, good early traction, signs of product-market fit.",
        "Exit Potential": "High likelihood of acquisition within 5–7 years by strategic players.",
        "Moat Analysis": "Tech-enabled supply chain, sticky customer base, and regional advantage.",
        "Red Flags": "- High burn rate\n- Crowded market\n- Regulatory dependencies",
        "Investment Scorecard": "Team: 8/10\nMarket: 7/10\nTraction: 6.5/10\nMoat: 7.5/10\nOverall Score: 7.25/10"
    }

    for section, content in sections.items():
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=section, ln=True)
        pdf.set_font("Arial", size=12)
        # Ensure encoding compatibility
        clean_content = content.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, txt=clean_content)
        pdf.ln(4)

    file_name = f"{company_name}_DealMemo.pdf"
    pdf.output(file_name.encode('latin-1', 'replace').decode('latin-1'))
    return file_name

# Streamlit app
st.set_page_config(page_title="BureauAI", layout="centered")
st.title("BureauAI - Deal Memo Generator")

company_name = st.text_input("Enter company name:")

if st.button("Generate Deal Memo"):
    if company_name.strip() == "":
        st.warning("Please enter a company name.")
    else:
        file_path = generate_pdf(company_name)
        with open(file_path, "rb") as file:
            st.download_button(
                label="Download Deal Memo PDF",
                data=file,
                file_name=file_path,
                mime="application/pdf"
            )
