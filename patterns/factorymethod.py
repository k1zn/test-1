from abc import ABC, abstractmethod

class Transport(ABC):
    @abstractmethod
    def move(self):
        pass


class Car(Transport):
    def move(self):
        return "Еду на машине"


class Bike(Transport):
    def move(self):
        return "Еду на велосипеде"


class TransportCreator(ABC):
    @abstractmethod
    def create_transport(self) -> Transport:
        pass


class CarCreator(TransportCreator):
    def create_transport(self):
        return Car()


class BikeCreator(TransportCreator):
    def create_transport(self):
        return Bike()

creator = CarCreator()
transport = creator.create_transport()
print(transport.move())
