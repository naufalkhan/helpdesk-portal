import os
import streamlit as st
import openai
from dotenv import load_dotenv

# Load environment variables and OpenAI API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app configuration
st.set_page_config(page_title="Helpdesk Support Portal", layout="centered")
st.title("Helpdesk Support Portal Demo")

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
                ai_reply = "[AI reply unavailable. Please ensure your API key is set and quota is available.]"

        # Display both replies
        st.subheader("Generic Reply")
        st.code(generic)
        st.subheader("AI-Powered Personalized Reply")
        st.write(ai_reply)
