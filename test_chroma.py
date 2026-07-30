import chromadb


client = chromadb.PersistentClient(
    path="data/chroma_db"
)


collection = client.get_collection(
    "milad_hospital"
)


result = collection.query(
    query_texts=[
        "آدرس بیمارستان میلاد کجاست؟"
    ],
    n_results=3
)


for doc in result["documents"][0]:
    print("----------------")
    print(doc)