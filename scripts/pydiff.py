#!/usr/bin/env python

import difflib
import sys
import os

filename1 = os.path.abspath(sys.argv[1])
filename2 = os.path.abspath(sys.argv[2])

with open(filename1) as i:
    first = i.readlines()

with open(filename2) as i:
    second = i.readlines()

diff = [x for x in difflib.unified_diff(first, second)]

if len(diff) != 0:
    print("{} and {} are different".format(filename1, filename2))
    for line in diff:
        print(line)

if len(diff) != 0:
    sys.exit(-1)
