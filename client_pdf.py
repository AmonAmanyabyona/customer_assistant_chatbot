import streamlit as st
import os
import hashlib
from pdf_loader import load_pdf
from embedding import get_embedding_function
from vectorstore import create_vectorstore, load_vectorstore
from retriever import get_retriever

def get_file_hash(file_path):
    """Generate a unique hash for the file to identify duplicates."""
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def upload_page():
    st.markdown("<h2>📤 Upload Your PDF</h2>", unsafe_allow_html=True)
    st.markdown("Upload a document to prepare it for intelligent chat. Once processed, switch to the chat tab.")

    # File uploader
    pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])
    if pdf_file:
        # Save file locally
        save_dir = "uploaded_pdfs"
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, pdf_file.name)

        with open(save_path, "wb") as f:
            f.write(pdf_file.getbuffer())

        # Generate hash and vectorstore path
        file_hash = get_file_hash(save_path)
        vectorstore_path = f"app_vectorstore_{file_hash}"

        # Load or create vectorstore
        if os.path.exists(vectorstore_path):
            st.info("✅ PDF already processed. Loading existing vectorstore...")
            vectorstore = load_vectorstore(vectorstore_path, get_embedding_function())
        else:
            st.info("🔄 New PDF detected. Processing and embedding...")
            pages = load_pdf(save_path)
            embedding_function = get_embedding_function()
            vectorstore = create_vectorstore(pages, embedding_function, vectorstore_path)
            st.success("🎉 PDF successfully processed!")

        # Store retriever in session state
        retriever = get_retriever(vectorstore)
        st.session_state.retriever = retriever
        st.session_state.pdf_name = pdf_file.name  # Optional: store filename
        st.success("Ready to chat! Switch to the 💬 Chat tab.")
