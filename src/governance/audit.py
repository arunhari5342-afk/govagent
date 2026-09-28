import json
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)


def initialize_audit_table() -> None:
    with engine.begin() as connection:
        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id BIGSERIAL PRIMARY KEY,
                    session_id TEXT,
                    action TEXT NOT NULL,
                    route TEXT,
                    tool_name TEXT,
                    approval_id BIGINT,
                    status TEXT NOT NULL,
                    reviewer TEXT,
                    details JSONB,
                    created_at TIMESTAMPTZ NOT NULL
                )
                """
            )
        )


def write_audit_log(
    session_id: str | None,
    action: str,
    route: str | None = None,
    tool_name: str | None = None,
    approval_id: int | None = None,
    status: str = "success",
    reviewer: str | None = None,
    details: dict | None = None,
) -> None:

    with engine.begin() as connection:
        connection.execute(
            text(
                """
                INSERT INTO audit_logs (
                    session_id,
                    action,
                    route,
                    tool_name,
                    approval_id,
                    status,
                    reviewer,
                    details,
                    created_at
                )
                VALUES (
                    :session_id,
                    :action,
                    :route,
                    :tool_name,
                    :approval_id,
                    :status,
                    :reviewer,
                    CAST(:details AS JSONB),
                    :created_at
                )
                """
            ),
            {
                "session_id": session_id,
                "action": action,
                "route": route,
                "tool_name": tool_name,
                "approval_id": approval_id,
                "status": status,
                "reviewer": reviewer,
                "details": json.dumps(
                    details or {}
                ),
                "created_at": datetime.now(
                    timezone.utc
                ),
            },
        )
