from util import get_tu
import ffig.cppmodel
from ffig.clang.cindex import TypeKind


def test_function_name():
    source = """
    void foo();
    void bar();
    """
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    functions = model.functions

    assert len(functions) == 2
    assert functions[0].name == 'foo'
    assert functions[1].name == 'bar'


def test_function_return_type():
    source = """
    int foo();
    double* bar();
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    functions = model.functions

    assert functions[0].return_type.kind == TypeKind.INT
    assert functions[1].return_type.kind == TypeKind.POINTER
    assert functions[1].return_type.is_pointer
    assert functions[1].return_type.pointee.kind == TypeKind.DOUBLE
    assert not functions[1].return_type.pointee.is_const


def test_function_arguments():
    source = """
    int foo();
    double bar(int x, char y);
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    functions = model.functions

    assert len(functions[0].arguments) == 0
    assert len(functions[1].arguments) == 2
    assert functions[1].arguments[0].type.kind == TypeKind.INT
    assert functions[1].arguments[0].name == 'x'
    assert functions[1].arguments[1].type.kind == TypeKind.CHAR_S
    assert functions[1].arguments[1].name == 'y'


def test_function_equality():
    source = """
    int foo();
    int foo(int);
    int foo(double);
    int foo(int,int);
    namespace x {
    int foo();
    }
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)

    for i, f in enumerate(model.functions):
        for j, g in enumerate(model.functions):
            if i == j:
                assert f == g
            else:
                assert not f == g


def test_string_representation():
    source = """
    double foo(int, char);
    double bar(int x, char y);
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    functions = model.functions

    assert str(functions[0]) == 'double foo(int, char)'
    assert str(functions[1]) == 'double bar(int x, char y)'


def test_force_noexcept():
    source = """
    double foo(int, char);
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu, force_noexcept=True)
    functions = model.functions

    assert str(functions[0]) == 'double foo(int, char) noexcept'
    assert functions[0].is_noexcept
