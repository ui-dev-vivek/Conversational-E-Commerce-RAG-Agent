from datetime import datetime

from app.config.database import Base
from app.models.product_model import Order
from sqlalchemy import DECIMAL, TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))

    amount = Column(DECIMAL(10, 2))
    payment_method = Column(String(50))  # card, upi, netbanking
    status = Column(String(50))  # pending, success, failed

    transaction_id = Column(String(255))  # from Razorpay/Stripe
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    order = relationship("Order", back_populates="payments")


class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))

    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    postal_code = Column(String(20))
    country = Column(String(100))

    status = Column(String(50))  # pending, shipped, delivered
    tracking_number = Column(String(255))

    shipped_at = Column(TIMESTAMP, nullable=True)
    delivered_at = Column(TIMESTAMP, nullable=True)

    order = relationship("Order", back_populates="shipments")
