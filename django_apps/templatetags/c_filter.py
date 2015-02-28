from django import template
import re

register = template.Library()

match_pointer_to_type = re.compile("const [A-Za-z0-9]+\s*\*$")

@register.filter
def to_c(s):
  if s=='int' or s=='bool' or s=='double' or s=='const char *':
    return s
  if re.match(match_pointer_to_type,s):
    return 'const void *'
  else:
    error = 'Type {} has no known c equivalent'.format(s)
    raise Exception(error)

