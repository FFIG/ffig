from ffig.cppmodel import TypeKind
import platform

# CPP filter to cast type if required


def restore_cpp_type(a):
    t = a.type
    n = a.name
    if t.kind == TypeKind.VOID:
        return n
    if t.kind == TypeKind.INT:
        return n
    if t.kind == TypeKind.DOUBLE:
        return n
    if t.kind == TypeKind.BOOL:
        return n
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return n
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            type_name = t.pointee.name.replace('const ', '')
            return '&(**capi_to_cpp_cast<{}>({}))'.format(type_name, n)
    raise Exception(
        'Type {} has no defined C++ type restoration (adding one for primitives is trivial)'.format(t.name))


# C filter to convert C++ type to C equivalent
def to_c(t, m):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'unsigned'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'const char*'
        if t.pointee.kind == TypeKind.RECORD:
            return '{}_{}'.format(m, t.pointee.name.replace('const ', ''))
    raise Exception('Type {} has no known c equivalent'.format(t.name))


def to_go(t, impl):
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float64'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'string'
        if t.pointee.kind == TypeKind.RECORD:
            return impl
    raise Exception('Type {} has no known Go equivalent'.format(t.name))


def to_go_convert(t):
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float64'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'C.GoString'
        if t.pointee.kind == TypeKind.RECORD:
            return 'unsafe.Pointer'
    raise Exception('Type {} has no known Go equivalent'.format(t.name))


def to_go_method_name(m):
    '''
    Returns the method name with the first character uppercased.

    In Go, only entities with an uppercase first character are exposed in the
    module interface.
    '''
    return m.capitalize()


def go_object(a):
    '''
    In analogy to the `c_object` filter below, this returns `a.name.ptr` for objects
    of class type, and `a.name` for everything else.
    '''
    t = a.type
    n = a.name
    if t.kind == TypeKind.POINTER and t.pointee.kind == TypeKind.RECORD:
        return '{}.ptr'.format(n)
    else:
        return n

# C++ header filter to extract C type from C++ type


def c_object(a):
    t = a.type
    n = a.name
    if t.kind == TypeKind.VOID:
        return n
    if t.kind == TypeKind.INT:
        return n
    if t.kind == TypeKind.DOUBLE:
        return n
    if t.kind == TypeKind.BOOL:
        return n
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return n
        if t.pointee.kind == TypeKind.RECORD:
            return '{}->object_'.format(n)
    raise Exception(
        'No object extraction is defined for type {}'.format(
            t.name))


# Python filter to translate C-type to Python ctype type
def to_py3_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_interop_string'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_hint_type(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'float'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'str'
        if t.pointee.kind == TypeKind.RECORD:
            # This is encoding the assumption that the name of a binding class
            # is the same as the name of the underlying C++ class.
            return to_cpp_type(t)
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_output_py3_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_interop_string'
        if t.pointee.kind == TypeKind.RECORD:
            return 'c_object_p'
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_py2_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_char_p'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_output_py2_ctype(t):
    if t.kind == TypeKind.VOID:
        return None
    if t.kind == TypeKind.INT:
        return 'c_int'
    if t.kind == TypeKind.DOUBLE:
        return 'c_double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'c_char_p'
        if t.pointee.kind == TypeKind.RECORD:
            return 'c_object_p'
    raise Exception(
        'No ctypes equivalent is defined for type {}'.format(
            t.name))


def to_cpp_type(t):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'const char *'
        if t.pointee.kind == TypeKind.RECORD:
            # This is a hack until we can get an unqualified type from libclang
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'No c++ type equivalent is defined for type {} (adding one for primitives is trivial)'.format(t.name))


def to_ruby_type(t):
    if t.kind == TypeKind.VOID:
        return 'void'
    if t.kind == TypeKind.INT:
        return 'int'
    if t.kind == TypeKind.DOUBLE:
        return 'double'
    if t.kind == TypeKind.BOOL:
        return 'bool'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'string'
        if t.pointee.kind == TypeKind.RECORD:
            return 'pointer'
    raise Exception('No ruby equivalent is defined for type {}'.format(t.name))


def to_ruby_output_type(t):
    if t.kind == TypeKind.INT:
        return 'FFI::MemoryPointer.new :int'
    if t.kind == TypeKind.DOUBLE:
        return 'FFI::MemoryPointer.new :double'
    if t.kind == TypeKind.BOOL:
        return 'FFI::MemoryPointer.new :int'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'FFI::MemoryPointer.new(:pointer, 1)'
        if t.pointee.kind == TypeKind.RECORD:
            return 'FFI::MemoryPointer.new :pointer'
    raise Exception('No ruby equivalent is defined for type {}'.format(t.name))


def restore_ruby_type(t):
    if t.kind == TypeKind.INT:
        return 'get_int(0)'
    if t.kind == TypeKind.DOUBLE:
        return 'get_double(0)'
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'read_pointer().read_string()'
        if t.pointee.kind == TypeKind.RECORD:
            return 'get_pointer(0)'
    raise Exception(
        'Type {} has no defined C++ type restoration (adding one for primitives is trivial)'.format(t.name))


def to_lua(t, v):
    if t.kind == TypeKind.INT or t.kind == TypeKind.DOUBLE:
        return '{}'.format(v)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return 'ffi.string({})'.format(v)
    raise Exception(
        'Type {} has no defined Lua type restoration'.format(t.name))


