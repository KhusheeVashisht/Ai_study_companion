import streamlit as st
import os

from backend.pdf_loader import load_document
from backend.vector_store import create_vector_store
from backend.rag_engine import ask_question

from utils.quiz import generate_quiz
from utils.flashcards import generate_flashcards
from utils.export import export_output
from utils.voice import listen_question


# ---------------- PAGE ----------------

st.set_page_config(
    page_title="AI Study Companion",
    layout="wide"
)

st.title(
    "🎓 AI Study Companion"
)


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title(
        "📚 About"
    )

    st.markdown(
        """
### AI Study Companion

Turn documents into learning.

Upload notes, resumes,
research papers or study material
and interact with them using AI.

---

### Features

📄 PDF / TXT / DOCX Upload

🧠 AI Question Answering

📚 Source Retrieval

📝 Quiz Generator

🎴 Flashcards

🎙️ Voice Questions

⬇️ Export Results

---

### Built By

**Khushee Vashisht**

MCA (AI/ML)

GitHub:
https://github.com/KhusheeVashisht

---

✨ Learn smarter.
"""
    )


# ---------------- UPLOAD ----------------

uploaded = st.file_uploader(
    "Upload study material",
    type=[
        "pdf",
        "txt",
        "docx"
    ]
)


if uploaded:

    os.makedirs(
        "data/uploaded_pdfs",
        exist_ok=True
    )

    path = (
        f"data/uploaded_pdfs/{uploaded.name}"
    )

    with open(
        path,
        "wb"
    ) as file:

        file.write(
            uploaded.getbuffer()
        )

    with st.status(
        "Preparing document...",
        expanded=True
    ) as status:

        st.write(
            "📄 Reading document..."
        )

        docs = (
            load_document(
                path
            )
        )

        st.write(
            "✂️ Splitting content..."
        )

        st.write(
            "🧠 Building knowledge base..."
        )

        db, chunks = (
            create_vector_store(
                docs
            )
        )

        status.update(
            label="Document ready",
            state="complete"
        )

    st.success(
        "Knowledge base ready!"
    )

    st.write(
        f"Pages detected: {len(docs)}"
    )

    st.write(
        f"Chunks created: {len(chunks)}"
    )

    preview = ""

    for page in docs[:2]:

        preview += (
            page.page_content
            + "\n\n"
        )

    st.subheader(
        "Preview"
    )

    st.text_area(
        "Preview",
        preview[:3000],
        height=350
    )

    st.divider()

    # ---------------- QUIZ ----------------

    st.subheader(
        "📝 Quiz Generator"
    )

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Easy",
            "Medium",
            "Hard"
        ]
    )

    num_questions = st.slider(
        "Questions",
        1,
        10,
        5
    )

    if st.button(
        "Generate Quiz"
    ):

        with st.status(
            "Creating quiz...",
            expanded=True
        ):

            quiz = (
                generate_quiz(
                    db,
                    difficulty,
                    num_questions
                )
            )

        st.markdown(
            quiz
        )

        export_output(
            quiz,
            "quiz.txt"
        )

    st.divider()

    # ---------------- FLASHCARDS ----------------

    st.subheader(
        "🎴 Flashcards"
    )

    card_count = st.slider(
        "Number of flashcards",
        1,
        15,
        5
    )

    if st.button(
        "Generate Flashcards"
    ):

        with st.status(
            "Creating flashcards...",
            expanded=True
        ):

            cards = (
                generate_flashcards(
                    db,
                    card_count
                )
            )

        st.markdown(
            cards
        )

        export_output(
            cards,
            "flashcards.txt"
        )

    st.divider()

    # ---------------- Q&A ----------------

    st.subheader(
        "💬 Ask Questions"
    )

    answer_mode = st.selectbox(
        "Choose response style",
        [
            "Short",
            "Detailed",
            "Exam Answer",
            "Bullet Points",
            "Simple Explanation"
        ]
    )

    col1, col2 = (
        st.columns(
            [4, 1]
        )
    )

    with col1:

        question = (
            st.text_input(
                "Ask about uploaded document"
            )
        )

    with col2:

        voice = (
            st.button(
                "🎙️ Speak"
            )
        )

    if voice:

        with st.spinner(
            "Listening..."
        ):

            spoken = (
                listen_question()
            )

        if spoken:

            question = spoken

            st.success(
                f"You said: {question}"
            )

        else:

            st.warning(
                "Voice not detected"
            )

    if question:

        with st.status(
            "Generating answer...",
            expanded=True
        ) as status:

            st.write(
                "🔍 Searching chunks..."
            )

            st.write(
                "📚 Collecting evidence..."
            )

            st.write(
                "✨ Generating answer..."
            )

            answer, sources = (
                ask_question(
                    db,
                    question,
                    answer_mode
                )
            )

            status.update(
                label="Answer ready",
                state="complete"
            )

        st.subheader(
            "Answer"
        )

        st.write(
            answer
        )

        export_output(
            answer,
            "answer.txt"
        )

        st.subheader(
            "Sources"
        )

        for i, source in enumerate(
            sources,
            start=1
        ):

            with st.expander(
                f"Source {i}"
            ):

                st.write(
                    source.page_content
                )