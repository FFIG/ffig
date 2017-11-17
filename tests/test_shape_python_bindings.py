import math
import nose
import shape


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


def test_shape_Circle_is_equal_to_itself():
    c = shape.Circle(2)
    assert c.is_equal(c)


def test_shape_Circle_is_equal_to_another_circle_with_the_same_radius():
    c1 = shape.Circle(2)
    c2 = shape.Circle(2)
    assert c1.is_equal(c2)


def test_shape_Circle_is_not_equal_to_circle_with_different_radius():
    c1 = shape.Circle(2)
    c2 = shape.Circle(3)
    assert not c1.is_equal(c2)


def test_shape_Circle_is_not_equal_to_square():
    c = shape.Circle(2)
    s = shape.Square(2)
    assert not c.is_equal(s)


@nose.tools.raises(Exception)
def test_exception_on_negative_radius():
    shape.Circle(-1)


def test_exception_text_is_a_string():
    try:
        shape.Circle(-1)
    except shape.Shape_error as e:
        assert isinstance(str(e), str)
