import mysql.connector as connector


class DB:
    def __init__(self):
        self.connection = None

    def connect(self, config):
        self.connection = connector.connect(**config)

    def cursor(self):
        return self.connection.cursor()

    def commit(self):
        self.connection.commit()


db = DB()
