import sys
import os
import math
import nose
import Shape

if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path manually.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = script_dir + '/../output'
    Shape.Config.set_library_path(output_dir)

def test_Shape_Circle_is_called_Circle():
    c = Shape.Circle(3)
    assert c.name() == "Circle"


def test_Shape_Circle_has_expected_area():
    r = 2.0
    c = Shape.Circle(r)
    a = math.pi * r * r
    print a
    print c.area()
    nose.tools.assert_almost_equal(c.area(), a)


def test_Shape_Circle_has_expected_perimeter():
    r = 2.0
    c = Shape.Circle(r)
    p = 2.0 * math.pi * r
    nose.tools.assert_almost_equal(c.perimeter(), p)


def test_Shape_Circle_is_equal_to_itself():
    c = Shape.Circle(2)
    assert c.is_equal(c)


def test_Shape_Circle_is_equal_to_another_circle_with_the_same_radius():
    c1 = Shape.Circle(2)
    c2 = Shape.Circle(2)
    assert c1.is_equal(c2)


def test_Shape_Circle_is_not_equal_to_circle_with_different_radius():
    c1 = Shape.Circle(2)
    c2 = Shape.Circle(3)
    assert not c1.is_equal(c2)

def test_Shape_Circle_is_not_equal_to_square():
    c = Shape.Circle(2)
    s = Shape.Square(2)
    assert not c.is_equal(s)


@nose.tools.raises(Exception)
def test_exception_on_negative_radius():
    Shape.Circle(-1)

