from retriever import retrieve_chunks
from formatter import format_docs
from chat_complettion import chat_with_model  # Reuse the existing chat_with_model function

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