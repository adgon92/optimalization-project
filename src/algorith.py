__author__ = 'Adam'

from console.input_parser import Parser

if __name__ == "__main__":
    # parser = Parser()
    # parser.read_input()
    from solvers.alg_solver import Solver
    solver = Solver('linear')
    solver.solve()