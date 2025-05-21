import logging
import sys
from pathlib import Path


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from prometheus_client import generate_latest
from app.config import settings
from app.database import mongodb
from app.logging_config import setup_logging
from app.middleware.logging import LoggingMiddleware
from app.prometheus_metrics import PrometheusMiddleware
from app.api.families import router as fam_router
from app.api.users import router as user_router
from app.api.transactions import router as tx_router

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Starting application")

app = FastAPI(title="FamilyFinance", version="1.0")

# Регистрируем LoggingMiddleware как функцию с декоратором @app.middleware("http")
@app.middleware("http")
async def logging_middleware(request, call_next):
    return await LoggingMiddleware(request, call_next)

# Регистрируем PrometheusMiddleware как класс с помощью add_middleware
app.add_middleware(PrometheusMiddleware, app_name="FamilyFinance")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/metrics", include_in_schema=False)
async def metrics():
    return PlainTextResponse(generate_latest())

@app.on_event("startup")
async def on_startup():
    await mongodb.init_db()

app.include_router(fam_router)
app.include_router(user_router)
app.include_router(tx_router)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "FamilyFinance API is up"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)