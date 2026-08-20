# Khởi tạo FastAPI app, include routers, middleware
from fastapi import FastAPI
from app.db.database import engine, Base
import app.models.event_model
import app.models.event_task
import app.models.user_model

app = FastAPI(
    title="Event Management Fastapi"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Kết nối server thành công"}