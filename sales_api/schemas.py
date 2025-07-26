from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Customer Schemas

class CustomerBase(BaseModel):

    name: str = Field(..., min_length=1, max_length=100, description="Name of the customer.")
    email: EmailStr = Field(..., max_length=255, description="Email address of the customer (must be unique).")
    region: Optional[str] = Field(None, max_length=50, description="Geographic region of the customer.")

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int = Field(..., description="Unique identifier for the customer.")

    class Config:
        orm_mode = True


# Product Schemas

class ProductBase(BaseModel):

    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Name of the product."
    )
    category: Optional[str] = Field(
        None,
        max_length=50,
        description="Category the product belongs to (e.g., 'Electronics', 'Books')."
    )
    price: float = Field(
        ...,
        gt=0, # Price must be greater than zero
        description="Price of the product."
    )

class ProductCreate(ProductBase):

    pass

class Product(ProductBase):

    id: int = Field(..., description="Unique identifier for the product.")

    class Config:
        orm_mode = True


# Sale Schemas

class SaleBase(BaseModel):

    customer_id: int = Field(..., description="ID of the customer making the sale.")
    product_id: int = Field(..., description="ID of the product sold.")
    quantity: int = Field(
        ...,
        gt=0,
        description="Number of units of the product sold."
    )

class SaleCreate(SaleBase):

    pass

class Sale(SaleBase):

    id: int = Field(..., description="Unique identifier for the sale.")
    total_price: float = Field(..., description="Calculated total price of the sale.")
    timestamp: datetime = Field(..., description="Timestamp of when the sale occurred.")

    class Config:
        orm_mode = True