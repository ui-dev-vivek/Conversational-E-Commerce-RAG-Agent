"""
Product search and retrieval tools using database.
"""

from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from .base_tool import BaseTool
from ...config.database import SessionLocal
from ...models.models import Product, Category


class SearchProductsTool(BaseTool):
    """Tool to search for products by name, category, price range, or tags."""
    
    name: str = "search_products"
    description: str = "Search for products by name, category, price range, or tags. Returns matching products with details."
    
    def _run(self, query: str = "", category: str = "", max_price: Optional[int] = None, 
             min_price: Optional[int] = None, limit: int = 5) -> Dict[str, Any]:
        """
        Search for products based on criteria using database.
        
        Args:
            query: Search query (product name, tags, description)
            category: Filter by category
            max_price: Maximum price filter
            min_price: Minimum price filter
            limit: Maximum number of results
            
        Returns:
            Dict with search results
        """
        db = SessionLocal()
        try:
            # Build query
            db_query = db.query(Product).filter(Product.in_stock == True)
            
            # Search by query (name, description, tags, material)
            # If query is empty or generic, show all products
            if query and query.strip():
                query_lower = query.lower()
                # Skip if query is too generic
                generic_terms = ['product', 'products', 'item', 'items', 'all', 'everything', 'show', 'me']
                is_generic = all(word in generic_terms for word in query_lower.split())
                
                if not is_generic:
                    db_query = db_query.filter(
                        or_(
                            Product.name.ilike(f"%{query_lower}%"),
                            Product.description.ilike(f"%{query_lower}%"),
                            Product.material.ilike(f"%{query_lower}%")
                        )
                    )
            
            # Filter by category
            if category:
                cat = db.query(Category).filter(Category.name.ilike(f"%{category}%")).first()
                if cat:
                    db_query = db_query.filter(Product.category_id == cat.id)
            
            # Filter by price range
            if min_price:
                db_query = db_query.filter(Product.price >= min_price)
            if max_price:
                db_query = db_query.filter(Product.price <= max_price)
            
            # Execute query
            products = db_query.limit(limit).all()
            
            # Format results
            results = []
            for product in products:
                results.append({
                    "id": product.sku,
                    "name": product.name,
                    "price": int(product.price),
                    "description": product.description[:100] + "..." if len(product.description) > 100 else product.description,
                    "category": product.category.name if product.category else "general",
                    "rating": product.rating,
                    "in_stock": product.in_stock,
                    "material": product.material
                })
            
            return {
                "success": True,
                "query": query,
                "category": category,
                "results_count": len(results),
                "products": results
            }
        finally:
            db.close()


class GetProductDetailsTool(BaseTool):
    """Tool to get detailed information about a specific product."""
    
    name: str = "get_product_details"
    description: str = "Get detailed information about a specific product by its ID."
    
    def _run(self, product_id: str) -> Dict[str, Any]:
        """
        Get detailed product information from database.
        
        Args:
            product_id: Product SKU to look up
            
        Returns:
            Dict with product details
        """
        db = SessionLocal()
        try:
            product = db.query(Product).filter(Product.sku == product_id).first()
            
            if not product:
                return {
                    "success": False,
                    "error": f"Product with ID '{product_id}' not found"
                }
            
            return {
                "success": True,
                "product": {
                    "id": product.sku,
                    "name": product.name,
                    "description": product.description,
                    "price": int(product.price),
                    "stock": product.stock,
                    "category": product.category.name if product.category else "general",
                    "rating": product.rating,
                    "in_stock": product.in_stock,
                    "material": product.material,
                    "tags": product.tags
                }
            }
        finally:
            db.close()


class ListCategoriesTool(BaseTool):
    """Tool to list all available product categories."""
    
    name: str = "list_categories"
    description: str = "Get a list of all available product categories in the store."
    
    def _run(self) -> Dict[str, Any]:
        """
        List all product categories from database.
        
        Returns:
            Dict with category list
        """
        db = SessionLocal()
        try:
            categories = db.query(Category).all()
            
            results = []
            for cat in categories:
                product_count = db.query(Product).filter(Product.category_id == cat.id).count()
                results.append({
                    "name": cat.name,
                    "product_count": product_count,
                    "display_name": cat.name.replace("_", " ").title(),
                    "description": cat.description
                })
            
            return {
                "success": True,
                "categories": results,
                "total_categories": len(results)
            }
        finally:
            db.close()
