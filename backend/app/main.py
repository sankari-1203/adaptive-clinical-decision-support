"""
Main FastAPI Application Entrypoint
Initializes lifespan events, CORS middleware, security filters, routers,
and optional static frontend serving.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.model_loader import load_all_artifacts
from app.routers import health, prediction
from app.config import REGULATORY_DISCLAIMER

# Setup secure application logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("cdss.app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Load and cache trained ML artifacts once during startup."""
    logger.info("Initializing Adaptive Clinical Decision Support System...")
    try:
        load_all_artifacts()
        logger.info("All disease pipeline artifacts successfully loaded and cached.")
    except Exception as e:
        logger.critical(f"Fatal startup error loading ML artifacts: {e}", exc_info=True)
        raise e
    yield
    logger.info("Shutting down Adaptive Clinical Decision Support System.")

app = FastAPI(
    title="Adaptive Clinical Decision Support System (CDSS)",
    description=(
        "Production-grade Clinical Decision Support API featuring dual-disease pipelines "
        "(Diabetes & Cardiovascular), multi-model ensemble (LR, SVM, RF, XGBoost), "
        "model disagreement, vote entropy, adaptive uncertainty quantification, "
        "and SHAP local explainability."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router)
app.include_router(prediction.router)

# Global Secure Exception Handler - Never expose filesystem paths or stack traces to client
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing request {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Clinical Decision Support System error.",
            "detail": "An unexpected error occurred while processing the request. Please verify inputs or contact clinical system administration.",
            "regulatory_notice": REGULATORY_DISCLAIMER,
        }
    )

# Mount static frontend directory if built
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if frontend_dist.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dist), html=True), name="static_frontend")
else:
    frontend_src = Path(__file__).resolve().parent.parent.parent / "frontend"
    if frontend_src.exists() and (frontend_src / "index.html").exists():
        app.mount("/client", StaticFiles(directory=str(frontend_src), html=True), name="dev_frontend")
