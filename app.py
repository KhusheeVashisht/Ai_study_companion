import streamlit as st
import os

from backend.pdf_loader import load_document
from backend.vector_store import create_vector_store
from backend.rag_engine import ask_question


st.set_page_config(
    page_title="AI Study Companion",
    layout="wide"
)

st.title("🎓 AI Study Companion")


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
            "📄 Reading uploaded document..."
        )

        docs = load_document(
            path
        )

        st.write(
            "✂️ Splitting document..."
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

    question = st.text_input(
        "Ask about the uploaded document"
    )

    if question:

        with st.status(
            "Generating answer...",
            expanded=True
        ) as answer_status:

            st.write(
                "🔍 Searching relevant chunks..."
            )

            st.write(
                "📚 Collecting supporting evidence..."
            )

            st.write(
                "✨ Generating response..."
            )

            answer, sources = (
                ask_question(
                    db,
                    question,
                    answer_mode
                )
            )

            answer_status.update(
                label="Answer ready",
                state="complete"
            )

        st.subheader(
            "Answer"
        )

        st.write(
            answer
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