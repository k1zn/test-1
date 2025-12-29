from abc import ABC, abstractmethod

class PricingStrategy(ABC):
    @abstractmethod
    def calculate(self, price: float) -> float:
        pass

class FullPriceStrategy(PricingStrategy):
    def calculate(self, price: float) -> float:
        return price

class StudentDiscountStrategy(PricingStrategy):
    def calculate(self, price: float) -> float:
        return price * 0.5

class TicketContext:
    def __init__(self, strategy: PricingStrategy):
        self.strategy = strategy

    def set_strategy(self, strategy: PricingStrategy):
        self.strategy = strategy

    def get_ticket_price(self, base_price: float):
        return self.strategy.calculate(base_price)

context = TicketContext(FullPriceStrategy())
print(f"Полная цена: {context.get_ticket_price(1000)}")

context.set_strategy(StudentDiscountStrategy())
print(f"Студенческая цена: {context.get_ticket_price(1000)}")