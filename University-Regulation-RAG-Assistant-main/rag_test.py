import chromadb
import ollama

from embedding_model import create_embedding


# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="university_regulations"
)


# Ask a question
question = input("\nEnter your question: ")

# Create embedding for the question
query_embedding = create_embedding(question)

# -----------------------------------------
# 1. Semantic search using ChromaDB
# -----------------------------------------

semantic_results = collection.query(
    query_embeddings=[query_embedding],
    n_results=10
)

semantic_documents = semantic_results["documents"][0]
semantic_metadatas = semantic_results["metadatas"][0]
semantic_distances = semantic_results["distances"][0]


# -----------------------------------------
# 2. Keyword search using chunks.json
# -----------------------------------------

import json
import re

with open("chunks.json", "r", encoding="utf-8") as file:
    all_chunks = json.load(file)


# Convert question into useful words
question_words = re.findall(
    r"\b[a-zA-Z]{3,}\b",
    question.lower()
)

# Remove common words
stop_words = {
    "what", "when", "where", "which", "who",
    "how", "why", "does", "this", "that",
    "are", "the", "for", "from", "with",
    "used", "using", "about", "into",
    "can", "will", "shall"
}

question_keywords = [
    word for word in question_words
    if word not in stop_words
]


keyword_results = []

for chunk in all_chunks:

    text = chunk["text"].lower()

    keyword_matches = 0

    for keyword in question_keywords:
        if keyword in text:
            keyword_matches += 1

    if keyword_matches > 0:
        keyword_results.append(
            (
                keyword_matches,
                chunk
            )
        )


# Sort keyword results
keyword_results.sort(
    key=lambda x: x[0],
    reverse=True
)


# -----------------------------------------
# 3. Combine semantic + keyword results
# -----------------------------------------

candidate_chunks = {}


# Add semantic results
for document, metadata, distance in zip(
    semantic_documents,
    semantic_metadatas,
    semantic_distances
):

    key = (
        metadata["page_number"],
        metadata["chunk_number"]
    )

    candidate_chunks[key] = {
        "text": document,
        "metadata": metadata,
        "semantic_distance": distance,
        "keyword_score": 0
    }


# Add keyword results
for keyword_score, chunk in keyword_results[:20]:

    key = (
        chunk["page_number"],
        chunk["chunk_number"]
    )

    if key not in candidate_chunks:

        candidate_chunks[key] = {
            "text": chunk["text"],
            "metadata": {
                "source": "R26_Regulations_B.Tech.pdf",
                "page_number": chunk["page_number"],
                "chunk_number": chunk["chunk_number"]
            },
            "semantic_distance": 999,
            "keyword_score": keyword_score
        }

    else:

        candidate_chunks[key]["keyword_score"] = keyword_score


# -----------------------------------------
# 4. Rerank combined candidates
# -----------------------------------------

ranked_chunks = list(candidate_chunks.values())


for chunk in ranked_chunks:

    semantic_score = 0

    if chunk["semantic_distance"] != 999:
        semantic_score = 1 / (
            1 + chunk["semantic_distance"]
        )

    keyword_score = chunk["keyword_score"]

    chunk["final_score"] = (
        semantic_score + keyword_score * 0.15
    )


ranked_chunks.sort(
    key=lambda x: x["final_score"],
    reverse=True
)


# -----------------------------------------
# 5. Select final context
# -----------------------------------------
# -----------------------------------------
# 5. Check retrieval relevance
# -----------------------------------------

# -----------------------------------------
# 5. Check keyword relevance
# -----------------------------------------

if not ranked_chunks:
    print("\n===== ANSWER =====\n")
    print(
        "I could not find this information in the provided "
        "university regulations."
    )
    exit()


# Get the most important words from the question
question_keywords = set(
    word.lower()
    for word in re.findall(r"\b[a-zA-Z]{3,}\b", question)
    if word.lower() not in stop_words
)


# Combine the top retrieved chunks
top_text = " ".join(
    chunk["text"].lower()
    for chunk in ranked_chunks[:5]
)


# Count how many question keywords appear
# in the retrieved regulation text
matched_keywords = [
    keyword
    for keyword in question_keywords
    if keyword in top_text
]


keyword_overlap = len(matched_keywords)


print("\n===== RELEVANCE CHECK =====")
print("Question keywords:", list(question_keywords))
print("Matched keywords:", matched_keywords)
print("Keyword overlap:", keyword_overlap)
top_chunks = ranked_chunks[:5]

documents = [
    chunk["text"]
    for chunk in top_chunks
]

metadatas = [
    chunk["metadata"]
    for chunk in top_chunks
]

print("\n===== RETRIEVED CHUNKS =====\n")

for chunk in top_chunks:

    print(
        "Page:",
        chunk["metadata"]["page_number"],
        "| Chunk:",
        chunk["metadata"]["chunk_number"],
        "| Score:",
        round(chunk["final_score"], 3)
    )
# Build context
context = ""

for i, document in enumerate(documents):

    page_number = metadatas[i]["page_number"]

    context += f"""
Source: R26_Regulations_B.Tech.pdf
Page: {page_number}

{document}

-------------------------
"""


# Create prompt for LLM
prompt = f"""
You are a University Regulation Assistant.

Answer the user's question using ONLY the information
provided in the regulation context below.

Do not use outside knowledge.
Do not make up information.

If the answer cannot be found in the provided context,
say:

"I could not find this information in the provided university regulations."

Regulation Context:
{context}

User Question:
{question}

Give a clear and concise answer.
"""


# Send prompt to Ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)


# Display answer
print("\n===== ANSWER =====\n")
print(response["message"]["content"])


# Display sources
print("\n===== SOURCES =====\n")

for metadata in metadatas:

    print(
        f"R26_Regulations_B.Tech.pdf - "
        f"Page {metadata['page_number']}"
    )