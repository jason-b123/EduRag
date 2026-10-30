def retrieve_documents(vector_store, query, k=3):
    """
    Retrieve relevant documents using MMR
    (Maximal Marginal Relevance).

    MMR membantu memilih dokumen yang:
    1. Relevan dengan pertanyaan
    2. Tidak terlalu mirip satu sama lain
    """

    results = vector_store.max_marginal_relevance_search(
        query,
        k=k,
        fetch_k=10,
        lambda_mult=0.5
    )

    # Remove exact duplicate chunks
    unique_results = []
    seen = set()

    for doc in results:
        content = doc.page_content.strip()

        if content in seen:
            continue

        seen.add(content)
        unique_results.append(doc)

    return unique_results