import json
import os

import chromadb

from sentence_transformers import SentenceTransformer


DATA_PATH = "data/clean_pages.json"

CHROMA_PATH = "data/chroma_db"


COLLECTION_NAME = "milad_hospital"


print("Loading embedding model...")

model = SentenceTransformer(
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


def split_text(text, chunk_size=120):

    words = text.split()

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[i:i + chunk_size]
        )

        if len(chunk.strip()) > 50:
            chunks.append(chunk)

    return chunks



def create_embeddings():


    with open(
        DATA_PATH,
        encoding="utf-8"
    ) as f:

        pages = json.load(f)



    documents = []

    metadatas = []

    ids = []



    counter = 0



    for page in pages:


        chunks = split_text(
            page["text"]
        )


        for chunk in chunks:


            documents.append(
                chunk
            )


            metadatas.append(
                {
                    "url": page["url"]
                }
            )


            ids.append(
                f"chunk_{counter}"
            )


            counter += 1



    print(
        f"Total chunks: {len(documents)}"
    )



    print(
        "Creating embeddings..."
    )


    embeddings = model.encode(
        documents,
        show_progress_bar=True
    )



    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )



    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )



    collection.add(

        documents=documents,

        embeddings=embeddings.tolist(),

        metadatas=metadatas,

        ids=ids

    )



    print(
        "Vector database created successfully"
    )



if __name__ == "__main__":

    create_embeddings()