from typing import Dict, Optional
from domain import Order
from application.interfaces import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self._orders: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Optional[Order]:
        return self._orders.get(order_id)
    
    def save(self, order: Order) -> None:
        self._orders[order.order_id] = order
    
    def clear(self) -> None:
        self._orders.clear()