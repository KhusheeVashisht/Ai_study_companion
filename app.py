import streamlit as st

st.set_page_config(
    page_title="AI Study Companion",
    layout="wide"
)

st.title("🎓 AI Study Companion")

uploaded = st.file_uploader(
    "Upload your notes",
    type=["pdf"]
)

if uploaded:

    st.success(
        f"{uploaded.name} uploaded!"
    )