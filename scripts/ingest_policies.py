import json
import os
from pathlib import Path

from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

POLICY_DIR = Path("data/policies")

engine = create_engine(DATABASE_URL)

model = SentenceTransformer(EMBEDDING_MODEL)


def chunk_text(
    text_value: str,
    chunk_size: int = 500,
    overlap: int = 50,
):
    words = text_value.split()

    chunks = []
    start = 0

    while start < len(words):
        end = start + chunk_size

        chunk = " ".join(words[start:end]).strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(words):
            break

        start = end - overlap

    return chunks


def ingest_document(file_path: Path):
    content = file_path.read_text(encoding="utf-8")

    chunks = chunk_text(content)

    title = file_path.stem.replace("_", " ").title()

    with engine.begin() as connection:

        existing = connection.execute(
            text(
                """
                SELECT id
                FROM policy_documents
                WHERE filename = :filename
                """
            ),
            {
                "filename": file_path.name,
            },
        ).scalar_one_or_none()

        if existing:
            connection.execute(
                text(
                    """
                    DELETE FROM policy_chunks
                    WHERE document_id = :document_id
                    """
                ),
                {
                    "document_id": existing,
                },
            )

            document_id = existing

        else:
            document_id = connection.execute(
                text(
                    """
                    INSERT INTO policy_documents
                    (filename, title)
                    VALUES (:filename, :title)
                    RETURNING id
                    """
                ),
                {
                    "filename": file_path.name,
                    "title": title,
                },
            ).scalar_one()

        embeddings = model.encode(
            chunks,
            normalize_embeddings=True,
        )

        for index, (chunk, embedding) in enumerate(
            zip(chunks, embeddings)
        ):
            metadata = {
                "source": file_path.name,
                "chunk_index": index,
                "title": title,
            }

            connection.execute(
                text(
                    """
                    INSERT INTO policy_chunks
                    (
                        document_id,
                        chunk_index,
                        content,
                        embedding,
                        metadata
                    )
                    VALUES
                    (
                        :document_id,
                        :chunk_index,
                        :content,
                        CAST(:embedding AS vector),
                        CAST(:metadata AS jsonb)
                    )
                    """
                ),
                {
                    "document_id": document_id,
                    "chunk_index": index,
                    "content": chunk,
                    "embedding": json.dumps(
                        embedding.tolist()
                    ),
                    "metadata": json.dumps(metadata),
                },
            )

    print(
        f"Ingested {file_path.name}: "
        f"{len(chunks)} chunks"
    )


def main():
    if not POLICY_DIR.exists():
        raise FileNotFoundError(
            f"Policy directory not found: {POLICY_DIR}"
        )

    files = sorted(
        POLICY_DIR.glob("*.txt")
    )

    if not files:
        raise RuntimeError(
            "No policy documents found."
        )

    for file_path in files:
        ingest_document(file_path)

    print("\nPolicy ingestion completed.")


if __name__ == "__main__":
    main()