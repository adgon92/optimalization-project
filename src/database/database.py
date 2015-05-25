__author__ = 'Przemek'

import sqlite3
import abc
import logging
import sys
import traceback

from PyQt4 import QtGui


class Database(object):
    DB_NAME = "Tasks.db"

    @staticmethod
    def connect(db_name):
        try:
            sqlite3.connect(db_name)
            logging.log(logging.DEBUG, "Connected to the {} database".format(db_name))
        except sqlite3.DatabaseError:
            print "Error. Can't connect to the database."
            ex_type, ex_value, ex_traceback = sys.exc_info()
            lines = traceback.format_exception(ex_type, ex_value, ex_traceback)
            message = ''.join("!! " + line for line in lines)

    @staticmethod
    def createTable(table_name, sql):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            cursor.execute('select name from sqlite_master where name=?', (table_name,))
            result = cursor.fetchall()
            keep_table = True
            if len(result) == 1:
                messBox = QtGui.QMessageBox()
                response = QtGui.QMessageBox.question(messBox, "Warning!", "The table {0} already exists,"
                                                                           "recreate it?".format(table_name),
                                                      QtGui.QMessageBox.Ok, QtGui.QMessageBox.No)
                if response == 1024:
                    print "recreating..."
                    keep_table = False
                    cursor.execute("drop table if exists {0}".format(table_name))
                    db.commit()
                else:
                    print "table kept"
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
    def update(sql, data):
        with sqlite3.connect(Database.DB_NAME) as db:
            cursor = db.cursor()
            if len(data) == 1:
                data = (data,)
            cursor.execute(sql, data)
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