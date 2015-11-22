#!/usr/bin/env python
from Shape import *
c = Circle(1)
print c.area()

try:
    c = Circle(-8)
except Exception as e:
    print e

