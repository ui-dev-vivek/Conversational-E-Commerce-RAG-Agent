from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ChatMessageInput(BaseModel):
    """Input validator for chat messages"""
    user_id: str = Field(..., min_length=1, max_length=100, description="User identifier")
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "show me red kurtis"
            }
        }


# ✅ NEW: Structured data models for tool responses

class ProductData(BaseModel):
    """Product data from search"""
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    description: str = Field(..., description="Product description")
    rating: Optional[float] = Field(None, description="Product rating 1-5")
    stock: Optional[int] = Field(None, description="Available stock")
    product_id: Optional[str] = Field(None, description="Product ID")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Red Cotton Kurti",
                "price": 599,
                "description": "Beautiful handmade cotton kurti",
                "rating": 4.5,
                "stock": 10,
                "product_id": "prod_123"
            }
        }


class CartItemData(BaseModel):
    """Cart item structure"""
    product_name: str
    quantity: int
    price: float
    product_id: Optional[str] = None


class CartSummary(BaseModel):
    """Cart summary"""
    items: List[CartItemData]
    total: float
    total_items: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [
                    {"product_name": "Red Kurti", "quantity": 2, "price": 599}
                ],
                "total": 1198,
                "total_items": 2
            }
        }


class OrderData(BaseModel):
    """Order tracking data"""
    order_id: str
    status: str
    estimated_delivery: str
    tracking_id: Optional[str] = None
    order_date: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "order_id": "ORD123456",
                "status": "Shipped",
                "estimated_delivery": "2025-12-20",
                "tracking_id": "TRACK123"
            }
        }


class ChatMessageOutput(BaseModel):
    """Output validator for chat responses with structured tool data"""
    user_id: str = Field(..., description="User identifier")
    message: str = Field(..., description="Original user message")
    reply: str = Field(..., description="AI assistant response")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    
    # ✅ NEW: Structured tool data
    tool_name: Optional[str] = Field(None, description="Tool used for this response")
    products: Optional[List[ProductData]] = Field(None, description="Products returned from search")
    cart: Optional[CartSummary] = Field(None, description="Cart summary")
    order: Optional[OrderData] = Field(None, description="Order tracking data")
    
    sources: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user_123",
                "message": "show me kurtis",
                "reply": "मैंने आपके लिए 3 कुर्तियाँ खोजी हैं...",
                "timestamp": "2025-12-14T10:30:00",
                "tool_name": "search_products",
                "products": [
                    {
                        "name": "Red Cotton Kurti",
                        "price": 599,
                        "description": "Beautiful cotton kurti",
                        "rating": 4.5,
                        "stock": 10
                    }
                ],
                "sources": ["Tool: search_products"]
            }
        }