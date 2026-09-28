import uuid

from src.graph.checkpointer import create_checkpointer
from src.graph.graph import build_graph


def chat(
    user_input: str,
    session_id: str | None = None,
    context: str = "",
):

    if not session_id:
        session_id = str(uuid.uuid4())

    graph = build_graph()

    with create_checkpointer() as checkpointer:

        checkpointer.setup()

        app = graph.compile(checkpointer=checkpointer)

        config = {"configurable": {"thread_id": session_id}}

        result = app.invoke(
            {
                "user_input": user_input,
                "session_id": session_id,
                "context": context,
            },
            config=config,
        )

    return {
        "session_id": session_id,
        "route": result.get("route"),
        "response": result.get("response"),
        "tool_result": result.get("tool_result"),
        "review": result.get("review"),
        "approval": result.get("approval"),
    }
