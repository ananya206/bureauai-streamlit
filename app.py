import streamlit as st
import openai
from fpdf import FPDF
import os

# Custom CSS for VC Dark Theme
st.markdown("""
    <style>
        .stApp {
            background-color: #0E0E0E;
            color: #FFFFFF;
            font-family: 'Segoe UI', sans-serif;
            background-image: radial-gradient(circle at top left, #1a1a1a, #0E0E0E);
        }

        h1, h2, h3, h4, h5, h6 {
            color: #ffffff;
            font-weight: 600;
        }

        .stTextInput>div>div>input,
        .stTextArea textarea {
            background-color: rgba(255,255,255,0.05);
            color: white;
            border-radius: 8px;
        }

        button[kind="primary"] {
            background-color: #D72638;
            color: white;
            border-radius: 10px;
            font-weight: 600;
        }

        button[kind="primary"]:hover {
            background-color: #b01e2c;
            color: white;
        }

        .css-1d391kg {
            background-color: #161616 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Load API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Function to generate memo content using OpenAI
def generate_memo(company_name):
    prompt = f"""
    You are an investment analyst. Write a professional investment memo for the company '{company_name}'. 
    Include the following sections:
    1. Executive Summary
    2. Why We Like This Deal
    3. Business Model
    4. Financials & Metrics
    5. Moat Analysis
    6. Exit Potential
    7. Risks & Red Flags
    8. Recommendation
    The tone should be concise, analytical, and VC/PE-style.
    """

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# Function to create PDF
class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 14)
        self.cell(0, 10, "Investment Memo", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_text_color(220, 50, 50)
        self.cell(0, 10, title, ln=True)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.set_text_color(255, 255, 255)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_memo(self, content):
        sections = content.split("\n\n")
        for section in sections:
            if ":" in section:
                title, body = section.split(":", 1)
            elif "\n" in section:
                title, body = section.split("\n", 1)
            else:
                title, body = section, ""
            self.chapter_title(title.strip())
            self.chapter_body(body.strip())

# Streamlit UI
st.title("📄 BureauAI - Investment Memo Generator")
company_name = st.text_input("Enter Company Name")

if st.button("Generate Memo"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner("Generating memo..."):
            memo = generate_memo(company_name)
            pdf = PDF()
            pdf.set_auto_page_break(auto=True, margin=15)
            pdf.add_page()
            pdf.add_memo(memo)
            file_name = f"{company_name}_Investment_Memo.pdf"
            file_path = os.path.join("/tmp", file_name)
            pdf.output(file_path)

        with open(file_path, "rb") as f:
            st.download_button("📥 Download Memo PDF", f, file_name, mime="application/pdf")
