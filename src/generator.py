from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def generate_answer(query, documents):
    """
    Generate an answer based only on retrieved documents.
    """

    # Membuat context dari dokumen hasil retrieval
    context_parts = []

    for i, doc in enumerate(documents, start=1):

        page = doc.metadata.get("page")

        # PyMuPDF menggunakan page index mulai dari 0
        if isinstance(page, int):
            page = page + 1

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        context_parts.append(
            f"""
[Sumber {i}]
File: {source}
Halaman: {page}

{doc.page_content}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
Kamu adalah asisten akademik untuk sistem EduRAG.

Jawablah pertanyaan pengguna berdasarkan CONTEXT
yang diberikan.

ATURAN:
1. Gunakan informasi dari CONTEXT sebagai dasar jawaban.
2. Kamu boleh menyimpulkan atau merangkum informasi
   yang terdapat dalam CONTEXT.
3. Jangan menggunakan pengetahuan dari luar CONTEXT.
4. Jika CONTEXT tidak memiliki informasi yang relevan,
   katakan:
   "Informasi tersebut tidak ditemukan dalam dokumen."
5. Jawab dalam bahasa Indonesia.
6. Jawab dengan jelas dan ringkas.
7. Jangan membuat fakta baru yang tidak didukung oleh CONTEXT.

CONTEXT:
{context}

PERTANYAAN:
{query}

JAWABAN:
"""

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.8-flash"
    )

    response = llm.invoke(prompt)

    # Gemini dapat mengembalikan content dalam bentuk
    # string atau list of dictionaries.
    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):

        texts = []

        for item in response.content:

            if isinstance(item, dict):

                text = item.get("text")

                if text:
                    texts.append(text)

            elif isinstance(item, str):
                texts.append(item)

        return "\n".join(texts)

    return str(response.content)


def get_sources(documents):
    """
    Mengambil source dan halaman dari dokumen hasil retrieval.
    """

    sources = []
    seen = set()

    for doc in documents:

        source = doc.metadata.get(
            "source",
            "Unknown"
        )

        page = doc.metadata.get("page")

        if isinstance(page, int):
            page = page + 1

        source_key = (source, page)

        if source_key in seen:
            continue

        seen.add(source_key)

        sources.append({
            "source": source,
            "page": page
        })

    return sources