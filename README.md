# EduRAG — Academic Document Question Answering System

EduRAG is a Retrieval-Augmented Generation (RAG) application that allows users to upload academic PDF documents and ask questions based on their contents.

The system retrieves relevant information from uploaded documents and uses Google Gemini to generate contextual answers with source references.

## Features

- **Multi-PDF Upload:** Upload and process multiple academic PDF documents.
- **Document Processing:** Extract text and metadata from PDF files.
- **Vector Search:** Store document embeddings using ChromaDB.
- **MMR Retrieval:** Retrieve relevant and diverse document chunks.
- **AI-Powered Answers:** Generate contextual answers using Google Gemini.
- **Source References:** Display the original document name and page number.

## Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| Programming Language | Python |
| LLM Orchestration | LangChain |
| Embedding Model | Google Gemini Embedding |
| Generative Model | Google Gemini |
| Vector Database | ChromaDB |
| PDF Processing | PyMuPDF |

## Project Structure

```text
EduRAG/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── document_loader.py
│   ├── text_splitter.py
│   ├── vector_store.py
│   ├── retriever.py
│   └── generator.py
├── test_generator.py
├── test_loader.py
├── test_retriever.py
└── test_sources.py
```

## How It Works

1. Users upload one or more academic PDF documents.
2. EduRAG extracts document text and metadata.
3. Documents are split into smaller text chunks.
4. Gemini generates embeddings for the chunks.
5. ChromaDB stores the embeddings.
6. MMR retrieves relevant context for the user's question.
7. Google Gemini generates an answer based on the retrieved context.
8. The application displays the answer and its source references.

## Current Status

EduRAG currently supports multi-document PDF processing, vector-based retrieval, AI-generated answers, and source references.

Future improvements may include hybrid search, reranking, retrieval evaluation, and persistent document management.
