from memory.vector_db import VectorDB
from memory.retriever import Retriever

# initialize components
vector_db = VectorDB()
retriever = Retriever()

# add controlled test documents
vector_db.add_document(
    text="The customs duty rate in India is around 10 percent for many goods.",
    metadata={"source": "test1", "title": "India Customs"}
)

vector_db.add_document(
    text="Customs duties are taxes imposed on imports and exports.",
    metadata={"source": "test2", "title": "General Definition"}
)

vector_db.add_document(
    text="Warehouse robotics is transforming logistics operations.",
    metadata={"source": "test3", "title": "Logistics Robotics"}
)

# run retrieval
query = "customs duty rate india"

documents = retriever.retrieve(query, k=3)

print("\nRetrieved Documents:\n")

for doc in documents:
    print(doc)
    print("\n---\n")