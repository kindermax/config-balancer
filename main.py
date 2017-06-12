import sys
from copy import deepcopy

from commands import run_command
from helpers import config_from_file, get_parser_args


def interact(data):
    config = deepcopy(data)
    while True:
        try:
            command = input('> ')
            config = run_command(command, config)
        except (EOFError, KeyboardInterrupt):
            sys.exit()


def main():
    config = {}

    if get_parser_args().file:
        config = config_from_file()

    interact(config)


if __name__ == '__main__':
    main()
    # parser_args = get_parser_args()