__author__ = 'Adam'

import argparse
import textwrap


# noinspection PyMethodMayBeStatic
class Parser(object):  # for new style inheritance

    def __init__(self):
        self.parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            conflict_handler='resolve',
            description=textwrap.dedent("""\
            Simulated annealing algorithm.
            Create your own prioritized task-list.
            --------------------------------------
            """)
        )
        self.__add_arguments()

    def __add_arguments(self):
        subparsers = self.__create_subparsers_group()
        self.__add_algorithm_input_args(subparsers)
        self.__add_data_import_args(subparsers)

    def __create_subparsers_group(self):
        return self.parser.add_subparsers(title="Work mode",
                                          dest="mode",
                                          description=textwrap.dedent("""\
                                          By default application triggers algorithm.
                                          You can type import flag if you need to create a new database file.
                                          """),
                                          help="Algorithm mode - start or import")

    def __add_algorithm_input_args(self, subparsers):
        start_parser = subparsers.add_parser('start',
                                             help="Triggers algorithm")
        arguments = [
            ('-l', '--loops', 'The number of iterations'),
            ('-t', '--temperature', 'Initial temperature'),
            ('-d', '--delta', 'Temperature delta'),
            ('-m', '--min-temperature', 'Minimal temperature')
        ]
        map(lambda arg: start_parser.add_argument(arg[0], arg[1], help=arg[2]), arguments)

    def __add_data_import_args(self, subparsers):
        import_parser = subparsers.add_parser('import',
                                              help="Import data to the local database")
        import_parser.add_argument('path',
                                   help='Path to a CSV file.')

    def read_input(self):
        args = self.parser.parse_args()
        if args.mode == 'import':
            from database.db_import.importer import Importer
            Importer().import_data(args.path)
        if args.mode == 'start':
            print args
            from workers.worker import Worker
            Worker(
                delta=args.delta,
                loops=args.loops,
                min_temperature=args.min_temperature,
                temperature=args.temperature
            ).work()
