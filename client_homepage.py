import streamlit as st

def home_page():

    # Welcome header
    st.markdown("<h1 style='text-align: center; color: #2d5a2d;'>Welcome to SmartReader 📘</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #555;'>Your intelligent PDF companion</h3>", unsafe_allow_html=True)
    st.divider()

    # Introduction
    st.markdown("""
    SmartReader lets you:
    - 📤 Upload any PDF document
    - 💬 Chat with it using natural language
    - 🔍 Ask questions, get summaries, and explore content intelligently

    Use the sidebar to navigate between:
    - **Upload PDF**: Prepare your document for chat
    - **Chat with PDF**: Ask questions and get answers
    """)

    # Optional branding or image
    #st.image("/home/amon/Documents/Novaetus/customer_assistant_chatbot/Amon_photo.jpg", use_container_width=True)  # Replace with your actual image path
    st.image("/home/amon/Documents/Novaetus/customer_assistant_chatbot/Amon_photo.jpg")

    # Footer
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 14px;'>Built with ❤️ for curious minds</p>", unsafe_allow_html=True)
