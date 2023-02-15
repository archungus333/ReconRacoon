# IMPORT
import datetime

# COLORS
endc = '\033[m'
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
purple = '\033[35m'
cyan = '\033[36m'
white = '\033[37m'

# TS
now = datetime.datetime.now()
cd = now.strftime("%D")
ct = now.strftime("%H:%M:%S")

# ASCII
racoon = rf'''┌───────────────────────────────────────────┐
│ DT: {cd}           ,,,                │
│ TS: {ct}        .'    `/\_/\          │
│                   .'       <@I@>          │
│        <((((((((((  )____(  \./           │
│                   \( \(   \(\(            │
│ {yellow}Recon{purple}Racoon{endc}        `-"`-"  " "            │
└───────────────────────────────────────────┘'''