def to_shared_lib(m):
    name = platform.system()
    if name == 'Darwin':
        return 'lib{}_c.dylib'.format(m)
    elif name == 'Windows':
        return '{}_c.dll'.format(m)
    else:
        return 'lib{}_c.so'.format(m)
    raise Exception("Unsupported platform {}".format(name))


def to_dotnet_c_param(arg):
    t = arg.type
    if t.kind == TypeKind.INT:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.DOUBLE:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return "IntPtr {}".format(arg.name)
    raise Exception(
        'Type {} has no defined dotnet C parameter translation (adding one may be trivial)'.format(
            t.name))


def to_dotnet_param(arg):
    t = arg.type
    if t.kind == TypeKind.INT:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.DOUBLE:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return '{} {}'.format(
                t.pointee.name.replace(
                    'const ', ''), arg.name)
    raise Exception(
        'Type {} has no defined dotnet parameter translation (adding one may be trivial)'.format(
            t.name))


def to_dotnet_output_param(t):
    if t.kind == TypeKind.INT:
        return t
    if t.kind == TypeKind.DOUBLE:
        return t
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "IntPtr"
        if t.pointee.kind == TypeKind.RECORD:
            return "IntPtr"
    raise Exception(
        'Type {} has no defined dotnet output parameter translation (adding one may be trivial)'.format(
            t.name))


def to_dotnet_output_value(t, rv):
    if t.kind == TypeKind.INT:
        return "{} {}".format(t, rv)
    if t.kind == TypeKind.DOUBLE:
        return "{} {}".format(t, rv)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "IntPtr {} = IntPtr.Zero".format(rv)
        if t.pointee.kind == TypeKind.RECORD:
            return "IntPtr {} = IntPtr.Zero".format(rv)
    raise Exception(
        'Type {} has no defined dotnet output value translation (adding one may be trivial)'.format(
            t.name))


def to_dotnet_return_type(t):
    if t.kind == TypeKind.INT:
        return t
    if t.kind == TypeKind.DOUBLE:
        return t
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "string"
        if t.pointee.kind == TypeKind.RECORD:
            return t.pointee.name.replace('const ', '')
    raise Exception(
        'Type {} has no defined dotnet return type translation (adding one may be trivial)'.format(
            t.name))


def dotnet_to_c_arg(arg):
    t = arg.type
    if t.kind == TypeKind.INT:
        return arg.name
    if t.kind == TypeKind.DOUBLE:
        return arg.name
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return "{}.c_obj_".format(arg.name)
    raise Exception(
        'Type {} has no defined dotnet to c argument translation (adding one may be trivial)'.format(
            t.name))


def to_dotnet_return_value(t, rv):
    if t.kind == TypeKind.INT:
        return rv
    if t.kind == TypeKind.DOUBLE:
        return rv
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "Marshal.PtrToStringAnsi({})".format(rv)
        if t.pointee.kind == TypeKind.RECORD:
            return 'new {}({})'.format(
                t.pointee.name.replace(
                    'const ', ''), rv)
    raise Exception(
        'Type {} has no defined dotnet return value translation (adding one may be trivial)'.format(
            t.name))


# Java conversions
def to_java_c_param(arg):
    t = arg.type
    if t.kind == TypeKind.INT:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.DOUBLE:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return "Pointer {}".format(arg.name)
    raise Exception(
        'Type {} has no defined java C parameter translation (adding one may be trivial)'.format(
            arg.type.name))


def to_java_param(arg):
    t = arg.type
    if t.kind == TypeKind.INT:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.DOUBLE:
        return "{} {}".format(arg.type, arg.name)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return '{} {}'.format(
                t.pointee.name.replace(
                    'const ', ''), arg.name)
    raise Exception(
        'Type {} has no defined java parameter translation (adding one may be trivial)'.format(
            arg.type.name))


def to_java_output_param(t):
    if t.kind == TypeKind.INT:
        return "IntByReference"
    if t.kind == TypeKind.DOUBLE:
        return "DoubleByReference"
    if t.kind == TypeKind.POINTER:
        return "PointerByReference"
    raise Exception(
        'Type {} has no defined java output parameter translation (adding one may be trivial)'.format(
            t.name))


def to_java_output_value(t, rv):
    if t.kind == TypeKind.INT:
        return "IntByReference {} = new IntByReference();".format(rv)
    if t.kind == TypeKind.DOUBLE:
        return "DoubleByReference {} = new DoubleByReference();".format(rv)
    if t.kind == TypeKind.POINTER:
        return "PointerByReference {} = new PointerByReference();".format(rv)
    raise Exception(
        'Type {} has no defined java output value translation (adding one may be trivial)'.format(
            t.name))


def to_java_return_type(t):
    if t.kind == TypeKind.DOUBLE:
        return t
    if t.kind == TypeKind.INT:
        return t
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "String"
    raise Exception(
        'Type {} has no defined java return type translation (adding one may be trivial)'.format(
            t.name))


def java_to_c_arg(arg):
    t = arg.type
    if t.kind == TypeKind.DOUBLE:
        return arg.name
    if t.kind == TypeKind.INT:
        return arg.name
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.RECORD:
            return "{}.ptr".format(arg.name)
    raise Exception(
        'Type {} has no defined java to c argument translation (adding one may be trivial)'.format(
            arg.type))


def to_java_return_value(t, rv):
    if t.kind == TypeKind.DOUBLE:
        return "{}.getValue()".format(rv)
    if t.kind == TypeKind.INT:
        return "{}.getValue()".format(rv)
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return "{}.getValue().getString(0)".format(rv)
    raise Exception(
        'Type {} has no defined java return value translation (adding one may be trivial)'.format(
            t.name))
