__author__ = 'Adam'

from file_proxy import FileProxy


class Importer(object):

    def __init__(self):
        pass

    def import_data(self, file_path):
        with FileProxy(file_path) as proxy:
            pass
