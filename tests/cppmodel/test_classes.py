from util import get_tu
import ffig.cppmodel
from ffig.clang.cindex import TypeKind


def test_class_name():
    source = 'class A{};'
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes

    assert len(classes) == 1
    assert classes[0].name == 'A'


def test_class_methods():
    source = """
    class A{};
    class B{
        void foo();
        int bar();
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes

    assert len(classes[0].methods) == 0
    assert len(classes[1].methods) == 2


def test_class_method_return_types():
    source = """
    class B{
        void foo();
        int bar();
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes

    assert classes[0].methods[0].return_type.kind == TypeKind.VOID
    assert classes[0].methods[1].return_type.kind == TypeKind.INT


def test_class_method_argument_types():
    source = """
    class A {
        int foo(int i, const char* p);
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes
    args = classes[0].methods[0].arguments

    assert args[0].type.kind == TypeKind.INT
    assert args[0].name == "i"
    assert args[1].type.kind == TypeKind.POINTER
    assert args[1].name == "p"


def test_class_method_const_qualifiers():
    source = """
    class A {
        int foo() const;
        int bar();
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes
    methods = classes[0].methods

    assert methods[0].is_const
    assert not methods[1].is_const


def test_class_methods_are_virtual():
    source = """
    class A {
        virtual int foo();
        int bar();
        virtual int foobar() = 0;
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes
    methods = classes[0].methods

    assert methods[0].is_virtual
    assert not methods[0].is_pure_virtual
    assert not methods[1].is_virtual
    assert methods[2].is_pure_virtual


def test_namespaces():
    source = """
    class A{};
    namespace outer {
        class B{};
        namespace inner {
            class C{};
        } // end inner
        class D{};
    } // end outer
    class E{};"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes

    assert classes[0].namespace == ""
    assert classes[1].namespace == "outer"
    assert classes[2].namespace == "outer::inner"
    assert classes[3].namespace == "outer"
    assert classes[4].namespace == ""


def test_access_specifiers():
    source = """
    class A { int foo(); };
    struct B { int foo(); };
    class C { public: int foo(); };
    """
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes

    assert not classes[0].methods[0].is_public
    assert classes[1].methods[0].is_public
    assert classes[2].methods[0].is_public


def test_class_member_data():
    source = """
    class A {};
    class B {
        int x_;
        B b_;
    };
    """

    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    c = model.classes[1]

    assert c.members[0].type.kind == TypeKind.INT
    assert c.members[0].type.name == "int"
    assert c.members[0].name == "x_"

    assert c.members[1].type.kind == TypeKind.RECORD
    assert c.members[1].type.name == "B"
    assert c.members[1].name == "b_"


def test_string_representation():
    source = """
    class A {
        virtual int foo();
        int bar();
        virtual int foobar() = 0;
        virtual int cfoobar(int x) const = 0;
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu)
    classes = model.classes
    methods = classes[0].methods

    assert str(methods[0]) == 'virtual int foo()'
    assert str(methods[1]) == 'int bar()'
    assert str(methods[2]) == 'virtual int foobar() = 0'
    assert str(methods[3]) == 'virtual int cfoobar(int x) const = 0'


def test_noexcept():
    source = """
    class A {
        virtual int foo();
    };"""
    tu = get_tu(source, 'cpp')

    model = ffig.cppmodel.Model(tu, force_noexcept=True)
    classes = model.classes
    methods = classes[0].methods

    assert str(methods[0]) == 'virtual int foo() noexcept'
    assert methods[0].is_noexcept
