import json
import chromadb

INPUT_PATH = "embeddings.json"

# Load embedded chunks
with open(INPUT_PATH, "r", encoding="utf-8") as file:
    chunks = json.load(file)

# Create a persistent ChromaDB client
client = chromadb.PersistentClient(path="chroma_db")

# Create or get our collection
collection = client.get_or_create_collection(
    name="university_regulations"
)

print("Adding documents to ChromaDB...")

# Prepare data
ids = []
documents = []
embeddings = []
metadatas = []

for chunk in chunks:
    ids.append(str(chunk["chunk_id"]))
    documents.append(chunk["text"])
    embeddings.append(chunk["embedding"])

    metadatas.append({
        "source": "R26_Regulations_B.Tech.pdf",
        "page_number": chunk["page_number"],
        "chunk_number": chunk["chunk_number"]
    })

# Add everything to ChromaDB
collection.add(
    ids=ids,
    documents=documents,
    embeddings=embeddings,
    metadatas=metadatas
)

print("ChromaDB creation completed!")
print("Total documents stored:", collection.count())