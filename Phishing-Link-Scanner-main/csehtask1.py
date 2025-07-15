import streamlit as st
import google.generativeai as genai
import os
import cred as key

PAGE_TITLE = "Phishing Website Detection"
LAYOUT = "wide"
MODEL_NAME = "gemini-2.0-flash"
API_KEY = key.API_KEY

# Configure the Streamlit page
st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)

# Apply custom CSS for dark UI and layout
st.markdown("""
    <style>
        body {
            background-color: #0f2027;
            background-image: linear-gradient(to right, #2c5364, #203a43, #0f2027);
            color: white;
        }
        .main {
            background-color: transparent;
        }
        .block-container {
            padding-top: 2rem;
        }
        input, .stTextInput > div > div > input {
            background-color: white !important;
            color: black !important;
        }
        .button-check {
            background-color: #f5f5dc;
            color: #2c2c2c;
            font-weight: bold;
            padding: 8px 24px;
            border-radius: 8px;
            border: none;
        }
        .custom-button {
            padding: 10px 24px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 8px;
            border: none;
        }
        .safe {
            background-color: #00cc44;
            color: white;
        }
        .unsafe {
            background-color: #ff4d4d;
            color: white;
        }
        .right-box {
            background-color: transparent;
            padding: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# Gemini configuration
if not API_KEY:
    st.error("❌ API key not found. Please check your configuration in 'cred.py'.")
    st.stop()

genai.configure(api_key=API_KEY)

# Simplified prompt with bullet-point instructions
PROMPT_TEMPLATE = """
You are a cybersecurity expert.

Analyze the following URL for potential phishing risks:

URL: {url}

Please check:
- Typosquatting (compare domain with known legitimate domains)
- HTTPS presence
- Shortened URL use
- Domain age
- IP reputation

Return the results in a simple bullet-point format, like:
- ✅ HTTPS: PASS
- ❌ Domain Age: FAIL – Very new domain

At the end, give a final verdict:
Phishing Risk: High/Medium/Low, with a clear emoji (🔴🟡🟢)
"""

# Generate report
def generate_report(url):
    prompt = PROMPT_TEMPLATE.format(url=url)
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
        return None

# Page layout
col1, col2 = st.columns([2, 3])

with col1:
    st.markdown(f"<h1 style='font-family:Courier New, monospace;'>{PAGE_TITLE}</h1>", unsafe_allow_html=True)
    url = st.text_input("Enter URL", key="url_input")

    if st.button("Check here"):
        if url:
            st.session_state['result'] = generate_report(url)
            st.session_state['url'] = url
        else:
            st.warning("⚠️ Please enter a URL.")

    st.markdown("<p style='font-size:12px; margin-top: 100px;'></p>", unsafe_allow_html=True)

with col2:
    if 'result' in st.session_state and st.session_state['result']:
        st.markdown(f"<p style='color:lightblue; font-size: 18px;'>{st.session_state['url']}</p>", unsafe_allow_html=True)

        result_text = st.session_state['result'].lower()

        if "high" in result_text or "🔴" in result_text:
            st.markdown("### ❌ Website is 100% unsafe to use...")
            st.markdown("<button class='custom-button unsafe'>Still want to Continue</button>", unsafe_allow_html=True)
        elif "medium" in result_text or "🟡" in result_text:
            st.markdown("### ⚠️ Website may be risky...")
            st.markdown("<button class='custom-button unsafe'>Proceed with Caution</button>", unsafe_allow_html=True)
        else:
            st.markdown("### ✅ Website is likely safe to use...")
            st.markdown("<button class='custom-button safe'>Continue</button>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 📝 Report Summary")
        st.markdown(st.session_state['result'])
