import streamlit as st
import google.generativeai as genai
import datetime

# -------------------- CONFIGURATION --------------------
GEMINI_API_KEY = "AIzaSyB6ID5OPGeueCDna8HMWxLEDAuAYeqKuZw"
MODEL_ID = "gemini-2.5-flash"  # or gemini-1.5-pro

st.set_page_config(
    page_title="🤖 SG AI Chatbot",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Intelligent AI Chatbot")
st.markdown("""
A clean, intelligent AI chatbot interface

Features:
- Persistent chat history
- Download chat as text
- Multiple model options
""")

# -------------------- INIT GOOGLE GENAI --------------------
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_ID)

# -------------------- SESSION STATE --------------------
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Chat Settings")
    if st.button("🧹 Clear Chat History"):
        st.session_state["messages"] = []

    if st.button("💾 Download Chat History"):
        if st.session_state["messages"]:
            chat_text = "\n".join(
                [f'{m["role"].capitalize()}: {m["content"]}' for m in st.session_state["messages"]]
            )
            st.download_button(
                "Download Chat as TXT",
                data=chat_text,
                file_name=f"chat_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        else:
            st.info("No chat history to download.")

# -------------------- DISPLAY CHAT --------------------
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------- CHAT INPUT --------------------
if user_input := st.chat_input("Type your message here..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = model.generate_content(user_input)
                reply = response.text
            except Exception as e:
                reply = f"⚠️ Error: {e}"
            st.markdown(reply)

    st.session_state["messages"].append({"role": "assistant", "content": reply})
