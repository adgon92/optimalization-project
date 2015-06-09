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
        c_tasks = self._check_order(c_tasks)
        c_tasks = self._index_tasks(c_tasks)
        return reduce(lambda x, y: x + y, [task.cost for task in c_tasks])

    # noinspection PyMethodMayBeStatic
    def _find_max_profit(self, tasks):
        profits = [task.cost for task in tasks]
        return min(profits)

    def _check_order(self, tasks):
        if tasks[0].prev_task_1 is not None:
            tasks[0].punish()
        for task in tasks[1:]:
            before = tasks[:tasks.index(task)]
            before_ids = [prev_task.id for prev_task in before]
            if task.prev_task_1 is not None:
                if not task.prev_task_1 in before_ids:
                    task.punish()
                if task.prev_task_2 is not None:
                    if not task.prev_task_2 in before_ids:
                        task.punish()
        return tasks

    def _index_tasks(self, tasks):
        for task in tasks:
            task.index = tasks.index(task)
        return tasks


class Solver(object):

    @staticmethod
    def _to_log(value):
        return -0.1/math.log(value)

    @staticmethod
    def _get_reduction_per_cycle(ini_tamp, final_temp, noc):
        return (final_temp/ini_tamp)**(1.0/(noc-1.0))

    NUMBER_OF_CYCLES = 300
    TRIALS_PER_CYCLE = 100
    START_WORSE_SOL_ACCEPTANCE = 0.9899
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
        self.ploter = Ploter()

    @property
    def cooling_method(self):
        factor = self.final_temperature/self.initial_temperature
        boltzmans_const = 1.0/(self.NUMBER_OF_CYCLES-1.0)
        cooling = {
            'linear': lambda
                current_cycle: self.initial_temperature - self.initial_temperature / self.NUMBER_OF_CYCLES * current_cycle,
            'geometrical': factor**boltzmans_const,
            'logarithmic': 1/math.log(boltzmans_const)
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
        temperatures = copy.deepcopy(objectives)
        objectives[0] = best_objective
        temperature = self.initial_temperature
        temperatures[0] = temperature
        print 'Initial temperature: {}'.format(temperature)
        delta_avg = 0.0
        nof_accepted_solutions = 0.0
        well_ordered = None
        for i in range(self.NUMBER_OF_CYCLES):
            print 'Cycle: {} with Temperature: {}'.format(i, temperature)
            for j in range(self.TRIALS_PER_CYCLE):
                # for k in range(5):
                #     tasks = self._reorder(tasks)
                tasks = self._reorder(copy.deepcopy(tasks)) if well_ordered is None else self._reorder(copy.deepcopy(well_ordered))
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
                    # print('Cycle: {}, sub: {}, {}'.format(i, j, tasks))
                    # print('Previous: {}'.format(best_solution))
                    best_objective = current_objective
                    well_ordered = tasks
                    nof_accepted_solutions += 1.0
                    # update DeltaE_avg
                    delta_avg = (delta_avg * (nof_accepted_solutions - 1.0) + current_delta) / nof_accepted_solutions
            best_solution = well_ordered
            objectives[i] = best_objective
            temperature = self._cool_down(temperature, i)
            temperatures[i] = temperature
        with open('{}_{}_{}.txt'.format(self._cooling_method, self.NUMBER_OF_CYCLES, self.TRIALS_PER_CYCLE), 'w+') as f:
            print >> f, best_objective
            print >> f, best_solution
        self.ploter.plot(objectives, self._cooling_method, self.initial_temperature, self.NUMBER_OF_CYCLES)
        self.ploter.save('objectives_{}_{}_{}.png'.format(self._cooling_method, self.NUMBER_OF_CYCLES, self.TRIALS_PER_CYCLE))
        self.ploter.show()
        self.ploter.plot_temperature(temperatures, self._cooling_method, self.initial_temperature, self.NUMBER_OF_CYCLES)
        self.ploter.save('temperatures_{}_{}_{}.png'.format(self._cooling_method, self.NUMBER_OF_CYCLES, self.TRIALS_PER_CYCLE))
        self.ploter.show()


    def _cool_down(self, temperature, current_cycle):
        return self.cooling_method * temperature if type(self.cooling_method) == float else self.cooling_method(current_cycle)

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