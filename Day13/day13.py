import chromadb

client = chromadb.Client()

collection = client.create_collection(name="doc_genai")

documents =[ "Python Programming: Python is a beginner-friendly programming language used for web development, automation, data science, and AI.",

    "Machine Learning: Machine learning is a branch of artificial intelligence that enables computers to learn patterns from data and make predictions.",

    "Artificial Intelligence: AI enables machines to perform tasks that normally require human intelligence, such as reasoning, learning, and problem-solving.",

    "Web Development: Web development involves creating websites using HTML, CSS, JavaScript, and backend programming languages such as Python.",

    "Data Science: Data science involves collecting, cleaning, analyzing, and visualizing data to discover useful insights."
]


collection.add(
    ids=["1","2","3","4","5"],
    documents=documents
)

result = collection.query(
    query_texts=["What is the Machine Learning ?"],
    n_results=3
)

print(result)