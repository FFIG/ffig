#!/usr/bin/env python

import os
import re
import sys
import clang.cindex
import cppmodel as model
import django_apps
from django.template import Context, Template
import django
import HTMLParser
import annotations
html_parser = HTMLParser.HTMLParser()

if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path for libclang manually.
    clang.cindex.Config.set_library_path(
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')

if not django.conf.settings.configured :
    django.conf.settings.configure(
            INSTALLED_APPS=('django_apps',),
            TEMPLATES = [
                {
                    'BACKEND': 'django.template.backends.django.DjangoTemplates',
                    'DIRS': [],
                    'APP_DIRS': True,
                    'OPTIONS': {
                        'context_processors': [
                            'django.template.context_processors.debug',
                            'django.template.context_processors.request',
                            'django.contrib.auth.context_processors.auth',
                            'django.contrib.messages.context_processors.messages',
                            ],
                        },
                    },
                ])

django.setup()


def collect_api_and_obj_classes(classes, api_annotation):
    class APIClass:
        def __init__(self,model_class):
            self.api_class = annotations.apply_class_annotations(model_class)
            self.impls = []
            # If a class has no pure virtual methods it can be considered as an
            # implementation class
            #if all([not m.is_pure_virtual for m in model_class.methods]):
            #    self.impls.append(model_class)

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
    return html_parser.unescape(s)

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

def collect_classes(source_files, args='-x c++ -std=c++14 -stdlib=libc++'):
    classes = []
    for f in source_files:
        with open(f) as i:
            tu = clang.cindex.TranslationUnit.from_source(i, args.split())
            #FIXME: Handle duplicates if multiple TUs pull in the same class def.
            classes.extend(model.Model(tu).classes)
    return classes


if __name__ == "__main__":
    if len(sys.argv) != 4:
            raise Exception("Requires 3 arguments: got {}".format(str(sys.argv[1:])))

    class_name = get_class_name(sys.argv[1])


    tu = clang.cindex.TranslationUnit.from_source(sys.argv[1], ['-std=c++11','-x', 'c++','-stdlib=libc++'])
    classes = model.Model(tu).classes
    api_classes = collect_api_and_obj_classes(classes, 'GENERATE_C_API')

    template_dir = sys.argv[2];
    output_dir = sys.argv[3];

    for t in [os.path.join(template_dir,x) for x in os.listdir(template_dir) if x.endswith(".tmpl")]:
        with open(t) as template_file, open(os.path.join(output_dir,get_template_output(class_name, get_template_name(t))),"w") as output_file:
            template = Template(template_file.read())
            s=render_api_and_obj_classes(api_classes, template)
            output_file.write(s)
