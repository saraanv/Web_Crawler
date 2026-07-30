import os

from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

from langchain_huggingface import HuggingFaceEmbeddings

from langchain_chroma import Chroma

from langchain_core.prompts import ChatPromptTemplate

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


def get_vectorstore():

    embeddings = get_embeddings()

    db = Chroma(
        persist_directory="data/chroma_db",
        embedding_function=embeddings
    )

    return db



def get_llm():

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=OPENAI_API_KEY
    )

    return llm


def create_rag_chain():

    vectorstore = get_vectorstore()


    retriever = vectorstore.as_retriever(
        search_kwargs={
            "k":4
        }
    )


    prompt = ChatPromptTemplate.from_template(
        """
تو یک دستیار بیمارستان هستی.

فقط بر اساس Context جواب بده.

اگر جواب در Context نبود بگو:
"اطلاعاتی در سایت پیدا نشد."

Context:

{context}


Question:

{input}

"""
    )


    llm = get_llm()


    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )


    rag_chain = create_retrieval_chain(
        retriever,
        document_chain
    )


    return rag_chain


if __name__ == "__main__":

    chain = create_rag_chain()


    response = chain.invoke(
        {
            "input":
            "شماره تماس بیمارستان میلاد چیست؟"
        }
    )


    print("\nANSWER:")
    print(response["answer"])


    print("\nSOURCES:")

    for doc in response["context"]:
        print(
            doc.metadata["url"]
        )