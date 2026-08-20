from pydantic import BaseModel
from typing import Optional, Any
from fastapi import Request, HTTPException, status
from datetime import datetime, timezone


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    timestamp: str
    path: str


def success_response(data: Any, message: str, request: Request) -> APIResponse:
    return APIResponse(
        statusCode=200,
        message=message,
        data=data,
        timestamp=datetime.now(timezone.utc),
        path=request.url.path
    )
