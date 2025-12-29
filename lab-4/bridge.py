# Реализация
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailSender(NotificationSender):
    def send(self, message):
        print(f"Отправка по Email: {message}")

class SmsSender(NotificationSender):
    def send(self, message):
        print(f"Отправка по SMS: {message}")

# Абстракция
class Ticket:
    def __init__(self, sender: NotificationSender):
        self.sender = sender

    def deliver(self, info):
        pass

class ElectronicTicket(Ticket):
    def deliver(self, info):
        self.sender.send(f"Электронный билет: {info}")

e_ticket = ElectronicTicket(SmsSender())
e_ticket.deliver("Поезд 102, место 12")