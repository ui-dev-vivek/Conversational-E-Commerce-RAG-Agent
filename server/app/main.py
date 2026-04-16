import logging

from app.routers.routes import api_router
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# from .routes import auth, products, orders, chat, cart


def create_app() -> FastAPI:
    app = FastAPI(
        title="E-Commerce Chat Assistant API",
        description="Backend API for the RAG-powered e-commerce chat assistant",
        version="0.2.0",
    )

    # ✅ CORS properly configure
    allowed_origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )

    # Custom exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ):
        logger.error(f"❌ Validation Error: {exc.errors()}")
        logger.error(f"   Request body: {await request.body()}")
        return JSONResponse(
            status_code=422,
            content={"detail": exc.errors(), "body": str(await request.body())},
        )

    # Include routers
    app.include_router(api_router)

    # Health check
    @app.get("/health")
    def health_check():
        return {"status": "✅ Server is running"}

    return app


app = create_app()
