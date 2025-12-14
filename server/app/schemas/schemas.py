from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any


class AddressSchema(BaseModel):
    id: Optional[int]
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class CategoryRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True


class ProductRead(BaseModel):
    id: int
    sku: str
    name: str
    description: Optional[str]
    price: float
    currency: str
    stock: int
    category_id: Optional[int]

    class Config:
        orm_mode = True


class OrderItemRead(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float

    class Config:
        orm_mode = True


class OrderRead(BaseModel):
    id: int
    order_number: str
    user_id: int
    status: str
    total_amount: float
    created_at: datetime
    items: List[OrderItemRead] = []

    class Config:
        orm_mode = True
