"""
Seed the database with sample products and categories for the e-commerce site.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent.resolve()
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.config.database import SessionLocal
from app.models.models import Category, Product

def seed_ecommerce_data():
    db = SessionLocal()
    
    try:
        # Create categories if they don't exist
        categories_data = [
            {"name": "Women's Clothing", "description": "Traditional and modern women's wear"},
            {"name": "Cosmetics", "description": "Natural and organic beauty products"},
            {"name": "Candles", "description": "Handcrafted aromatic candles"},
            {"name": "Soaps", "description": "Handmade natural soaps"},
            {"name": "Home Decor", "description": "Beautiful decorative items for your home"}
        ]
        
        categories = {}
        for cat_data in categories_data:
            category = db.query(Category).filter(Category.name == cat_data["name"]).first()
            if not category:
                category = Category(**cat_data)
                db.add(category)
                db.flush()
            categories[cat_data["name"]] = category.id
        
        # Create products
        products_data = [
            # Women's Clothing
            {
                "sku": "WC001",
                "name": "Elegant Cotton Kurti",
                "description": "Beautiful handcrafted cotton kurti with traditional embroidery",
                "price": 1499.00,
                "currency": "INR",
                "stock": 25,
                "category_id": categories["Women's Clothing"],
                "image_url": "https://placehold.co/600x400/FF6B6B/FFFFFF?text=Elegant+Cotton+Kurti",
                "rating": 4.5,
                "material": "Cotton",
                "tags": ["kurti", "cotton", "embroidery", "traditional"]
            },
            {
                "sku": "WC002",
                "name": "Floral Print Saree",
                "description": "Gorgeous floral print saree perfect for special occasions",
                "price": 2999.00,
                "currency": "INR",
                "stock": 15,
                "category_id": categories["Women's Clothing"],
                "image_url": "https://placehold.co/600x400/4ECDC4/FFFFFF?text=Floral+Print+Saree",
                "rating": 4.8,
                "material": "Silk Blend",
                "tags": ["saree", "floral", "silk", "party wear"]
            },
            {
                "sku": "WC003",
                "name": "Designer Palazzo Set",
                "description": "Trendy palazzo set with matching dupatta",
                "price": 1899.00,
                "currency": "INR",
                "stock": 30,
                "category_id": categories["Women's Clothing"],
                "image_url": "https://placehold.co/600x400/45B7D1/FFFFFF?text=Designer+Palazzo+Set",
                "rating": 4.3,
                "material": "Rayon",
                "tags": ["palazzo", "modern", "casual"]
            },
            
            # Cosmetics
            {
                "sku": "COS001",
                "name": "Natural Face Cream",
                "description": "Organic face cream with natural ingredients for glowing skin",
                "price": 899.00,
                "currency": "INR",
                "stock": 50,
                "category_id": categories["Cosmetics"],
                "image_url": "https://placehold.co/600x400/FF9F43/FFFFFF?text=Natural+Face+Cream",
                "rating": 4.6,
                "material": "Organic",
                "tags": ["face cream", "organic", "natural", "skincare"]
            },
            {
                "sku": "COS002",
                "name": "Herbal Lip Balm",
                "description": "Moisturizing lip balm with herbal extracts",
                "price": 299.00,
                "currency": "INR",
                "stock": 100,
                "category_id": categories["Cosmetics"],
                "image_url": "https://placehold.co/600x400/FECA57/FFFFFF?text=Herbal+Lip+Balm",
                "rating": 4.4,
                "material": "Herbal",
                "tags": ["lip balm", "herbal", "moisturizing"]
            },
            {
                "sku": "COS003",
                "name": "Rose Water Toner",
                "description": "Pure rose water toner for refreshing skin",
                "price": 499.00,
                "currency": "INR",
                "stock": 75,
                "category_id": categories["Cosmetics"],
                "image_url": "https://placehold.co/600x400/FF9FF3/FFFFFF?text=Rose+Water+Toner",
                "rating": 4.7,
                "material": "Natural",
                "tags": ["toner", "rose water", "natural"]
            },
            
            # Candles
            {
                "sku": "CAN001",
                "name": "Lavender Bliss Candle",
                "description": "Soothing lavender scented candle for relaxation",
                "price": 499.00,
                "currency": "INR",
                "stock": 60,
                "category_id": categories["Candles"],
                "image_url": "https://placehold.co/600x400/5F27CD/FFFFFF?text=Lavender+Bliss+Candle",
                "rating": 4.8,
                "material": "Soy Wax",
                "tags": ["candle", "lavender", "aromatherapy", "relaxation"]
            },
            {
                "sku": "CAN002",
                "name": "Vanilla Dream Candle",
                "description": "Sweet vanilla scented candle for cozy evenings",
                "price": 549.00,
                "currency": "INR",
                "stock": 45,
                "category_id": categories["Candles"],
                "image_url": "https://placehold.co/600x400/F368E0/FFFFFF?text=Vanilla+Dream+Candle",
                "rating": 4.5,
                "material": "Soy Wax",
                "tags": ["candle", "vanilla", "sweet", "cozy"]
            },
            {
                "sku": "CAN003",
                "name": "Sandalwood Serenity Candle",
                "description": "Traditional sandalwood scented candle",
                "price": 599.00,
                "currency": "INR",
                "stock": 40,
                "category_id": categories["Candles"],
                "image_url": "https://placehold.co/600x400/D6A2E8/FFFFFF?text=Sandalwood+Candle",
                "rating": 4.9,
                "material": "Beeswax",
                "tags": ["candle", "sandalwood", "traditional"]
            },
            
            # Soaps
            {
                "sku": "SOAP001",
                "name": "Handmade Soap Set",
                "description": "Set of 3 handmade natural soaps with different fragrances",
                "price": 599.00,
                "currency": "INR",
                "stock": 80,
                "category_id": categories["Soaps"],
                "image_url": "https://placehold.co/600x400/0ABDE3/FFFFFF?text=Handmade+Soap+Set",
                "rating": 4.6,
                "material": "Natural",
                "tags": ["soap", "handmade", "natural", "gift set"]
            },
            {
                "sku": "SOAP002",
                "name": "Neem & Tulsi Soap",
                "description": "Antibacterial soap with neem and tulsi extracts",
                "price": 249.00,
                "currency": "INR",
                "stock": 120,
                "category_id": categories["Soaps"],
                "image_url": "https://placehold.co/600x400/10AC84/FFFFFF?text=Neem+Tulsi+Soap",
                "rating": 4.7,
                "material": "Herbal",
                "tags": ["soap", "neem", "tulsi", "antibacterial"]
            },
            {
                "sku": "SOAP003",
                "name": "Charcoal Detox Soap",
                "description": "Activated charcoal soap for deep cleansing",
                "price": 349.00,
                "currency": "INR",
                "stock": 90,
                "category_id": categories["Soaps"],
                "image_url": "https://placehold.co/600x400/222F3E/FFFFFF?text=Charcoal+Detox+Soap",
                "rating": 4.5,
                "material": "Charcoal",
                "tags": ["soap", "charcoal", "detox", "cleansing"]
            },
            
            # Home Decor
            {
                "sku": "DEC001",
                "name": "Decorative Glass Vase",
                "description": "Elegant handcrafted glass vase for flowers",
                "price": 799.00,
                "currency": "INR",
                "stock": 35,
                "category_id": categories["Home Decor"],
                "image_url": "https://placehold.co/600x400/54A0FF/FFFFFF?text=Decorative+Glass+Vase",
                "rating": 4.4,
                "material": "Glass",
                "tags": ["vase", "glass", "decorative", "flowers"]
            },
            {
                "sku": "DEC002",
                "name": "Wooden Wall Art",
                "description": "Handcrafted wooden wall art with traditional designs",
                "price": 1299.00,
                "currency": "INR",
                "stock": 20,
                "category_id": categories["Home Decor"],
                "image_url": "https://placehold.co/600x400/576574/FFFFFF?text=Wooden+Wall+Art",
                "rating": 4.8,
                "material": "Wood",
                "tags": ["wall art", "wooden", "traditional", "handcrafted"]
            },
            {
                "sku": "DEC003",
                "name": "Ceramic Planter Set",
                "description": "Set of 3 beautiful ceramic planters",
                "price": 999.00,
                "currency": "INR",
                "stock": 40,
                "category_id": categories["Home Decor"],
                "image_url": "https://placehold.co/600x400/1DD1A1/FFFFFF?text=Ceramic+Planter+Set",
                "rating": 4.6,
                "material": "Ceramic",
                "tags": ["planter", "ceramic", "plants", "set"]
            }
        ]
        
        for prod_data in products_data:
            product = db.query(Product).filter(Product.sku == prod_data["sku"]).first()
            if product:
                # Update existing product
                for key, value in prod_data.items():
                    setattr(product, key, value)
            else:
                # Create new product
                product = Product(**prod_data, in_stock=True)
                db.add(product)
        
        db.commit()
        print("✅ Database seeded/updated successfully!")
        print(f"   - Processed {len(categories_data)} categories")
        print(f"   - Processed {len(products_data)} products")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("🌱 Seeding e-commerce database...")
    seed_ecommerce_data()
