import chromadb

from embedding_model import create_embedding



client = chromadb.PersistentClient(
    path="data/chroma_db"
)


collection = client.get_collection(
    "milad_hospital"
)



question = "آدرس بیمارستان میلاد کجاست؟"



query_embedding = create_embedding(
    question
)



result = collection.query(

    query_embeddings=[
        query_embedding
    ],

    n_results=3

)



for i in range(3):

    print("----------------")
    
    print(
        result["documents"][0][i]
    )

    print(
        result["metadatas"][0][i]
    )