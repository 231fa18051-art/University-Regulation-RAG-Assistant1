import chromadb

# Connect to the existing ChromaDB database
client = chromadb.PersistentClient(path="chroma_db")

# Get our collection
collection = client.get_collection(
    name="university_regulations"
)

# Test question
query = "Table 14 Grading Information 90 80 70 60 50 46 Grade Points"

# Search ChromaDB
results = collection.query(
    query_texts=[query],
    n_results=5
)

print("\n===== RETRIEVED RESULTS =====\n")

for i in range(len(results["documents"][0])):
    print(f"--- Result {i + 1} ---")

    print("Page:", results["metadatas"][0][i]["page_number"])
    print("Chunk:", results["metadatas"][0][i]["chunk_number"])

    print("\nText:")
    print(results["documents"][0][i])

    print("\nDistance:", results["distances"][0][i])
    print("\n")
