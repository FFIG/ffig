from asset import *
from shape import *
from tree import *
from nose.tools import make_decorator

if sys.version_info[0] == 3:
    from typing import *


def python3only(func):
    name = func.__name__

    def newfunc(*arg, **kw):
        if sys.version_info[0] == 3:
            func(*arg, **kw)
    newfunc = make_decorator(func)(newfunc)
    return newfunc


@python3only
def test_type_hints_for_class_initialisor():
    p = Tree(levels=3)
    hs = get_type_hints(p.__init__)

    assert len(hs) == 2
    assert hs["return"] == Tree
    assert hs["levels"] == Union[int, type(None)]


@python3only
def test_type_hints_for_initialisor_of_impl_class():
    p = Pentagon(1.0)
    hs = get_type_hints(p.__init__)

    assert len(hs) == 2
    assert hs["return"] == Pentagon
    assert hs["side"] == Union[float, type(None)]


@python3only
def test_type_hints_for_class_method_with_zero_arguments():
    t = Tree(1)
    hs = get_type_hints(t.data)

    assert len(hs) == 1
    assert hs["return"] == int


@python3only
def test_type_hints_for_class_method_with_one_argument():
    c = Circle(4.0)
    hs = get_type_hints(c.is_equal)

    assert len(hs) == 2
    assert hs["return"] == int
    assert hs["s"] == AbstractShape


@python3only
def test_type_hints_for_class_method_returning_fwd_declared_type():
    t = Tree(levels=5)
    hs = get_type_hints(t.left_subtree)

    assert len(hs) == 1
    assert hs["return"] == Tree
