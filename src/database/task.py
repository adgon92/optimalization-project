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

    @property
    def cost(self):
        profit_per_hour = 1.0 / (float(self.profit) / self.execution_time)
        base_cost = profit_per_hour / self.priority
        return base_cost if not self.punished else base_cost*100

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
        # return str((
        # self.id, self.topic, self.priority, self.profit, self.execution_time, self.prev_task_1, self.prev_task_2))
        return str(self.id)