from django import template
import re

register = template.Library()

match_pointer_to_class = re.compile("const\s+(.*)\s*\*$")

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

