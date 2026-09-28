from typing import Literal

from pydantic import BaseModel, Field


class ApprovalAction(BaseModel):
    action: Literal["approve", "reject"]
    endpoint: str


class ApprovalUI(BaseModel):
    type: Literal["approval_request"]
    approval_id: int
    title: str
    message: str
    actions: list[ApprovalAction] = Field(
        min_length=1,
        max_length=2,
    )
