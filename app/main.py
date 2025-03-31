from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app, Counter, Histogram
from starlette.middleware.base import BaseHTTPMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.logging import LoggerMiddleware, logger
from app.api.routes import router
from app.services.singleton import load_model
from app.services.model_service import ModelService
from fastapi.routing import APIRoute

# Prometheus metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 0.5, 1, 2, 5]
)

class MetricsMiddleware(BaseHTTPMiddleware):
    """Middleware to collect Prometheus metrics for each request."""
    async def dispatch(self, request, call_next):
        method = request.method
        # Skip metrics endpoint to avoid double counting
        if request.url.path.rstrip('/') == '/metrics':
            return await call_next(request)
            
        endpoint = request.url.path.rstrip('/')
        if endpoint.startswith("/api/v1"):
            endpoint = "/api/v1/*"  # Group all API endpoints
        
        logger.info(f"Processing request: {method} {endpoint}")
        
        import time
        start_time = time.time()
        response = await call_next(request)
        latency_ms = (time.time() - start_time) * 1000  # Milliseconds
        latency_seconds = latency_ms / 1000  # Convert to seconds
        
        # Debug log for observed latency
        logger.debug(f"[MetricsMiddleware] Observed Latency: {latency_ms:.2f}ms ({latency_seconds:.4f}s)")
        
        # Increment request count
        REQUEST_COUNT.labels(
            method=method, 
            endpoint=endpoint, 
            http_status=response.status_code
        ).inc()
        
        # Observe latency in seconds (Prometheus expects seconds)
        REQUEST_LATENCY.labels(
            method=method,
            endpoint=endpoint
        ).observe(latency_seconds) 
        
        return response

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown tasks."""
    logger.info("Starting up the application")
    # Load model into singleton
    load_model(settings.MODEL_PATH)
    # Create model service that uses the singleton
    app.state.model_service = ModelService()
    logger.info("Application startup complete")
    yield
    logger.info("Shutting down the application")

# Create FastAPI application
app = FastAPI(
    title=settings.API_TITLE,
    version=settings.API_VERSION,
    description="API for sentiment analysis of text sentences",
    lifespan=lifespan
)

@app.get("/")
async def root():
    """Redirect root URL to API documentation."""
    return RedirectResponse(url="/docs")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add logging middleware
app.middleware("http")(LoggerMiddleware())

# Add Metrics middleware
app.add_middleware(MetricsMiddleware)

# Include API routes
app.include_router(router, prefix="/api/v1")

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

@app.get("/status", tags=["status"])
async def status_endpoint():
    """Check the status of the application."""
    import sys
    reload_enabled = "--reload" in " ".join(sys.argv)
    model_loaded = hasattr(app.state, "model_service") and app.state.model_service is not None
    return {
        "model_loaded": model_loaded,
        "uvicorn_reload": reload_enabled,
    }

@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError):
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Expose Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app, name="metrics")

if __name__ == "__main__":
    import sys
    if "--reload" in " ".join(sys.argv):
        logger.warning("Auto reload is enabled! Disable --reload for production to prevent repeated model loading.")
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
    )