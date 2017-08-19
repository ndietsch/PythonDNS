#!/usr/bin/python

# The purpose of this code is to take an argument of a domain, query the TXT records and break down any SPF records that are found
# This is my first real attempt at python code and so the semantics are probably a joke as I am still learning how python works
# The code will be used to query SPF records 

import sys
import getopt
import dns.resolver
from collections import deque

# Usage: getspf.py --domain=<domain>
# At the end of the processing, the domain variable will be set to the argument
options, args = getopt.getopt(sys.argv[1:], "domain:", ['domain='])
domain = ""
for o, a in options:
	if o in ("--domain"):
		domain = a

if not domain:
	print "no domain specified"
	print "Usage: getspf.py --domain=<domain>"
	sys.exit()
	
# This is where the DNS query happens and any exceptions are handled
try:
	answers = dns.resolver.query(domain, 'TXT')
except (dns.resolver.NoAnswer):
	print "Could not find TXT records for %s" % domain
	sys.exit()
except (dns.resolver.NXDOMAIN):
	print "Could not find domain: %s" % domain
	sys.exit()

# Process the TXT records 
# - Check if record contains spf
# - Break down the elements of the record into the version, the catcher and any elements
print "SPF report for %s\n" % domain
for rdata in answers:
	for txt in rdata.strings:
		if 'v=spf' in txt:
			array = deque(txt.split(" "))
			version = array.popleft()
			catcher = array.pop()
			print "-Version: %s" % version
			print "-Restriction: %s" % catcher
			for element in array:
				print "--Element: %s" % element
			sys.exit()

