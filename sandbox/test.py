#!/usr/bin/env python

import numpy as np
from Shape import *
import unittest

class TestExceptionPoC(unittest.TestCase):
    
    def test_correct_construction(self):
        c = Circle(1)
        self.assertAlmostEqual(c.area(), np.pi) 

    def test_exception_on_negative_radius(self):
        with self.assertRaisesRegexp(Shape_error, 'Circle radius "-1" cannot be negative'):
            Circle(-1)

if __name__ == "__main__":
    unittest.main()
