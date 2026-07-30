from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def get_embeddings():

    return HuggingFaceEmbeddings(
        model_name=
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    )


db = Chroma(
    persist_directory="data/chroma_db",
    embedding_function=get_embeddings()
)


print("Count:")
print(
    db._collection.count()
)


results = db.similarity_search(
    "آدرس بیمارستان میلاد کجاست؟",
    k=3
)


print("\nRESULTS:\n")


for i, doc in enumerate(results):

    print("----------------")
    print(i+1)

    print(doc.page_content[:500])

    print(
        doc.metadata
    )