import streamlit as st
import requests
import os
from typing import List
import base64


API_BASE = os.getenv("STREAMLIT_API_BASE", "http://127.0.0.1:8000")
UPLOAD_ENDPOINT = f"{API_BASE}/upload"
ASK_ENDPOINT = f"{API_BASE}/ask"


def upload_files_to_backend(files: List[st.runtime.uploaded_file_manager.UploadedFile]) -> dict:
    if not files:
        return {"error": "No files provided"}
    files_payload = [("files", (f.name, f.getvalue(), f.type or "application/octet-stream")) for f in files]
    try:
        resp = requests.post(UPLOAD_ENDPOINT, files=files_payload)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def ask_question_to_backend(question: str) -> dict:
    try:
        resp = requests.post(ASK_ENDPOINT, json={"question": question})
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}

def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


st.set_page_config(page_title="StudyMate AI", layout="wide")

with st.sidebar:
    st.markdown("<h2 style='color:#4F46E5;'> StudyMate AI</h2>", unsafe_allow_html=True)
    st.markdown("Your intelligent learning companion")

    st.markdown("###  Upload Documents")
    uploaded = st.file_uploader(
        "Select PDFs / text files",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True
    )
    if st.button("Upload Selected Files"):
        if not uploaded:
            st.warning("Choose at least one file to upload.")
        else:
            with st.spinner("Uploading and indexing..."):
                result = upload_files_to_backend(uploaded)
            if result.get("error"):
                st.error(f"Upload failed: {result['error']}")
            else:
                st.success(result.get("message", "Files uploaded"))


if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "question_input" not in st.session_state:
    st.session_state["question_input"] = ""


image_path = os.path.join(os.path.dirname(__file__), "future-artificial-intelligence.webp")
if os.path.exists(image_path):
    img_base64 = get_base64_of_image(image_path)
    img_html = f'<img src="data:image/webp;base64,{img_base64}" width="500">'
else:
    img_html = ""

if not st.session_state["messages"]:
    st.markdown(
        f"""
        <div style="text-align:center; margin-top:10px;">
            {img_html}
            <h1 style="color:#4F46E5;">Welcome to StudyMate AI</h1>
            <p>Your intelligent learning companion powered by advanced AI.  
            Upload your study materials, ask questions, and get personalized explanations tailored to your learning style.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_message(role, text):
    if role == "user":
        st.markdown(
            f"""
            <div style="background-color:#DCF8C6; padding:8px 12px; border-radius:12px; 
                        margin:3px 0; max-width:80%; align-self:flex-end; float:right; clear:both;">
                <b>You:</b> {text}
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div style="background-color:#FFFFFF; padding:8px 12px; border-radius:12px; 
                        margin:3px 0; border:1px solid #E5E7EB; max-width:60%; float:left; clear:both;">
                <b>Assistant:</b> {text}
            </div>
            """,
            unsafe_allow_html=True
        )


for msg in st.session_state["messages"]:
    render_message(msg["role"], msg["text"])


def handle_send():
    question = st.session_state.question_input.strip()
    if not question:
        return
    st.session_state.messages.append({"role": "user", "text": question})
    with st.spinner("Fetching answer..."):
        resp = ask_question_to_backend(question)
    if resp.get("error"):
        st.error(f"Error: {resp['error']}")
    else:
        answer_text = resp.get("answer") or resp.get("result") or str(resp)
        st.session_state.messages.append({
            "role": "assistant",
            "text": answer_text
        })
    st.session_state.question_input = ""  


st.text_input(
    "Ask me anything about your studies...",
    key="question_input",
    on_change=handle_send
)
