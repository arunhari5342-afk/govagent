from src.graph.checkpointer import (
    create_checkpointer,
)
from src.graph.graph import build_graph


def create_app():

    graph = build_graph()

    return graph


if __name__ == "__main__":

    graph = create_app()

    with create_checkpointer() as checkpointer:

        checkpointer.setup()

        app = graph.compile(
            checkpointer=checkpointer
        )

        config = {
            "configurable": {
                "thread_id": "govagent-session-001"
            }
        }

        result = app.invoke(
            {
                "user_input": (
                    "What is the employee "
                    "leave policy?"
                ),
                "session_id": (
                    "govagent-session-001"
                ),
                "context": """
Employees can submit leave requests
through the approved HR process.

A leave request should include the
start date, end date, and leave type.

Leave requests may require manager
approval.
""",
            },
            config=config,
        )

        print("\nROUTE:")
        print(result["route"])

        print("\nRESPONSE:")
        print(result["response"])