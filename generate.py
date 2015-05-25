#!/usr/bin/env python

import os
import re
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

def get_class_name(header_path):
  header_name = os.path.basename(header_path)
  return re.sub(".h$","",header_name)

def get_template_name(template_path):
  template_name = os.path.basename(template_path)
  return re.sub(".tmpl$","",template_name)

def get_template_output(class_name, template_name):
  split_name = template_name.split('.')
  suffix_name = '.'.join(split_name[:-1])
  extension = split_name[-1]
  return "{}{}.{}".format(class_name, suffix_name, extension)

if __name__ == "__main__":
  if len(sys.argv) == 1:
    raise Exception("Requires 3 arguments: annotated_header template output. Did you mean to run 'build.sh'?")
  if len(sys.argv) < 4:
    raise Exception("Requires 3 arguments: annotated_header template output")
  
  class_name = get_class_name(sys.argv[1])
  #for t in sys.argv[2:]:
  #  print get_template_name(t)
  #  print get_template_output(class_name, get_template_name(t))

  classes = model.parse_classes(sys.argv[1])
  api_classes = collect_api_and_obj_classes(classes, 'GENERATE_C_API')

  for t in sys.argv[2:]:
    with open(t) as template_file, open(get_template_output(class_name, get_template_name(t)),"w") as output_file:                
      template = Template(template_file.read())
      s=render_api_and_obj_classes(api_classes, template)
      output_file.write(s)
