__author__ = 'Przemek'

import sqlite3
import abc


class Database(object):
    DB_NAME = "Tasks.db"

    @staticmethod
    def connect(db_name):
        try:
            sqlite3.connect(db_name)
        except sqlite3.DatabaseError:
            print "Error. Can't connect to the database."


    @staticmethod
    def createTable(table_name, sql):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute('select name from sqlite_master where name=?', (table_name,))
            result = cursor.fetchall()
            keep_table = True
            if len(result) == 1:
                keep_table = False
                cursor.execute("drop table if exists {0}".format(table_name))
                db.commit()
            else:
                keep_table = False
            if not keep_table:
                cursor.execute(sql)
                db.commit()

    @staticmethod
    def dropTable(db_name, tableName):
        with sqlite3.connect(db_name) as db:
            cursor = db.cursor()
            cursor.execute("drop table {0}".format(tableName))
            db.commit()

    @staticmethod
    @abc.abstractmethod
    def insert(sql, values):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql, values)
            db.commit()

    @staticmethod
    @abc.abstractmethod
    def delete(sql, data):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql, (data,))
            db.commit()

    @staticmethod
    @abc.abstractmethod
    def selectAll(sql):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute(sql)
            products = cursor.fetchall()
            return products

    @staticmethod
    @abc.abstractmethod
    def selectOne(sql):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            db.text_factory = str
            cursor.execute(sql)
            product = cursor.fetchone()
            return product
