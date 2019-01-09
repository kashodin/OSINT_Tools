#!/usr/bin/env python3
#pingsweep.py ver 2.0
#Hostname -> IP address resolver  || IP -> hostname resolver
#Author: Kashodin
import sys
import os
import multiprocessing
import time
import socket
import re
import netaddr
from sys import stdout

def usage():
	print('\nUsage: "pingSweep.py *ip address range*"')
	print('Supported ip range formats are:')
	print("10.10.1.1-10.10.2.50")
	print("10.10.0.0/16")
	print('\nUsage: "pingSweep.py ip-list.txt')
	print('Usage: "pingSweep.py hostname-list.txt')



def getHost(ipaddress):
	print("...pinging "+str(ipaddress))
	socket.setdefaulttimeout(1)
	try:
		result = socket.gethostbyaddr(ipaddress)
	except (socket.herror):
		result = ("Offline","[]",str(ipaddress))
	return result

def getIP(hostname):
	print("...resolving "+str(hostname))
	try:
		result = (hostname, "[]", socket.gethostbyname(hostname))
	except socket.gaierror:
		result = (str(hostname), "[]", "Offline")
	return result

def do_the_thing(ip_list):
	pool_size = 255#multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=pool_size, )
	responses = pool.map(getHost, tuple(ip_list) )
	pool.close()
	pool.join()

	with open('ip_results.txt', 'w') as output:
		print("\n")
		for k in responses:
			if k[0] != "Offline":
				print(str(k[0])+": "+str(k[2]))
			output.write(str(k[0])+": "+str(k[2]).strip('[]\'')+'\n')

def do_hostnames(hostname_list):
	pool_size = 255#multiprocessing.cpu_count()
	pool = multiprocessing.Pool(processes=pool_size, )
	responses = pool.map(getIP, tuple(hostname_list) )
	pool.close()
	pool.join()

	with open('hostnames_results.txt', 'w') as output:
		print("\n")
		for k in responses:
			if k[2] != "Offline":
				print(str(k[0])+": "+str(k[2]))
			output.write(str(k[0])+": "+str(k[2])+'\n')

def main():
	ip_list = []
	hostname_list = []
	if len(sys.argv) > 1: #check there are cmdline args
		if str(sys.argv[1]) == 'ips-list.txt':
				with open(sys.argv[1], "r") as file:
					for line in file:
						ip_list.append(line.strip())
					file.close
				do_the_thing(ip_list)

		elif str(sys.argv[1]) == 'hostnames-list.txt':
			with open(sys.argv[1], "r") as ins:
				for line in ins:
					hostname_list.append(line.strip())
				ins.close
			do_hostnames(hostname_list)

		else:		
			reMatch = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])-(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$", sys.argv[1], re.M|re.I)
			if reMatch is not None:
				print("Passed a valid - range")
				start, end = reMatch.group().split("-")
				i = start.split(".")[3]
				while start != end:
					ip_list.append(start)
					one, two, three, four = start.split(".")
					if int(four) < 255:
						four = str(int(four)+1)
						start = one + "." + two + "." + three + "." + four
					else:
						four = "0"
						if int(three) < 255:
							three = str(int(three)+1)
							start = one + "." + two + "." + three + "." + four
						else:
							three = "0"
							if int(two) < 255:
								two = str(int(two)+1)
								start = one + "." + two + "." + three + "." + four
							else:
								two = "0"
								if int(one) < 255:
									one = str(int(one)+1)
									start = one + "." + two + "." + three + "." + four

				ip_list.append(end)
				do_the_thing(ip_list)
				

			else:
				reMatch = re.match("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])/(3[012]|[12][0-9]|[1-9])$", sys.argv[1], re.M|re.I)
				if reMatch is not None:
					print("Passed a valid /range")
					network = reMatch.group()
					ip_list = netaddr.IPNetwork(network)
					do_the_thing(ip_list)
					
				else:
					usage()
	else:
		usage()




if __name__ == "__main__":
	main()