import re
from app.models.vector_store import load_vector_store
from app.models.llm_model import get_llm

qna_system_message = """
You are a versatile and helpful AI assistant that can handle multiple modes of interaction based only on the provided context.
User input will contain the necessary context starting with the token: ###Context.
The context contains relevant portions of one or more documents.

User questions will start with the token: ###Question.

You can handle the following types of queries based on user intent:
1. Natural Question Answering — Give clear, concise numbered steps.
2. Document Chat — Respond conversationally while staying grounded in context.
3. Chapter Summarization — Provide a short, clear summary in bullet points.
4. Quiz Mode — Create up to 5 multiple-choice questions with 4 options each and clearly mark the correct answer.
5. Multi-Document Support — If relevant, indicate which document a point comes from (e.g., "(Doc 2)").
6. Citation & Source Tracking — If asked, include inline citations [source_x] and list references at the end.
7. Language Support — If requested, answer in the target language.
8. Personal Learning Journal — Provide a short reflection and 3 actionable learning items.

Rules:
- Always use ONLY the given context to answer.
- If the answer is not in the context, respond exactly: "I don't know".
- Do not explicitly mention the context in your final answer.
- Adjust your answer style according to the detected query type.
"""

qna_user_message_template = """
###Context
Here are some documents that are relevant to the question mentioned below.
{context}

###Question
{question}

###Instructions
Determine the type of query from the question (QA, summarization, quiz, etc.) and follow the system rules for formatting.
"""

def answer_question(query: str):
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_type='similarity', search_kwargs={"k": 5})

    
    relevant_document_chunks = retriever.invoke(query)

    context_text = "\n\n".join([doc.page_content for doc in relevant_document_chunks])

    user_message = qna_user_message_template.format(
        context=context_text,
        question=query
    )

    llm = get_llm()
    response = llm.invoke([
        {"role": "system", "content": qna_system_message},
        {"role": "user", "content": user_message}
    ])

    return {
        "answer": response.content,
        
    }
