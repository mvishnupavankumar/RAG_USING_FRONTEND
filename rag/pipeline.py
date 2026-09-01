from __future__ import annotations

import re
from typing import Iterable

from langchain_core.messages import BaseMessage

from config import MAX_HISTORY_MESSAGES
from llm.model import get_llm
from llm.prompt import prompt
from rag.retriever import retrieve


def _compact_history(history: Iterable[BaseMessage]) -> list[BaseMessage]:
    items = list(history)
    return items[-MAX_HISTORY_MESSAGES:]


def conversational_rag(
    user_input: str,
    chat_history: list[BaseMessage],
    vectorstore,
) -> tuple[str, list[dict]]:
    if vectorstore is None:
        messages = prompt.invoke(
            {
                "question": user_input,
                "context": "No documents have been uploaded to this notebook yet.",
                "chat_history": _compact_history(chat_history),
            }
        )
        response = get_llm().invoke(messages)
        return response.content, []

    docs_with_scores = retrieve(vectorstore, user_input)

    citations = []
    context_blocks = []
    for index, (doc, score) in enumerate(docs_with_scores, start=1):
        source = doc.metadata.get("source", "Unknown")
        chunk_id = doc.metadata.get("chunk_id", "?")
        total_chunks = doc.metadata.get("total_chunks", "?")

        context_blocks.append(
            f"[{index}] Source: {source} (Chunk {chunk_id}/{total_chunks})\n{doc.page_content}"
        )
        citations.append(
            {
                "id": index,
                "source": source,
                "chunk_id": chunk_id,
                "total_chunks": total_chunks,
                "content": doc.page_content,
                "score": round(float(score), 4),
            }
        )

    context = "\n\n".join(context_blocks) or "No relevant context found."

    messages = prompt.invoke(
        {
            "question": user_input,
            "context": context,
            "chat_history": _compact_history(chat_history),
        }
    )

    response = get_llm().invoke(messages)
    answer = response.content

    cited_ids = {int(n) for n in re.findall(r"\[(\d+)\]", answer)}
    if cited_ids:
        used = [citation for citation in citations if citation["id"] in cited_ids]
    else:
        used = citations

    # Retrieval scores are backend diagnostics; keep them out of the user-facing citation card.
    for citation in used:
        citation.pop("score", None)

    return answer, used
