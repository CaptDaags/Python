

# Definately ripped from the intertubes - My only contrib slimming it down to Windows
# Quick and nasty for a bit of sysadmin I was doing.

import sys
import os
# import platform
import subprocess
 
# plat = platform.system()
scriptDir = sys.path[0]
hosts = os.path.join(scriptDir, 'hosts.txt')
hostsFile = open(hosts, "r")
lines = hostsFile.readlines()
#if plat == "Windows":
for line in lines:
    line = line.strip( )
    ping = subprocess.Popen(
        ["ping", "-n", "1", "-l", "1", "-w", "100", line],
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE
    )
    out, error = ping.communicate()
    print (out)
    print (error)

# if plat == "Linux":
#     for line in lines:
#         line = line.strip( )
#         ping = subprocess.Popen(
#             ["ping", "-c", "1", "-l", "1", "-s", "1", "-W", "1", line],
#             stdout = subprocess.PIPE,
#             stderr = subprocess.PIPE
#         )
#         out, error = ping.communicate()
#         print out
#         print error

hostsFile.close()