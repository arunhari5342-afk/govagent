from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.graph.reviewer_agent import reviewer_agent
from src.services.approval_service import process_approval
from src.services.chat_service import chat

app = FastAPI(
    title="GovAgent API",
    description="Governed enterprise helpdesk and policy assistant",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    message: str
    session_id: str = "default-session"


class ApprovalRequest(BaseModel):
    approved: bool
    reviewer: str
    comment: str | None = None


class ReviewRequest(BaseModel):
    question: str
    response: str
    context: str = ""


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
    try:
        return chat(
            user_input=request.message,
            session_id=request.session_id,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/approvals/{approval_id}")
def approval_endpoint(
    approval_id: int,
    request: ApprovalRequest,
):
    try:
        return process_approval(
            approval_id=approval_id,
            approved=request.approved,
            reviewer=request.reviewer,
            comment=request.comment,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.get("/agents/reviewer")
def reviewer_agent_info():
    return {
        "name": "GovAgent Reviewer Agent",
        "type": "specialist_agent",
        "description": "Reviews whether assistant responses are grounded in supplied policy context.",
        "endpoint": "/agents/reviewer",
        "method": "POST",
    }


@app.post("/agents/reviewer")
def reviewer_endpoint(request: ReviewRequest):
    try:
        result = reviewer_agent(
            {
                "user_input": request.question,
                "response": request.response,
                "context": request.context,
            }
        )

        return result.get(
            "review",
            {
                "grounded": False,
                "issues": ["Reviewer did not return a review."],
            },
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/review")
def review_endpoint(request: ReviewRequest):
    return reviewer_endpoint(request)
