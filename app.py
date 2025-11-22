import streamlit as st
import os
import groq
from dotenv import load_dotenv
from datetime import datetime
import PyPDF2
from io import BytesIO
import markdown

load_dotenv()

# ------------------------------------------
# Load API key
# ------------------------------------------
API_KEY = os.getenv("GROQ_API_KEY")

if not API_KEY:
    st.error("Please add your Groq API key to the .env file as GROQ_API_KEY")
    st.stop()

client = groq.Groq(api_key=API_KEY)

# ------------------------------------------
# Session State
# ------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_content" not in st.session_state:
    st.session_state.uploaded_content = []

if "file_names" not in st.session_state:
    st.session_state.file_names = []

if "show_upload" not in st.session_state:
    st.session_state.show_upload = False


# ------------------------------------------
# Extract PDF Text
# ------------------------------------------
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


# ------------------------------------------
# LLM Reply
# ------------------------------------------
def llm_reply(user_message):
    system_content = "You are a helpful Study Mentor AI. Respond concisely using Markdown."

    if st.session_state.uploaded_content:
        system_content += "\n\nYou have access to these study materials:\n"
        for i, content in enumerate(st.session_state.uploaded_content):
            fname = st.session_state.file_names[i]
            system_content += f"\n--- {fname} ---\n{content[:3000]}\n"

    messages = [{"role": "system", "content": system_content}]
    messages.extend(st.session_state.messages)
    messages.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=1000,
            temperature=0.7,
        )
        return response.choices[0].message.content, None

    except Exception as e:
        return None, str(e)


# ------------------------------------------
# UI Setup
# ------------------------------------------
st.set_page_config(page_title="Study Mentor", page_icon="📚", layout="wide")

st.markdown("""
<style>

header[data-testid="stHeader"] { display: none; }
footer { display: none; }

/* Fixed Header – stays on top */
.fixed-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    background: white;
    padding: 1rem 2rem;
    border-bottom: 1px solid #e5e7eb;
    z-index: 1000;
}

/* Main content scrolls under header */
.main .block-container {
    margin-top: 80px;
    padding-bottom: 120px !important;
}

/* Chat container */
.chat-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

/* User message bubble */
.user-message {
    align-self: flex-end;
    max-width: 70%;
    background: #dcf8c6;
    padding: 10px 15px;
    border-radius: 10px;
    border-top-right-radius: 0;
}

/* Bot message bubble */
.bot-message {
    align-self: flex-start;
    max-width: 70%;
    background: white;
    padding: 10px 15px;
    border-radius: 10px;
    border-top-left-radius: 0;
    border: 1px solid #ddd;
}

/* FULLY FIXED FOOTER INPUT BAR */
#global-footer-input {
    position: fixed !important;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    background: white;
    padding: 0.7rem 1rem;
    border-top: 1px solid #d1d5db;
    z-index: 10000 !important;
}


/* Input style */
.stTextInput > div > div > input {
    border-radius: 25px;
    padding: 10px 20px;
    border: 1px solid #d1d5db;
}

/* Send button */
.send-btn {
    background: #2d3748;
    color: white;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------
# Fixed Header
# ------------------------------------------
st.markdown('<div class="fixed-header"><h3>📚 AI Study Mentor</h3></div>', unsafe_allow_html=True)


# ------------------------------------------
# Pinned Files
# ------------------------------------------
if st.session_state.file_names:
    with st.expander("📌 Pinned Study Materials", expanded=True):
        for i, name in enumerate(st.session_state.file_names):
            col1, col2 = st.columns([0.9, 0.1])
            col1.text("📄 " + name)
            if col2.button("×", key=f"del{i}"):
                st.session_state.file_names.pop(i)
                st.session_state.uploaded_content.pop(i)
                st.rerun()


# ------------------------------------------
# Chat Section
# ------------------------------------------
if not st.session_state.messages:
    st.markdown("<h4 style='text-align:center;margin-top:60px;'>Ask anything or upload notes to begin 📚</h4>", unsafe_allow_html=True)
else:
    chat_html = "<div class='chat-container'>"

    for msg in st.session_state.messages:
        role = "user-message" if msg["role"] == "user" else "bot-message"
        content = markdown.markdown(msg["content"])
        chat_html += f"<div class='{role}'>{content}</div>"

    chat_html += "<div style='height:120px;'></div></div>"  # Space above input box
    st.markdown(chat_html, unsafe_allow_html=True)


# ------------------------------------------
# FIXED GLOBAL FOOTER INPUT BAR
# ------------------------------------------
st.markdown("""
<div id="global-footer-input">
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([0.08, 0.84, 0.08])

with col1:
    if st.button("📎", key="attach_btn"):
        st.session_state.show_upload = not st.session_state.show_upload
        st.rerun()

with col2:
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input(
            "Message",
            placeholder="Message Study Mentor...",
            label_visibility="collapsed"
        )
        submitted = st.form_submit_button("Send")

with col3:
    st.markdown('<div class="send-btn">↑</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ------------------------------------------
# When the user sends a message
# ------------------------------------------
if submitted and user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.rerun()


# ------------------------------------------
# Get bot reply
# ------------------------------------------
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.spinner("Thinking..."):
        reply, error = llm_reply(st.session_state.messages[-1]["content"])
        if error:
            st.error(error)
        else:
            st.session_state.messages.append({"role": "assistant", "content": reply})
            st.rerun()


# ------------------------------------------
# File Upload Popup
# ------------------------------------------
if st.session_state.show_upload:
    with st.form("upload_form"):
        st.write("### Upload Study Materials")
        files = st.file_uploader("Choose PDF/TXT", type=["pdf", "txt"], accept_multiple_files=True)
        upload = st.form_submit_button("Upload")

        if upload and files:
            for f in files:
                if f.name not in st.session_state.file_names:
                    text = extract_text_from_pdf(f) if f.type == "application/pdf" else f.read().decode()
                    st.session_state.file_names.append(f.name)
                    st.session_state.uploaded_content.append(text)
            st.session_state.show_upload = False
            st.rerun()