import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


def main():
    with engine.begin() as connection:

        # Enable pgvector extension
        connection.execute(
            text("CREATE EXTENSION IF NOT EXISTS vector")
        )

        # Create policy_documents table
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS policy_documents (
                    id SERIAL PRIMARY KEY,
                    filename TEXT NOT NULL,
                    title TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )

        # Create policy_chunks table
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS policy_chunks (
                    id SERIAL PRIMARY KEY,
                    document_id INTEGER NOT NULL
                        REFERENCES policy_documents(id)
                        ON DELETE CASCADE,
                    chunk_index INTEGER NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector(384),
                    metadata JSONB DEFAULT '{}'::jsonb,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )

    print("Database initialized successfully.")
    print("pgvector extension and policy tables are ready.")


if __name__ == "__main__":
    main()