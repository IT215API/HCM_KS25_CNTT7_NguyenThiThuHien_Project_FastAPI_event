# Công việc sự kiện endpoints
from fastapi import APIRouter


router = APIRouter(
    prefix="/event-tasks",
    tags=["Event Tasks"]
)

