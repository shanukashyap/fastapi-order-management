class ProductNotFoundException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class OrderNotFoundException(Exception):
    def __init__(self, order_id: int):
        self.order_id = order_id


class InvalidQuantityException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class InsufficientStockException(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class InvalidStatusTransitionException(Exception):
    def __init__(self, current_status: str, new_status: str):
        self.current_status = current_status
        self.new_status = new_status