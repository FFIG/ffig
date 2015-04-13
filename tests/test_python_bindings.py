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
  def setUp(self):
    self.radius = 3.0
    self.circle = Shape.Circle(self.radius)

  def tearDown(self):
    del self.circle
  
  def test_Shape_Circle_is_called_Circle(self):
    self.assertEqual("Circle", self.circle.name())

  def test_Shape_Circle_has_expected_area(self):
    area = self.radius * self.radius * math.pi
    
    self.assertAlmostEqual(area, self.circle.area())

  def test_Shape_Circle_has_expected_perimeter(self):
    perimeter = 2.0 * math.pi * self.radius
    
    self.assertAlmostEqual(perimeter, self.circle.perimeter())

def main():
  unittest.main()

if __name__ == '__main__':
  main()

