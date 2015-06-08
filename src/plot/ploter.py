__author__ = 'Przemek'

import numpy as np
import matplotlib.pyplot as plt

class ploter():

    def plot(self, fs):
        plt.plot(fs,'r.-')

    def save(self):
        plt.savefig('iterations.png')

    def show(self):
        plt.show()


