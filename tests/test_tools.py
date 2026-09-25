from src.mcp_server.database import initialize_mock_data
from src.mcp_server.tools import create_ticket
from src.mcp_server.tools import get_leave_balance


def setup_module():
    initialize_mock_data()


def test_get_leave_balance():
    result = get_leave_balance("EMP001")

    assert result["found"] is True
    assert result["annual_leave"] == 12
    assert result["sick_leave"] == 8


def test_unknown_employee():
    result = get_leave_balance("EMP999")

    assert result["found"] is False


def test_create_ticket():
    result = create_ticket(
        employee_id="EMP001",
        title="VPN connection problem",
        description="Unable to connect to the company VPN.",
    )

    assert result["ticket_id"].startswith("TKT-")
    assert result["status"] == "open"