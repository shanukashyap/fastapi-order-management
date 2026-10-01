from sqlalchemy.orm import Session

from . import models
from .schemas import OrderStatus
from .exceptions import (
    ProductNotFoundException,
    OrderNotFoundException,
    InsufficientStockException,
    InvalidStatusTransitionException
)


# ==========================================
# PRODUCT FUNCTIONS
# ==========================================

def create_product(
    db: Session,
    name: str,
    price: float,
    stock: int
):
    product = models.Product(
        name=name,
        price=price,
        stock=stock
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_products(db: Session):
    return db.query(models.Product).all()


def get_product(
    db: Session,
    product_id: int
):
    return db.query(models.Product).filter(
        models.Product.id == product_id
    ).first()


# ==========================================
# ORDER FUNCTIONS
# ==========================================

def create_order(
    db: Session,
    customer: str,
    items
):
    total_amount = 0

    validated_items = []

    # --------------------------------------
    # Validate all products and quantities
    # before changing database
    # --------------------------------------

    for item in items:

        product = get_product(
            db,
            item.product_id
        )

        if not product:
            raise ProductNotFoundException(
                item.product_id
            )

        if item.quantity > product.stock:
            raise InsufficientStockException(
                item.product_id
            )

        subtotal = product.price * item.quantity

        total_amount += subtotal

        validated_items.append(
            {
                "product": product,
                "quantity": item.quantity,
                "unit_price": product.price,
                "subtotal": subtotal
            }
        )

    # --------------------------------------
    # Create order
    # --------------------------------------

    order = models.Order(
        customer=customer,
        total_amount=total_amount,
        status=OrderStatus.PLACED.value
    )

    db.add(order)
    db.flush()

    # --------------------------------------
    # Create order items
    # --------------------------------------

    for item in validated_items:

        product = item["product"]

        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=item["quantity"],
            unit_price=item["unit_price"]
        )

        db.add(order_item)

        # Reduce stock
        product.stock -= item["quantity"]

    db.commit()
    db.refresh(order)

    return order


def get_orders(db: Session):
    return db.query(models.Order).all()


def get_order(
    db: Session,
    order_id: int
):
    return db.query(models.Order).filter(
        models.Order.id == order_id
    ).first()


# ==========================================
# ORDER STATUS
# ==========================================

STATUS_FLOW = {
    OrderStatus.PLACED.value: OrderStatus.PROCESSING.value,
    OrderStatus.PROCESSING.value: OrderStatus.SHIPPED.value,
    OrderStatus.SHIPPED.value: OrderStatus.DELIVERED.value
}


def update_order_status(
    db: Session,
    order_id: int,
    new_status: str
):
    order = get_order(
        db,
        order_id
    )

    if not order:
        raise OrderNotFoundException(
            order_id
        )

    current_status = order.status

    expected_next_status = STATUS_FLOW.get(
        current_status
    )

    if expected_next_status != new_status:
        raise InvalidStatusTransitionException(
            current_status,
            new_status
        )

    order.status = new_status

    db.commit()
    db.refresh(order)

    return order