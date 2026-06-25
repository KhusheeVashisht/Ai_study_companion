from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from dotenv import (
    load_dotenv
)

load_dotenv()


def ask_question(
        db,
        question
):

    docs = (
        db.similarity_search(
            question,
            k=3
        )
    )

    context = "\n\n".join(
        [
            doc.page_content
            for doc in docs
        ]
    )

    llm = (
        ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        )
    )

    prompt = f"""
Answer only from the provided notes.

Notes:
{context}

Question:
{question}
"""

    response = (
        llm.invoke(
            prompt
        )
    )

    return (
        response.content,
        docs
    )