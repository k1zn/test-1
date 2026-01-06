from dataclasses import dataclass
from typing import Optional
from .interfaces import OrderRepository, PaymentGateway


@dataclass
class PayOrderResult:
    success: bool
    order_id: str
    message: str


class PayOrderUseCase:
    def __init__(self, order_repository: OrderRepository, payment_gateway: PaymentGateway):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> PayOrderResult:
        order = self.order_repository.get_by_id(order_id)
        if order is None:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message=f"Order {order_id} not found"
            )
        
        try:
            order.pay()
        except ValueError as e:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message=str(e)
            )
        
        total = order.total()
        payment_success = self.payment_gateway.charge(order_id, total)
        
        if not payment_success:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                message="Payment gateway declined transaction"
            )
        
        self.order_repository.save(order)
        
        return PayOrderResult(
            success=True,
            order_id=order_id,
            message=f"Order {order_id} paid successfully"
        )
