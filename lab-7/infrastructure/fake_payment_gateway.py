from typing import Set
from domain import Money
from application.interfaces import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.failed_order_ids: Set[str] = set()
        self.processed_payments: list = []
    
    def charge(self, order_id: str, money: Money) -> bool:
        self.processed_payments.append({
            "order_id": order_id,
            "amount": money.amount,
            "currency": money.currency
        })
        
        if order_id in self.failed_order_ids:
            return False
        
        return self.should_succeed
    
    def fail_for_order(self, order_id: str) -> None:
        self.failed_order_ids.add(order_id)
    
    def reset(self) -> None:
        self.processed_payments.clear()
        self.failed_order_ids.clear()