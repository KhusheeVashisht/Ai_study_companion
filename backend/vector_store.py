from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings


def create_vector(docs):

    embed=OpenAIEmbeddings()

    db=FAISS.from_documents(
        docs,
        embed
    )

    return db