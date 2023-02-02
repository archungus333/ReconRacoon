# ReconRacoon
![Supported Python versions](https://img.shields.io/badge/python-3.7+-blue.svg)

```
                        ,,,
                     .'    `/\_/\
                   .'       <@I@>
        <((((((((((  )____(  \./
                   \( \(   \(\(
   ReconRacoon      `-"`-"  " "

Just some 1337 Racoon digging through other peoples trash bins.
```

## Features
- Response code enumeration of domains & IPs
- Common webserver port check via seclists
- Simple information header analysis
                        

```
usage: ReconRacoon [-h] -t TARGET [-d TIMEOUT] [-u USER_AGENT] [-c] [-v]

Extensive Enumeration of Multiple Subdomains

options:
  -h, --help            show this help message and exit
  -t TARGET, --target TARGET
                        Target subdomains or IPs (str/file)
  -d TIMEOUT, --delay TIMEOUT
                        Timeout for all web requests
  -u USER_AGENT, --user-agent USER_AGENT
                        Use custom user agent
  -c, --common-ports    Check all common webserver ports (seclist)
  -v, --verbose         Display verbose output (timeouts/errors)
```
