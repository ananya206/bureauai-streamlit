import streamlit as st
import openai
from openai import OpenAI

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Bureau.AI - Deal Memo Generator",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="auto"
)

# ---- DARK MODE VC STYLING ----
custom_css = """
<style>
    body, .stApp {
        background-color: #0F1117;
        color: #F1F1F1;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, h4, h5, h6, p, label {
        color: #FFFFFF !important;
    }
    .stTextInput input {
        background-color: #1C1F26;
        color: white;
        border: 1px solid #3D3D3D;
        border-radius: 8px;
    }
    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
        font-weight: bold;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
    }
    .markdown-text-container ul {
        margin-left: 1.5em;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---- LOGO AND TITLE ----
st.image("logo.png", use_container_width=True)
st.markdown("<h1 style='text-align: center;'>Bureau.AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>From Idea to Investment Insight — Instantly</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---- OPENAI API KEY ----
client = OpenAI(api_key=st.secrets["openai_api_key"])

# ---- FUNCTION TO GENERATE DEAL MEMO ----
def generate_memo(company_name):
    prompt = f"""
You are a venture capital analyst creating a one-pager deal memo on the company '{company_name}'. Use only bullet points under each section and keep all points crisp and under 25 words each. Include a dedicated section for 'Key Competitors'. Format:

- Company Overview
- Problem & Solution
- Product
- Traction
- Market
- Key Competitors
- Risks
- Investment Thesis
Keep tone sharp and insights professional. No long paragraphs.
    """
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a concise, sharp venture capital analyst."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content.strip()

# ---- MAIN APP INTERFACE ----
company_name = st.text_input("Enter a Company Name", placeholder="e.g., O'Leche")

if st.button("Generate Deal Memo") and company_name:
    with st.spinner("Generating deal memo..."):
        try:
            memo = generate_memo(company_name)
            st.markdown("---")
            st.markdown(f"## 📄 Deal Memo: {company_name}")
            st.markdown(memo)
        except Exception as e:
            st.error(f"❌ An error occurred while generating the memo:\n\n{e}")
