from src.vector_store import load_vector_store
from src.retriever import retrieve_documents

vector_store = load_vector_store()

query = "Apa yang dimaksud dengan Interrupt Service Routine?"

results = retrieve_documents(
    vector_store,
    query,
    k=3
)

print("\n===== HASIL RETRIEVAL =====")

for i, doc in enumerate(results):
    page = doc.metadata.get("page")

    if isinstance(page, int):
        page = page + 1

    print(f"\n--- Result {i + 1} ---")
    print("Page:", page)

    print("Content:")
    print(doc.page_content)