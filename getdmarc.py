#!/usr/bin/python

# The purpose of this code is to take an argument of a domain, query the TXT records and break down any DMARC records that are found
# This is my first real attempt at python code and so the semantics are probably a joke as I am still learning how python works
# The code will be used to query DMARC records 

import sys
import getopt
import dns.resolver
from collections import deque

# Usage: getdmarc.py --domain=<domain>
# At the end of the processing, the domain variable will be set to the argument
options, args = getopt.getopt(sys.argv[1:], "domain:", ['domain='])
domain = ""
for o, a in options:
	if o in ("--domain"):
		domain = a

if not domain:
	print "no domain specified"
	print "Usage: getdmarc.py --domain=<domain>"
	sys.exit()
	
# This is where the DNS query happens and any exceptions are handled
# Prepend _dmarc to the passed domain name
query = "%s.%s" % ('_dmarc', domain)

try:
	answers = dns.resolver.query(query, 'TXT')
except (dns.resolver.NoAnswer):
	print "Could not find TXT records for %s" % domain
	sys.exit()
except (dns.resolver.NXDOMAIN):
	print "Could not find domain: %s" % domain
	sys.exit()

# Process the TXT records 
# - Check if record contains DMARC
# - Break down the elements
print "DMARC report for %s\n" % domain
for rdata in answers:
	for txt in rdata.strings:
		(version, policy, aggregate_report, full_report) = deque(txt.split("; "))
		print version
		print policy
		print aggregate_report
		print full_report

