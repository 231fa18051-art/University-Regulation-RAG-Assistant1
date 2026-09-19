import chromadb
import ollama
import json
import re

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from embedding_model import create_embedding
from query_understanding import understand_query


# =========================================================
# Grade Point Mapping
# =========================================================

GRADE_POINT_MAPPING = {
    10: ("O", "Outstanding"),
    9: ("S", "Excellent"),
    8: ("A", "Very good"),
    7: ("B", "Good"),
    6: ("C", "Fair"),
    5: ("M", "Marginal"),
}


# =========================================================
# Marks to Grade Mapping
# =========================================================

MARKS_GRADE_MAPPING = [
    (90, 100, "O", "Outstanding", 10),
    (80, 89.99, "S", "Excellent", 9),
    (70, 79.99, "A", "Very good", 8),
    (60, 69.99, "B", "Good", 7),
    (50, 59.99, "C", "Fair", 6),
    (46, 49.99, "M", "Marginal", 5),
]


# =========================================================
# FastAPI App
# =========================================================

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# Connect to ChromaDB
# =========================================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="university_regulations"
)


# =========================================================
# Load chunks once when server starts
# =========================================================

with open(
    "chunks.json",
    "r",
    encoding="utf-8"
) as file:
    all_chunks = json.load(file)


# =========================================================
# Request format
# =========================================================

class QuestionRequest(BaseModel):
    question: str


# =========================================================
# Home Route
# =========================================================

@app.get("/")
def home():
    return {
        "message": "University Regulation RAG Assistant API is running!"
    }


# =========================================================
# Ask Question
# =========================================================

@app.post("/ask")
def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        return {
            "question": question,
            "answer": "Please enter a question.",
            "sources": []
        }

    question_lower = question.lower()


    # =====================================================
    # Direct Marks Detection
    # =====================================================

    marks_match = re.search(
        r"\b(\d+(?:\.\d+)?)\s*marks?\b",
        question_lower
    )

    marks = None

    if marks_match:
        marks = float(marks_match.group(1))


    # =====================================================
    # Direct Grade Point Detection
    # =====================================================

    grade_point = None

    for point in GRADE_POINT_MAPPING:

        if f"{point} grade point" in question_lower:
            grade_point = point
            break


    # =====================================================
    # Direct Marks → Grade Answer
    # =====================================================

    if marks is not None:

        for (
            min_marks,
            max_marks,
            letter_grade,
            description,
            grade_point_value
        ) in MARKS_GRADE_MAPPING:

            if min_marks <= marks <= max_marks:

                if min_marks == 90:
                    range_text = "90 and above"

                elif min_marks == 80:
                    range_text = "80 to less than 90"

                elif min_marks == 70:
                    range_text = "70 to less than 80"

                elif min_marks == 60:
                    range_text = "60 to less than 70"

                elif min_marks == 50:
                    range_text = "50 to less than 60"

                elif min_marks == 46:
                    range_text = "46 to 49"

                else:
                    range_text = (
                        f"{min_marks:g} to {max_marks:g}"
                    )

                answer = (
                    f"According to Table 14, {marks:g} marks "
                    f"falls in the {range_text} range. "
                    f"The grade is {letter_grade} "
                    f"({description}) with Grade Point "
                    f"{grade_point_value}."
                )

                return {
                    "question": question,
                    "answer": answer,
                    "sources": [
                        {
                            "document": "R26_Regulations_B.Tech.pdf",
                            "page": 43
                        }
                    ]
                }


    # =====================================================
    # Direct Grade Point Answer
    # =====================================================

    if grade_point is not None:

        letter_grade, description = (
            GRADE_POINT_MAPPING[grade_point]
        )

        answer = (
            f"According to Table 14, Grade Point "
            f"{grade_point} corresponds to the "
            f"{letter_grade} grade "
            f"({description})."
        )

        return {
            "question": question,
            "answer": answer,
            "sources": [
                {
                    "document": "R26_Regulations_B.Tech.pdf",
                    "page": 43
                }
            ]
        }


    # =====================================================
    # Query Understanding
    # =====================================================

    expanded_query = understand_query(question)


    # =====================================================
    # Create Query Embedding
    # =====================================================

    query_embedding = create_embedding(
        expanded_query
    )


    # =====================================================
    # Semantic Search
    # =====================================================

    semantic_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=10
    )

    semantic_documents = semantic_results["documents"][0]
    semantic_metadatas = semantic_results["metadatas"][0]
    semantic_distances = semantic_results["distances"][0]


    # =====================================================
    # Keyword Search
    # =====================================================

    question_words = re.findall(
        r"\b[a-zA-Z]{3,}\b",
        expanded_query.lower()
    )

    stop_words = {
        "what",
        "when",
        "where",
        "which",
        "who",
        "how",
        "why",
        "does",
        "this",
        "that",
        "are",
        "the",
        "for",
        "from",
        "with",
        "used",
        "using",
        "about",
        "into",
        "can",
        "will",
        "shall"
    }

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


    # =====================================================
    # Combine Search Results
    # =====================================================

    candidate_chunks = {}


    for (
        document,
        metadata,
        distance
    ) in zip(
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


    for (
        keyword_score,
        chunk
    ) in keyword_results[:20]:

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

            candidate_chunks[key]["keyword_score"] = (
                keyword_score
            )


    # =====================================================
    # Rerank Results
    # =====================================================

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
            +
            keyword_score * 0.15
        )


    ranked_chunks.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )


    # =====================================================
    # Select Top 5 Chunks
    # =====================================================

    top_chunks = ranked_chunks[:5]


    # =====================================================
    # Build Context
    # =====================================================

    context_parts = []

    for chunk in top_chunks:

        page_number = chunk["metadata"]["page_number"]

        context_parts.append(
            f"Page {page_number}:\n"
            f"{chunk['text']}"
        )

    context = "\n\n---\n\n".join(context_parts)


    # =====================================================
    # Short Grounded Prompt
    # =====================================================

    prompt = f"""
You are a university regulation assistant.

Answer the student's question using ONLY the regulation context below.

Rules:
- Do not use outside knowledge.
- Do not invent information.
- Read all relevant context.
- If the answer is supported by the context, answer directly.
- Related wording is acceptable; the exact words do not need to appear.
- If the context genuinely does not contain the answer, say:
"I could not find this information in the provided university regulations."
- Keep the answer concise, preferably 2-4 sentences.

REGULATION CONTEXT:
{context}

STUDENT QUESTION:
{question}

Answer:
"""


    # =====================================================
    # Generate Answer using Qwen
    # =====================================================

    response = ollama.chat(
        model="qwen2.5:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "num_predict": 50
        }
    )


    answer = response["message"]["content"].strip()


    # =====================================================
    # Create Unique Sources
    # =====================================================

    sources = []

    seen_sources = set()

    for chunk in top_chunks:

        metadata = chunk["metadata"]

        source_key = (
            metadata["source"],
            metadata["page_number"]
        )

        if source_key not in seen_sources:

            sources.append(
                {
                    "document": metadata["source"],
                    "page": metadata["page_number"]
                }
            )

            seen_sources.add(source_key)


    # =====================================================
    # Return Response
    # =====================================================

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }