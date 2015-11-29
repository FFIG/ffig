import unittest
import sys
import os
import math

testdir = os.path.dirname(__file__)
moduledir = '../output'
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

  def test_Shape_Circle_is_equal_to_self(self):
    self.assertTrue(self.circle.is_equal(self.circle))

  def test_Shape_Circle_is_equal_to_circle_with_same_radius(self):
    self.assertTrue(self.circle.is_equal(Shape.Circle(self.radius)))
  
  def test_Shape_Circle_is_not_equal_to_circle_with_different_radius(self):
    self.assertFalse (self.circle.is_equal(Shape.Circle(self.radius+1)))
  
  def test_Shape_Circle_is_not_equal_to_square(self):
    self.assertFalse(self.circle.is_equal(Shape.Square(4)))

  def test_exception_on_negative_radius(self):
    with self.assertRaisesRegexp(Shape.Shape_error, 'Circle radius "-1" cannot be negative.'):
      Shape.Circle(-1)

def main():
  unittest.main()

if __name__ == '__main__':
  main()

