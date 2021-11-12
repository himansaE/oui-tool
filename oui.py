#!/usr/bin/python3

import subprocess
import re
import sys
from os import path

if(len(sys.argv) == 1):
    print("\nusage:  oui.py <MAC Address>")
    exit()

arg = str(sys.argv[1])

mac = ""
matched = False
if(re.match(r"^(?:[A-z0-9]{2}[:-]){5}[A-z0-9]{2}$", arg) != None):
    matched = True
    mac = "".join(re.split("-|:", arg)[:3])

if(re.match(r"^[0-9A-z]{6}$", arg) != None):
    matched = True
    mac = arg

if(matched == False):
    print("Invalid MAC Address.")
    exit()

mac = mac.upper()

oui_files = subprocess.check_output(["locate", "oui.txt"])
oui_files = [i for i in (oui_files.decode().split('\n')) if i]

if(len(oui_files) == 0):
    print("\nNo oui.txt found on  'locate oui.txt' . ")
    exit(2)

found = []
for file in oui_files:
    if(path.isfile(file)):
        try:
            out = subprocess.check_output(
                ["grep", mac, "-i", file]).decode()
            reg = re.findall(r"\w+\s*(?:\(.+\))?\s*(.+)", out)
            found.append(reg[0])
        except:
            pass
found = set(found)
if(len(found) == 0):
    print('No record found.')
    exit(1)
for i in set(found):
    print("\n", mac, "-", i)
