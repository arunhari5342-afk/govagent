import json

from sqlalchemy import text

from src.mcp_server.database import engine
from src.mcp_server.tools import create_ticket
from src.observability.tracing import trace_span


def initialize_approval_table():

    with engine.begin() as connection:

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS approvals (
                    id SERIAL PRIMARY KEY,

                    session_id TEXT NOT NULL,

                    action_type TEXT NOT NULL,

                    payload JSONB NOT NULL,

                    status TEXT NOT NULL
                        DEFAULT 'pending',

                    reviewer TEXT,

                    comment TEXT,

                    created_at TIMESTAMP
                        DEFAULT CURRENT_TIMESTAMP,

                    decided_at TIMESTAMP
                )
                """
            )
        )


def create_approval(
    session_id: str,
    action_type: str,
    payload: dict,
):

    initialize_approval_table()

    with engine.begin() as connection:

        row = connection.execute(
            text(
                """
                INSERT INTO approvals
                (
                    session_id,
                    action_type,
                    payload,
                    status
                )
                VALUES
                (
                    :session_id,
                    :action_type,
                    CAST(:payload AS JSONB),
                    'pending'
                )
                RETURNING
                    id,
                    session_id,
                    action_type,
                    payload,
                    status,
                    created_at
                """
            ),
            {
                "session_id": session_id,
                "action_type": action_type,
                "payload": json.dumps(payload),
            },
        ).mappings().one()

    return dict(row)


def process_approval(
    approval_id: int,
    approved: bool,
    reviewer: str,
    comment: str,
):

    initialize_approval_table()

    with engine.begin() as connection:

        row = connection.execute(
            text(
                """
                SELECT
                    id,
                    session_id,
                    action_type,
                    payload,
                    status
                FROM approvals
                WHERE id = :approval_id
                """
            ),
            {
                "approval_id": approval_id,
            },
        ).mappings().first()

        if not row:
            raise ValueError(
                "Approval request was not found."
            )

        if row["status"] != "pending":
            raise ValueError(
                "Approval request has already been decided."
            )

        # -------------------------------------------------
        # Reject approval
        # -------------------------------------------------

        if not approved:

            connection.execute(
                text(
                    """
                    UPDATE approvals
                    SET
                        status = 'rejected',
                        reviewer = :reviewer,
                        comment = :comment,
                        decided_at = CURRENT_TIMESTAMP
                    WHERE id = :approval_id
                    """
                ),
                {
                    "approval_id": approval_id,
                    "reviewer": reviewer,
                    "comment": comment,
                },
            )

            return {
                "approval_id": approval_id,
                "status": "rejected",
                "reviewer": reviewer,
                "comment": comment,
            }

        # -------------------------------------------------
        # Approved action
        # -------------------------------------------------

        action_type = row["action_type"]

        payload = row["payload"]

        if action_type != "create_ticket":

            raise ValueError(
                "Unsupported approval action."
            )

        # -------------------------------------------------
        # Create ticket with tracing
        # -------------------------------------------------

        with trace_span(
            "tool.create_ticket",
            {
                "tool": "create_ticket",
                "employee_id": payload[
                    "employee_id"
                ],
            },
        ):

            result = create_ticket(
                employee_id=payload[
                    "employee_id"
                ],
                title=payload[
                    "title"
                ],
                description=payload[
                    "description"
                ],
            )

        # -------------------------------------------------
        # Update approval status
        # -------------------------------------------------

        connection.execute(
            text(
                """
                UPDATE approvals
                SET
                    status = 'approved',
                    reviewer = :reviewer,
                    comment = :comment,
                    decided_at = CURRENT_TIMESTAMP
                WHERE id = :approval_id
                """
            ),
            {
                "approval_id": approval_id,
                "reviewer": reviewer,
                "comment": comment,
            },
        )

    return {
        "approval_id": approval_id,
        "status": "approved",
        "reviewer": reviewer,
        "comment": comment,
        "action_result": result,
    }