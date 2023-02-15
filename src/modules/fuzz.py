# IMPORT
import argparse
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
    parser = argparse.ArgumentParser(prog='reconracoon.py fuzz', description='Module for TEMPLATE')
    parser.add_argument('-t', '--target', dest='target', help='ARGS go HERE')
    args, sysargs = parser.parse_known_args()
    # Call main function
    main(args)


# MAIN
def main(args):
    print(args.target)
