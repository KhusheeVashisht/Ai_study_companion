from langchain_community.document_loaders import PyPDFLoader


def load_pdf(filepath):

    loader = PyPDFLoader(filepath)

    documents = loader.load()

    return documents