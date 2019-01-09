#!/usr/bin/env python3
#sd_discover ver. 1.0
#takes a list of TLD's and finds all subdomains
#Author: Kashodin
import sys
import os
import sublist3r
from sys import stdout


def usage():
	print('\nUsage: "python3 sublist_discover.py tld.txt"')
	print('supplied file must be named "tld.txt"')
	print('and contain one tld per line, duplicates handled')



#sublist3r usage notes:
	#subdomains = sublist3r.main(domain, no_threads, savefile, ports, silent, verbose, enable_bruteforce, engines)
	#subdomains = sublist3r.main('yahoo.com', 40, 'yahoo_subdomains.txt', ports= None, silent=False, verbose= False, enable_bruteforce= False, engines=None)
def get_subs(tld_list, sub_list, verbose_toggle, brute_toggle, ports_list=None):
	for tld in tld_list:
		savefile = "sd_discover_"+str(tld)+".txt"
		subdomains = sublist3r.main(tld, 40, savefile, ports=ports_list, silent=False, verbose= verbose_toggle, enable_bruteforce=brute_toggle, engines=None)
		for line in subdomains:
			if line.strip() not in sub_list:
				sub_list.append(line.strip())
	
	print('\nTotal unique subdomains: '+str(len(sub_list)))
	with open('sd_discover_results.txt', 'w') as output:
		for k in sub_list:
			output.write(str(k))
			if verbose_toggle:
				print(k)
	print('\nResults saved to "sd_discover_results.txt"')





def main():
	tld_list = []
	sub_list = []
	ports_list = []
	verbose_toggle = False
	brute_toggle = False
	pscan = False
	if len(sys.argv) > 1: #check there are cmdline args
		if str(sys.argv[1]) == 'tld.txt': #check the file contains tlds (dupes are fine)
				with open(sys.argv[1], "r") as file: #build internal python list free of dups
					for line in file:
						if line.strip() not in tld_list:
							tld_list.append(line.strip())
					file.close

		temp = input('Verbose mode?  (Y/N)')
		if temp == 'Y' or temp == 'y':
			verbose_toggle = True

		temp = input('Run subbrute for discovery?  (Y/N)\n**increases run duration drastically**')
		if temp == 'Y' or temp == 'y':
			brute_toggle = True

		temp = input('Port scan subdomains?  (Y/N)\n**will be able to specify which ports next**')
		if temp == 'Y' or temp == 'y':
			pscan = True

		if pscan:
			port = input('port to add to scan list(enter nothing to end adding ports): ')
			ports_list.append(port)
			while port is not '':
				port = input('port to add to scan list(enter nothing to end adding ports): ')
				if port is not '':
					ports_list.append(port)

			get_subs(tld_list, sub_list, verbose_toggle, brute_toggle, ports_list)
		else:
			get_subs(tld_list, sub_list, verbose_toggle, brute_toggle)
	else:
		usage()


if __name__ == "__main__":
	main()