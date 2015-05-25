__author__ = 'Adam'

from file_proxy import FileProxy


class Importer(object):

    def __init__(self):
        pass

    def import_data(self):
        print "Importing data..."
        with FileProxy() as proxy:
            proxy.get_json_data()

