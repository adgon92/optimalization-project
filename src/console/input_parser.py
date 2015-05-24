__author__ = 'Adam'

import argparse
import textwrap


class Parser(object):  # for new style inheritance

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            conflict_handler='resolve',
            description=textwrap.dedent("""
            Simulated annealing algorithm.
            Create your own prioritized task-list.
            --------------------------------------
            """)
        )
        self.__add_arguments()

    def __add_arguments(self):
        self.__add_core_group()

    def __add_core_group(self):
        """
        Adds mutually exclusive group - we can import txt file into the database or launch the algorithm
        """
        core_funcs = self.parser.add_mutually_exclusive_group()
        core_funcs.add_argument("-s", "--start",
                                action="store_true",
                                help="Start algorithm")
        core_funcs.add_argument("-i", "--import",
                                action="store_true",
                                help="Triggers data import")

    def read_input(self):
        self.parser.parse_args()