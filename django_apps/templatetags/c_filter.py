from django import template
import re

register = template.Library()

match_pointer_to_char = re.compile("const\s+char\s*\*$")
match_pointer_to_class = re.compile("const\s+.*\s*\*$")

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
