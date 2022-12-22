import psycopg2 as pg
import os


class PgConn:

    def __init__(self, db_name):
        self.db_name = db_name

    def __enter__(self):
        self.conn = pg.connect(host=os.getenv('POSTGRES_HOST'),
                               database=self.db_name,
                               user=os.getenv('POSTGRES_USER'),
                               password=os.getenv('POSTGRES_PASSWORD'))
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        if exc_val:
            raise
