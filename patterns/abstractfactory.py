from abc import ABC, abstractmethod

class Chair(ABC):
    @abstractmethod
    def sit(self):
        pass


class Table(ABC):
    @abstractmethod
    def put_on(self):
        pass


class ModernChair(Chair):
    def sit(self):
        return "Сижу на модерновом стуле"


class ModernTable(Table):
    def put_on(self):
        return "Кладу на модерновый стол"


class VictorianChair(Chair):
    def sit(self):
        return "Сижу на викторианском стуле"


class VictorianTable(Table):
    def put_on(self):
        return "Кладу на викторианский стол"


class FurnitureFactory(ABC):
    @abstractmethod
    def create_chair(self) -> Chair:
        pass

    @abstractmethod
    def create_table(self) -> Table:
        pass

class ModernFactory(FurnitureFactory):
    def create_chair(self):
        return ModernChair()

    def create_table(self):
        return ModernTable()


class VictorianFactory(FurnitureFactory):
    def create_chair(self):
        return VictorianChair()

    def create_table(self):
        return VictorianTable()

factory = ModernFactory()
chair = factory.create_chair()
table = factory.create_table()

print(chair.sit())
print(table.put_on())
