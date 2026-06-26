from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader
)


def load_document(
        filepath
):

    if filepath.endswith(
        ".pdf"
    ):

        loader = (
            PyPDFLoader(
                filepath
            )
        )

    elif filepath.endswith(
        ".txt"
    ):

        loader = (
            TextLoader(
                filepath
            )
        )

    elif filepath.endswith(
        ".docx"
    ):

        loader = (
            Docx2txtLoader(
                filepath
            )
        )

    else:

        raise Exception(
            "Unsupported format"
        )

    return loader.load()