"""
Shopping cart management tools using database.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base_tool import BaseTool
from ...config.database import SessionLocal
from ...models.models import CartItem, Product, User


class AddToCartTool(BaseTool):
    """Tool to add products to the shopping cart."""
    
    name: str = "add_to_cart"
    description: str = "Add a product to the user's shopping cart. Requires product_id and user_id."
    
    def _run(self, user_id: int, product_id: str, quantity: int = 1) -> Dict[str, Any]:
        """
        Add product to cart in database.
        
        Args:
            user_id: User ID
            product_id: Product SKU to add
            quantity: Quantity to add (default: 1)
            
        Returns:
            Dict with cart update status
        """
        db = SessionLocal()
        try:
            # Find product
            product = db.query(Product).filter(Product.sku == product_id).first()
            if not product:
                return {
                    "success": False,
                    "message": f"Product {product_id} not found"
                }
            
            # Check if already in cart
            cart_item = db.query(CartItem).filter(
                and_(CartItem.user_id == user_id, CartItem.product_id == product.id)
            ).first()
            
            if cart_item:
                # Update quantity
                cart_item.quantity += quantity
                message = f"Updated {product.name} quantity to {cart_item.quantity}"
            else:
                # Add new item
                cart_item = CartItem(
                    user_id=user_id,
                    product_id=product.id,
                    quantity=quantity
                )
                db.add(cart_item)
                message = f"Added {product.name} to cart"
            
            db.commit()
            
            # Get total items
            total_items = db.query(CartItem).filter(CartItem.user_id == user_id).count()
            
            return {
                "success": True,
                "message": message,
                "product_name": product.name,
                "quantity": cart_item.quantity,
                "cart_total_items": total_items
            }
        finally:
            db.close()


class ViewCartTool(BaseTool):
    """Tool to view the shopping cart contents."""
    
    name: str = "view_cart"
    description: str = "View all items in the user's shopping cart with total price."
    
    def _run(self, user_id: int) -> Dict[str, Any]:
        """
        View cart contents from database.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with cart contents and total
        """
        db = SessionLocal()
        try:
            cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
            
            if not cart_items:
                return {
                    "success": True,
                    "message": "Your cart is empty",
                    "cart_items": [],
                    "total_items": 0,
                    "total_price": 0
                }
            
            # Format cart items
            items = []
            total_price = 0
            total_quantity = 0
            
            for cart_item in cart_items:
                product = cart_item.product
                item_total = product.price * cart_item.quantity
                total_price += item_total
                total_quantity += cart_item.quantity
                
                items.append({
                    "product_id": product.sku,
                    "product_name": product.name,
                    "price": int(product.price),
                    "quantity": cart_item.quantity,
                    "total": int(item_total)
                })
            
            return {
                "success": True,
                "cart_items": items,
                "total_items": total_quantity,
                "total_price": int(total_price),
                "currency": "INR"
            }
        finally:
            db.close()


class RemoveFromCartTool(BaseTool):
    """Tool to remove products from the shopping cart."""
    
    name: str = "remove_from_cart"
    description: str = "Remove a product from the user's shopping cart by product_id."
    
    def _run(self, user_id: int, product_id: str) -> Dict[str, Any]:
        """
        Remove product from cart in database.
        
        Args:
            user_id: User ID
            product_id: Product SKU to remove
            
        Returns:
            Dict with removal status
        """
        db = SessionLocal()
        try:
            # Find product
            product = db.query(Product).filter(Product.sku == product_id).first()
            if not product:
                return {
                    "success": False,
                    "message": f"Product {product_id} not found"
                }
            
            # Find cart item
            cart_item = db.query(CartItem).filter(
                and_(CartItem.user_id == user_id, CartItem.product_id == product.id)
            ).first()
            
            if not cart_item:
                return {
                    "success": False,
                    "message": f"{product.name} not found in cart"
                }
            
            # Remove item
            db.delete(cart_item)
            db.commit()
            
            # Get remaining items
            total_items = db.query(CartItem).filter(CartItem.user_id == user_id).count()
            
            return {
                "success": True,
                "message": f"Removed {product.name} from cart",
                "cart_total_items": total_items
            }
        finally:
            db.close()


class ClearCartTool(BaseTool):
    """Tool to clear all items from the shopping cart."""
    
    name: str = "clear_cart"
    description: str = "Remove all items from the user's shopping cart."
    
    def _run(self, user_id: int) -> Dict[str, Any]:
        """
        Clear cart in database.
        
        Args:
            user_id: User ID
            
        Returns:
            Dict with clear status
        """
        db = SessionLocal()
        try:
            items_count = db.query(CartItem).filter(CartItem.user_id == user_id).count()
            
            if items_count == 0:
                return {
                    "success": True,
                    "message": "Cart was already empty"
                }
            
            # Delete all cart items
            db.query(CartItem).filter(CartItem.user_id == user_id).delete()
            db.commit()
            
            return {
                "success": True,
                "message": f"Cleared {items_count} items from cart"
            }
        finally:
            db.close()
