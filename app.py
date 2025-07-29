import streamlit as st
import openai
import os

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
if os.path.exists("logo.png"):
    st.image("logo.png", use_container_width=True)
else:
    st.warning("Logo image not found. Please ensure 'logo.png' is in the same folder as app.py.")

st.markdown("<h1 style='text-align: center;'>Bureau.AI</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Automated VC-style Deal Memo Generator</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---- GPT API KEY ----
try:
    openai.api_key = st.secrets["openai_api_key"]
except KeyError:
    st.error("OpenAI API key not found in Streamlit secrets. Please add it in `.streamlit/secrets.toml` as `openai_api_key = \"your-key\"`.")
    st.stop()

# ---- FUNCTION TO GENERATE DEAL MEMO ----
def generate_memo(company_name):
    prompt = f"""
You are a VC analyst at a top-tier fund. Write a one-pager deal memo about the company '{company_name}' based on any publicly available information. Format it with:
- Company Overview
- Problem & Solution
- Product
- Traction
- Market
- Competition
- Risks
- Investment Thesis
Make it crisp, insightful, and professional.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert VC analyst."},
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
            st.error(f"An error occurred while generating the memo: {e}")
