from .database import create_ticket as db_create_ticket
from .database import get_leave_balance as db_get_leave_balance


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