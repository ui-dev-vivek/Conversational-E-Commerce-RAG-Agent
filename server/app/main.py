from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

