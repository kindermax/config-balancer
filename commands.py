import json
import os
from collections import Sequence
from copy import deepcopy
from datetime import datetime
from pprint import pprint

import sys

from helpers import update, get_parser_args

commands = {}


def command(names):
    """Bind function to command name"""
    def decorator(f):
        if isinstance(names, Sequence) and not isinstance(names, str):
            # we can bind several names to one function
            for name in names:
                commands[name] = f
        else:
            commands[names] = f
        return f
    return decorator


def run_command(cmd, config):
    if cmd not in commands:
        print('incorrect command')
        return config
    new_config = deepcopy(config)
    command_func = commands[cmd]
    new_config = command_func(new_config)
    return new_config


@command('add server')
def add_server(config):
    server_name = input('> server name: ')
    new_config = deepcopy(config)
    if server_name not in config:
        new_config[server_name] = {}
    return new_config


@command('add service')
def add_service(config):
    if not config.keys():
        print('add server for the first!')
        return config
    service_name = input('> service name: ')
    services_amount = int(input('> services amount: '))
    new_config = deepcopy(config)
    new_config = update(new_config, service_name, services_amount)
    return new_config


@command('print')
def print_config(config):
    print('Current config:')
    pprint(config)
    return config


@command(['help', '?'])
def print_help(config):
    print("Commands:")
    commands_help = '\n\t'.join(
        ['', *sorted([cmd for cmd in commands.keys() if cmd != '?'])]
    )
    commands_help = commands_help.replace('help', 'help, ?')
    print(commands_help)
    return config


@command('save')
def save_config(config):
    filename = 'config_{}'.format(datetime.now().timestamp())
    args = get_parser_args()
    if args.output:
        filename = os.path.abspath(args.output)
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(config, f)
    return config


@command('exit')
def close(config):
    sys.exit()
