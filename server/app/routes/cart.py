from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from ..config.database import get_db
from ..models.models import CartItem, Product, User
from ..utils.auth import decode_access_token

router = APIRouter()


class AddToCartRequest(BaseModel):
    product_id: int
    quantity: int = 1


class UpdateCartRequest(BaseModel):
    quantity: int


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


@router.get("/")
async def get_cart(token: str, db: Session = Depends(get_db)):
    """
    Get all items in user's cart.
    """
    user_id = get_current_user_id(token, db)
    
    cart_items = db.query(CartItem).filter(CartItem.user_id == user_id).all()
    
    result = []
    total = 0.0
    
    for item in cart_items:
        product = item.product
        item_total = product.price * item.quantity
        total += item_total
        
        result.append({
            "id": item.id,
            "product_id": product.id,
            "product_name": product.name,
            "product_image": product.image_url,
            "price": product.price,
            "currency": product.currency,
            "quantity": item.quantity,
            "item_total": item_total,
            "stock": product.stock
        })
    
    return {
        "items": result,
        "total": total,
        "currency": "INR",
        "item_count": len(result)
    }


@router.post("/add")
async def add_to_cart(
    request: AddToCartRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Add a product to cart or update quantity if already exists.
    """
    user_id = get_current_user_id(token, db)
    
    # Check if product exists and is in stock
    product = db.query(Product).filter(Product.id == request.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if not product.in_stock or product.stock < request.quantity:
        raise HTTPException(status_code=400, detail="Product out of stock")
    
    # Check if item already in cart
    existing_item = db.query(CartItem).filter(
        CartItem.user_id == user_id,
        CartItem.product_id == request.product_id
    ).first()
    
    if existing_item:
        # Update quantity
        existing_item.quantity += request.quantity
        db.commit()
        db.refresh(existing_item)
        return {
            "message": "Cart updated",
            "cart_item_id": existing_item.id,
            "quantity": existing_item.quantity
        }
    else:
        # Create new cart item
        new_item = CartItem(
            user_id=user_id,
            product_id=request.product_id,
            quantity=request.quantity
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {
            "message": "Item added to cart",
            "cart_item_id": new_item.id,
            "quantity": new_item.quantity
        }


@router.put("/{cart_item_id}")
async def update_cart_item(
    cart_item_id: int,
    request: UpdateCartRequest,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Update quantity of a cart item.
    """
    user_id = get_current_user_id(token, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    if request.quantity <= 0:
        db.delete(cart_item)
        db.commit()
        return {"message": "Item removed from cart"}
    
    # Check stock
    if cart_item.product.stock < request.quantity:
        raise HTTPException(status_code=400, detail="Insufficient stock")
    
    cart_item.quantity = request.quantity
    db.commit()
    db.refresh(cart_item)
    
    return {
        "message": "Cart updated",
        "cart_item_id": cart_item.id,
        "quantity": cart_item.quantity
    }


@router.delete("/{cart_item_id}")
async def remove_from_cart(
    cart_item_id: int,
    token: str,
    db: Session = Depends(get_db)
):
    """
    Remove an item from cart.
    """
    user_id = get_current_user_id(token, db)
    
    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user_id
    ).first()
    
    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    
    db.delete(cart_item)
    db.commit()
    
    return {"message": "Item removed from cart"}


@router.delete("/clear")
async def clear_cart(token: str, db: Session = Depends(get_db)):
    """
    Clear all items from cart.
    """
    user_id = get_current_user_id(token, db)
    
    db.query(CartItem).filter(CartItem.user_id == user_id).delete()
    db.commit()
    
    return {"message": "Cart cleared"}
