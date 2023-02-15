# IMPORT
import argparse
import os
import sys
from ..framework import cli
# IMPORT MODULE
import socket
from rich.progress import track


# CUSTOM FUNCTIONS #
def enum(new, domain, subs, ips, verbose, wildcard):
    for subdom in track(new):
        try:
            dns = f'{subdom}.{domain}'
            ip = socket.gethostbyname(dns)
            if ip != wildcard:
                print(f'\r{cli.green}[+]{cli.endc} Hostname: {cli.green}{subdom}{cli.endc}.{cli.blue}{domain}{cli.endc}\t IP: {ip}')
                ips.append(ip)
                subs.append(f'{subdom}.{domain}')
            else:
                pass
        except Exception as E:
            if verbose is True:
                print(f'\r{cli.red}[-]{cli.endc} Hostname: {dns}\t Response: {cli.red}{E}{cli.endc} ')
            else:
                pass


def gen_output(outfile, subs, ips):
    # Generate Out Files
    if outfile:
        with open(outfile, 'w') as f:
            for line in subs:
                f.write(f'{line}\n')
            for line in ips:
                f.write(f'{line}\n')


# INIT
def init():
    # Argparse
    parser = argparse.ArgumentParser(prog='reconracoon.py enum', description='Module for Subdomain Enumeration')
    parser.add_argument('-t', '--target', required=True)
    parser.add_argument('-w', '--wordlist', required=True)
    parser.add_argument('-o', '--output')
    # parser.add_argument('-t', '--threads', nargs='?', const=2, type=int)
    parser.add_argument('-v', '--verbose', action='store_true')
    args, sysargs = parser.parse_known_args()
    # Validate Target
    try:
        if os.path.isfile(args.target) is False:
            transfer = str(args.target)
        if os.path.isfile(args.target) is True:
            print(f'{cli.red}[x]{cli.endc} Error: Files not Supported')
            sys.exit()
    except Exception as E:
        print(f'{cli.red}[x]{cli.endc} Error: {E}')
    # Call main function
    main(args, target=transfer)


# MAIN
def main(args, target):
    # Var
    outfile = args.output
    wordlist = args.wordlist
    verbose = args.verbose
    # Parse Wordlist
    f = open(wordlist)
    lst = f.readlines()
    # Filter Wordlist
    new = list(map(str.strip, lst))
    new = list(dict.fromkeys(new))
    new = [x.lower() for x in new]
    wildcard = socket.gethostbyname(target)
    print(f'\r{cli.blue}[$]{cli.endc} Wildcard: {cli.green}*{cli.endc}.{cli.blue}{target}{cli.endc}\t IP: {wildcard}')
    # Lists
    ips = []
    subs = []
    # Main Loop
    enum(new, target, subs, ips, verbose, wildcard)
    # Generate Out Files
    gen_output(outfile, subs, ips)
