#!/usr/bin/env python3
#mangler.py ver 1
#mangler
#Author: Kashodin
import sys
import os
import subprocess
from sys import stdout

def usage():
	print("Usage: python mangler.py wordlist.txt")
	print("where 'wordlist.txt' is a file with all words to concat")


def main():
	words = []
	output = []
	if len(sys.argv) > 1:
		with open(sys.argv[1], 'r') as infile:
			for line in infile:
				words.append(line.strip())
			infile.close()
	
		for k in words:
			for j in words:
				if k == j:
					break
				curr = str(k)+':'+str(j)
				curr2 = str(j)+':'+str(k)
				if curr2 not in output:
					output.append(curr2)
				if curr not in output:
					output.append(curr)
				
	
		with open('manglees.txt', 'w') as outfile:
			for l in output:
				outfile.write(l)
				outfile.write('\n')

#		with open('mangle_out.txt', 'w') as finalout:
#			for x in output:
#				finalout.write(subprocess.check_output(['/opt/Hasher/hashes/__main__.py', '-C', '--hash-type', 'mysql323', '--hash', 'hashgoeshere', '--plaintext', str(x)]))
#				finalout.write('')

	else:
		usage()	



if __name__ == "__main__":
	main()