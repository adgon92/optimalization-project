__author__ = 'Przemek'

import numpy as np
import matplotlib.pyplot as plt


class Ploter:
    def __init__(self):
        pass

    def plot_temperature(self, temperature, cooling_method, initial_temperature, numb_of_cycles):
        plt.plot(temperature, 'b.-')
        plt.xlabel('Number of cycles')
        plt.ylabel('Temperature')
        plt.text(0.7 * numb_of_cycles, max(temperature),
                 self._get_chart_description(cooling_method, initial_temperature, numb_of_cycles))

    def plot(self, objectives, cooling_method, initial_temperature, numb_of_cycles):
        plt.plot(objectives, 'r.-')
        plt.xlabel('Number of cycles')
        plt.ylabel('Quality of solution')
        plt.text(0.7 * numb_of_cycles, max(objectives),
                 self._get_chart_description(cooling_method, initial_temperature, numb_of_cycles),
                 withdash=False)

    @staticmethod
    def _get_chart_description(cooling_method, initial_temperature, numb_of_cycles):
        return 'Cooling method {}\nInitial temperature: {}\nNumb of cycles: {}'.format(cooling_method,
                                                                                       initial_temperature,
                                                                                       numb_of_cycles)

    def save(self, path):
        plt.savefig(path)

    def show(self):
        plt.show()


