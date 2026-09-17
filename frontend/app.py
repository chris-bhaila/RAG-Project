import requests
import streamlit as st

BACKEND_URL = "http://127.0.0.1:8000"

st.title("RAG Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Upload a document")
    uploaded_file = st.file_uploader(
        "Choose a file", type=["pdf", "docx", "txt", "csv"]
    )
    if uploaded_file is not None and st.button("Upload"):
        with st.spinner("Uploading and processing..."):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            response = requests.post(f"{BACKEND_URL}/upload/", files=files)
        if response.ok:
            st.success(f"Uploaded {uploaded_file.name}")
        else:
            st.error(f"Upload failed: {response.text}")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if question := st.chat_input("Ask a question about your documents"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = requests.post(f"{BACKEND_URL}/chat", json={"question": question})
        if response.ok:
            answer = response.json()["answer"]
        else:
            answer = f"Error: {response.text}"
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
