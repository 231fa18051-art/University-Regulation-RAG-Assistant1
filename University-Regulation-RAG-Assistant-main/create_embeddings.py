import json
from sentence_transformers import SentenceTransformer

INPUT_PATH = "chunks.json"
OUTPUT_PATH = "embeddings.json"

# Load chunks
with open(INPUT_PATH, "r", encoding="utf-8") as file:
    chunks = json.load(file)

# Load embedding model
print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded!")

# Extract text from chunks
texts = [chunk["text"] for chunk in chunks]

# Create embeddings
print("Creating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

# Add embeddings to each chunk
for chunk, embedding in zip(chunks, embeddings):
    chunk["embedding"] = embedding.tolist()

# Save embeddings
with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False)

print("\nEmbedding creation completed!")
print("Total chunks:", len(chunks))
print("Saved embeddings to:", OUTPUT_PATH)
