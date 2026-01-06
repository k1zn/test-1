from dataclasses import dataclass
from decimal import Decimal
from .money import Money


@dataclass
class OrderLine:
    product_name: str
    quantity: int
    unit_price: Money

    def __post_init__(self):
        if not self.product_name:
            raise ValueError("Product name cannot be empty")
        if self.quantity <= 0:
            raise ValueError("Quantity must be positive")
        if self.unit_price.amount <= 0:
            raise ValueError("Price must be positive")

    def total_price(self) -> Money:
        return Money(
            self.unit_price.amount * Decimal(self.quantity),
            self.unit_price.currency
        )
