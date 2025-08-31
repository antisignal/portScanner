#%%
import csv
import errno
#%%
import pandas as pd
#%%
import socket
#%%
from enum import Enum
#%%
csvpath = "/home/alex/Downloads/service-names-port-numbers.csv"
#%%
f = open(csvpath)
#%%
csv_reader = csv.DictReader(f)
#%%
class PortData:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
#%%
portsToScan = {}
#%%
for row in csv_reader:
    try:
        int(row['Port Number'])
    except:
        continue
    if row['Transport Protocol'] == "tcp":
        print(row["Service Name"])
        portDataEntry = PortData(
            row['Service Name'],
            row['Description'],
        )
        if int(row["Port Number"]) <= 1024:
            portsToScan[int(row['Port Number'])] = portDataEntry

#%%
HOST = "127.0.0.1"
PORT = 0

#%%
TARGET = "45.33.32.156"
# TARGET = "127.0.0.1"
#%%
portResults = {}
#%%
class Result(Enum):
    OPEN = 1
    CLOSED = 2
    FILTERED = 3
    UNKNOWN = 4
#%% md
# 
#%%
for port in portsToScan:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    # s.bind((HOST, PORT))
    try:
        s.connect((TARGET, int(port)))
        portResults[port] = Result.OPEN
        s.shutdown(socket.SHUT_RDWR)
    except TimeoutError as e:
        print("port", port, "filtered:", e)
        portResults[port] = Result.FILTERED
        continue
    except OSError as e:
        if e.errno == errno.ECONNREFUSED:
            portResults[port] = Result.CLOSED
            continue
        if e.errno == errno.EINVAL:
            print("invalid input: ", e)
        else:
            print(e)
        portResults[port] = Result.FILTERED
        continue
    except:
        portResults[port] = Result.UNKNOWN
#%%
print(portResults)
#%%
for k in portResults:
    if portResults[k] == Result.OPEN or portResults[k] == Result.FILTERED:
        name = portsToScan[k].name
        desc = portsToScan[k].desc
        rawStatus = portResults[k]
        status = ""
        if rawStatus == Result.FILTERED:
            status = "filtered"
        if rawStatus == Result.OPEN:
            status = "open"
        print(k, name, desc, status)
#%%
scanData = {}
scanData["Port Number"] = [k for k in portResults if portResults[k] == Result.OPEN or portResults[k] == Result.FILTERED]
scanData["Service"] = [portsToScan[k].name for k in portResults if portResults[k] == Result.OPEN or portResults[k] == Result.FILTERED]
scanData["Description"] = [portsToScan[k].desc for k in portResults if portResults[k] == Result.OPEN or portResults[k] == Result.FILTERED]
scanData["Result"] = [portResults[k] for k in portResults if portResults[k] == Result.OPEN or portResults[k] == Result.FILTERED]
#%%
df = pd.DataFrame(scanData)
#%%
print(df)