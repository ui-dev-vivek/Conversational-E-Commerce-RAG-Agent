"""Helper script to create database tables.

Run this from the server directory:
    python -m app.create_tables
"""
from app.config.database import engine
from app.models import Base


def create_all_tables():
    """Create all tables defined in models."""
    print(f"Creating tables using engine: {engine.url}")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully!")


if __name__ == "__main__":
    create_all_tables()
