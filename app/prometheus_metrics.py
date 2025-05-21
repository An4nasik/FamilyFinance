"""
Module for adding Prometheus metrics to the FastAPI application.
"""
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Counter, Histogram
import time

# Define metrics
REQUEST_COUNT = Counter(
    "app_request_count", 
    "Application Request Count", 
    ["app_name", "method", "endpoint", "status_code"]
)

REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", 
    "Application Request Latency", 
    ["app_name", "method", "endpoint"]
)

def get_path_template(request):
    """
    Get the path template for a given request.
    For example, convert "/users/123" to "/users/{id}".
    """
    for route in request.app.routes:
        # Новая версия FastAPI по-другому обрабатывает совпадения маршрутов
        try:
            match, _ = route.matches(request.scope)
            # В новых версиях FastAPI/Starlette, match может быть True вместо FULL
            if match is True or (hasattr(route.matches, 'FULL') and match == route.matches.FULL):
                return route.path
        except Exception:
            pass
    return request.url.path


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    Middleware for collecting Prometheus metrics for FastAPI.
    """
    def __init__(self, app, app_name="fastapi-app"):
        super().__init__(app)
        self.app_name = app_name

    async def dispatch(self, request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        # Record request latency
        latency = time.time() - start_time
        path_template = get_path_template(request)
        REQUEST_LATENCY.labels(
            app_name=self.app_name,
            method=request.method,
            endpoint=path_template
        ).observe(latency)
        
        # Record request count
        REQUEST_COUNT.labels(
            app_name=self.app_name,
            method=request.method,
            endpoint=path_template,
            status_code=response.status_code
        ).inc()
        
        return response
