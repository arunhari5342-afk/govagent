import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)


def initialize_mock_data():
    with engine.begin() as connection:

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS employee_leave_balance (
                    employee_id TEXT PRIMARY KEY,
                    annual_leave INTEGER NOT NULL,
                    sick_leave INTEGER NOT NULL
                )
                """
            )
        )

        connection.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS helpdesk_tickets (
                    id SERIAL PRIMARY KEY,
                    employee_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
        )

        connection.execute(
            text(
                """
                INSERT INTO employee_leave_balance
                (
                    employee_id,
                    annual_leave,
                    sick_leave
                )
                VALUES
                ('EMP001', 12, 8),
                ('EMP002', 7, 10)
                ON CONFLICT (employee_id)
                DO NOTHING
                """
            )
        )


def get_leave_balance(employee_id: str):
    with engine.connect() as connection:

        row = connection.execute(
            text(
                """
                SELECT
                    employee_id,
                    annual_leave,
                    sick_leave
                FROM employee_leave_balance
                WHERE employee_id = :employee_id
                """
            ),
            {
                "employee_id": employee_id,
            },
        ).mappings().first()

    if not row:
        return {
            "employee_id": employee_id,
            "found": False,
            "message": "Employee leave balance was not found.",
        }

    return {
        "employee_id": row["employee_id"],
        "found": True,
        "annual_leave": row["annual_leave"],
        "sick_leave": row["sick_leave"],
    }


def create_ticket(
    employee_id: str,
    title: str,
    description: str,
):
    with engine.begin() as connection:

        ticket_id = connection.execute(
            text(
                """
                INSERT INTO helpdesk_tickets
                (
                    employee_id,
                    title,
                    description,
                    status
                )
                VALUES
                (
                    :employee_id,
                    :title,
                    :description,
                    'open'
                )
                RETURNING id
                """
            ),
            {
                "employee_id": employee_id,
                "title": title,
                "description": description,
            },
        ).scalar_one()

    return {
        "ticket_id": f"TKT-{ticket_id:04d}",
        "employee_id": employee_id,
        "status": "open",
        "title": title,
    }