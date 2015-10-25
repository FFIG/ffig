from django import template
import re

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
def cast_c_type(s):
  if s=='int' or s=='bool' or s=='double' or s=='const char *':
    return ''
  if re.match(match_pointer_to_class,s):
    return '({})'.format(s)
  else:
    error = 'Type {} has no known c equivalent'.format(s)
    raise Exception(error)


#C filter to convert C++ type to C equivalent
@register.filter
def to_c(s):
  if s=='void' or s=='int' or s=='bool' or s=='double':
    return s
  if re.match(match_pointer_to_char,s):
    return 'const char*'
  if re.match(match_pointer_to_class,s):
    return 'const void*'
  else:
    error = 'Type {} has no known c equivalent'.format(s)
    raise Exception(error)

#C++ header filter to extract C type from C++ type
@register.filter
def c_object(v,t):
  if t=='void' or t=='int' or t=='bool' or t=='double':
    return v
  if re.match(match_pointer_to_char,t):
    return 'v'
  if re.match(match_pointer_to_class,t):
    return '{}->object_'.format(v)
  else:
    error = 'No c object extraction is defined for type "{}"'.format(t)
    raise Exception(error)


#Python filter to translate C-type to Python ctype type
@register.filter
def to_ctype(s):
  if s=='void':
    return None
  if s=='bool':
    return 'bool'
  if s=='int':
    return 'c_int'
  if s=='void*':
    return 'c_void_p'
  if s=='double':
    return 'c_double'
  if s=='const char *':
    return 'c_char_p'
  m = match_pointer_to_class.match(s)
  if m: 
    return m.group(1) 
  
  error = 'Type {} has no known ctypes equivalent'.format(s)
  raise Exception(error)

