from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class OrderStatus(str, Enum):
    PLACED = "PLACED"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"


# -------------------------
# PRODUCT SCHEMAS
# -------------------------

class ProductCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    price: float = Field(
        ...,
        gt=0
    )

    stock: int = Field(
        ...,
        ge=0
    )


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int

    model_config = ConfigDict(
        from_attributes=True
    )


# -------------------------
# ORDER ITEM SCHEMAS
# -------------------------

class OrderItemCreate(BaseModel):
    product_id: int = Field(
        ...,
        gt=0
    )

    quantity: int = Field(
        ...,
        gt=0
    )


class OrderItemResponse(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float


# -------------------------
# ORDER SCHEMAS
# -------------------------

class OrderCreate(BaseModel):
    customer: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    items: list[OrderItemCreate] = Field(
        ...,
        min_length=1
    )


class OrderStatusUpdate(BaseModel):
    status: OrderStatus


class OrderResponse(BaseModel):
    id: int
    customer: str
    items: list[OrderItemResponse]
    total_amount: float
    status: OrderStatus