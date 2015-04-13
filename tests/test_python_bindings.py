import unittest
import sys
import os
import math

testdir = os.path.dirname(__file__)
moduledir = '../'
modulepath = os.path.abspath(os.path.join(testdir, moduledir))
sys.path.insert(0, modulepath)

import Shape
Shape.Config.set_library_path(modulepath)

class TestPythonBindings(unittest.TestCase):
  def test_Shape_Circle_is_called_Circle(self):
    radius = 2.0

    c = Shape.Circle(radius)
    
    self.assertEqual("Circle", c.name())

  def test_Shape_Circle_has_expected_area(self):
    radius = 2.0
    area = radius * radius * math.pi

    c = Shape.Circle(radius)
    
    self.assertAlmostEqual(area, c.area())

  def test_Shape_Circle_has_expected_perimeter(self):
    radius = 2.0
    perimeter = 2.0 * math.pi * radius

    c = Shape.Circle(radius)
    
    self.assertAlmostEqual(perimeter, c.perimeter())

def main():
  unittest.main()

if __name__ == '__main__':
  main()

