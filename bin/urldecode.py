#!/usr/bin/env python
import sys
import urllib as ul
if not sys.stdin.isatty():
    string=sys.stdin.read()
else:
    print('expecting stdin')
    sys.exit(-1)
print ul.unquote_plus(string)

