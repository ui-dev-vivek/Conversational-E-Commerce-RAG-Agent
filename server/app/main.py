from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from .routes import auth, products, orders, chat

def create_app() -> FastAPI:
    app = FastAPI(
        title="E-Commerce Chat Assistant API",
        description="Backend API for the RAG-powered e-commerce chat assistant",
        version="0.1.0",
    )

    # ✅ CORS properly configure करो
    allowed_origins = [
        "http://localhost:3000",           # Local dev
        "http://localhost:5173",           # Vite dev server
        "https://3mfgg5hv-5173.inc1.devtunnels.ms",  # DevTunnel
        "https://3mfgg5hv-5173.inc1.devtunnels.ms/",
    ]
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        max_age=600,
    )

    logger.info(f"✅ CORS enabled for: {allowed_origins}")

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(products.router, prefix="/api/products", tags=["products"])
    app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    
    # Health check
    @app.get("/health")
    def health_check():
        return {"status": "✅ Server is running"}
    
    return app


app = create_app()