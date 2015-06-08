__author__ = 'gontarz'

import math
import random
import copy
import numpy as np
from settings import START_VECTOR
from database.database import TopicDatabase
from plot.ploter import Ploter


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
        self._index_tasks(c_tasks)
        return reduce(lambda x, y: x + y, [task.cost for task in c_tasks])

    # noinspection PyMethodMayBeStatic
    def _find_max_profit(self, tasks):
        profits = [task.cost for task in tasks]
        return max(profits)

    def _check_order(self, tasks):
        for task in tasks[1:]:
            before = tasks[:tasks.index(task)]
            before_ids = [prev_task.id for prev_task in before]
            if task.prev_task_1 is not None:
                if not task.prev_task_1 in before_ids:
                    # print('Punishing {}. Cost before: {}'.format(task.topic, task.cost))
                    task.punish()
                    # print('     Cost after: {}'.format(task.cost))
                if task.prev_task_2 is not None:
                    if not task.prev_task_2 in before_ids:
                        task.punish()

    def _index_tasks(self, tasks):
        for task in tasks:
            task.index = tasks.index(task)


class Solver(object):

    @staticmethod
    def _to_log(value):
        return -0.1/math.log(value)

    @staticmethod
    def _get_reduction_per_cycle(ini_tamp, final_temp, noc):
        return (final_temp/ini_tamp)**(1.0/(noc-1.0))

    NUMBER_OF_CYCLES = 50
    TRIALS_PER_CYCLE = 10
    START_WORSE_SOL_ACCEPTANCE = 0.9999
    END_WORSE_SOL_ACCEPTANCE = 0.003

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
        self.ploter = Ploter()

    @property
    def cooling_method(self):
        factor = self.final_temperature/self.initial_temperature
        boltzmans_const = 1.0/(self.NUMBER_OF_CYCLES-1.0)
        cooling = {
            'linear': 1-self.initial_temperature/(100*self.NUMBER_OF_CYCLES),
            'geometrical': factor**boltzmans_const,
            'logarithmic': 1/math.log10(boltzmans_const)
        }
        return cooling[self._cooling_method]

    @cooling_method.setter
    def cooling_method(self, method):
        allowed_values = ('linear', 'geometrical', 'logarithmic')
        if method not in allowed_values:
            raise AttributeError('Allowed vales are: {}'.format(''.join(allowed_values)))
        self._cooling_method = method

    def solve(self):
        ini_vector = START_VECTOR
        tasks = self._get_tasks(ini_vector)
        best_objective = self.objective.get(tasks)
        best_solution = tasks
        objectives = np.zeros(self.NUMBER_OF_CYCLES + 1)
        objectives[0] = best_objective
        temperature = self.initial_temperature
        print 'Initial temperature: {}'.format(temperature)
        delta_avg = 0.0
        nof_accepted_solutions = 0.0
        for i in range(self.NUMBER_OF_CYCLES):
            print 'Cycle: {} with Temperature: {}'.format(i, temperature)
            for j in range(self.TRIALS_PER_CYCLE):
                for k in range(5):
                    tasks = self._reorder(tasks)
                #tasks = self._reorder(tasks)
                current_objective = self.objective.get(tasks)
                current_delta = abs(current_objective-best_objective)
                if current_objective > best_objective:  # worse solution case
                    # Initialize DeltaE_avg if a worse solution was found
                    #   on the first iteration
                    if not i and not j:
                        delta_avg = current_delta
                    prob_of_acceptance = math.exp(-current_delta/(delta_avg*temperature))
                    # determine whether to accept worse point
                    if random.random() < prob_of_acceptance:
                        accept = True  # accept the worse solution
                    else:
                        accept = False  # don't accept the worse solution
                else:  # objective function is lower, automatically accept
                    accept = True
                if accept:  # update currently accepted solution
                    best_objective = current_objective
                    best_solution = tasks
                    nof_accepted_solutions += 1.0
                    # update DeltaE_avg
                    delta_avg = (delta_avg * (nof_accepted_solutions - 1.0) + current_delta) / nof_accepted_solutions
            objectives[i] = best_objective
            temperature = self._cool_down(temperature)
        print(best_objective)
        print(best_solution)
        self.ploter.plot(objectives)
        self.ploter.show()
        self.ploter.save('test_plot.png')


    def _cool_down(self, temperature):
        print self.cooling_method
        return self.cooling_method * temperature

    def _get_tasks(self, ids):
        with TopicDatabase() as db:
            return [db.select_one('Temat{}'.format(task_id)) for task_id in ids]

    def _reorder(self, tasks):
        first = second = self._rand_index()
        while first == second:
            second = self._rand_index()
        tasks[first], tasks[second] = tasks[second], tasks[first]
        return tasks


    def _rand_index(self):
        return random.randint(0, len(START_VECTOR) - 1)
