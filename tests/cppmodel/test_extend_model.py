from util import get_named_tu
import ffig.cppmodel
import nose


def test_new_class_is_added():
    tu_a = get_named_tu('class A{};', 'a.cpp')
    tu_b = get_named_tu('class B{};', 'b.cpp')

    model = ffig.cppmodel.Model(tu_a)
    model.extend(tu_b)
    classes = model.classes

    assert len(classes) == 2


def test_duplicate_class_is_ignored():
    tu_a = get_named_tu('class A{};', 'a.cpp')

    model = ffig.cppmodel.Model(tu_a)
    model.extend(tu_a)
    classes = model.classes

    assert len(classes) == 1


@nose.tools.raises(Exception)
def test_multiply_defined_class_is_an_error():
    tu_a = get_named_tu('class A{};', 'a.cpp')
    tu_a_too = get_named_tu('class A{};', 'a_too.cpp')

    model = ffig.cppmodel.Model(tu_a)
    model.extend(tu_a_too)


def test_new_function_is_added():
    tu_f = get_named_tu('void f(int);', 'f.cpp')
    tu_g = get_named_tu('void g(int);', 'g.cpp')

    model = ffig.cppmodel.Model(tu_f)
    model.extend(tu_g)

    assert len(model.functions) == 2


def test_function_with_different_args_is_added():
    tu_f = get_named_tu('void f(int);', 'f.cpp')
    tu_g = get_named_tu('void f(double);', 'g.cpp')

    model = ffig.cppmodel.Model(tu_f)
    model.extend(tu_g)

    assert len(model.functions) == 2


def test_duplicate_function_is_ignored():
    tu_f = get_named_tu('void f(int);', 'f.cpp')
    tu_f_too = get_named_tu('void f(int);', 'f_too.cpp')

    model = ffig.cppmodel.Model(tu_f)
    model.extend(tu_f_too)

    assert len(model.functions) == 1
