from typing import List
from dataclasses import dataclass, field
from decimal import Decimal
from .order_line import OrderLine
from .order_status import OrderStatus
from .money import Money


@dataclass
class Order:
    order_id: str
    lines: List[OrderLine] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING

    def add_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.append(line)

    def remove_line(self, line: OrderLine) -> None:
        if self.status == OrderStatus.PAID:
            raise ValueError("Cannot modify paid order")
        self.lines.remove(line)

    def total(self) -> Money:
        if not self.lines:
            return Money(Decimal("0"))
        
        total = self.lines[0].total_price()
        for line in self.lines[1:]:
            total = total + line.total_price()
        return total

    def pay(self) -> None:
        if not self.lines:
            raise ValueError("Cannot pay empty order")
        
        if self.status == OrderStatus.PAID:
            raise ValueError("Order already paid")
        
        self.status = OrderStatus.PAID

    def is_paid(self) -> bool:
        return self.status == OrderStatus.PAID
