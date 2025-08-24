# This is the first iteration of the Python attempt at creating a port scanner.
# It will have the following features:
# - accept a host to target via the command line
# - scan every port from 1 to 1024
# - flag ports as open, closed, or filtered

# It will later scan ports concurrently (in Go likely)
# and have options for more stealthy scans, e.g. SYN scans.

import socket

def main():
    for i in range(1, 1024):


if __name__ == '__main__':
    main()