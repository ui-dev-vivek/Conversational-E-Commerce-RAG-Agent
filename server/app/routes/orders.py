from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import random
import string
from ..config.database import get_db
from ..models.models import Order, OrderItem, CartItem, Product, User
from ..utils.auth import decode_access_token

router = APIRouter()


class PaymentRequest(BaseModel):
    card_number: str
    card_holder: str
    expiry_date: str
    cvv: str
    billing_address: str


class CreateOrderRequest(BaseModel):
    items: Optional[List[dict]] = None  # If None, use cart items


def get_current_user_id(token: str, db: Session) -> int:
    """Helper function to get user ID from token"""
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_id


def generate_order_number():
    """Generate unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"ORD-{timestamp}-{random_str}"


@router.get("/")
async def get_user_orders(token: str, db: Session = Depends(get_db)):
    """
    Get all orders for the current user.
    """
    user_id = get_current_user_id(token, db)
    
    orders = db.query(Order).filter(Order.user_id == user_id).order_by(Order.created_at.desc()).all()
    
    result = []
    for order in orders:
        items = []
        for item in order.items:
            items.append({
                "product_id": item.product_id,
                "product_name": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.quantity * item.unit_price
            })
        
        result.append({
            "id": order.id,
            "order_number": order.order_number,
            "status": order.status,
            "total_amount": order.total_amount,
            "tracking_id": order.tracking_id,
            "estimated_delivery": order.estimated_delivery,
            "created_at": order.created_at.isoformat(),
            "items": items
        })
    
    return result


@router.get("/{order_id}")
async def get_order(order_id: int, token: str, db: Session = Depends(get_db)):
    """
    Get a specific order by ID.
    """
    user_id = get_current_user_id(token, db)
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    items = []
    for item in order.items:
        items.append({
            "product_id": item.product_id,
            "product_name": item.product.name,
            "product_image": item.product.image_url,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "total": item.quantity * item.unit_price
        })
    
    return {
        "id": order.id,
        "order_number": order.order_number,
        "status": order.status,
        "total_amount": order.total_amount,
        "tracking_id": order.tracking_id,
        "estimated_delivery": order.estimated_delivery,
        "created_at": order.created_at.isoformat(),
        "items": items
    }


@router.post("/create")
async def create_order(
    token: str,
    db: Session = Depends(get_db)
):
    """
    Create an order from cart items.
    """
    user_id = get_current_user_id(token, db)
    
    # Get cart items
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    # Calculate total and validate stock
    total_amount = 0.0
    order_items_data = []
    
    for cart_item in cart_items:
        product = cart_item.product
        
        if not product.in_stock or product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Product '{product.name}' is out of stock"
            )
        
        item_total = product.price * cart_item.quantity
        total_amount += item_total
        
        order_items_data.append({
            "product_id": product.id,
            "quantity": cart_item.quantity,
            "unit_price": product.price
        })
    
    # Create order
    order_number = generate_order_number()
    new_order = Order(
        order_number=order_number,
        user_id=user_id,
        status="pending_payment",
        total_amount=total_amount
    )
    
    db.add(new_order)
    db.flush()  # Get order ID without committing
    
    # Create order items
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    return {
        "order_id": new_order.id,
        "order_number": new_order.order_number,
        "total_amount": new_order.total_amount,
        "status": new_order.status,
        "message": "Order created successfully. Please proceed to payment."
    }


@router.post("/{order_id}/payment")
async def process_payment(
    order_id: int,
    payment: PaymentRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Process payment for an order.
    Simulates payment with success/failure based on card number.
    """
    user_id = get_current_user_id(token, db)
    
    # Get order
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "pending_payment":
        raise HTTPException(
            status_code=400,
            detail=f"Order cannot be paid. Current status: {order.status}"
        )
    
    # Simulate payment processing
    # If card number ends with even digit -> success, odd -> failure
    last_digit = int(payment.card_number[-1])
    payment_success = (last_digit % 2 == 0)
    
    if payment_success:
        # Payment successful
        order.status = "confirmed"
        order.tracking_id = f"TRK-{generate_order_number()}"
        order.estimated_delivery = "3-5 business days"
        
        # Update product stock
        for item in order.items:
            product = item.product
            product.stock -= item.quantity
            if product.stock <= 0:
                product.in_stock = False
        
        # Clear cart
        db.query(CartItem).filter(CartItem.user_id == user_id).delete()
        
        db.commit()
        db.refresh(order)
        
        return {
            "success": True,
            "message": "Payment successful! Your order has been confirmed.",
            "order_number": order.order_number,
            "tracking_id": order.tracking_id,
            "estimated_delivery": order.estimated_delivery,
            "status": order.status
        }
    else:
        # Payment failed
        order.status = "payment_failed"
        db.commit()
        
        return {
            "success": False,
            "message": "Payment failed. Please check your card details and try again.",
            "order_number": order.order_number,
            "status": order.status
        }


@router.post("/{order_id}/retry-payment")
async def retry_payment(
    order_id: int,
    payment: PaymentRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Retry payment for a failed order.
    """
    user_id = get_current_user_id(token, db)
    
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == user_id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status not in ["payment_failed", "pending_payment"]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot retry payment for order with status: {order.status}"
        )
    
    # Reset status to pending
    order.status = "pending_payment"
    db.commit()
    
    # Process payment
    return await process_payment(order_id, payment, token, db)

