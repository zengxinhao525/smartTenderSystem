from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"] = Field(..., description="Message role")
    content: str = Field(..., min_length=1, description="Message content")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Latest user message")
    history: list[ChatMessage] = Field(default_factory=list, description="Conversation history")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="Assistant reply")
    model: str = Field(..., description="Resolved model name")
    fallback: bool = Field(..., description="Whether the response used the fallback path")


class UploadAnalysisResponse(BaseModel):
    file_name: str = Field(..., description="Uploaded file name")
    file_path: str = Field(..., description="Saved file path on server")
    bid_info: dict = Field(..., description="Extracted bid information")
    draft: str = Field(..., description="Generated draft content")
    review: str = Field(..., description="Latest review result")
    approved: bool = Field(..., description="Whether automatic review approved the draft")
    need_human: bool = Field(..., description="Whether manual review is required")
