import chromadb
client = chromadb.PersistentClient(path="./chroma_db")
collection =client.get_or_create_collection("prilytixs")
collection.add(
documents=["python is user frendly programming languade","We learn python easyly compair to java"],
metadatas=[{"sources":"wikipidea"},{"sources":"prelytix.pdf"}],
ids=["docs1","docs2"]
)
result=collection.query(
    query_texts=["what is python ?"],
    n_results=1

)
print(result)