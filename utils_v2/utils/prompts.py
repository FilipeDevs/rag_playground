STANDALONE_TEMPLATE = """
Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question, in its original language.

Chat History:

{chat_history}

Follow Up Input: {question}
Standalone question:"""

QUESTION_CONTEXT_TEMPLATE = """
Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context:

{context}
---

Question: {question}
Helpful Answer:"""
