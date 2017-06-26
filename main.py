import sys
from copy import deepcopy

from commands import run_command
from helpers import config_from_file, get_parser_args


def interact(data):
    config = deepcopy(data)
    while True:
        try:
            command = input('> ')
            # run_command must return new config or None
            new_config = run_command(command, config)
            if new_config is not None:
                config = new_config
        except (EOFError, KeyboardInterrupt):
            sys.exit()


def main():
    config = {}

    if get_parser_args().file:
        config = config_from_file()

    interact(config)


if __name__ == '__main__':
    main()
