from src.vector_store import load_vector_store
from src.retriever import retrieve_documents
from src.generator import generate_answer


# Load vector store
vector_store = load_vector_store()


# Pertanyaan
query = "Apa yang dimaksud dengan Interrupt Service Routine?"
# query = "Bagaimana penggunaan Interrupt Service Routine?"


# Retrieval
documents = retrieve_documents(
    vector_store,
    query,
    k=3
)


# Generate answer
answer = generate_answer(
    query,
    documents
)


print("\n===== PERTANYAAN =====")
print(query)

print("\n===== JAWABAN =====")
print(answer)