# IMPORT
import argparse
import os
from ..framework import cli
# IMPORT MODULE
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 100

# Common http ports
ports = [66, 80, 81, 443, 445, 457, 1080, 1100, 1241, 1352, 1433, 1434, 1521,
         1944, 2301, 3000, 3128, 3306, 4000, 4001, 4002, 4100, 4443, 5000,
         5432, 5800, 5801, 5802, 6346, 6347, 7001, 7002, 8443, 8888, 30821]


# CUSTOM FUNCTIONS #
def placeholder1():
    pass


def placeholder2():
    pass


# Https enumeration
def enum_https(target, timeout, headers, verbose):
    # https
    https_fqdn = f'https://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(https_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
        if r.headers["server"]:
            srv = r.headers["server"]
        else:
            srv = "None"
        if r.status_code in range(100, 199):
            print(f'{cli.blue}INFO{cli.endc} - {https_fqdn} [{cli.blue}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(200, 299):
            print(f'{cli.green}SUCCESS{cli.endc} - {https_fqdn} [{cli.green}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(300, 399):
            print(f'{cli.yellow}REDIRECTION{cli.endc} - {https_fqdn} [{cli.yellow}{r.status_code}{cli.endc}] ({srv}) {cli.yellow}→{cli.endc} {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{cli.purple}CLIENT_ERROR{cli.endc} - {https_fqdn} [{cli.purple}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(500, 599):
            print(f'{cli.red}SERVER_ERROR{cli.endc} - {https_fqdn} [{cli.red}{r.status_code}{cli.endc}] ({srv})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if verbose is True:
            print(f'{cli.red}TIMEOUT{cli.endc} - {https_fqdn} [{cli.red}after {timeout}/s {cli.endc}]')
        else:
            pass
    except Exception as E:
        if verbose is True:
            print(f'{cli.red}ERROR{cli.endc} - {https_fqdn} [{cli.red}{E}{cli.endc}]')
        else:
            pass


# Http enumeration
def enum_http(target, timeout, headers, verbose):
    # http
    http_fqdn = f'http://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(http_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
        if r.headers["server"]:
            srv = r.headers["server"]
        else:
            srv = "None"
        if r.status_code in range(100, 199):
            print(f'{cli.blue}INFO{cli.endc} - {http_fqdn}[{cli.blue}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(200, 299):
            print(f'{cli.green}SUCCESS{cli.endc} - {http_fqdn} [{cli.green}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(300, 399):
            print(f'{cli.yellow}REDIRECTION{cli.endc} - {http_fqdn} [{cli.yellow}{r.status_code}{cli.endc}] ({srv}) {cli.yellow}→{cli.endc} {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{cli.purple}CLIENT_ERROR{cli.endc} - {http_fqdn} [{cli.purple}{r.status_code}{cli.endc}] ({srv})')
        elif r.status_code in range(500, 599):
            print(f'{cli.red}SERVER_ERROR{cli.endc} - {http_fqdn} [{cli.red}{r.status_code}{cli.endc}] ({srv})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if verbose is True:
            print(f'{cli.red}TIMEOUT{cli.endc} - {http_fqdn} [{cli.red}after {timeout}/s {cli.endc}]')
        else:
            pass
    except Exception as E:
        if verbose is True:
            print(f'{cli.red}ERROR{cli.endc} - {http_fqdn} [{cli.red}{E}{cli.endc}]')
        else:
            pass


def enum_robots(target, timeout, headers, verbose, robots):
    # download robots.txt
    http_fqdn = f'http://{target}'
    https_fqdn = f'https://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    if robots:
        try:
            r = sesh.get(http_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
            if r.status_code in range(200, 299):
                robo = f'{http_fqdn}/robots.txt'
                robo = requests.get(robo, allow_redirects=False)
                if not os.path.exists('robots'):
                    os.makedirs('robots')
                open(f'robots/HTTP_{target}.txt', 'wb').write(robo.content)
            else:
                robo = f'{https_fqdn}/robots.txt'
                robo = requests.get(robo, allow_redirects=False)
                if not os.path.exists('robots'):
                    os.makedirs('robots')
                open(f'robots/HTTPS_{target}.txt', 'wb').write(robo.content)
        except requests.exceptions.ConnectTimeout:
            if verbose is True:
                print(f'{cli.red}TIMEOUT{cli.endc} - {http_fqdn} [{cli.red}after {timeout}/s {cli.endc}]')
            else:
                pass
        except Exception as E:
            if verbose is True:
                print(f'{cli.red}ERROR{cli.endc} - {http_fqdn} [{cli.red}{E}{cli.endc}]')
            else:
                pass
    else:
        pass


# INIT
def init():
    # Args
    parser = argparse.ArgumentParser(prog='reconracoon.py resolve', description='Module for TEMPLATE')
    parser.add_argument('-t', '--target', dest='target', type=str, required=True,
                        help='Target subdomains or IPs (str/file)')
    parser.add_argument('-d', '--delay', dest='timeout', type=float, default=1.0, help='Timeout for all web requests')
    parser.add_argument('-u', '--user-agent', dest='user_agent',
                        default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                        type=str, help='Use custom user agent')
    parser.add_argument('-c', '--common-ports', action='store_true', help='Check all common webserver ports (seclist)')
    parser.add_argument('-r', '--robots', action='store_true',
                        help='Saves the robots.txt of each target in a folder (robots/)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose output (timeouts/errors)')
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
    # Var
    if args.user_agent:
        agent = {'User-Agent': args.user_agent}
    # Check Target
    try:
        if type(target) is str:
            if args.common_ports:
                for port in ports:
                    enum_https(f'{target}:{port}', args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                    enum_http(f'{target}:{port}', args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                    enum_robots(target, args.timeout, {'User-Agent': args.user_agent}, args.verbose, args.robots)
            else:
                enum_https(target, args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                enum_http(target, args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                enum_robots(target, args.timeout, {'User-Agent': args.user_agent}, args.verbose, args.robots)
        if type(target) is list:
            if args.common_ports:
                for url in target:
                    for port in ports:
                        enum_https(f'{url}:{port}', args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                        enum_http(f'{url}:{port}', args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                        enum_robots(url, args.timeout, {'User-Agent': args.user_agent}, args.verbose, args.robots)
            else:
                for url in target:
                    enum_https(url, args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                    enum_http(url, args.timeout, {'User-Agent': args.user_agent}, args.verbose)
                    enum_robots(url, args.timeout, {'User-Agent': args.user_agent}, args.verbose, args.robots)
        else:
            pass
    except KeyboardInterrupt:
        print(f'{cli.red} leaving..{cli.endc}')
        exit()

