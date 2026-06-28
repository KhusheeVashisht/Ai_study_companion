import streamlit as st


def export_output(
    content,
    filename
):

    st.download_button(
        label=f"Download {filename}",
        data=content,
        file_name=filename,
        mime="text/plain"
    )