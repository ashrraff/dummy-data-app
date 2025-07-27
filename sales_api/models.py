from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    region = Column(String(255), nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))

    sales = relationship("Sale", back_populates="customers")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True) # Added index
    category = Column(String(100), nullable=True) # Explicitly set nullable=True
    price = Column(Float, nullable=False) # Consider adding validation in schemas for price > 0

    # Audit columns
    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))
    is_active = Column(Boolean, default=True) # For soft deletes

    sales = relationship("Sale", back_populates="products")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    
    timestamp = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), index=True)

    customers = relationship("Customer", back_populates="sales")
    products = relationship("Product", back_populates="sales")

    created_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc))
    updated_at = Column(DateTime, default=datetime.datetime.now(datetime.timezone.utc), onupdate=datetime.datetime.now(datetime.timezone.utc))