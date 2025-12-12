from fastapi import FastAPI
from app.routers import auth
from app.db.database import Base, engine

app = FastAPI(title="FastAPI Auth Project")

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"messgae" : "FastAPI Auth System Running"}