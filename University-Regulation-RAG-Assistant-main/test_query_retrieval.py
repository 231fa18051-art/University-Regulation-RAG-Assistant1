import chromadb
from embedding_model import create_embedding
from query_understanding import understand_query


client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="university_regulations"
)


questions = [
    # Attendance
    "What is the minimum attendance requirement?",
    "Can I write exams with 72% attendance?",

    # Grading
    "What is the grading system?",
    "I got 85 marks, which grade will I get?",
    "What does 9 grade point mean?",

    # SGPA
    "How do I calculate my SGPA?",
    "How do I find my semester GPA?",

    # CGPA
    "How is CGPA calculated?",
    "How is my overall academic GPA calculated?",

    # Supplementary / Failure
    "What are the rules for supplementary examinations?",
    "I failed a subject. Can I write it again?",

    # Branch Change
    "What is the procedure for changing the branch?",
    "I want to move from CSE to ECE. What should I do?",

    # Promotion
    "What are the rules for promotion to the next semester?",
    "Can I go to the next semester with backlogs?",

    # Credits
    "How many credits are required for completing B.Tech?",
    "How many credits do I need to graduate?",

    # Lateral Entry
    "What are the rules for lateral entry students?",
    "I joined B.Tech after diploma. What rules apply to me?"
]


for question in questions:

    print("\n" + "=" * 80)
    print("QUESTION:", question)

    expanded_query = understand_query(question)

    print("\nEXPANDED QUERY:")
    print(expanded_query)

    query_embedding = create_embedding(expanded_query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    print("\nTOP 3 RETRIEVED RESULTS:")

    for i in range(3):

        metadata = results["metadatas"][0][i]

        print(
            f"Result {i + 1}: "
            f"Page {metadata['page_number']} | "
            f"Chunk {metadata['chunk_number']} | "
            f"Distance {results['distances'][0][i]:.4f}"
        )