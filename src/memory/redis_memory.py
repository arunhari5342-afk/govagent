import json
import os

import redis
from dotenv import load_dotenv


load_dotenv()

REDIS_URL = os.environ["REDIS_URL"]

DEFAULT_TTL = 60 * 60 * 24
MAX_MESSAGES = 20


client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
)


def session_key(session_id: str) -> str:
    return f"govagent:session:{session_id}"


def save_message(
    session_id: str,
    role: str,
    content: str,
):
    key = session_key(session_id)

    existing = client.get(key)

    if existing:
        messages = json.loads(existing)
    else:
        messages = []

    messages.append(
        {
            "role": role,
            "content": content,
        }
    )

    messages = messages[-MAX_MESSAGES:]

    client.setex(
        key,
        DEFAULT_TTL,
        json.dumps(messages),
    )


def get_messages(session_id: str):
    key = session_key(session_id)

    value = client.get(key)

    if not value:
        return []

    return json.loads(value)


def clear_session(session_id: str):
    client.delete(session_key(session_id))