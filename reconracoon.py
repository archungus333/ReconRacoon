import datetime
import os
import requests
import argparse
import datetime
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.adapters.DEFAULT_RETRIES = 100

# Response types
informational = '\033[34m'
successful = '\033[32m'
redirection = '\033[33m'
client_error = '\033[35m'
server_error = '\033[31m'
endc = '\033[m'

# Timstamp
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%D")

# Ascii banner
racoon = rf'''┌───────────────────────────────────────────┐
│ DT: {current_date}           ,,,                │
│ TS: {current_time}        .'    `/\_/\          │
│                   .'       <@I@>          │
│        <((((((((((  )____(  \./           │
│                   \( \(   \(\(            │
│ {redirection}Recon{client_error}Racoon{endc}        `-"`-"  " "            │
└───────────────────────────────────────────┘'''
print(racoon)

# Argparse
parser = argparse.ArgumentParser(prog='ReconRacoon', description='Extensive Enumeration of Multiple Subdomains')
parser.add_argument('-t', '--target', dest='target', type=str, required=True, help='Target subdomains or IPs (str/file)')
parser.add_argument('-d', '--delay', dest='timeout', type=float, default=1.0, help='Timeout for all web requests')
parser.add_argument('-u', '--user-agent', dest='user_agent', default='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36', type=str, help='Use custom user agent')
parser.add_argument('-c', '--common-ports', action='store_true', help='Check all common webserver ports (seclist)')
parser.add_argument('-r', '--robots', action='store_true', help='Saves the robots.txt of each target in a folder (robots/)')
parser.add_argument('-v', '--verbose', action='store_true', help='Display verbose output (timeouts/errors)')
#parser.add_argument('-s', '--screenshot', action='store_true', help='Takes a screenshot of the webpage and stores it in screenshots/')
args = parser.parse_args()

# Common http ports
ports = [66, 80, 81, 443, 445, 457, 1080, 1100, 1241, 1352, 1433, 1434, 1521,
         1944, 2301, 3000, 3128, 3306, 4000, 4001, 4002, 4100, 4443, 5000,
         5432, 5800, 5801, 5802, 6346, 6347, 7001, 7002, 8443, 8888, 30821]


# Https enumeration
def enum_https(target, timeout, headers):
    # https
    https_fqdn = f'https://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(https_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
        if r.status_code in range(100, 199):
            print(f'{informational}INFO{endc} - {https_fqdn} [{informational}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(200, 299):
            print(f'{successful}SUCCESS{endc} - {https_fqdn} [{successful}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(300, 399):
            print(f'{redirection}REDIRECTION{endc} - {https_fqdn} [{redirection}{r.status_code}{endc}] {endc}({r.headers["server"]}) {redirection}→{endc} {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{client_error}CLIENT_ERROR{endc} - {https_fqdn} [{client_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(500, 599):
            print(f'{server_error}SERVER_ERROR{endc} - {https_fqdn} [{server_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if args.verbose is True:
            print(f'{server_error}TIMEOUT{endc} - {https_fqdn} [{server_error}after {timeout}/s {endc}]')
        else:
            pass
    except Exception as E:
        if args.verbose is True:
            print(f'{server_error}ERROR{endc} - {https_fqdn} [{server_error}{E}{endc}]')
        else:
            pass


# Http enumeration
def enum_http(target, timeout, headers):
    # http
    http_fqdn = f'http://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    try:
        r = sesh.get(http_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
        if r.status_code in range(100, 199):
            print(f'{informational}INFO{endc} - {http_fqdn}[{informational}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(200, 299):
            print(f'{successful}SUCCESS{endc} - {http_fqdn} [{successful}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(300, 399):
            print(f'{redirection}REDIRECTION{endc} - {http_fqdn} [{redirection}{r.status_code}{endc}] {endc}({r.headers["server"]}) {redirection}→{endc} {r.headers["location"]}')
        elif r.status_code in range(400, 499):
            print(f'{client_error}CLIENT_ERROR{endc} - {http_fqdn} [{client_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        elif r.status_code in range(500, 599):
            print(f'{server_error}SERVER_ERROR{endc} - {http_fqdn} [{server_error}{r.status_code}{endc}] {endc}({r.headers["server"]})')
        else:
            pass
    except requests.exceptions.ConnectTimeout:
        if args.verbose is True:
            print(f'{server_error}TIMEOUT{endc} - {http_fqdn} [{server_error}after {timeout}/s {endc}]')
        else:
            pass
    except Exception as E:
        if args.verbose is True:
            print(f'{server_error}ERROR{endc} - {http_fqdn} [{server_error}{E}{endc}]')
        else:
            pass


def enum_robots(target, timeout, headers):
    #download robots.txt
    http_fqdn = f'http://{target}'
    https_fqdn = f'https://{target}'
    sesh = requests.session()
    sesh.keep_alive = False
    if args.robots:
        try:
            r = sesh.get(http_fqdn, allow_redirects=False, verify=False, timeout=timeout, headers=headers)
            if r.status_code in range(200, 299):
                robo = f'{http_fqdn}/robots.txt'
                robo = requests.get(robo, allow_redirects=False)
                if not os.path.exists('robots'):
                    os.makedirs('robots')
                open(f'robots/HTTP_{target}.txt', 'wb').write(robo.content)
            elif r.status_code in range(300, 399):
                robo = f'{https_fqdn}/robots.txt'
                robo = requests.get(robo, allow_redirects=False)
                if not os.path.exists('robots'):
                    os.makedirs('robots')
                open(f'robots/HTTPS_{target}.txt', 'wb').write(robo.content)
        except requests.exceptions.ConnectTimeout:
            if args.verbose is True:
                print(f'{server_error}TIMEOUT{endc} - {http_fqdn} [{server_error}after {timeout}/s {endc}]')
            else:
                pass
        except Exception as E:
            if args.verbose is True:
                print(f'{server_error}ERROR{endc} - {http_fqdn} [{server_error}{E}{endc}]')
            else:
                pass
    else:
        pass


if __name__ == '__main__':
    # Var
    if args.user_agent:
        agent = {'User-Agent': args.user_agent}
    # Check Target
    try:
        if os.path.isfile(args.target) is False:
            if args.common_ports:
                for port in ports:
                    enum_https(f'{args.target}:{port}', args.timeout, {'User-Agent': args.user_agent})
                    enum_http(f'{args.target}:{port}', args.timeout, {'User-Agent': args.user_agent})
                    enum_robots(args.target, args.timeout, {'User-Agent': args.user_agent})
            else:
                enum_https(args.target, args.timeout, {'User-Agent': args.user_agent})
                enum_http(args.target, args.timeout, {'User-Agent': args.user_agent})
                enum_robots(args.target, args.timeout, {'User-Agent': args.user_agent})
        if os.path.isfile(args.target) is True:
            with open(args.target) as file:
                targets = [x.strip() for x in file.readlines()]
                if args.common_ports:
                    for url in targets:
                        for port in ports:
                            enum_https(f'{url}:{port}', args.timeout, {'User-Agent': args.user_agent})
                            enum_http(f'{url}:{port}', args.timeout, {'User-Agent': args.user_agent})
                            enum_robots(url, args.timeout, {'User-Agent': args.user_agent})
                else:
                    for url in targets:
                        enum_https(url, args.timeout, {'User-Agent': args.user_agent})
                        enum_http(url, args.timeout, {'User-Agent': args.user_agent})
                        enum_robots(url, args.timeout, {'User-Agent': args.user_agent})
        else:
            pass
    except KeyboardInterrupt:
        print(f'{server_error} leaving..{endc}')
        exit()
