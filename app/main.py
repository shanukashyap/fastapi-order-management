from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    status
)

from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from . import schemas
from . import crud
from .exceptions import (
    ProductNotFoundException,
    OrderNotFoundException,
    InsufficientStockException,
    InvalidStatusTransitionException
)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

Base.metadata.create_all(
    bind=engine
)


# ==========================================
# FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="FastAPI Order Management System",
    description="""
    A complete Order Management API built with FastAPI.

    Features:
    - Product management
    - Order creation
    - Server-side total calculation
    - Product validation
    - Quantity validation
    - Stock management
    - Order status workflow
    """,
    version="1.0.0"
)


# ==========================================
# ROOT
# ==========================================

@app.get("/")
def root():
    return {
        "message": "FastAPI Order Management API is running",
        "docs": "/docs"
    }


# ==========================================
# PRODUCT APIs
# ==========================================

@app.post(
    "/products",
    response_model=schemas.ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db)
):
    return crud.create_product(
        db=db,
        name=product.name,
        price=product.price,
        stock=product.stock
    )


@app.get(
    "/products",
    response_model=list[schemas.ProductResponse]
)
def get_products(
    db: Session = Depends(get_db)
):
    return crud.get_products(db)


# ==========================================
# CREATE ORDER
# ==========================================

@app.post(
    "/orders",
    response_model=schemas.OrderResponse,
    status_code=status.HTTP_201_CREATED
)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db)
):

    try:

        created_order = crud.create_order(
            db=db,
            customer=order.customer,
            items=order.items
        )

        return format_order_response(
            created_order
        )

    except ProductNotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=f"Product with ID {e.product_id} does not exist"
        )

    except InsufficientStockException as e:

        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock for product ID {e.product_id}"
        )


# ==========================================
# GET ALL ORDERS
# ==========================================

@app.get(
    "/orders",
    response_model=list[schemas.OrderResponse]
)
def get_orders(
    db: Session = Depends(get_db)
):

    orders = crud.get_orders(db)

    return [
        format_order_response(order)
        for order in orders
    ]


# ==========================================
# GET SINGLE ORDER
# ==========================================

@app.get(
    "/orders/{order_id}",
    response_model=schemas.OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = crud.get_order(
        db,
        order_id
    )

    if not order:

        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {order_id} does not exist"
        )

    return format_order_response(order)


# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@app.put(
    "/orders/{order_id}/status",
    response_model=schemas.OrderResponse
)
def update_order_status(
    order_id: int,
    status_update: schemas.OrderStatusUpdate,
    db: Session = Depends(get_db)
):

    try:

        order = crud.update_order_status(
            db=db,
            order_id=order_id,
            new_status=status_update.status.value
        )

        return format_order_response(order)

    except OrderNotFoundException as e:

        raise HTTPException(
            status_code=404,
            detail=f"Order with ID {e.order_id} does not exist"
        )

    except InvalidStatusTransitionException as e:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Invalid status transition: "
                f"{e.current_status} → {e.new_status}. "
                f"Allowed next status must follow: "
                f"PLACED → PROCESSING → SHIPPED → DELIVERED"
            )
        )


# ==========================================
# FORMAT ORDER RESPONSE
# ==========================================

def format_order_response(order):

    items = []

    for item in order.items:

        subtotal = (
            item.unit_price *
            item.quantity
        )

        items.append(
            schemas.OrderItemResponse(
                product_id=item.product_id,
                product_name=item.product.name,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal
            )
        )

    return schemas.OrderResponse(
        id=order.id,
        customer=order.customer,
        items=items,
        total_amount=order.total_amount,
        status=order.status
    )