from django import template
import re

register = template.Library()

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
  else:
    error = 'Type {} has no known ctypes equivalent'.format(s)
    raise Exception(error)

