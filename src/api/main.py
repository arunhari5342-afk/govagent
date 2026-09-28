from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from src.governance.audit import initialize_audit_table
from src.services.approval_service import (
    initialize_approval_table,
    process_approval,
)
from src.services.chat_service import chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_audit_table()
    initialize_approval_table()

    yield


app = FastAPI(
    title="GovAgent",
    version="1.0.0",
    lifespan=lifespan,
)


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    context: str | None = None


class ApprovalRequest(BaseModel):
    approved: bool
    reviewer: str
    comment: str | None = None


@app.get("/")
def root():
    return {
        "name": "GovAgent",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }


@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return chat(
        user_input=request.message,
        session_id=request.session_id,
        context=request.context or "",
    )


@app.post("/approvals/{approval_id}")
def approval(
    approval_id: int,
    request: ApprovalRequest,
):
    return process_approval(
        approval_id=approval_id,
        approved=request.approved,
        reviewer=request.reviewer,
        comment=request.comment,
    )
