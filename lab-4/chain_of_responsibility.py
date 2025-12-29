class BaseHandler:
    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return True

class SeatAvailabilityHandler(BaseHandler):
    def handle(self, request):
        if not request.get("has_seats"):
            return "Ошибка: Мест нет"
        return super().handle(request)

class PaymentHandler(BaseHandler):
    def handle(self, request):
        if request.get("balance") < request.get("price"):
            return "Ошибка: Недостаточно средств"
        return super().handle(request)

chain = SeatAvailabilityHandler(PaymentHandler())
request = {"has_seats": True, "balance": 500, "price": 1000}
print(chain.handle(request)) # Ошибка: Недостаточно средств