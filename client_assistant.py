import asyncio
import streamlit as st
import hashlib
import os
from pdf_loader import load_pdf
from embedding import get_embedding_function
from vectorstore import create_vectorstore, load_vectorstore
from retriever import get_retriever, retrieve_chunks
from chat_complettion import chat_with_model  # Function for Q&A
from rag_pipeline import rag_chain
from response_processing import process_response

# **Ensure proper event loop setup**
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# **Set page layout for wider view**
st.set_page_config(page_title="Chatbot", layout="wide")

# **Header Title**
st.markdown("<h1 style='text-align: center; color: black;'>SmartReader: Explore, Ask, Summarize 📘</h1>", unsafe_allow_html=True)
st.divider()  # Adds a visual separator

def get_file_hash(file_path):
    """Generate a unique hash for the file to identify duplicates."""
    with open(file_path, "rb") as f:
        file_bytes = f.read()
    return hashlib.md5(file_bytes).hexdigest()

def process_pdf(pdf_filepath):
    """Check if the document already exists before reprocessing."""
    file_hash = get_file_hash(pdf_filepath)
    vectorstore_path = f"app_vectorstore_{file_hash}"  # Use hash as unique ID
    
    if os.path.exists(vectorstore_path):  
        print("Vectorstore already exists! Loading existing embeddings.")
        vectorstore = load_vectorstore(vectorstore_path, get_embedding_function())
    else:
        print("🚀 New PDF detected! Processing and creating vectorstore.")
        pages = load_pdf(pdf_filepath)
        embedding_function = get_embedding_function()
        vectorstore = create_vectorstore(pages, embedding_function, vectorstore_path)
    
    retriever = get_retriever(vectorstore)
    return retriever

# **File Upload Section**
col1, col2, col3 = st.columns([1, 3, 1])  # Centers content nicely

with col2:
    pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

if pdf_file:
    # Ensure a stable file path
    save_directory = "uploaded_pdfs"
    os.makedirs(save_directory, exist_ok=True)  # Create directory if it doesn't exist
    save_path = os.path.join(save_directory, pdf_file.name)

    # Save the uploaded PDF
    with open(save_path, "wb") as f:
        f.write(pdf_file.getbuffer())  # Write the uploaded file to disk

    retriever = process_pdf(save_path)  # Pass full path instead of just the filename
    st.divider()  # Adds separation before the next section
# Custom Chat UI after PDF upload
import time
from datetime import datetime
import random

# Inject custom CSS
st.markdown(
    """<style>
    /* your full CSS block here */
    </style>""",
    unsafe_allow_html=True,
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat header
st.markdown('<div class="chat-header">Chat</div>', unsafe_allow_html=True)

# Display messages
for message in st.session_state.messages:
    if message["sender"] == "other":
        st.markdown(
            f"""<div class="message-left">
                <div class="message-text">{message["text"]}</div>
                <div class="timestamp">{message["time"]}</div>
            </div>""",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""<div class="message-right">
                <div class="message-text">{message["text"]}</div>
                <div class="timestamp-right">{message["time"]}</div>
            </div>""",
            unsafe_allow_html=True,
        )

st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)

# Input section
col1, col2 = st.columns([6, 1])
with col1:
    user_input = st.text_input("", placeholder="Type a question about the PDF...", key="message_input", label_visibility="collapsed")
with col2:
    send_button = st.button("➤", key="send_button")

# Handle message submission
if send_button and user_input.strip():
    current_time = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"text": user_input, "time": current_time, "sender": "user"})

    # Retrieve chunks from PDF
    retrieved_docs = retrieve_chunks(retriever, user_input)
    if not retrieved_docs:
        response = "No relevant information found in the uploaded PDF."
    else:
        context = "\n\n".join(doc.page_content for doc in retrieved_docs)
        prompt = f"Based on the retrieved text, answer concisely:\n\n{context}\n\n{user_input}"
        response = chat_with_model(prompt)

    response_time = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"text": response, "time": response_time, "sender": "other"})
    st.rerun()
