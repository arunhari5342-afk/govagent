import os
from contextlib import contextmanager

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver

load_dotenv()


CHECKPOINT_DATABASE_URL = os.environ["POSTGRES_CHECKPOINT_URL"]


@contextmanager
def create_checkpointer():

    with PostgresSaver.from_conn_string(CHECKPOINT_DATABASE_URL) as checkpointer:

        yield checkpointer
