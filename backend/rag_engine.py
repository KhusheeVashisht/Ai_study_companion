from langchain.chains import RetrievalQA


def ask(query,llm,db):

    chain=RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever()
    )

    return chain.run(query)