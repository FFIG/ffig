from django import template
register = template.Library()

@register.filter
def to_ctype(s):
  if s=='int':
    return 'c_int'
  if s=='void*':
    return 'c_void_p'
  if s=='double':
    return 'c_double'
  if s=='const char *':
    return 'c_char_p'
  else:
    raise Exception('Type {} has no known ctypes equivalent'.format(s))

