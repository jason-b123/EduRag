import tempfile

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()


def create_vector_store(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)

    print(f"Jumlah dokumen: {len(documents)}")
    print(f"Jumlah chunks: {len(chunks)}")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    # Gunakan direktori sementara yang writable
    chroma_path = tempfile.mkdtemp(
        prefix="edurag_chroma_"
    )

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=chroma_path
    )

    return vector_store
