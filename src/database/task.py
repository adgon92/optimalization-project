__author__ = 'gontarz'


class Task(object):

    def __init__(self, *args, **kwargs):
        self.id, \
            self.topic, \
            self.priority, \
            self.profit, \
            self.execution_time, \
            self.prev_task_1, \
            self.prev_task_2 = args
        self.punished = False
        self._index = 0

    @property
    def cost(self):
        profit_per_hour = 1.0 / (float(self.profit) / self.execution_time)
        base_cost = profit_per_hour / self.priority**2
        indexed_cost = base_cost * self.index * 20   # doubled index
        indexed_cost = base_cost
        return indexed_cost if not self.punished else indexed_cost*100000

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        if index >= 0:
            self._index = index + 1
        else:
            raise AttributeError('Index has to be greater than zero.')

    def punish(self):
        self.punished = True

    def dictify(self):
        return (
            self.id,
            {
                "topic": self.topic,
                "cost": self.cost,
                "prev_task_1": self.prev_task_1,
                "prev_task_2": self.prev_task_2
            }
        )

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str((
        self.id, self.topic, self.priority, self.profit, self.execution_time, self.prev_task_1, self.prev_task_2)) + '\n'
        # return str(self.id)
        # return str(self.id) + ' - ' + str(self.cost) + ' - ' + str()