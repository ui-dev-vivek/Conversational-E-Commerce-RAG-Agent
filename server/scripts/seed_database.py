"""
Database seeding script.
Populates database with sample categories, products, and users.
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from app.config.database import SessionLocal
from app.models.models import User, Category, Product
from app.utils.auth import get_password_hash

def seed_database():
    """Seed database with sample data."""
    db = SessionLocal()
    
    try:
        print("🌱 Seeding database...")
        
        # 1. Create Categories
        print("\n📁 Creating categories...")
        categories_data = [
            {"name": "womens_clothing", "description": "Women's fashion and apparel"},
            {"name": "cosmetics", "description": "Natural and organic cosmetics"},
            {"name": "candles", "description": "Scented and decorative candles"},
            {"name": "soaps", "description": "Handmade natural soaps"},
            {"name": "decor_items", "description": "Home decoration items"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not existing:
                category = Category(**cat_data)
                db.add(category)
                db.flush()
                categories[cat_data["name"]] = category.id
                print(f"  ✓ Created category: {cat_data['name']}")
            else:
                categories[cat_data["name"]] = existing.id
                print(f"  → Category exists: {cat_data['name']}")
        
        db.commit()
        
        # 2. Load and create Products from JSON
        print("\n🛍️  Creating products...")
        products_file = Path(__file__).parent.parent / "data" / "products.json"
        
        with open(products_file, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        product_count = 0
        for category_name, products_list in products_data.get("categories", {}).items():
            category_id = categories.get(category_name)
            
            for product_data in products_list:
                existing = db.query(Product).filter(Product.sku == product_data["id"]).first()
                if not existing:
                    product = Product(
                        sku=product_data["id"],
                        name=product_data["name"],
                        description=product_data["description"],
                        price=product_data["price"],
                        currency="INR",
                        stock=100 if product_data.get("in_stock", True) else 0,
                        category_id=category_id,
                        tags=product_data.get("tags", []),
                        rating=product_data.get("rating", 0.0),
                        in_stock=product_data.get("in_stock", True),
                        material=product_data.get("material_or_ingredients", "")
                    )
                    db.add(product)
                    product_count += 1
        
        db.commit()
        print(f"  ✓ Created {product_count} products")
        
        # 3. Create Sample Users
        print("\n👤 Creating sample users...")
        users_data = [
            {
                "username": "testuser",
                "email": "test@example.com",
                "password": "test123",
                "full_name": "Test User"
            },
            {
                "username": "admin",
                "email": "admin@ajcreations.in",
                "password": "admin123",
                "full_name": "Admin User"
            }
        ]
        
        for user_data in users_data:
            existing = db.query(User).filter(User.email == user_data["email"]).first()
            if not existing:
                user = User(
                    username=user_data["username"],
                    email=user_data["email"],
                    hashed_password=get_password_hash(user_data["password"]),
                    full_name=user_data["full_name"],
                    is_active=True
                )
                db.add(user)
                print(f"  ✓ Created user: {user_data['email']}")
            else:
                print(f"  → User exists: {user_data['email']}")
        
        db.commit()
        
        # Summary
        print("\n✅ Database seeding completed!")
        print(f"\n📊 Summary:")
        print(f"  - Categories: {db.query(Category).count()}")
        print(f"  - Products: {db.query(Product).count()}")
        print(f"  - Users: {db.query(User).count()}")
        
        print("\n🔑 Test Credentials:")
        print("  Email: test@example.com")
        print("  Password: test123")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
