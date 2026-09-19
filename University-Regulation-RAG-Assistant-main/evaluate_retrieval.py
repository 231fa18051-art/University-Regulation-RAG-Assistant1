import json
import re
import chromadb

from embedding_model import create_embedding


# -----------------------------------------
# Load evaluation questions
# -----------------------------------------

with open(
    "evaluation_questions.json",
    "r",
    encoding="utf-8"
) as file:

    questions = json.load(file)


# -----------------------------------------
# Load chunks
# -----------------------------------------

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as file:

    all_chunks = json.load(file)


# -----------------------------------------
# Connect to ChromaDB
# -----------------------------------------

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="university_regulations"
)


# -----------------------------------------
# Stop words
# -----------------------------------------

stop_words = {
    "what", "when", "where", "which", "who",
    "how", "why", "does", "this", "that",
    "are", "the", "for", "from", "with",
    "used", "using", "about", "into",
    "can", "will", "shall"
}


# -----------------------------------------
# Evaluate each question
# -----------------------------------------

for item in questions:

    question = item["question"]
    topic = item["topic"]

    print("\n" + "=" * 70)
    print("Topic:", topic)
    print("Question:", question)
    print("=" * 70)


    # -----------------------------------------
    # Semantic search
    # -----------------------------------------

    query_embedding = create_embedding(question)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    semantic_documents = results["documents"][0]
    semantic_metadatas = results["metadatas"][0]
    semantic_distances = results["distances"][0]


    # -----------------------------------------
    # Keyword search
    # -----------------------------------------

    question_words = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        question.lower()
    )

    question_keywords = [
        word
        for word in question_words
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


    keyword_results.sort(
        key=lambda x: x[0],
        reverse=True
    )


    # -----------------------------------------
    # Combine results
    # -----------------------------------------

    candidate_chunks = {}


    # Semantic results

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


    # Keyword results

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
    # Reranking
    # -----------------------------------------

    ranked_chunks = list(
        candidate_chunks.values()
    )


    for chunk in ranked_chunks:

        semantic_score = 0

        if chunk["semantic_distance"] != 999:

            semantic_score = 1 / (
                1 + chunk["semantic_distance"]
            )

        keyword_score = chunk["keyword_score"]

        chunk["final_score"] = (
            semantic_score
            + keyword_score * 0.15
        )


    ranked_chunks.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    # -----------------------------------------
    # Display top results
    # -----------------------------------------

    print("\nTop retrieved chunks:")

    for rank, chunk in enumerate(
        ranked_chunks[:5],
        start=1
    ):

        print(
            f"{rank}. "
            f"Page {chunk['metadata']['page_number']} "
            f"| Chunk {chunk['metadata']['chunk_number']} "
            f"| Score {chunk['final_score']:.3f}"
        )