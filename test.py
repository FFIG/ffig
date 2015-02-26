#!/usr/bin/env python
import trace
import sys
sys.path.insert(0,'.')
from Shape import *

c = Circle(10)
print("Circle(10).area() = {}".format(c.area()))

