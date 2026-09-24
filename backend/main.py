from fastapi import FastAPI
from backend.api.health import router as health_router

app = FastAPI()
app.include_router(health_router)


@app.get("/health")
def health():
    return {"status": "ok"}
