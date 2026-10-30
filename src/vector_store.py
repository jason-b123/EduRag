import os
import shutil

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
load_dotenv()

CHROMA_PATH = "chroma_db"


def create_vector_store(documents):
    # Bersihkan vector store sebelumnya
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

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

    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )

    return vector_store

def load_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )

    return vector_store