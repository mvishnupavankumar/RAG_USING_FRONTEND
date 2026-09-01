from __future__ import annotations

from langchain_community.vectorstores import FAISS

from config import LAMBDA_MULT, RETRIEVER_FETCH_K, RETRIEVER_K


def retrieve(vectorstore: FAISS, query: str) -> list[tuple[object, float]]:
    embedding = vectorstore.embeddings.embed_query(query)
    return vectorstore.max_marginal_relevance_search_with_score_by_vector(
        embedding,
        k=RETRIEVER_K,
        fetch_k=RETRIEVER_FETCH_K,
        lambda_mult=LAMBDA_MULT,
    )
