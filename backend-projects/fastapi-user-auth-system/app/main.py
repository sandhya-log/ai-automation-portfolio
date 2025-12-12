from fastapi import FastAPI
from app.routers import auth
app = FastAPI(title="FastAPI Auth Project")

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def home():
    return {"messgae" : "FastAPI Auth System Running"}