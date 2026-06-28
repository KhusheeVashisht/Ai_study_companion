from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from dotenv import (
    load_dotenv
)

load_dotenv()


def generate_flashcards(
        db,
        count
):

    docs = (
        db.similarity_search(
            "Generate flashcards",
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
Generate {count}
study flashcards.

Rules:

- Use ONLY uploaded document
- Keep concise
- Format exactly:

Front:
...

Back:
...

Document:
{context}
"""

    response = (
        llm.invoke(
            prompt
        )
    )

    return response.content