# IMPORT
import argparse
import os
from ..framework import cli
# IMPORT MODULE
# import xyz


# CUSTOM FUNCTIONS #
def placeholder1():
    pass


def placeholder2():
    pass


def placeholder3():
    pass


# INIT
def init():
    # Args
    parser = argparse.ArgumentParser(prog='reconracoon.py resolve', description='Module for TEMPLATE')
    parser.add_argument('-t', '--target', dest='target', help='ARGS go HERE')
    parser.add_argument('-v', '--verbose', action='store_true', help='ARGS go HERE')
    args, sysargs = parser.parse_known_args()
    # Validate Target
    try:
        if os.path.isfile(args.target) is False:
            transfer = str(args.target)
        if os.path.isfile(args.target) is True:
            with open(args.target) as file:
                transfer = [x.strip() for x in file.readlines()]
    except Exception as E:
        print(f'{cli.red}[x]{cli.endc} Error: {E}')
    # Call main function
    main(args, target=transfer)


# MAIN
def main(args, target):
    print(args)
    print(target)
