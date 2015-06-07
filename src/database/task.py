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

    @property
    def cost(self):
        profit_per_hour = self.profit / self.execution_time
        return profit_per_hour * self.priority

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
        self.id, self.topic, self.priority, self.profit, self.execution_time, self.prev_task_1, self.prev_task_2))