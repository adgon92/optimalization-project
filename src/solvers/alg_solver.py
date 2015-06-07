__author__ = 'gontarz'

import math
import copy
from settings import START_VECTOR


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
        return reduce(lambda x, y: x + y, [self._get_obj_cost(task) for task in tasks])

    # noinspection PyMethodMayBeStatic
    def _find_max_profit(self, tasks):
        profits = [task.cost for task in tasks]
        return max(profits)

    def _check_order(self, tasks):
        for task in tasks[1:]:
            before = tasks[:tasks.index(tasks)]
            before_ids = [prev_task.id for prev_task in before]
            if task.prev_task_1 is not None:
                if not task.prev_task_1 in before_ids:
                    task.punish()
                if task.prev_task_2 is not None:
                    if not task.prev_task_2 in before_ids:
                        task.punish()


    def _get_obj_cost(self, task):
        pass


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
    INITIAL_TEMPERATURE = _to_log(START_WORSE_SOL_ACCEPTANCE)
    FINAL_TEMPERATURE = _to_log(END_WORSE_SOL_ACCEPTANCE)
    REDUCTION_PER_CYCLE = _get_reduction_per_cycle(INITIAL_TEMPERATURE, FINAL_TEMPERATURE, NUMBER_OF_CYCLES)

    def __init__(self, method):
        self._cooling_method = self.cooling_method(method)

    @property
    def cooling_method(self):
        factor = self.FINAL_TEMPERATURE/self.INITIAL_TEMPERATURE
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

