#!/usr/bin/python3

from container import Container
from time import sleep
import json
import subprocess
import sys

# time between updates
try:
    delay = int(sys.argv[1])
    if not delay > 0:
        raise ValueError
except IndexError:
    sys.stderr.write("ERROR: no delay time specified")
except ValueError:
    sys.stderr.write("ERROR: bad format for delay time")

# run as daemon
while True:
    filename = "IDs-hostnames.json"
    try:
        with open(filename, "r") as f:
            ctdict = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: The file {filename} could not be found.")
    except json.decoder.JSONDecodeError:
        print(f"ERROR: The file {filename} is not a valid JSON file.")
    except PermissionError:
        print(f"ERROR: You do not have permission to access the file {filename}.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while opening and reading the file {filename}:", e)

    # creates Containers from "pct config" output
    containers = list()
    for id, hostname in ctdict.items():
        try:
            call = subprocess.run(["pct", "config", id],
                                capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: code {e.returncode}: {e.stderr}")
            continue
        containers.append(Container(id, hostname, call.stdout))

    # updates DNS record on DonDominio for each container
    for ct in containers:
        command = ["dondns/dondns.sh", "-c", "dondns/dondns.conf",
                    "-h", ct.hostname, "-i", ct.ip]
        try:
            call = subprocess.run(command, capture_output=True, text=True, check=True)
            output = call.stdout.replace('\n', ' ')
            print(f"{ct.hostname} ({ct.id}):  {output}")
        except subprocess.CalledProcessError as e:
            print(f"ERROR for {ct.hostname} ({ct.id}): code {e.returncode}: {e.stderr}")
            continue

    sleep(delay)