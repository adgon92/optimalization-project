__author__ = 'Przemek'

import sqlite3
from settings import DB_NAME


class Database(object):

    table_name = "Tasks"
    sql = """CREATE TABLE "Tasks"(
                topic TEXT PRIMARY KEY NOT NULL,
                priority INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                execution_time INTEGER NOT NULL,
                previous_task_1 INTEGER DEFAULT NULL,
                previous_task_2 INTEGER DEFAULT NULL);
                """

    def connect(self, db_name):
        try:
            sqlite3.connect(db_name)
        except sqlite3.DatabaseError:
            print "Error. Can't connect to the database."


    def create_table(self, table_name, sql):
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute('select name from sqlite_master where name=?', (table_name,))
            result = cursor.fetchall()
            if len(result) == 1:
                keep_table = False
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                keep_table = False
            if not keep_table:
                cursor.execute(sql)
                db.commit()

    def insert(self):
        pass

    def drop_table(self, db_name, table_name):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("drop table {0}".format(table_name))
            db.commit()

    def insert(self, values):
        sql = "DELETE FROM Tasks WHERE topic=?"
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()

    def delete(self, data):
        sql = "DELETE FROM Tasks WHERE topic=?"
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql, (data,))
            db.commit()

    def select_all(self):
        sql = "SELECT * FROM Tasks"
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql)
            products = cursor.fetchall()
            return products

    def select_one(self, topic):
        sql = "SELECT * FROM Tasks WHERE topic={}".format(topic)
        with sqlite3.connect(DB_NAME) as db:
            cursor = db.cursor()
            db.text_factory = str
            cursor.execute(sql)
            product = cursor.fetchone()
            return product
