class DatabaseInterface:
    def execute_query(self, query):
        pass

class RealDatabase(DatabaseInterface):
    def execute_query(self, query):
        print(f"Выполнение запроса в RailwayTicketsV2: {query}")

class DatabaseProxy(DatabaseInterface):
    def __init__(self, real_db: RealDatabase):
        self._real_db = real_db

    def execute_query(self, query):
        print(f"[LOG]: Попытка выполнить запрос: {query}")
        # Здесь можно добавить проверку прав доступа
        self._real_db.execute_query(query)

# Использование
db = DatabaseProxy(RealDatabase())
db.execute_query("SELECT * FROM tickets")