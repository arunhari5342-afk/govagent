from src.memory.redis_memory import (
    clear_session,
    get_messages,
    save_message,
)


def test_redis_session_memory():
    session_id = "test-session-001"

    clear_session(session_id)

    save_message(
        session_id,
        "user",
        "What is the leave policy?",
    )

    save_message(
        session_id,
        "assistant",
        "The leave policy explains the approved leave process.",
    )

    messages = get_messages(session_id)

    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"

    clear_session(session_id)

    assert get_messages(session_id) == []
