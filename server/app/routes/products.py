from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional, List
from ..config.database import get_db
from ..models.models import Product, Category

router = APIRouter()


@router.get("/")
async def list_products(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all products, optionally filtered by category or search term.
    """
    query = db.query(Product).filter(Product.in_stock == True)
    
    if category:
        cat = db.query(Category).filter(Category.name.ilike(f"%{category}%")).first()
        if cat:
            query = query.filter(Product.category_id == cat.id)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    products = query.all()
    
    return [{
        "id": p.id,
        "sku": p.sku,
        "name": p.name,
        "description": p.description,
        "price": p.price,
        "currency": p.currency,
        "stock": p.stock,
        "category_id": p.category_id,
        "category_name": p.category.name if p.category else None,
        "image_url": p.image_url,
        "rating": p.rating,
        "material": p.material,
        "tags": p.tags
    } for p in products]


@router.get("/by-category")
async def get_products_by_category(db: Session = Depends(get_db)):
    """
    Get all products grouped by category.
    """
    categories = db.query(Category).all()
    result = {}
    
    for category in categories:
        products = db.query(Product).filter(
            Product.category_id == category.id,
            Product.in_stock == True
        ).all()
        
        result[category.name] = {
            "category_id": category.id,
            "category_description": category.description,
            "products": [{
                "id": p.id,
                "sku": p.sku,
                "name": p.name,
                "description": p.description,
                "price": p.price,
                "currency": p.currency,
                "stock": p.stock,
                "image_url": p.image_url,
                "rating": p.rating,
                "material": p.material,
                "tags": p.tags
            } for p in products]
        }
    
    return result


@router.get("/{product_id}")
async def get_product(product_id: int, db: Session = Depends(get_db)):
    """
    Get a single product by ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return {
        "id": product.id,
        "sku": product.sku,
        "name": product.name,
        "description": product.description,
        "price": product.price,
        "currency": product.currency,
        "stock": product.stock,
        "category_id": product.category_id,
        "category_name": product.category.name if product.category else None,
        "image_url": product.image_url,
        "rating": product.rating,
        "material": product.material,
        "tags": product.tags,
        "in_stock": product.in_stock
    }
