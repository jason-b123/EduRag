import streamlit as st
import tempfile
import shutil
from pathlib import Path

from src.document_loader import load_pdf
from src.vector_store import create_vector_store
from src.retriever import retrieve_documents
from src.generator import generate_answer, get_sources


st.set_page_config(
    page_title="EduRAG",
    page_icon="📚",
    layout="wide"
)


st.title("📚 EduRAG")
st.caption("Academic Document Question Answering System")


# =========================
# SIDEBAR
# =========================

st.sidebar.header("📄 Document")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDF documents",
    type=["pdf"],
    accept_multiple_files=True
)


# =========================
# DOCUMENT PROCESSING
# =========================

if uploaded_files:

    st.sidebar.success(
        f"{len(uploaded_files)} PDF selected"
    )

    for uploaded_file in uploaded_files:
        st.sidebar.write(f"📄 {uploaded_file.name}")

    if st.sidebar.button("🔄 Process Documents"):

        all_documents = []

        with st.spinner("Processing documents..."):

            with tempfile.TemporaryDirectory() as temp_dir:

                for uploaded_file in uploaded_files:

                    # Simpan PDF sementara dengan nama asli
                    temp_path = (
                        Path(temp_dir) / uploaded_file.name
                    )

                    with open(temp_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    # Load isi PDF
                    documents = load_pdf(str(temp_path))

                    # Pastikan metadata source menggunakan
                    # nama file asli
                    for doc in documents:
                        doc.metadata["source"] = uploaded_file.name

                    all_documents.extend(documents)

            # Buat satu vector store dari semua PDF
            vector_store = create_vector_store(all_documents)

            st.session_state.vector_store = vector_store
            st.session_state.document_names = [
                file.name for file in uploaded_files
            ]
            st.session_state.page_count = len(all_documents)

        st.sidebar.success("Documents processed!")

# =========================
# DOCUMENT STATUS
# =========================

if "vector_store" in st.session_state:

    st.success(
        f"📚 {len(st.session_state.document_names)} documents "
        f"processed, with "
        f"{st.session_state.page_count} pages in total."
    )

    with st.expander("View processed documents"):
        for name in st.session_state.document_names:
            st.write(f"📄 {name}")

    st.divider()

    st.subheader("💬 Ask about your document")

    query = st.text_input(
        "Question",
        placeholder="Contoh: Apa yang dimaksud dengan Interrupt Service Routine?"
    )

    if query:

        with st.spinner("Searching document..."):

            documents = retrieve_documents(
                st.session_state.vector_store,
                query,
                k=3
            )
            # =========================
            # GENERATE ANSWER
            # =========================

            with st.spinner("Generating answer..."):

                answer = generate_answer(
                    query,
                    documents
                )

            st.subheader("🤖 Answer")

            st.write(answer)

        st.subheader("🔎 Retrieved Information")

        for i, doc in enumerate(documents):

            page = doc.metadata.get("page")

            if isinstance(page, int):
                page += 1

            with st.expander(
                f"Result {i + 1} — Page {page}"
            ):
                st.write(doc.page_content)


        # =========================
        # SOURCES
        # =========================

        sources = get_sources(documents)

        st.subheader("📚 Sources")

        for source in sources:

            st.write(
                f"📄 {Path(source['source']).name} "
                f"— Page {source['page']}"
            )

else:

    st.info(
        "Upload PDF kemudian klik "
        "**Process Document** untuk memulai."
    )