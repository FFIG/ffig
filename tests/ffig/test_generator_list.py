import ffig.generators
from nose.tools import assert_equals

def test_generator_list():
    python_entry = list(filter(lambda x: x[0] == 'python',
        ffig.generators.generator_context.list_generators()))[0]

    assert_equals(python_entry[1], 'Python2 and Python3 generator using ctypes')
