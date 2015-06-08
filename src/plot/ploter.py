__author__ = 'Przemek'

import numpy as np
import matplotlib.pyplot as plt

class Ploter:

    def __init__(self):
        pass

    def plot(self, objectives):
        plt.plot(objectives,'r.-')

    def save(self, path):
        plt.savefig(path)

    def show(self):
        plt.show()


