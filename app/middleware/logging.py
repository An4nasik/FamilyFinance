import time, logging, contextvars
from uuid import uuid4
from fastapi import Request, Response

# Используем контекстную переменную для хранения request_id
request_id_ctx = contextvars.ContextVar("request_id", default=None)

# Функция-middleware для работы с @app.middleware("http")
async def LoggingMiddleware(request: Request, call_next):
    # Создаем уникальный идентификатор запроса
    rid = str(uuid4())
    request_id_ctx.set(rid)
    logger = logging.getLogger("app.middleware")
    start = time.time()
    
    path = request.url.path
    method = request.method
    client_host = request.client.host if request.client else "unknown"
    
    # Skip logging for the metrics endpoint to avoid log spam
    should_log = path != "/metrics"
    
    # Capture request info before processing
    if should_log:
        logger.info(
            f"Request started: {method} {path}",
            extra={
                "request_id": rid,
                "client_host": client_host,
                "method": method,
                "path": path,
                "event_type": "request_start"
            }
        )
    
    try:
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        
        # Log the complete request with response info
        if should_log:
            logger.info(
                f"{method} {path} -> {response.status_code} [{duration:.2f}ms]",
                extra={
                    "request_id": rid,
                    "method": method,
                    "path": path,
                    "status_code": response.status_code,
                    "duration_ms": round(duration, 2),
                    "client_host": client_host,
                    "event_type": "request_complete"
                }
            )
        return response
    except Exception as e:
        duration = (time.time() - start) * 1000
        if should_log:
            logger.error(
                f"Request failed: {method} {path} -> 500 [{duration:.2f}ms]",
                exc_info=True,
                extra={
                    "request_id": rid,
                    "method": method,
                    "path": path,
                    "error": str(e),
                    "duration_ms": round(duration, 2),
                    "client_host": client_host,
                    "event_type": "request_error"
                }
            )
        raise
