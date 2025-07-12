import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# — Load local .env if present —
load_dotenv()

# — Retrieve API key —
api_key = None
if "OPENAI_API_KEY" in st.secrets:
    api_key = st.secrets["OPENAI_API_KEY"]
else:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.set_page_config(page_title="Helpdesk Support Portal")
    st.error(
        """
        **No OpenAI API key found.**  
        - On Streamlit Cloud: add `OPENAI_API_KEY = "sk-..."` under **Settings → Secrets**.  
        - Locally: set `OPENAI_API_KEY` in your shell or create `.streamlit/secrets.toml`.  
        """
    )
    st.stop()

# — Initialize new v1 OpenAI client —
client = OpenAI(api_key=api_key)

# — Streamlit UI setup —
st.set_page_config(page_title="Helpdesk Support Portal", layout="centered")
st.title("Helpdesk Support Portal Demo")

# — Inputs —
email = st.text_input("Your email address:")
issue = st.text_area("Describe the issue you're facing:", height=200)

if st.button("Report Issue"):
    if not email.strip() or not issue.strip():
        st.error("Please enter both your email address and an issue description.")
    else:
        # Generic reply
        generic = (
            f"Dear {email},\n\n"
            f"Thank you for reporting: \"{issue}\". We will investigate and follow up shortly.\n\n"
            "Best regards,\nSupport Team"
        )

        # AI-powered reply via v1 client
        prompt = (
            f"You are a helpful support agent. A client with email {email} reports:\n"
            f"\"{issue}\"\n"
            "Draft a concise, friendly reply that acknowledges the issue and outlines next steps."
        )
        with st.spinner("Generating AI-powered reply…"):
            try:
                resp = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful support agent."},
                        {"role": "user",   "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=150,
                )
                ai_reply = resp.choices[0].message.content.strip()
            except Exception as e:
                st.error(f"❌ OpenAI API error:\n{e}")
                ai_reply = "[AI call failed—see error above]"

        # Display
        st.subheader("Generic Reply")
        st.code(generic)

        st.subheader("AI-Powered Personalized Reply")
        st.write(ai_reply)
