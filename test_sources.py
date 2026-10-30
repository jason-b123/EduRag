from src.vector_store import load_vector_store
from src.retriever import retrieve_documents
from src.generator import get_sources


vector_store = load_vector_store()

query = "Apa yang dimaksud dengan Interrupt Service Routine?"

documents = retrieve_documents(
    vector_store,
    query,
    k=3
)

sources = get_sources(documents)

print("\n===== SOURCES =====")

for source in sources:
    print(f"📄 {source['source']} — Page {source['page']}")