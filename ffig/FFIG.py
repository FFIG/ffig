#!/usr/bin/env python

# FFIG (Foreign Function Interface Generation) parses C/C++ headers with
# libclang and passes the class and function information on to templates to
# generate a c-api and language bindings.

import argparse
import clang
from cppmodel import Model, apply_class_annotations
import os
import re
import sys
import filters.capi_filter
import inspect

from os.path import abspath, join, dirname

import jinja2
from jinja2 import Environment, FileSystemLoader

if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path for libclang manually.
    clang.cindex.Config.set_library_path(
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib')
    
ffig_dir = abspath(dirname(__file__))

def collect_api_and_obj_classes(classes, api_annotation):
    class APIClass:

        def __init__(self, model_class):
            self.api_class = apply_class_annotations(model_class)
            self.impls = []
            # If a class has no pure virtual methods it can be considered as an
            # implementation class
            # if all([not m.is_pure_virtual for m in model_class.methods]):
            #    self.impls.append(model_class)

    api_classes = {c.name: APIClass(c) for c in classes if api_annotation in c.annotations}

    for c in classes:
        for b in c.base_classes:
            if b in api_classes:
                api_classes[b].impls.append(c)

    return [c for k, c in api_classes.items()]


def render_api_and_obj_classes(api_classes, template):
    s = ""
    for c in api_classes:
        s += str(template.render({"class": c.api_class, "impl_classes": c.impls}))
    return s

def get_class_name(header_path):
    header_name = os.path.basename(header_path)
    return re.sub(".h$", "", header_name)


def get_template_name(template_path):
    template_name = os.path.basename(template_path)
    return re.sub(".tmpl$", "", template_name)


def get_template_output(class_name, template_name):
    split_name = template_name.split('.')
    suffix_name = '.'.join(split_name[:-1])
    extension = split_name[-1]
    return "{}{}.{}".format(class_name, suffix_name, extension)

# -- END Old code --


def main(args):
    cwd = os.getcwd()
    
    #FIXME: Remove the need for this constraint.
    if len(args.inputs) != 1:
        raise Exception("Multiple input files are currently not supported.")

    #FIXME: Loop over files and extend the model once we can handle multiple input files.
    i = join(cwd, args.inputs[0])
    tu = clang.cindex.TranslationUnit.from_source(i, '-x c++ -std=c++14 -stdlib=libc++'.split())
    m = Model(tu)

    m.module_name = args.module_name

    # -- BEGIN Old approach
    classes = m.classes
    api_classes = collect_api_and_obj_classes(classes, 'GENERATE_C_API')

    output_dir = abspath(join(cwd, args.output_dir))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    env = Environment(loader=FileSystemLoader(args.template_dir))
    for f,_ in inspect.getmembers(filters.capi_filter):
    #for f in ['to_output_ctype', 'to_ctype']:
        env.filters[f] = getattr(filters.capi_filter, f)

    for t in args.bindings:
        with open(join(output_dir, get_template_output(args.module_name, get_template_name(t))), "w") as output_file:
            template = env.get_template(t)
            s = render_api_and_obj_classes(api_classes, template)
            output_file.write(s)
    # -- END Old approach


if __name__ == '__main__':

    ffig_dir = abspath(dirname(__file__))

    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-o', '--output',
        help='output directory (relative to cwd)',
        default='.',
        dest='output_dir')
    parser.add_argument(
        '-i', '--input',
        nargs='+',
        help='header files for input',
        dest='inputs')
    parser.add_argument(
        '--libclang',
        help='path to libclang',
        default='',
        dest='libclang')
    parser.add_argument(
        '-b', '--bindings',
        help='bindings files to generate',
        nargs='+',
        dest='bindings',
        required=True)
    parser.add_argument(
        '-t', '--template-dir',
        help='directory to search for templates',
        default=join(ffig_dir, 'templates'),
        dest='template_dir')
    parser.add_argument(
        '-m', '--module-name',
        help='module name for generated files',
        dest='module_name',
        required=True)

    args = parser.parse_args()

    main(args)
