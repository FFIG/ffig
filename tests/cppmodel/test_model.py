from util import get_tu
import ffig.cppmodel
from nose.tools import assert_equals


def test_repr():
    source = 'class A{}; void foo();'
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)

    assert_equals(
        str(model),
        "<cppmodel.Model filename=t.cpp, classes=['A'], functions=['foo']>")
