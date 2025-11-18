from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
<<<<<<< HEAD

from .routes import auth, products, orders, chat
from .config.database import engine, SessionLocal, get_db
# # create tables if they don't exist
# from models import Base
# Base.metadata.create_all(bind=engine)

def create_app() -> FastAPI:
	app = FastAPI(
		title="E-Commerce Chat Assistant API",
		description="Backend API for the RAG-powered e-commerce chat assistant",
		version="0.1.0",
	)

	# Allow typical local dev origins; adjust in production
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)

	# include routers
	app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
	app.include_router(products.router, prefix="/api/products", tags=["products"])
	app.include_router(orders.router, prefix="/api/orders", tags=["orders"])
	app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
	return app


app = create_app()

=======
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
>>>>>>> 3111f70e589ab7b0a94810f7f151575630b441fd
