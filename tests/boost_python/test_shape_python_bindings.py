import math
import nose
import Shape_py as shape


def test_shape_Circle_is_called_Circle():
    c = shape.Circle(3)
    assert c.name == "Circle"


def test_shape_Circle_has_expected_area():
    r = 2.0
    c = shape.Circle(r)
    a = math.pi * r * r
    nose.tools.assert_almost_equal(c.area, a)


def test_shape_Circle_has_expected_perimeter():
    r = 2.0
    c = shape.Circle(r)
    p = 2.0 * math.pi * r
    nose.tools.assert_almost_equal(c.perimeter, p)
