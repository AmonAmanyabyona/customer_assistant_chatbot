from retriever import retrieve_chunks
from formatter import format_docs
from chat_complettion import chat_with_model  # Reuse the existing chat_with_model function

# def rag_chain(question, retriever):
#     """
#     Runs a Retrieval-Augmented Generation (RAG) pipeline:
#     1. Retrieves relevant chunks from the document.
#     2. Formats the context.
#     3. Constructs a prompt.
#     4. Sends it to the LLM via chat_with_model.
#     """

#     # Step 1: Retrieve relevant chunks
#     retrieved_docs = retrieve_chunks(retriever, question)
#     if not retrieved_docs:
#         return "No relevant information found in the uploaded PDF."

#     # Step 2: Format retrieved context
#     formatted_context = format_docs(retrieved_docs)

#     # Step 3: Construct prompt
#     prompt = f"""
# You are a helpful assistant that answers questions based only on the provided context.
# If the context does not contain relevant information, respond politely and briefly with something like:
# "This is outside my area of expertise based on the document."

# Do not invent or infer information. Only use what is explicitly stated in the context.
# Avoid phrases like "According to the context" or "Based on the document." Just answer naturally, as if you're speaking directly to the client.
# Context:
# {formatted_context}

# Question:
# {question}
# """

#     # Step 4: Query the model
#     response_text = chat_with_model(prompt)

#     # Step 5: Validate response
#     if not response_text.strip():
#         raise ValueError("Error: GPT response is empty!")

#     return response_text




# the above RAG setup treats each question in isolation. It retrieves chunks based only on the latest user input, without considering the previous conversation. So when the user asks a follow-up like “So it is possible to restore my account without issues?”, the retriever doesn’t see the earlier context about password recovery and might not find matching chunks — leading to that fallback response.

#How to Fix It
# You can fix this in two ways:

# 1. Include Chat History in the RAG Prompt
# Update the rag_chain() to include recent messages (especially the last assistant response) in the prompt like below

def rag_chain(question, retriever, previous_answer=None):
    retrieved_docs = retrieve_chunks(retriever, question)
    formatted_context = format_docs(retrieved_docs)

    # Include previous assistant response if available
    history_context = f"\nPrevious answer: {previous_answer}\n" if previous_answer else ""

    prompt = f"""
You are a helpful assistant responding to client questions based on the provided document.

Only use information found in the context below. If the answer is not present, reply briefly and politely that you don't have that information.

Avoid phrases like "According to the context" or "Based on the document." Just answer naturally, as if you're speaking directly to the client.

{history_context}
Context:
{formatted_context}

Question:
{question}
"""
    response_text = chat_with_model(prompt)
    if not response_text.strip():
        raise ValueError("Error: GPT response is empty!")
    return response_text



# Option 2: Use a Conversational Memory Chain (Advanced)
# If you want deeper context tracking (like remembering multiple turns), you’d need to implement a memory-aware chain using LangChain or a custom context window. But for now, including the last assistant message is a great lightweight fix.