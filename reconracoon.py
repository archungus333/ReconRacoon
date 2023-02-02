import os
import requests
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 100

# Ascii banner
racoon = r'''
                        ,,,
                     .'    `/\_/\
                   .'       <@I@>
        <((((((((((  )____(  \./
                   \( \(   \(\(
   ReconRacoon      `-"`-"  " "
'''
print(racoon)

# Argparse
parser = argparse.ArgumentParser(prog='ReconRacoon', description='Extensive Enumeration of Multiple Subdomains')
parser.add_argument('-t', '--target', dest='target', type=str, required=True, help='Target subdomains or IPs (str/file)')
parser.add_argument('-d', '--delay', dest='timeout',type=float, default=1, help='Timeout for all web requests')
parser.add_argument('-u', '--user-agent', dest='user_agent', type=str, help='Use custom user agent')
parser.add_argument('-c', '--common-ports', action='store_true', help='Check all common webserver ports (seclist)')
parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose output (timeouts/errors)')
args = parser.parse_args()

# Response types
informational = '\033[34m'
successful = '\033[32m'
redirection = '\033[33m'
client_error = '\033[35m'
server_error = '\033[31m'
endc = '\033[m'

# Common http ports
ports = [66, 80, 81, 443, 445, 457, 1080, 1100, 1241, 1352, 1433, 1434, 1521,
         1944, 2301, 3000, 3128, 3306, 4000, 4001, 4002, 4100, 4443, 5000,
         5432, 5800, 5801, 5802, 6346, 6347, 7001, 7002, 8443, 8888, 30821]


# Https enumeration
def enum_https(target, timeout):
    # https
    https_fqdn = f'https://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(https_fqdn, allow_redirects=False, verify=False, timeout=timeout)
        if r.status_code in range(100, 199):
            print(f'{https_fqdn} [{informational}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(200, 299):
            print(f'{https_fqdn} [{successful}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(300, 399):
            print(f'{https_fqdn} [{redirection}{r.status_code}{endc}] {endc}({r.headers["server"]}) → {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{https_fqdn} [{client_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(500, 599):
            print(f'{https_fqdn} [{server_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if args.verbose is True:
            print(f'{https_fqdn} [{server_error}timeout{endc}]')
        else:
            pass
    except Exception as E:
        if args.verbose is True:
            print(f'{https_fqdn} [{server_error}error{endc}] [{server_error}{E}{endc}]')
        else:
            pass


# Http enumeration
def enum_http(target, timeout):
    # http
    http_fqdn = f'http://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(http_fqdn, allow_redirects=False, verify=False, timeout=timeout)
        if r.status_code in range(100, 199):
            print(f'{http_fqdn} [{informational}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(200, 299):
            print(f'{http_fqdn} [{successful}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(300, 399):
            print(f'{http_fqdn} [{redirection}{r.status_code}{endc}] {endc}({r.headers["server"]}) → {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{http_fqdn} [{client_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(500, 599):
            print(f'{http_fqdn} [{server_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if args.verbose is True:
            print(f'{http_fqdn} [{server_error}timeout{endc}]')
        else:
            pass
    except Exception as E:
        if args.verbose is True:
            print(f'{http_fqdn} [{server_error}error{endc}] [{server_error}{E}{endc}]')
        else:
            pass


if __name__ == '__main__':
    # Check Target
    if os.path.isfile(args.target) is False:
        if args.common:
            for port in ports:
                enum_https(f'{args.url}:{port}', args.timeout)
                enum_http(f'{args.url}:{port}', args.timeout)
        else:
            enum_https(args.url, args.timeout)
            enum_http(args.url, args.timeout)
    if os.path.isfile(args.target) is True:
        with args.url_file as file:
            targets = [x.strip() for x in file.readlines()]
            if args.common:
                for url in targets:
                    for port in ports:
                        enum_https(f'{url}:{port}', args.timeout)
                        enum_http(f'{url}:{port}', args.timeout)
            else:
                for url in targets:
                    enum_https(url, args.timeout)
                    enum_http(url, args.timeout)
    else:
        pass
