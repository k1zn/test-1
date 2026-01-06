import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from decimal import Decimal
from domain import Order, OrderLine, Money, OrderStatus
from application.pay_order_use_case import PayOrderUseCase
from infrastructure.in_memory_order_repository import InMemoryOrderRepository
from infrastructure.fake_payment_gateway import FakePaymentGateway


@pytest.fixture
def repository():
    return InMemoryOrderRepository()


@pytest.fixture
def payment_gateway():
    return FakePaymentGateway(should_succeed=True)


@pytest.fixture
def use_case(repository, payment_gateway):
    return PayOrderUseCase(repository, payment_gateway)


def test_successful_payment_of_valid_order(use_case, repository):
    order = Order(order_id="order-123")
    order.add_line(OrderLine("Product A", 2, Money(Decimal("10.00"))))
    order.add_line(OrderLine("Product B", 1, Money(Decimal("15.00"))))
    repository.save(order)
    
    result = use_case.execute("order-123")
    
    assert result.success is True
    assert result.order_id == "order-123"
    assert "paid successfully" in result.message
    
    saved_order = repository.get_by_id("order-123")
    assert saved_order.is_paid() is True
    assert saved_order.status == OrderStatus.PAID


def test_error_when_paying_empty_order(use_case, repository):
    order = Order(order_id="empty-order")
    repository.save(order)
    
    result = use_case.execute("empty-order")
    
    assert result.success is False
    assert "Cannot pay empty order" in result.message
    
    saved_order = repository.get_by_id("empty-order")
    assert saved_order.is_paid() is False
    assert saved_order.status == OrderStatus.PENDING


def test_error_when_paying_already_paid_order(use_case, repository):
    order = Order(order_id="paid-order")
    order.add_line(OrderLine("Product", 1, Money(Decimal("20.00"))))
    order.pay()
    repository.save(order)
    
    result = use_case.execute("paid-order")
    
    assert result.success is False
    assert "Order already paid" in result.message


def test_cannot_modify_order_after_payment(repository, payment_gateway):
    order = Order(order_id="order-456")
    order.add_line(OrderLine("Product", 1, Money(Decimal("10.00"))))
    repository.save(order)
    
    use_case = PayOrderUseCase(repository, payment_gateway)
    
    result = use_case.execute("order-456")
    assert result.success is True
    
    paid_order = repository.get_by_id("order-456")
    
    with pytest.raises(ValueError, match="Cannot modify paid order"):
        paid_order.add_line(OrderLine("Another Product", 1, Money(Decimal("5.00"))))
    
    with pytest.raises(ValueError, match="Cannot modify paid order"):
        paid_order.remove_line(paid_order.lines[0])


def test_correct_total_calculation():
    order = Order(order_id="calc-order")
    order.add_line(OrderLine("Item A", 3, Money(Decimal("10.50"))))
    order.add_line(OrderLine("Item B", 2, Money(Decimal("7.25"))))
    order.add_line(OrderLine("Item C", 1, Money(Decimal("9.00"))))
    
    total = order.total()
    
    expected_total = Decimal("31.50") + Decimal("14.50") + Decimal("9.00")
    assert total.amount == expected_total
    assert total.currency == "USD"


def test_payment_gateway_declined(repository):
    order = Order(order_id="declined-order")
    order.add_line(OrderLine("Product", 1, Money(Decimal("100.00"))))
    repository.save(order)
    
    failing_gateway = FakePaymentGateway(should_succeed=False)
    use_case = PayOrderUseCase(repository, failing_gateway)
    
    result = use_case.execute("declined-order")
    
    assert result.success is False
    assert "declined" in result.message.lower()


def test_order_not_found(use_case):
    result = use_case.execute("non-existent")
    
    assert result.success is False
    assert "not found" in result.message.lower()


def test_payment_gateway_receives_correct_amount(repository, payment_gateway):
    order = Order(order_id="amount-test")
    order.add_line(OrderLine("Product", 2, Money(Decimal("25.00"))))
    repository.save(order)
    
    use_case = PayOrderUseCase(repository, payment_gateway)
    
    result = use_case.execute("amount-test")
    
    assert result.success is True
    assert len(payment_gateway.processed_payments) == 1
    assert payment_gateway.processed_payments[0]["amount"] == Decimal("50.00")
    assert payment_gateway.processed_payments[0]["order_id"] == "amount-test"


if __name__ == "__main__":
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(should_succeed=True)
    uc = PayOrderUseCase(repo, gateway)
    
    test_successful_payment_of_valid_order(uc, repo)
    print("[v] test_successful_payment_of_valid_order")
    
    repo.clear()
    gateway.reset()
    test_error_when_paying_empty_order(uc, repo)
    print("[v] test_error_when_paying_empty_order")
    
    repo.clear()
    gateway.reset()
    test_error_when_paying_already_paid_order(uc, repo)
    print("[v] test_error_when_paying_already_paid_order")
    
    repo.clear()
    gateway.reset()
    test_cannot_modify_order_after_payment(repo, gateway)
    print("[v] test_cannot_modify_order_after_payment")
    
    test_correct_total_calculation()
    print("[v] test_correct_total_calculation")
    
    repo.clear()
    gateway.reset()
    test_payment_gateway_declined(repo)
    print("[v] test_payment_gateway_declined")
    
    repo.clear()
    gateway.reset()
    test_order_not_found(uc)
    print("[v] test_order_not_found")
    
    repo.clear()
    gateway.reset()
    test_payment_gateway_receives_correct_amount(repo, gateway)
    print("[v] test_payment_gateway_receives_correct_amount")
    
    print("\nAll tests passed!")
