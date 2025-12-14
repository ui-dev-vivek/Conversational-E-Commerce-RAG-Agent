from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .routes import auth, products, orders, chat, cart

def create_app() -> FastAPI:
    app = FastAPI(
        title="E-Commerce Chat Assistant API",
        description="Backend API for the RAG-powered e-commerce chat assistant",
        version="0.1.0",
    )

    # ✅ CORS properly configure करो
    allowed_origins = ["*"]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )

    logger.info(f"✅ CORS enabled for: {allowed_origins}")

    # Custom exception handler for validation errors
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"❌ Validation Error: {exc.errors()}")
        logger.error(f"   Request body: {await request.body()}")
        return JSONResponse(
            status_code=422,
            content={
                "detail": exc.errors(),
                "body": str(await request.body())
            }
        )

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(products.router, prefix="/api/products", tags=["products"])
    app.include_router(cart.router, prefix="/api/cart", tags=["cart"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    
    # Health check
    @app.get("/health")
    def health_check():
        return {"status": "✅ Server is running"}
    
    return app


app = create_app()