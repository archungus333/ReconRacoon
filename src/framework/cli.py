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
current_time = now.strftime("%H:%M:%S")
current_date = now.strftime("%D")

# ASCII
racoon = rf'''┌───────────────────────────────────────────┐
│ DT: {current_date}           ,,,                │
│ TS: {current_time}        .'    `/\_/\          │
│                   .'       <@I@>          │
│        <((((((((((  )____(  \./           │
│                   \( \(   \(\(            │
│ {yellow}Recon{purple}Racoon{endc}        `-"`-"  " "            │
└───────────────────────────────────────────┘'''
