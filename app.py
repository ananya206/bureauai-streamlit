import streamlit as st
import openai
from fpdf import FPDF

# App Config
st.set_page_config(page_title="BureauAI - Investment Memo Generator", layout="centered")

# Custom VC dark theme styling
custom_css = """
<style>
    html, body, [class*="css"] {
        background-color: #111111;
        color: #f5f5f5;
        font-family: 'Helvetica Neue', sans-serif;
    }

    .title {
        font-size: 48px;
        font-weight: 900;
        letter-spacing: -1px;
        text-transform: uppercase;
        color: #f0f0f0;
    }

    .subtitle {
        font-size: 14px;
        letter-spacing: 2px;
        color: #888;
        margin-top: -20px;
        margin-bottom: 30px;
    }

    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #888;
        border-radius: 8px;
        padding: 10px;
    }

    .stButton>button {
        background-color: #eaeaea;
        color: black;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        font-weight: 600;
    }

    .stButton>button:hover {
        background-color: #ffffff;
        color: black;
        transform: scale(1.01);
        transition: all 0.3s ease-in-out;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# API key access
openai.api_key = st.secrets["openai_api_key"]

# PDF Generator
def generate_pdf(memo_text, company_name):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, memo_text)
    filename = f"{company_name}_Investment_Memo.pdf"
    pdf.output(filename)
    return filename

# GPT Deal Memo Generator
def generate_memo(company_name):
    prompt = f"""
    Create a crisp, professional one-page investment memo for a venture capital analyst.

    Company: {company_name}
    Include sections: Business Overview, Market Opportunity, Traction, Business Model, Competitive Landscape, Red Flags, Investment Rationale, and Conclusion.
    Keep it realistic, jargon-aware, and avoid exaggeration.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# Title Section
st.markdown('<div class="title">BureauAI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Investment Memo Generator</div>', unsafe_allow_html=True)

# Input Form
company_name = st.text_input("Enter Company Name")

if st.button("Generate Investment Memo") and company_name:
    with st.spinner("Generating memo..."):
        memo = generate_memo(company_name)
        st.subheader("📄 Generated Memo")
        st.code(memo, language="markdown")

        # Generate downloadable PDF
        pdf_file = generate_pdf(memo, company_name)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label="📥 Download PDF",
                data=f,
                file_name=pdf_file,
                mime="application/pdf"
            )
