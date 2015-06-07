__author__ = 'gontarz'


class Objective(object):
    def __init__(self):
        pass

    def get(self, tasks):
        """
        :param tasks: A vector containing tasks in given order
        :type tasks: list
        """
        return reduce(lambda x, y: x + y, [self._get_obj_cost(task) for task in tasks])

    def _get_obj_cost(self, task):
        pass


