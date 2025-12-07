"""
Database initialization script.
Creates all tables in the MySQL database.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config.database import engine, Base, DATABASE_URL
from app.models.models import User, Address, Category, Product, CartItem, Order, OrderItem

def init_database():
    """Initialize database tables."""
    print("🔧 Initializing database...")
    print(f"📍 Database URL: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully!")
        print("\nCreated tables:")
        for table in Base.metadata.sorted_tables:
            print(f"  - {table.name}")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

if __name__ == "__main__":
    init_database()
