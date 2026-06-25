from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

from dotenv import (
    load_dotenv
)

load_dotenv()


STYLE_PROMPTS = {

    "Short":
    "Answer briefly and directly.",

    "Detailed":
    "Answer thoroughly and include explanations.",

    "Exam Answer":
    "Write in exam style with introduction, body and conclusion.",

    "Bullet Points":
    "Answer using bullet points only.",

    "Simple Explanation":
    "Explain in very easy language."
}


def ask_question(
        db,
        question,
        answer_mode
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

    style = (
        STYLE_PROMPTS.get(
            answer_mode,
            STYLE_PROMPTS["Detailed"]
        )
    )

    prompt = f"""
Answer ONLY using uploaded document content.

If there is not enough information,
say:

"I could not find enough evidence in the uploaded document."

Response Style:
{style}

Document:
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