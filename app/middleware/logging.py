import time, logging, contextvars
from uuid import uuid4
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from fastapi import Request, Response

request_id_ctx = contextvars.ContextVar("request_id", default=None)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        rid = str(uuid4())
        request_id_ctx.set(rid)
        logger = logging.getLogger("app.middleware")
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} [{duration:.2f}ms]", extra={"request_id": rid})
        return response