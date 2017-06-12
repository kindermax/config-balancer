import json
import os
import sys
from argparse import ArgumentParser
from copy import deepcopy
from operator import itemgetter


def get_parser_args():

    parser = ArgumentParser()
    parser.add_argument('-f', help='choose file with configuration',
                        dest='file', type=str)
    parser.add_argument('-o', help='output file', dest='output', type=str)

    if 'h' in parser.parse_args():
        parser.print_help()

    return parser.parse_args()


def config_from_file():
    args = get_parser_args()
    if args.file:
        try:
            filename = os.path.abspath(args.file)
            with open(filename, encoding='utf-8') as file_conf:
                new_config = json.load(file_conf)
                return new_config
        except IOError:
            print('invalid config path')
            sys.exit(1)
        except ValueError:
            print('file does not contain any valid config')
            sys.exit(1)


def update(data, service, count):
    load_per_machine = [
        [key, sum(val.values()), 0] for key, val in data.items()
    ]
    # sort by sum of service on machine and its name
    machines = sorted(deepcopy(load_per_machine), key=itemgetter(1, 0))

    remains = count
    while remains:
        # if config has one machine, just add all services to it
        if len(machines) == 1:
            machines[0][1] += 1
            machines[0][2] += 1
            remains -= 1
        else:
            # adding services until machine at idx 0 becomes more loaded
            # than machine at idx 1
            while machines[0][1] < machines[1][1] and remains:
                machines[0][1] += 1
                machines[0][2] += 1
                remains -= 1

            # always sorting almost sorted machines list
            if remains:
                machines.sort(key=itemgetter(1,0))

            idx = 1
            if remains == 1:
                idx = 0

            if remains and machines[0][1] == machines[1][1] :
                machines[idx][1] += 1
                machines[idx][2] += 1
                remains -= 1

    config = deepcopy(data)

    for machine, _, svc_count in machines:
        if not svc_count:
            continue
        if service not in config[machine]:
            config[machine][service] = svc_count
        else:
            config[machine][service] += svc_count

    return config