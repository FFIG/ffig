import sys
import model
from django.template import Context, Template
import django
if not django.conf.settings.configured : django.conf.settings.configure()

def collect_api_and_obj_classes(classes, api_annotation):
  api_classes = []
  api_classes.extend([c for c in classes if api_annotation in c.annotations])
  obj_classes = []
  #for c in classes:
  #  for b in c.base_classes:
  #    if b in [x.name for x in api_classes]:
  #      obj_classes.append((c,b))

  return obj_classes, api_classes

def render_api_and_obj_classes(obj_classes,api_classes,template):

  for c in api_classes:
    print(template.render(Context({"class": c})))
  #for c,b in obj_classes:
  #  print(template.render(Context({"class": c, "base": b})))

def generate_c_api(class_file, template, api_annotation='GENERATE_C_API'):
  classes = model.parse_classes(class_file)
  obj_classes,api_classes = collect_api_and_obj_classes(classes, api_annotation)
  render_api_and_obj_classes(obj_classes,api_classes,template)

if __name__ == "__main__":
  s=""
  with open(sys.argv[2]) as template_file:
    for line in template_file:
      s=s+line
  generate_c_api(sys.argv[1], Template(s))
