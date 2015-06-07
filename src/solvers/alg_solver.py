__author__ = 'gontarz'

import math
import copy
import numpy as np
from settings import START_VECTOR
from database.database import TopicDatabase


class Objective(object):
    def __init__(self, start_vector):
        self.max_profit = self._find_max_profit(start_vector)

    def get(self, tasks):
        """
        :param tasks: A vector containing tasks in given order
        :type tasks: list
        """
        c_tasks = copy.deepcopy(tasks)
        self._check_order(c_tasks)
        return reduce(lambda x, y: x + y, [task.cost for task in c_tasks])

    # noinspection PyMethodMayBeStatic
    def _find_max_profit(self, tasks):
        profits = [task.cost for task in tasks]
        return max(profits)

    def _check_order(self, tasks):
        print(tasks)
        for task in tasks[1:]:
            before = tasks[:tasks.index(task)]
            before_ids = [prev_task.id for prev_task in before]
            if task.prev_task_1 is not None:
                if not task.prev_task_1 in before_ids:
                    print('Punishing {}. Cost before: {}'.format(task.topic, task.cost))
                    task.punish()
                    print('     Cost after: {}'.format(task.cost))
                if task.prev_task_2 is not None:
                    if not task.prev_task_2 in before_ids:
                        task.punish()


class Solver(object):

    @staticmethod
    def _to_log(value):
        return -0.1/math.log(value)

    @staticmethod
    def _get_reduction_per_cycle(ini_tamp, final_temp, noc):
        return (final_temp/ini_tamp)**(1.0/(noc-1.0))

    NUMBER_OF_CYCLES = 50
    TRIALS_PER_CYCLE = 50
    NUMBER_OF_ACCEPTED_SOLUTIONS = 0.0
    START_WORSE_SOL_ACCEPTANCE = 0.7
    END_WORSE_SOL_ACCEPTANCE = 0.001

    def __init__(self, method):
        self.initial_temperature = self._to_log(self.START_WORSE_SOL_ACCEPTANCE)
        self.final_temperature = self._to_log(self.END_WORSE_SOL_ACCEPTANCE)
        self.reduction_per_cycle = self._get_reduction_per_cycle(
            self.initial_temperature,
            self.final_temperature,
            self.NUMBER_OF_CYCLES
        )
        self.cooling_method = method
        self.start_tasks = self._get_tasks(START_VECTOR)
        self.objective = Objective(self.start_tasks)

    @property
    def cooling_method(self):
        factor = self.final_temperature/self.initial_temperature
        boltzmans_const = 1.0/(self.NUMBER_OF_CYCLES-1.0)
        cooling = {
            'linear': 1/boltzmans_const,
            'geometrical': factor**boltzmans_const,
            'logarithmic': 1/math.log10(boltzmans_const)
        }
        return cooling[self._cooling_method]

    @cooling_method.setter
    def cooling_method(self, method):
        allowed_values = ('linear', 'geometrical', 'logarithmic')
        if method not in allowed_values:
            raise AttributeError('Allowed vales are: {}'.format(allowed_values))
        self._cooling_method = method

    def solve(self):
        ini_vector = START_VECTOR
        tasks = self._get_tasks(ini_vector)
        best = self.objective.get(tasks)
        solutions = np.zeros(self.NUMBER_OF_CYCLES + 1)
        solutions[0] = best
        temperature = self.initial_temperature

    def _get_tasks(self, ids):
        with TopicDatabase() as db:
            return [db.select_one('Temat{}'.format(task_id)) for task_id in ids]
