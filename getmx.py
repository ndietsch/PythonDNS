#!/usr/bin/python

import dns.resolver
import sys
import getopt

options, args = getopt.getopt(sys.argv[1:], "domain:", ['domain='])

for o, a in options:
	if o in ("--domain"):
		domain = a

	
answers = dns.resolver.query(domain, 'MX')
for rdata in answers:
    print rdata

