from django import template
import re

register = template.Library()
match_pointer_to_type = re.compile("const [A-Za-z0-9]+\s*\*$")

@register.filter
def to_c(s):
  if s=='int':
    return s
  if s=='double':
    return s
  if s=='const char *':
    return s
  if re.match(match_pointer_to_type,s):
    return 'const void *'
  else:
    raise Exception('Type {} has no known c equivalent'.format(s))

