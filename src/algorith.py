__author__ = 'Adam'

from console.input_parser import Parser

if __name__ == "__main__":
    # parser = Parser()
    # parser.read_input()
    from database.database import TopicDatabase

    with TopicDatabase() as db:
        print db.select_all()