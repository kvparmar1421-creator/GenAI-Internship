
from pymilvus import MilvusClient

# Connect to local Milvus database
client = MilvusClient("./student_knowledge.db")

collection_name = "learning_resources"

try:
    # Create collection
    if client.has_collection(collection_name):
        client.drop_collection(collection_name)

    client.create_collection(
        collection_name=collection_name,
        dimension=4
    )

    # Store learning resources
    documents = [
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3, 0.4],
            "topic": "Python",
            "content": "Python is used for programming and automation."
        },
        {
            "id": 2,
            "vector": [0.2, 0.3, 0.4, 0.5],
            "topic": "RAG",
            "content": "RAG retrieves relevant information for AI answers."
        },
        {
            "id": 3,
            "vector": [0.8, 0.7, 0.6, 0.5],
            "topic": "Database",
            "content": "Databases store and manage information."
        }
    ]

    # Insert documents
    client.insert(
        collection_name=collection_name,
        data=documents
    )

    print("Learning resources saved successfully!")

    # Search for similar information
    query_vector = [0.1, 0.2, 0.3, 0.4]

    results = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=2,
        output_fields=["topic", "content"]
    )

    print("\nRelevant learning resources:")

    for item in results[0]:
        print("\nTopic:", item["entity"]["topic"])
        print("Content:", item["entity"]["content"])
        print("Similarity distance:", item["distance"])

except Exception as error:
    print("Error:", error)

finally:
    client.close()
