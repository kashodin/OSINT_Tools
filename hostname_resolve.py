#!/usr/bin/env python3
#Hostname -> IP address script Ver. 1.0.0
#Kashodin

import sys
import os
import socket
import netaddr
from sys import stdout


def main():
	failed = []
	if len(sys.argv) > 1:
		with open(sys.argv[1], "r") as ins:
			for line in ins:
				try:
					print(str(line.strip())+" = "+str(socket.gethostbyname(line.strip())))
				except socket.gaierror:
					failed.append(line.strip())
		print("The following hostnames could not resolve:")
		for k in failed:
			print(k)
	else:
		print("Run with single cmd line arg, that is the name of the hostname file")
		print("Hostname file formatted with single hostname per line")



if __name__ == "__main__":
	main()