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
        plt.text(0.7*numb_of_cycles, max(temperature),
                 'Cooling method: '.join(cooling_method)
                 +'\nInitial temperature: '.join(initial_temperature)
                 +'\nNumb of cycles: '.join(numb_of_cycles))

    def plot(self, objectives, cooling_method, initial_temperature, numb_of_cycles):
        plt.plot(objectives,'r.-')
        plt.xlabel('Number of cycles')
        plt.ylabel('Quality of solution')
        plt.text(0.7*numb_of_cycles, max(objectives),
                 'Cooling method: '.join(cooling_method)
                 +'\nInitial temperature: '.join(initial_temperature)
                 +'\nNumb of cycles: '.join(numb_of_cycles))

    def save(self, path):
        plt.savefig(path)

    def show(self):
        plt.show()


