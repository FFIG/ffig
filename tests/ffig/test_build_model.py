import ffig.FFIG
from nose.tools import assert_equals


def test_build_model_from_str():
    source = 'class A{}; void foo();'
    filename = 'test.cpp'
    model = ffig.FFIG.build_model_from_source(filename, 'test_source',
            [(filename, source)])

    assert_equals(
            str(model),
            "<cppmodel.Model filename=test.cpp, classes=['A'], functions=['foo']>")
