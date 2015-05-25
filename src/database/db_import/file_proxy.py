__author__ = 'Adam'

from settings import DATA_FILE_PATH
import csv


class FileProxy(object):

    def __init__(self):
        self.file = None
        self.reader = None

    def __enter__(self):
        print "Opening data file..."
        self.file = open(DATA_FILE_PATH, 'r')
        print "Data file opened SUCCESSFULLY"
        self.reader = csv.reader(self.file)
        return self

    def __exit__(self, ex_type, value, traceback):
        if ex_type is not None:
            print 'Exception caught: {}\n {}\n      Cause: {}'.format(ex_type, '\n'.join(traceback), value)
        self.file.close()
        print "Data file closed"

    def read_lines(self):
        if self.reader is not None:
            lines = []
            for row in self.reader:
                lines.append(row)
            return lines
        raise RuntimeError('File reader has not been defined yet.')

    def get_json_data(self):
        print 'Reading data from file...'
        return self.__convert_lines_to_json()

    def __convert_lines_to_json(self):
        print 'Converting data to JSON format...'
        lines = self.read_lines()
        keys = lines[0]
        result = {line[0]: dict(zip(keys[1:], line[1:])) for line in lines[1:]}
        print 'Converted SUCCESSFULLY'
        print result
        return result