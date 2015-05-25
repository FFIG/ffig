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

def generate_c_api(class_file, template, api_annotation='GENERATE_C_API'):
  classes = model.parse_classes(class_file)
  api_classes = collect_api_and_obj_classes(classes, api_annotation)
  return render_api_and_obj_classes(api_classes,template)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    raise Exception("Requires 3 arguments: annotated_header template output. Did you mean to run 'build.sh'?")
  if len(sys.argv) != 4:
    raise Exception("Requires 3 arguments: annotated_header template output")
  with open(sys.argv[2]) as template_file:
    s=generate_c_api(sys.argv[1], Template(template_file.read()))
    with open(sys.argv[3],"w") as output_file:
      output_file.write(s)
