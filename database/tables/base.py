from server.sql_conn import db

class Base(db.Model):
    __abstract__ = True
