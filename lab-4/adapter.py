class ModernPaymentSystem:
    def pay_rubles(self, amount):
        print(f"Оплата {amount} руб. через современный шлюз")

class LegacyPaymentSystem:
    def send_payment(self, amount_usd):
        print(f"Оплата ${amount_usd} через старую систему")

class PaymentAdapter(ModernPaymentSystem):
    def __init__(self, legacy_system: LegacyPaymentSystem):
        self.legacy_system = legacy_system

    def pay_rubles(self, amount):
        amount_usd = amount / 80 
        self.legacy_system.send_payment(amount_usd)

old_system = LegacyPaymentSystem()
adapter = PaymentAdapter(old_system)
adapter.pay_rubles(9000)