from fastapi import Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from app.schemas.api_schema import APIResponse


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=APIResponse(
            statusCode=422,
            message="Dữ liệu không hợp lệ",
            data=None,
            error=exc.errors(),
            timestamp=datetime.now(timezone.utc),
            path=request.url.path
        ).model_dump()
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=APIResponse(
            statusCode=exc.status_code,
            message=exc.detail,
            data=None,
            error=exc.detail,
            timestamp=datetime.now(timezone.utc),
            path=request.url.path
        ).model_dump()
    )


async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=APIResponse(
            statusCode=500,
            message="Hệ thống gặp sự cố",
            data=None,
            error=str(exc),
            timestamp=datetime.now(timezone.utc),
            path=request.url.path
        ).model_dump()
    )