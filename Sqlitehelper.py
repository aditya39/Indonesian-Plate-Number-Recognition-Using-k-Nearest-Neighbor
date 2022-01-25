import sqlite3

class SqliteHelper:

    def __init__(self, name=None):
        self.conn = None
        self.cursor = None

        if name:
            self.open(name)

    def open(self, name):
        try:
            self.conn = sqlite3.connect(name)
            self.cursor = self.conn.cursor()

        except sqlite3.Error as e:
            print("Gagal terhubung dengan database...")

    def edit(self, query):
        c = self.cursor
        c.execute(query)
        self.conn.commit()

    def insert(self,query,inserts):
        c = self.cursor
        c.execute(query,inserts)
        self.conn.commit()

    def select(self,query):
        c = self.cursor
        c.execute(query)
        return c.fetchall()


