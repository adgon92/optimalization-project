__author__ = 'Przemek'

import sqlite3
from settings import DB_NAME
from string import Template
from copy import copy


class Database(object):

    table_name = "Tasks"
    sql = """CREATE TABLE "Tasks"(
                id INTEGER PRIMARY KEY NOT null,
                topic TEXT NOT NULL,
                priority INTEGER NOT NULL,
                profit INTEGER NOT NULL,
                execution_time INTEGER NOT NULL,
                previous_task_1 INTEGER DEFAULT NULL,
                previous_task_2 INTEGER DEFAULT NULL);
                """

    def __init__(self):
        self.cursor = None
        self.db = None

    def __enter__(self):
        try:
            self.db = sqlite3.connect(DB_NAME)
        except sqlite3.DatabaseError as err:
            print "Error. Can't connect to the database."
            raise err
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def drop_table(self, table_name):
        self.cursor.execute("drop table {0}".format(table_name))
        self.db.commit()

    def create_table(self, sql=None):
            sql = sql if sql is not None else self.sql
            self.cursor.execute('select name from sqlite_master where name=?', (self.table_name,))
            result = self.cursor.fetchall()
            if len(result) == 1:
                keep_table = False
                self.cursor.execute("drop table if exists {0}".format(self.table_name))
                self.db.commit()
            else:
                keep_table = False
            if not keep_table:
                self.cursor.execute(sql)
                self.db.commit()

    def delete(self, data):
        sql = "DELETE * FROM Tasks WHERE topic=?"
        self.cursor.execute(sql, (data,))
        self.db.commit()

    def select_all(self):
        sql = "SELECT * FROM Tasks"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def select_one(self, topic):
        sql = "SELECT * FROM Tasks WHERE topic=?"
        self.db.text_factory = str
        self.cursor.execute(sql, (topic,))
        return self.cursor.fetchone()


class TopicDatabase(Database):

    def __init__(self):
        super(TopicDatabase, self).__init__()
        self.sql_core_template = Template("""INSERT INTO Tasks VALUES
            ($id, '$topic', $priority, $profit, $execution_time""")
        self.core_db_columns = "(id, topic, priority, profit, execution_time"

    def is_topic_defined(self, topic):
        return True if self.select_one(topic) else False

    def insert_topic_data(self, topic, **task_params):
        if not self.is_topic_defined(topic):
            task_params["topic"] = topic
            task_params["id"] = int(topic.replace('Temat', ''))
            sql_core = self.sql_core_template.substitute(task_params)
            columns = copy(self.core_db_columns)
            if task_params["previous_task_1"]:
                sql_core += ', {}'.format(task_params["previous_task_1"])
                columns += ', previous_task_1'
            if task_params["previous_task_2"]:
                sql_core += ', {}'.format(task_params["previous_task_2"])
                columns += ', previous_task_2'
            sql = sql_core + ')'
            columns += ') '
            sql = sql.replace('VALUES', columns + ' VALUES')
            print sql
            self.cursor.execute(sql)
            self.db.commit()