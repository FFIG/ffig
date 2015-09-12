from django import template
import re

register = template.Library()

match_pointer_to_char = re.compile("const\s+char\s*\*$")

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
 
