from django import template
import re

register = template.Library()

match_pointer_to_char = re.compile("const\s+char\s*\*$")

@register.filter
def to_c(s):
  if s=='void' or s=='int' or s=='bool' or s=='double':
    return s
  if re.match(match_pointer_to_char,s):
    return 'const char*'
  else:
    error = 'Type {} has no known c equivalent'.format(s)
    raise Exception(error)

