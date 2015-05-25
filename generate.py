#!/usr/bin/env python

import sys
import model
import django_apps
from django.template import Context, Template
import django

if not django.conf.settings.configured : 
  django.conf.settings.configure(INSTALLED_APPS=('django_apps',),)                                 

django.setup()


def collect_api_and_obj_classes(classes, api_annotation):
  class APIClass:
    def __init__(self,model_class):
      self.api_class = model_class
      self.impls = []

  api_classes = {c.name:APIClass(c) for c in classes if api_annotation in c.annotations}
  
  for c in classes:
    for b in c.base_classes:
      if api_classes.has_key(b):
        api_classes[b].impls.append(c)

  return [c for k,c in api_classes.iteritems()]

def render_api_and_obj_classes(api_classes,template):
  s=""
  for c in api_classes:
    s+=str(template.render(Context({"class": c.api_class, "impl_classes":c.impls})))
  return s

if __name__ == "__main__":
  if len(sys.argv) == 1:
    raise Exception("Requires 3 arguments: annotated_header template output. Did you mean to run 'build.sh'?")
  if len(sys.argv) < 4:
    raise Exception("Requires 3 arguments: annotated_header template output")
  
  classes = model.parse_classes(sys.argv[1])
  api_classes = collect_api_and_obj_classes(classes, 'GENERATE_C_API')

  for t,o in zip(sys.argv[2::2], sys.argv[3::2]):
    with open(t) as template_file, open(o,"w") as output_file:                
      template = Template(template_file.read())
      s=render_api_and_obj_classes(api_classes, template)
      output_file.write(s)
