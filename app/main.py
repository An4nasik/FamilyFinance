import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.config import settings
from app.database import mongodb
from app.logging_config import setup_logging
from app.middleware.logging import LoggingMiddleware
from app.api.families import router as fam_router
from app.api.users import router as user_router
from app.api.transactions import router as tx_router

setup_logging()
logger = logging.getLogger(__name__)
logger.info("Starting application")

app = FastAPI(title="FamilyFinance", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(LoggingMiddleware)


@app.on_event("startup")
async def on_startup():
    await mongodb.init_db()


app.include_router(fam_router)
app.include_router(user_router)
app.include_router(tx_router)

app.mount("/frontend", StaticFiles(directory="../frontend"), name="frontend")


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/frontend/index.html")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)