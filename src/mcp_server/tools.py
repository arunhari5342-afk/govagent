from pathlib import Path

from .database import create_ticket as db_create_ticket
from .database import get_leave_balance as db_get_leave_balance

PROJECT_ROOT = Path(__file__).resolve().parents[2]
POLICY_DIRECTORY = PROJECT_ROOT / "data" / "policies"


def get_leave_balance(employee_id: str):
    """
    Retrieve the current leave balance for an employee.

    This is a read-only enterprise tool.
    """

    if not employee_id:
        raise ValueError("employee_id is required")

    return db_get_leave_balance(employee_id)


def create_ticket(
    employee_id: str,
    title: str,
    description: str,
):
    """
    Create a helpdesk ticket for an employee.

    This tool performs an external write operation.
    """

    if not employee_id:
        raise ValueError("employee_id is required")

    if not title.strip():
        raise ValueError("title is required")

    if not description.strip():
        raise ValueError("description is required")

    if len(title) > 200:
        raise ValueError("title is too long")

    if len(description) > 5000:
        raise ValueError("description is too long")

    return db_create_ticket(
        employee_id=employee_id,
        title=title,
        description=description,
    )


def search_policy(
    query: str,
):
    """
    Search enterprise policy documents.

    This MCP tool performs a simple deterministic keyword search.
    The main Policy-RAG pipeline remains responsible for semantic
    pgvector retrieval.
    """

    if not query or not query.strip():
        raise ValueError("query is required")

    normalized_query = query.lower().strip()
    query_terms = {term for term in normalized_query.split() if len(term) > 2}

    results = []

    if not POLICY_DIRECTORY.exists():
        return {
            "query": query,
            "found": False,
            "results": [],
            "message": "Policy directory was not found.",
        }

    for policy_path in sorted(POLICY_DIRECTORY.glob("*.txt")):
        content = policy_path.read_text(encoding="utf-8")

        normalized_content = content.lower()

        matching_terms = [term for term in query_terms if term in normalized_content]

        if matching_terms:
            results.append(
                {
                    "filename": policy_path.name,
                    "matched_terms": matching_terms,
                    "content": content,
                }
            )

    return {
        "query": query,
        "found": bool(results),
        "results": results,
    }
