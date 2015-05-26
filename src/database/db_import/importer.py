__author__ = 'Adam'

from file_proxy import FileProxy
from database.database import TopicDatabase


class Importer(object):

    def __init__(self):
        pass

    def import_data(self):
        print "Importing data..."
        with FileProxy() as proxy:
            json_data = proxy.get_json_data()
            with TopicDatabase() as db:
                db.create_table()
                for topic, description in json_data.items():
                    db.insert_topic_data(topic, **description)