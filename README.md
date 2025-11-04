# Client Assistant Chatbot
This repository contains an AI-powered assistant designed to help clients resolve company-related issues through natural language interaction. Built with modern retrieval-augmented generation (RAG) techniques, the assistant can understand user queries, retrieve relevant information from internal documents, and respond conversationally.

# Features
 Document-aware responses: Uses LangChain and ChromaDB to retrieve relevant chunks from company documents.

 Contextual memory: Optionally includes previous assistant responses for more coherent multi-turn conversations.

 Natural language interface: Powered by HuggingFace and Azure AI models for fluent, human-like replies.

 PDF support: Users can upload PDFs and chat with their contents.

 Streamlit UI: A clean, interactive front-end for users to engage with the assistant.

# Tech Stack (all found in requirements.txt file
This project uses the following packages:

langchain, langchain-community, langchain-huggingface, langchain-chroma,chromadb, sentence-transformers, torch,azure-ai-inference, pypdf, pandas, python-dotenv and streamlit for the user interface

# For Demo, look at chat_demo.pdf
To help you visualize how the assistant works, I've included a sample interaction in chat_demo.pdf. It shows a typical conversation between a user and the assistant, demonstrating how queries are answered based on document context.
