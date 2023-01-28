from classes import Container
import json
import subprocess

filename = "CTsVMs.json"
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

containers = list()
for id, hostname in ctdict.items():
    try:
        call = subprocess.run(["pct", "config", id],
                              capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"ERROR: code {e.returncode}: {e.stderr}")
        continue
    containers.append(Container(id, hostname, call.stdout))

for ct in containers:
    print("id:", ct.id)
    print("hn:", ct.hostname)
    print("ip:", ct.ip)