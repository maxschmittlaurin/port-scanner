# Author : Maximilien Schmitt-Laurin


# This is a simple port scanner that detects which ports are open and which ones are close/filtered.
# This script uses the socket api to see if you can connect to a port on a specified ip address. 
# Once you've successfully connected a port is seen as open.
# This script does not discriminate the difference between filtered and closed ports.



# The socket module in Python is an interface to the Berkeley sockets API.
import socket

# We need to create regular expressions to ensure that the input is correctly formatted.
import re

import subprocess
import sys
from datetime import datetime

# Regular Expression Pattern to recognise IPv4 addresses.

ip_address_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")


# Regular Expression Pattern to extract the number of ports you want to scan. 
# You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)

port_range_pattern = re.compile("([0-9]+)-([0-9]+)")


# Initialising the port numbers, will be using the variables later on.

port_min = 0
port_max = 65535

open_ports = []


# Blank the screen.

subprocess.call('cls', shell=True)


# Ask user to input the IP address they want to scan.

while True:

    ip_address_entered = input("\n Enter the IP address of a remote host to scan :  ")

    if ip_address_pattern.search(ip_address_entered):

        print(f"\n {ip_address_entered} is a valid IP address.\n")
        break

    else:
        print(f"\n {ip_address_entered} is not a valid IP address.\n")


# Ask user to input the range of ports to scan.

while True:

    # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all 
    # the ports is not advised.

    print("\n Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
    
    port_range = input("\n Enter port range: ")

    port_range_valid = port_range_pattern.search(port_range.replace(" ",""))

    if port_range_valid:

        port_min = int(port_range_valid.group(1))
        port_max = int(port_range_valid.group(2))
        break


# Print a nice banner with information on which host are we about to scan.

print("")
print("_" * 60)
print(" Please wait, scanning remote host...", ip_address_entered)
print("_" * 60)
print("")

# Check the date and time the scan was started.

scanStartTime = datetime.now()


# Basic socket port scanning

for port in range(port_min, port_max + 1):

    # Connect to socket of target machine. We need the IP address and the port number we want to connect to.
    
    try:

        # Create a socket object.

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            # We want to set a timeout for the socket to try and connect to the server.

            s.settimeout(0.5)

            # We use the socket object we created to connect to the IP address we entered 
            # and the port number. If it can't connect to this socket it will cause an 
            # exception and the open_ports list will not append the value.

            s.connect((ip_address_entered, port))


            # If the following line runs then then it was successful in connecting to the port.
            
            open_ports.append(port)

            print(f" Port {port}:      Open")

            s.close()
            

    except:

        print(f" Port {port}:      Close or Filtered")


# Check the date and time again.

scanEndTime = datetime.now()


# Calculate the difference in time to know how long the scan took.

totalScanTime = scanEndTime - scanStartTime


# Printing the information on the screen.

print(f"\n Scanning completed in : {totalScanTime} \n")

for port in open_ports:

    # We use an f string to easily format the string with variables so we don't have to do concatenation.
    print(f" Port {port} is open on {ip_address_entered}.")

print("")