from util import get_tu
import ffig.cppmodel
from nose.tools import assert_equals
from nose.tools import assert_raises


def test_repr():
    source = 'class A{}; void foo();'
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)

    assert_equals(
        str(model),
        "<cppmodel.Model filename=t.cpp, classes=['A'], functions=['foo']>")


def test_exception_for_missing_include():
    source = '#include "major_tom.h"'
    tu = get_tu(source, 'cpp')

    def f():
        ffig.cppmodel.Model(tu)
    assert_raises(ValueError, f)
