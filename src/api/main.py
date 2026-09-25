from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from src.services.approval_service import process_approval
from src.services.chat_service import chat


app = FastAPI(
    title="GovAgent API",
    description="Agentic enterprise assistant API",
    version="1.0.0",
)


# ---------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=5000,
    )

    session_id: str | None = None

    context: str = ""


class ChatResponse(BaseModel):
    session_id: str

    route: str | None

    response: str | None

    tool_result: dict | None = None

    review: dict | None = None

    approval: dict | None = None


class ApprovalRequest(BaseModel):
    approved: bool

    reviewer: str = Field(
        min_length=1,
        max_length=200,
    )

    comment: str = Field(
        default="",
        max_length=2000,
    )


# ---------------------------------------------------------
# Basic API Endpoints
# ---------------------------------------------------------


@app.get("/")
def root():
    return {
        "service": "GovAgent",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


# ---------------------------------------------------------
# Chat Endpoint
# ---------------------------------------------------------


@app.post(
    "/chat",
    response_model=ChatResponse,
)
def chat_endpoint(
    request: ChatRequest,
):
    return chat(
        user_input=request.message,
        session_id=request.session_id,
        context=request.context,
    )


# ---------------------------------------------------------
# Human Approval Endpoint
# ---------------------------------------------------------


@app.post(
    "/approvals/{approval_id}",
)
def approval_endpoint(
    approval_id: int,
    request: ApprovalRequest,
):
    try:
        result = process_approval(
            approval_id=approval_id,
            approved=request.approved,
            reviewer=request.reviewer,
            comment=request.comment,
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )


# ---------------------------------------------------------
# A2A-style Reviewer Agent Card
# ---------------------------------------------------------


@app.get("/agents/reviewer")
def reviewer_agent_card():
    return {
        "name": "GovAgent Reviewer",
        "description": (
            "Checks generated answers against "
            "the supplied policy sources."
        ),
        "version": "1.0",
        "agent_type": "reviewer",
        "capabilities": [
            "groundedness_check",
            "source_consistency_check",
        ],
        "input": {
            "question": "string",
            "context": "string",
            "draft_answer": "string",
        },
        "output": {
            "grounded": "boolean",
            "issues": "array",
        },
    }