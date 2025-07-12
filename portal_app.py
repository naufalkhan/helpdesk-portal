import os
import streamlit as st
import openai

# Streamlit app configuration
st.set_page_config(page_title="Helpdesk Support Portal", layout="centered")
st.title("Helpdesk Support Portal Demo")

# Retrieve OpenAI key, with fallback to env var
api_key = None
# Try Streamlit secrets first
try:
    api_key = st.secrets["OPENAI_API_KEY"]
except Exception:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        """
        No OpenAI API key found.
        - On Streamlit Cloud: add `OPENAI_API_KEY` in Secrets.
        - Locally: create `.streamlit/secrets.toml` or set `OPENAI_API_KEY` env var.
        """
    )
# Assign to OpenAI
openai.api_key = api_key

# --- User Inputs ---
email = st.text_input("Your email address:")
issue = st.text_area("Describe the issue you're facing:", height=200)

# --- Generate Replies on Button Click ---
if st.button("Report Issue"):
    if not email.strip() or not issue.strip():
        st.error("Please provide both your email and a description of the issue.")
    else:
        # Generic template reply
        generic = (
            f"Dear {email},\n\n"
            f"Thank you for reporting: \"{issue}\". We will investigate and follow up shortly.\n\n"
            "Best regards,\nSupport Team"
        )

        # AI-powered personalized reply
        prompt = (
            f"You are a helpful support agent. A client with email {email} reports the following issue:\n"
            f"\"{issue}\"\n"
            "Draft a concise, friendly reply that acknowledges their issue and outlines next steps."
        )
        with st.spinner("Generating AI-powered reply..."):
            if not openai.api_key:
                ai_reply = "[AI reply unavailable: missing OPENAI_API_KEY in Streamlit secrets.]"
            else:
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "You are a helpful support agent."},
                            {"role": "user",   "content": prompt}
                        ],
                        temperature=0.7,
                        max_tokens=150
                    )
                    ai_reply = response.choices[0].message.content.strip()
                except Exception:
                    ai_reply = "[AI reply unavailable. Please ensure your API key is correct and quota is available.]"

        # Display both replies
        st.subheader("Generic Reply")
        st.code(generic)
        st.subheader("AI-Powered Personalized Reply")
        st.write(ai_reply)

# To run locally:
# 1) pip install streamlit openai
# 2) Create .streamlit/secrets.toml with:
#       OPENAI_API_KEY = "sk-..."
# 3) streamlit run portal_app.py
