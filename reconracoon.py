# IMPORT
import sys
from os import listdir
from os.path import isfile, join
# IMPORT SRC
from bin.framework import cli
from bin.modules import enum
from bin.modules import resolve

# BANNER
print(cli.racoon)
# ARGS
args = sys.argv
# MODULES
modules = [f.strip(".py") for f in listdir('bin/modules') if isfile(join('bin/modules', f))]

# MAIN
try:
    if args[1] in modules:
        print(f"{cli.green}[+]{cli.endc} Selected: {args[1]}")
        selected = getattr(sys.modules[__name__], args[1])
        selected.init()
    else:
        print(f"{cli.red}[x]{cli.endc} Selected module doesn't exist: '{args[1]}'")
        for mod in modules:
            print(f'[{cli.purple}>{cli.endc}] {mod}')
except IndexError:
    print(f'{cli.yellow}[?]{cli.endc} Please Select Module:')
    for mod in modules:
        print(f'[{cli.purple}>{cli.endc}] {mod}')
    sys.exit()
