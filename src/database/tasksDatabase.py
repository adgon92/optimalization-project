__author__ = 'Przemek'

import sqlite3

from database import Database

class TasksDatabase(Database):

    tableName = "Tasks"
    sql = """CREATE TABLE "Tasks"(
                topic TEXT PRIMARY KEY NOT NULL,
                priority INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                execution_time INTEGER NOT NULL,
                previous_task_1 INTEGER DEFAULT NULL,
                previous_task_2 INTEGER DEFAULT NULL);
                """

    @staticmethod
    def insert(topic, **kwargs):
        # dla Adama :)
        #sql = "insert into Tasks ()"
        #Database.insert()
        pass

    @staticmethod
    def delete(data):
        assert type(data) == str
        sql = "DELETE FROM Tasks WHERE topic=?"
        Database.delete(sql, data)

    @staticmethod
    def selectAll():
        sql = "SELECT * FROM Tasks"
        return Database.selectAll(sql)

    @staticmethod
    def selectOne(topic):
        assert type(topic) == str
        sql = "SELECT * FROM Tasks WHERE topic={}".format(topic)
        return Database.selectOne(sql)




def main():
    db = TasksDatabase
    res = db.createTable('Tasks', db.sql)
    print res

if __name__ == "__main__":
    main()