from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from dotenv import (
    load_dotenv
)

load_dotenv()


def generate_quiz(
        db,
        difficulty,
        num_questions
):

    docs = (
        db.similarity_search(
            "Generate quiz",
            k=5
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
Generate {num_questions}
multiple choice questions.

Difficulty:
{difficulty}

Rules:

- Use ONLY uploaded document
- 4 options
- Mark correct answer
- Explain answer briefly

Document:
{context}
"""

    response = (
        llm.invoke(
            prompt
        )
    )

    return response.content