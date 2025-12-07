"""
Order management and tracking tools using database.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from sqlalchemy import and_

from .base_tool import BaseTool
from ...config.database import SessionLocal
from ...models.models import Order, OrderItem, Product, CartItem


class GetOrderStatusTool(BaseTool):
    """Tool to get the status of a specific order."""
    
    name: str = "get_order_status"
    description: str = "Get the current status and details of an order by order_id."
    
    def _run(self, user_id: int, order_id: str) -> Dict[str, Any]:
        """
        Get order status from database.
        
        Args:
            user_id: User ID
            order_id: Order number to look up
            
        Returns:
            Dict with order status and details
        """
        db = SessionLocal()
        try:
            order = db.query(Order).filter(
                and_(Order.user_id == user_id, Order.order_number == order_id)
            ).first()
            
            if not order:
                return {
                    "success": False,
                    "message": f"Order {order_id} not found"
                }
            
            # Get order items
            items = []
            for order_item in order.items:
                items.append({
                    "product_name": order_item.product.name,
                    "quantity": order_item.quantity,
                    "price": int(order_item.unit_price)
                })
            
            return {
                "success": True,
                "order": {
                    "order_id": order.order_number,
                    "status": order.status,
                    "total_amount": int(order.total_amount),
                    "tracking_id": order.tracking_id,
                    "estimated_delivery": order.estimated_delivery,
                    "order_date": order.created_at.strftime("%Y-%m-%d"),
                    "items": items
                }
            }
        finally:
            db.close()


class ListOrdersTool(BaseTool):
    """Tool to list all orders for a user."""
    
    name: str = "list_orders"
    description: str = "Get a list of all orders placed by the user, sorted by date."
    
    def _run(self, user_id: int, limit: int = 10) -> Dict[str, Any]:
        """
        List user orders from database.
        
        Args:
            user_id: User ID
            limit: Maximum number of orders to return
            
        Returns:
            Dict with order list
        """
        db = SessionLocal()
        try:
            orders = db.query(Order).filter(Order.user_id == user_id)\
                .order_by(Order.created_at.desc()).limit(limit).all()
            
            if not orders:
                return {
                    "success": True,
                    "message": "No orders found",
                    "orders": [],
                    "total_orders": 0
                }
            
            results = []
            for order in orders:
                results.append({
                    "order_id": order.order_number,
                    "status": order.status,
                    "total_price": int(order.total_amount),
                    "order_date": order.created_at.isoformat(),
                    "items_count": len(order.items)
                })
            
            return {
                "success": True,
                "orders": results,
                "total_orders": len(results)
            }
        finally:
            db.close()


class CreateOrderTool(BaseTool):
    """Tool to create a new order from cart items."""
    
    name: str = "create_order"
    description: str = "Create a new order from the user's cart items. This simulates the checkout process."
    
    def _run(self, user_id: int, payment_method: str = "COD") -> Dict[str, Any]:
        """
        Create order from cart in database.
        
        Args:
            user_id: User ID
            payment_method: Payment method (COD, UPI, Card, etc.)
            
        Returns:
            Dict with order confirmation
        """
        db = SessionLocal()
        try:
            # Get cart items
            cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
            
            if not cart_items:
                return {
                    "success": False,
                    "message": "Cannot create order with empty cart"
                }
            
            # Calculate total
            total_amount = sum(item.product.price * item.quantity for item in cart_items)
            
            # Generate order number and tracking ID
            order_number = f"ORD{random.randint(10000, 99999)}"
            tracking_id = f"TRK{random.randint(100000, 999999)}"
            
            # Calculate estimated delivery
            estimated_delivery = (datetime.now() + timedelta(days=random.randint(5, 10))).strftime("%Y-%m-%d")
            
            # Create order
            order = Order(
                order_number=order_number,
                user_id=user_id,
                status="Confirmed",
                total_amount=total_amount,
                tracking_id=tracking_id,
                estimated_delivery=estimated_delivery
            )
            db.add(order)
            db.flush()
            
            # Create order items
            for cart_item in cart_items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=cart_item.product_id,
                    quantity=cart_item.quantity,
                    unit_price=cart_item.product.price
                )
                db.add(order_item)
            
            # Clear cart
            db.query(CartItem).filter(CartItem.user_id == user_id).delete()
            
            db.commit()
            
            return {
                "success": True,
                "message": "Order placed successfully!",
                "order": {
                    "order_id": order_number,
                    "tracking_id": tracking_id,
                    "total_amount": int(total_amount),
                    "estimated_delivery": estimated_delivery,
                    "status": "Confirmed",
                    "payment_method": payment_method
                }
            }
        finally:
            db.close()


class TrackOrderTool(BaseTool):
    """Tool to track order delivery status."""
    
    name: str = "track_order"
    description: str = "Track the delivery status of an order using tracking_id or order_id."
    
    def _run(self, user_id: int, order_id: str = "", tracking_id: str = "") -> Dict[str, Any]:
        """
        Track order delivery from database.
        
        Args:
            user_id: User ID
            order_id: Order number (optional)
            tracking_id: Tracking ID (optional)
            
        Returns:
            Dict with tracking information
        """
        db = SessionLocal()
        try:
            # Find order
            query = db.query(Order).filter(Order.user_id == user_id)
            
            if order_id:
                query = query.filter(Order.order_number == order_id)
            elif tracking_id:
                query = query.filter(Order.tracking_id == tracking_id)
            else:
                return {
                    "success": False,
                    "message": "Please provide order_id or tracking_id"
                }
            
            order = query.first()
            
            if not order:
                return {
                    "success": False,
                    "message": "Order not found"
                }
            
            # Simulate tracking updates
            tracking_updates = [
                {
                    "status": "Order Confirmed",
                    "date": order.created_at.strftime("%Y-%m-%d %H:%M"),
                    "location": "AJ Creations Warehouse"
                },
                {
                    "status": "Packed",
                    "date": (order.created_at + timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                    "location": "AJ Creations Warehouse"
                },
                {
                    "status": "Shipped",
                    "date": (order.created_at + timedelta(days=2)).strftime("%Y-%m-%d %H:%M"),
                    "location": "In Transit"
                }
            ]
            
            return {
                "success": True,
                "order_id": order.order_number,
                "tracking_id": order.tracking_id,
                "current_status": order.status,
                "estimated_delivery": order.estimated_delivery,
                "tracking_updates": tracking_updates
            }
        finally:
            db.close()
