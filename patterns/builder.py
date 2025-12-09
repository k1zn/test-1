class House:
    def __init__(self):
        self.walls = None
        self.roof = None
        self.windows = None

    def __str__(self):
        return f"Дом: стены={self.walls}, крыша={self.roof}, окна={self.windows}"


class HouseBuilder:
    def __init__(self):
        self.house = House()

    def build_walls(self, walls):
        self.house.walls = walls
        return self

    def build_roof(self, roof):
        self.house.roof = roof
        return self

    def build_windows(self, windows):
        self.house.windows = windows
        return self

    def build(self):
        return self.house

builder = HouseBuilder()
house = (
    builder
    .build_walls("кирпичные")
    .build_roof("черепичная")
    .build_windows("панорамные")
    .build()
)

print(house)
