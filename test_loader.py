from src.document_loader import load_pdf
from src.vector_store import create_vector_store


pdf_path = "data/documents/machine_learning.pdf"

documents = load_pdf(pdf_path)

print("Jumlah halaman:", len(documents))

vector_store = create_vector_store(documents)

print("Vector store berhasil dibuat!")