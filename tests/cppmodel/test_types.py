from util import get_tu
import ffig.cppmodel
from ffig.clang.cindex import TypeKind
from nose.tools import assert_equals


def test_pointer_type():
    source = "double* pd();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.POINTER
    assert not f.return_type.is_const
    assert f.return_type.pointee.kind == TypeKind.DOUBLE
    assert not f.return_type.pointee.is_const


def test_const_pointer_to_double_type():
    source = "double* const cpd();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.POINTER
    assert f.return_type.is_const
    assert f.return_type.pointee.kind == TypeKind.DOUBLE
    assert not f.return_type.pointee.is_const


def test_const_pointer_to_const_double_type():
    source = "const double* const cpcd();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    functions = model.functions
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.POINTER
    assert f.return_type.is_const
    assert f.return_type.pointee.kind == TypeKind.DOUBLE
    assert f.return_type.pointee.is_const


def test_pointer_to_pointer_type():
    source = "double** ppd();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.POINTER
    assert f.return_type.is_pointer
    assert f.return_type.pointee.kind == TypeKind.POINTER
    assert f.return_type.pointee.is_pointer
    assert f.return_type.pointee.pointee.kind == TypeKind.DOUBLE


def test_pointer_to_record_type():
    source = "class A{}; A* pA();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.POINTER
    assert f.return_type.is_pointer
    assert f.return_type.pointee.kind == TypeKind.RECORD


def test_reference_to_record_type():
    source = "class A{}; A& pA();"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    f = model.functions[0]

    assert f.return_type.kind == TypeKind.LVALUEREFERENCE
    assert not f.return_type.is_pointer
    assert f.return_type.is_reference
    assert f.return_type.pointee.kind == TypeKind.RECORD


def test_string_representation():
    source = "class A{};"

    tu = get_tu(source, 'cpp')
    model = ffig.cppmodel.Model(tu)
    c = model.classes[0]

    assert_equals(str(c), "<cppmodel.Class A>")
