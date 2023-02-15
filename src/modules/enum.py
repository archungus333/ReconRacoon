# IMPORT
import argparse
from ..framework import cli
# IMPORT MODULE
import socket
from rich.progress import track
from rich import print as rprint


# CUSTOM FUNCTIONS #
def enum(new, domain, subs, ips, verbose, wildcard):
    for subdom in track(new):
        try:
            dns = f'{subdom}.{domain}'
            ip = socket.gethostbyname(dns)
            if ip != wildcard:
                rprint(
                    f'\r[green][+][/green] Hostname: [green]{subdom}[/green].[blue]{domain}[/blue]\t IP: [white]{ip}[/white]')
                ips.append(ip)
                subs.append(f'{subdom}.{domain}')
            else:
                pass
        except Exception as E:
            if verbose is True:
                rprint(f'\r[red][-][/red] Hostname: {dns}\t Response: [red]{E}[/red]')
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
    parser.add_argument('-d', '--domain', required=True)
    parser.add_argument('-w', '--wordlist', required=True)
    parser.add_argument('-o', '--output')
    # parser.add_argument('-t', '--threads', nargs='?', const=2, type=int)
    parser.add_argument('-v', '--verbose', action='store_true')
    args, sysargs = parser.parse_known_args()
    # Call main function
    main(args)


# MAIN
def main(args):
    # Var
    outfile = args.output
    wordlist = args.wordlist
    domain = args.domain
    verbose = args.verbose
    # Parse Wordlist
    f = open(wordlist)
    lst = f.readlines()
    # Filter Wordlist
    new = list(map(str.strip, lst))
    new = list(dict.fromkeys(new))
    new = [x.lower() for x in new]
    wildcard = socket.gethostbyname(domain)
    rprint(f'\r[blue][$][/blue] Wildcard: [green]*[/green].[blue]{domain}[/blue]\t IP: [white]{wildcard}[/white]')
    # Lists
    ips = []
    subs = []
    # Main Loop
    enum(new, domain, subs, ips, verbose, wildcard)
    # Generate Out Files
    gen_output(outfile, subs, ips)
