__author__ = 'Adam'


class Worker(object):

    def __init__(self, delta=None, loops=None, min_temperature=None, temperature=None):
        print delta, loops, min_temperature, temperature
        pass

    def work(self):
        print "Working..."