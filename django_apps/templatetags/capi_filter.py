from django import template
import cppmodel
from cppmodel import TypeKind

register = template.Library()


#CPP filter to cast type if required
@register.filter
def cast_c_type(t):
    if t.kind == TypeKind.VOID:
        return ''
    if t.kind == TypeKind.INT:
        return ''
    if t.kind == TypeKind.DOUBLE:
        return ''
    if t.kind == TypeKind.BOOL:
        return ''
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return ''
        if t.pointee.kind == TypeKind.RECORD:
            return '({})'.format(t.name)
    raise Exception('Type {} has no known c equivalent'.format(t.name))


#C filter to convert C++ type to C equivalent
@register.filter
def to_c(t):
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
            return 'const void*'
    raise Exception('Type {} has no known c equivalent'.format(t.name))


#C++ header filter to extract C type from C++ type
@register.filter
def c_object(v,t):
    if t.kind == TypeKind.VOID:
        return v
    if t.kind == TypeKind.INT:
        return v
    if t.kind == TypeKind.DOUBLE:
        return v
    if t.kind == TypeKind.BOOL:
        return v
    if t.kind == TypeKind.POINTER:
        if t.pointee.kind == TypeKind.CHAR_S:
            return v
        if t.pointee.kind == TypeKind.RECORD:
            return '{}->object_'.format(v)
    raise Exception('No object extraction is defined for type {}'.format(t.name))


#Python filter to translate C-type to Python ctype type
@register.filter
def to_ctype(t):
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
            return t.pointee.name.replace('const ','')
    raise Exception('No ctypes equivalent is defined for type {}'.format(t.name))

@register.filter
def to_output_ctype(t):
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
    raise Exception('No ctypes equivalent is defined for type {}'.format(t.name))

