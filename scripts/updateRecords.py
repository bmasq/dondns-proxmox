"""
NOTICE: The "dondns.sh" script and "dondns.conf" file are products of
Soluciones Corporativas IP, S.L. and are available under the GNU Lesser
General Public License v3.0. These files, originally named "dondomcli.sh"
and "dondomcli.conf," along with their documentation and source code, can
be found on the official repository at https://github.com/dondominio/
dondns-bash.git. The author can be contacted at info@dondominio.com or
through the website dondominio.com. Copyright © 2023 Soluciones
Corporativas IP, S.L.
"""

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
    exit(1)
except ValueError:
    sys.stderr.write("ERROR: bad format for delay time")
    exit(1)


# run as daemon
while True:
    filename = "IDs-hostnames.json"
    ctdict = dict()
    try:
        with open(filename, "r") as f:
            ctdict = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: The file {filename} could not be found.")
        exit(1)
    except json.decoder.JSONDecodeError:
        print(f"ERROR: The file {filename} is not a valid JSON file.")
        exit(1)
    except PermissionError:
        print(f"ERROR: You do not have permission to access the file {filename}.")
        exit(1)
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while opening and reading the file {filename}:", e)
        exit(1)

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