import streamlit as st
from datetime import datetime
from retriever import retrieve_chunks
from chat_complettion import chat_with_model
from client_chain import rag_chain  # Import RAG pipeline

def chat_page():
    st.markdown("<h2>💬 Chat with Your Document</h2>", unsafe_allow_html=True)

    # Check if retriever is available
    if "retriever" not in st.session_state:
        st.warning("⚠️ Please upload a PDF first in the 'Upload PDF' section.")
        return


    # Restart chat button
    if st.button("🔄 Restart Chat"):
        st.session_state.messages = [
            {
                "text": "👋  Hello! I'm your Client assistant. I'm here to help you find answers from your queries. Just ask me anything—whether it's a question, a clarification, or something you're struggling to understand.",
                "time": datetime.now().strftime("%I:%M %p"),
                "sender": "other"
            }
        ]
        st.rerun()

    # Chat mode selector
    st.markdown("### 🤖 Choose Chat Mode")
    chat_mode = st.radio(
        "Select how you'd like to chat with your PDF:",
        ["🔍 Basic Prompt", "🧠 RAG Pipeline"],
        index=1,
        horizontal=True
    )
    use_rag = chat_mode == "🧠 RAG Pipeline"

    # Inject custom CSS
    st.markdown(
        """
        <style>
            .chat-header { background-color: #e8f5e8; padding: 15px; border-radius: 10px 10px 0 0;
                           text-align: center; font-size: 18px; font-weight: bold; color: #2d5a2d;
                           margin-bottom: 20px; }
            .message-left { background-color: #f0f8f0; padding: 12px 16px; border-radius: 15px;
                            margin: 10px 0; max-width: 70%; float: left; clear: both;
                            border: 1px solid #d4edda; color: #2d5a2d; }
            .message-right { background-color: #2d5a2d; color: white; padding: 12px 16px;
                             border-radius: 15px; margin: 10px 0; max-width: 70%; float: right;
                             clear: both; }
            .timestamp, .timestamp-right { font-size: 11px; margin-top: 5px; color: #666; }
            .timestamp-right { color: #ccc; }
            .message-text { margin: 0; line-height: 1.4; }
            .clearfix::after { content: ""; display: table; clear: both; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize chat history with a welcome message
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "text": "👋 Hello! I'm your Client assistant. I'm here to help you find answers from your queries. Just ask me anything—whether it's a question, a clarification, or something you're struggling to understand.",
                "time": datetime.now().strftime("%I:%M %p"),
                "sender": "other"
            }
        ]

    # Chat header
    st.markdown('<div class="chat-header">Chat</div>', unsafe_allow_html=True)

    # Display messages
    for message in st.session_state.messages:
        if message["sender"] == "other":
            st.markdown(
                f"""
                <div class="message-left">
                    <div class="message-text">{message["text"]}</div>
                    <div class="timestamp">{message["time"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="message-right">
                    <div class="message-text">{message["text"]}</div>
                    <div class="timestamp-right">{message["time"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown('<div class="clearfix"></div>', unsafe_allow_html=True)

    # Input section
    col1, col2 = st.columns([6, 1])
    with col1:
        user_input = st.text_input("", placeholder="Type a question about the PDF...",
                                   key="message_input", label_visibility="collapsed")
    with col2:
        send_button = st.button("➤", key="send_button")

    # Handle message submission
    if send_button and user_input.strip():
        current_time = datetime.now().strftime("%I:%M %p")
        st.session_state.messages.append({"text": user_input, "time": current_time, "sender": "user"})

        retriever = st.session_state.retriever

        # Choose between RAG and basic prompt
        if use_rag:
            try:
                previous_answer = next((m["text"] for m in reversed(st.session_state.messages) if m["sender"] == "other"), None)
                response = rag_chain(user_input, retriever, previous_answer)

                #response = rag_chain(user_input, retriever)
            except Exception as e:
                response = f"Error using RAG: {str(e)}"
        else:
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
