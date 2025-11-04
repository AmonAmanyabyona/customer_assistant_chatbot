
import streamlit as st
from client_homepage import home_page
from client_pdf import upload_page
from client_chat import chat_page

# Must be first Streamlit command
st.set_page_config(page_title="SmartReader", layout="wide")

# Initialize session state
if "domain" not in st.session_state:
    st.session_state.domain = "Home"

# Sidebar styling for hoverable buttons
st.sidebar.markdown("""
<style>
div[data-testid="stButton"] > button {
    background-color: transparent;
    color: #2d5a2d;
    border: none;
    padding: 10px 15px;
    text-align: left;
    width: 100%;
    font-size: 16px;
    transition: background-color 0.3s ease;
}
div[data-testid="stButton"] > button:hover {
    background-color: #e8f5e8;
    color: black;
    border-radius: 6px;
}
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("📚 SmartReader Navigation")
if st.sidebar.button("🏠 Home"):
    st.session_state.domain = "Home"
if st.sidebar.button("📤 Upload PDF"):
    st.session_state.domain = "Upload"
if st.sidebar.button("💬 Chat with PDF"):
    st.session_state.domain = "Chat"

# Main content area
if st.session_state.domain == "Home":
    home_page()
elif st.session_state.domain == "Upload":
    upload_page()
elif st.session_state.domain == "Chat":
    chat_page()
