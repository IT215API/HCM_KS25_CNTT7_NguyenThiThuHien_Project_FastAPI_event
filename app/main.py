# Khởi tạo FastAPI app, include routers, middleware
from fastapi import FastAPI, HTTPException
from app.db.database import engine, Base
import app.models.event_model
import app.models.event_task
import app.models.user_model
from app.core.exception_handler import http_exception_handler, validation_exception_handler, global_exception_handler
from fastapi.exceptions import RequestValidationError


app = FastAPI(
    title="Event Management Fastapi"
)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

Base.metadata.create_all(bind=engine)

@app.get("/health")
def health_check():
    return {"message": "Kết nối server thành công"}