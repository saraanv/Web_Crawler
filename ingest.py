import json
import os

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter



DATA_FILE = "data/pages.json"

CHROMA_PATH = "data/chroma_db"



def load_pages():

    with open(
        DATA_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        pages = json.load(f)


    documents = []


    for page in pages:

        doc = Document(
            page_content=page["text"],
            metadata={
                "url": page["url"]
            }
        )

        documents.append(doc)


    return documents




def create_database():


    print("Loading pages...")


    documents = load_pages()


    print(
        f"Pages: {len(documents)}"
    )


    splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


    chunks = splitter.split_documents(
        documents
    )


    print(
        f"Chunks: {len(chunks)}"
    )



    print(
        "Loading embedding model..."
    )


    embeddings = HuggingFaceEmbeddings(

        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

    )



    print(
        "Creating Chroma..."
    )


    db = Chroma.from_documents(

        documents=chunks,

        embedding=embeddings,

        persist_directory=CHROMA_PATH

    )


    print(
        "Database created!"
    )



    print(
        "Count:",
        db._collection.count()
    )




if __name__ == "__main__":

    create_database()