from fastapi import FastAPI
from app.api.health import router as health_router
from app.api.signals import router as signals_router

app = FastAPI(
    title="Engineering signal aggregator",
    version="0.1.0",
)

app.include_router(health_router, prefix="/api")
app.include_router(signals_router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok"}
