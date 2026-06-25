import streamlit as st
import os

from backend.pdf_loader import load_pdf
from backend.vector_store import create_vector_store
from backend.rag_engine import ask_question


st.set_page_config(
    page_title="AI Study Companion",
    layout="wide"
)

st.title("🎓 AI Study Companion")


uploaded = st.file_uploader(
    "Upload study material",
    type=["pdf"]
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

    docs = load_pdf(
        path
    )

    st.success(
        "PDF loaded successfully!"
    )

    st.write(
        f"Pages detected: {len(docs)}"
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

    db, chunks = (
        create_vector_store(
            docs
        )
    )

    st.success(
        "Knowledge base ready!"
    )

    st.write(
        f"Chunks created: {len(chunks)}"
    )

    question = st.text_input(
        "Ask your notes"
    )

    if question:

        with st.spinner(
            "Thinking..."
        ):

            answer, sources = (
                ask_question(
                    db,
                    question
                )
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

            st.write(
                f"Source {i}"
            )

            st.info(
                source.page_content[:300]
            )