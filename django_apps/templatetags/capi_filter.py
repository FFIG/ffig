from django import template
import re
import cppmodel
from cppmodel import TypeKind

register = template.Library()

match_pointer_to_char = re.compile("const\s+char\s*\*$")
match_pointer_to_class = re.compile("const\s+(.*)\s*\*$")


@register.filter
def to_objc(s):
    if s=='void' or s=='int' or s=='bool' or s=='double':
        return s
    if re.match(match_pointer_to_char,s):
        return 'NSString*'
    else:
        error = 'Type {} has no known obj-c equivalent'.format(s)
        raise Exception(error)


@register.filter
def wrap_objc_type(t,v):
    if t=='void' or t=='int' or t=='bool' or t=='double':
        return v
    if re.match(match_pointer_to_char,t):
            return '[[NSString alloc] initWithUTF8String:{}]'.format(v)
    else:
        error = 'Type {} has no known obj-c wrapper type'.format(t)
        raise Exception(error)


@register.filter
def unwrap_objc_type(t,v):
    if t=='void' or t=='int' or t=='bool' or t=='double':
        return v
    if re.match(match_pointer_to_char,t):
            return '[s UTF8String]'.format(v)
    else:
        error = 'Type {} has no known obj-c wrapper type'.format(t)
        raise Exception(error)


#Obj-c filter to cast type if required
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
            return match_pointer_to_class.match(t.name).group(1)
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

