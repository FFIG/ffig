from django import template
import re

register = template.Library()

match_pointer_to_type = re.compile("const [A-Za-z0-9]+\s*\*$")

@register.filter
def to_ctype(s):
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
  if re.match(match_pointer_to_type,s):
    return 'c_object_p'
  else:
    error = 'Type {} has no known ctypes equivalent'.format(s)
    raise Exception(error)

