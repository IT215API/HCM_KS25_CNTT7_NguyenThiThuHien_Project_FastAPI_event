# Khởi tạo FastAPI app, include routers, middleware
from fastapi import FastAPI
from app.db.database import engine, Base

app = FastAPI(
    title="Event Management Fastapi"
)

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Kết nối server thành công"}