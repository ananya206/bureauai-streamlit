import streamlit as st
from fpdf import FPDF
import openai
import os
from datetime import datetime

# Load OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["openai_api_key"]

# Page configuration
st.set_page_config(
    page_title="BUREAU.AI Deal Memo Generator",
    layout="centered",
    page_icon="📄",
    initial_sidebar_state="collapsed"
)

# Add dark theme with custom CSS
st.markdown("""
    <style>
        body, .stApp {
            background-color: #111111;
            color: #e0e0e0;
        }
        .title {
            font-size: 2.5em;
            font-weight: bold;
            text-align: center;
            margin-top: 10px;
            color: #ffffff;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #bbbbbb;
        }
        .stTextInput > label {
            color: #dddddd;
        }
        .stButton > button {
            background-color: #009999;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

# Load logo
st.image("Screenshot 2025-07-29 at 11.38.00 AM.png", use_column_width=True)

# Title
st.markdown('<div class="title">BUREAU.AI</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Auto-generate high-quality 1-pager deal memos from a company name</div>', unsafe_allow_html=True)

# Input field
company_name = st.text_input("Enter the company name (e.g., O'Leche):")

# Function to generate memo
def generate_memo(company):
    prompt = f"""
You are a Venture Capital Analyst. Write a concise, VC-style 1-pager deal memo for the company "{company}". 
It should include:

- Company Overview  
- Product/Service  
- Market Opportunity  
- Competitive Landscape  
- Traction / Metrics  
- Business Model  
- Red Flags (if any)  
- Investment Rationale  
- Exit Potential  
- Investment Recommendation  

Use a professional tone. Keep it realistic and compelling.
"""

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()

# Function to save memo as PDF
def save_pdf(content, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    for line in content.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(filename)

# Generate memo
if st.button("Generate Deal Memo"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Generating memo..."):
            memo = generate_memo(company_name)
            filename = f"{company_name}_Deal_Memo.pdf"
            save_pdf(memo, filename)
            st.success("Memo generated successfully!")
            st.download_button(label="📥 Download PDF", data=open(filename, "rb"), file_name=filename, mime="application/pdf")
            st.markdown("---")
            st.subheader("📋 Deal Memo Preview")
            st.markdown(f"```markdown\n{memo}\n```")
