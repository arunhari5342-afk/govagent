import json
import os

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text

from src.observability.tracing import trace_span

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

engine = create_engine(DATABASE_URL)

model = SentenceTransformer(EMBEDDING_MODEL)


def retrieve_policy_chunks(
    query: str,
    top_k: int = 3,
) -> list[dict]:
    """
    Retrieve the most relevant policy chunks
    from PostgreSQL/pgvector.
    """

    if not query.strip():
        return []

    with trace_span(
        "retrieval.search",
        {
            "component": "policy_retrieval",
            "query_length": len(query),
            "top_k": top_k,
            "embedding_model": EMBEDDING_MODEL,
        },
    ):

        embedding = model.encode(
            query,
            normalize_embeddings=True,
        )

        embedding_json = json.dumps(embedding.tolist())

        with engine.connect() as connection:

            rows = (
                connection.execute(
                    text("""
                    SELECT
                        pc.id,
                        pc.document_id,
                        pc.chunk_index,
                        pc.content,
                        pc.metadata,
                        pc.embedding <=> CAST(
                            :embedding AS vector
                        ) AS distance
                    FROM policy_chunks pc
                    ORDER BY pc.embedding <=> CAST(
                        :embedding AS vector
                    )
                    LIMIT :top_k
                    """),
                    {
                        "embedding": embedding_json,
                        "top_k": top_k,
                    },
                )
                .mappings()
                .all()
            )

    results = []

    for row in rows:

        results.append(
            {
                "chunk_id": row["id"],
                "document_id": row["document_id"],
                "chunk_index": row["chunk_index"],
                "content": row["content"],
                "metadata": row["metadata"],
                "distance": float(row["distance"]),
            }
        )

    return results


def build_policy_context(
    query: str,
    top_k: int = 3,
) -> str:
    """
    Retrieve policy chunks and combine them
    into grounded LLM context.
    """

    results = retrieve_policy_chunks(
        query=query,
        top_k=top_k,
    )

    if not results:
        return "No relevant policy information was retrieved."

    context_parts = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        metadata = result.get(
            "metadata",
            {},
        )

        source = metadata.get(
            "source",
            "unknown",
        )

        context_parts.append(f"""
[Policy Source {index}]
Source: {source}
Similarity distance: {result["distance"]:.4f}

{result["content"]}
""".strip())

    return "\n\n".join(context_parts)
