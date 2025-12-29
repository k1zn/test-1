class RouteIterator:
    def __init__(self, routes):
        self._routes = routes
        self._index = 0

    def __next__(self):
        try:
            route = self._routes[self._index]
            self._index += 1
            return route
        except IndexError:
            raise StopIteration()

class RailwayNetwork:
    def __init__(self):
        self.routes = []

    def add_route(self, route):
        self.routes.append(route)

    def __iter__(self):
        return RouteIterator(self.routes)

network = RailwayNetwork()
network.add_route("Москва - СПБ")
network.add_route("Казань - Сочи")

for route in network:
    print(f"Маршрут: {route}")