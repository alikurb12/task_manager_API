from fastapi import FastAPI
from app.api.v1.router import router
import app.models
app = FastAPI(title="Task Manager API")
app.include_router(router)

@app.get("/health")
async def health():
    return {"status" : "ok"}