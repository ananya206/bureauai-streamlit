import streamlit as st
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
    body {
        background-color: #0F1117;
        color: #FFFFFF;
    }
    .stApp {
        background-color: #0F1117;
    }
    h1, h2, h3, h4, h5, h6, p, label, .stTextInput > label {
        color: #FFFFFF !important;
    }
    .stTextInput input {
        background-color: #1C1F26;
        color: white;
    }
    .stButton button {
        background-color: #2563eb;
        color: white;
        border-radius: 10px;
    }
    .stButton button:hover {
        background-color: #1d4ed8;
        color: white;
    }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

# ---- LOGO AND TITLE ----
st.image("logo.png", use_container_width=True)
st.markdown("<h1 style='text-align: center;'>Bureau.AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Automated VC-style Deal Memo Generator</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---- GPT API CLIENT SETUP ----
client = OpenAI(api_key=st.secrets["openai_api_key"])

# ---- FUNCTION TO GENERATE DEAL MEMO ----
def generate_memo(company_name):
    prompt = f"""
You are a top-tier VC analyst. Write a crisp, one-pager deal memo about the company '{company_name}'.
Use only bullet points. Keep each point short and professional. Structure it as follows:

- Company Overview
- Problem & Solution
- Product
- Traction
- Market
- Competition
- Competitors (name at least 3)
- Risks
- Investment Thesis

Avoid fluff. Prioritize clarity and brevity.
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a sharp, insightful VC analyst who writes bullet-style memos."},
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
            st.error(f"An error occurred while generating the memo:\n\n{e}")
