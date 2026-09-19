import json
from langchain_text_splitters import RecursiveCharacterTextSplitter

INPUT_PATH = "regulations_data.json"
OUTPUT_PATH = "chunks.json"

# Load extracted PDF data
with open(INPUT_PATH, "r", encoding="utf-8") as file:
    pages = json.load(file)

# Create text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)

chunks = []

for page in pages:
    page_text = page["text"]
    page_number = page["page_number"]

    split_texts = text_splitter.split_text(page_text)

    for chunk_number, text in enumerate(split_texts, start=1):
        chunks.append({
            "chunk_id": len(chunks) + 1,
            "page_number": page_number,
            "chunk_number": chunk_number,
            "text": text
        })

# Save chunks
with open(OUTPUT_PATH, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)

print("Chunking completed!")
print("Total chunks:", len(chunks))
print("Saved chunks to:", OUTPUT_PATH)