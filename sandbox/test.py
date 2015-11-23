#!/usr/bin/env python

import numpy as np
from Shape import *
import unittest

class TestExceptionPoC(unittest.TestCase):
    
    def test_circle_construction(self):
        r = 1
        c = Circle(r)

    def test_area(self):
        r = 2
        c = Circle(r)
        self.assertAlmostEqual(c.area(), np.pi * r * r) 
    
    def test_perimeter(self):
        r = 2
        c = Circle(r)
        self.assertAlmostEqual(c.perimeter(), 2 * np.pi * r) 
    
    def test_name(self):
        r = 2
        c = Circle(r)
        self.assertEqual(c.name(), "Circle") 
    
    def test_equality(self):
        c1 = Circle(1)
        c1_ = Circle(1)
        c2 = Circle(2)
        self.assertTrue(c1.is_equal(c1)) 
        self.assertTrue(c1.is_equal(c1_)) 
        self.assertTrue(c1_.is_equal(c1)) 
        self.assertFalse(c1.is_equal(c2)) 
        self.assertFalse(c2.is_equal(c1)) 
    
    def test_exception_on_negative_radius(self):
        with self.assertRaisesRegexp(Shape_error, 'Circle radius "-1" cannot be negative'):
            Circle(-1)

if __name__ == "__main__":
    unittest.main()
