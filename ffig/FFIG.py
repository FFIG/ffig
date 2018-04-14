#!/usr/bin/env python

# FFIG (Foreign Function Interface Generation) parses C/C++ headers with
# libclang and passes the class and function information on to templates to
# generate a c-api and language bindings.

import argparse
import ffig.clang as clang
import inspect
import jinja2
import logging
import os
import os.path
import re
import sys

logging.basicConfig(level=logging.WARNING)

import ffig.annotations
import ffig.cppmodel
import ffig.filters.capi_filter
import ffig.generators

clang.cindex.Config.set_compatibility_check(False)


def find_clang_library_path():
    paths = [
        '/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/lib',
        '/Library/Developer/CommandLineTools/usr/lib',
    ]
    for path in paths:
        if os.path.isfile(os.path.join(path, 'libclang.dylib')):
            return path
    raise Exception('Unable to find libclang.dylib')


if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path for libclang manually.
    clang.cindex.Config.set_library_path(find_clang_library_path())

ffig_dir = os.path.abspath(os.path.dirname(__file__))


def collect_api_and_obj_classes(classes, api_annotation):
    api_classes = {c.name: c
                   for c in classes if api_annotation in c.annotations}

    for _, c in api_classes.items():
        ffig.annotations.apply_class_annotations(c)
        c. impls = []

    for c in classes:
        for base in c.base_classes:
            if base in api_classes:
                ffig.annotations.apply_class_annotations(c)
                api_classes[base].impls.append(c)

    return [c for k, c in api_classes.items()]


def write_bindings_to_disk(
        module_name,
        bindings,
        api_classes,
        env,
        output_dir):
    """
    Write the bindings to disk, return Nothing
    Input:
    - module_name - string
    - list of bindings to generate
    - api_classes
    - environment to get templates from
    - output_dir where to write to
    """

    bindings.extend("_c.cpp.tmpl _c.h.tmpl".split())
    bindings = list(set(bindings))

    for binding in bindings:
        ffig.generators.generate(module_name, binding,
                                 api_classes, env, output_dir)


def build_model_from_source(
        path_to_source,
        module_name,
        unsaved_files=None):
    """
    Input:
    - full path to source file
    - module_name taken from args
    - [Optional] List of 2-tuples of unsaved file content in the format:
      (filename, content_string)

    Returns:
    - model built from a clang.cindex TranslationUnit with a name from args
    """
    ffig_include_dir = os.path.join(os.path.dirname(__file__), 'include')
    tu = clang.cindex.TranslationUnit.from_source(
        path_to_source,
        '-x c++ -std=c++14 -stdlib=libc++ -I{}'.format(ffig_include_dir).split(),
        unsaved_files=unsaved_files)

    model = ffig.cppmodel.Model(tu)
    model.module_name = module_name

    return model


def make_output_dir(cwd, o_dir_path):
    """
    Function that creates the output_dir under the given path in cwd,
    if no such dir exists yet. Returns nothing.
    Input:
    - current working directory
    - output_dir path
    """
    output_dir = os.path.abspath(os.path.join(cwd, o_dir_path))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)


def set_template_env(template_dir):
    """
    Function that sets the Jinja2 template environment from a given dir.
    Returns nothing.
    Input:
    - template_dir path
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        lstrip_blocks=True,
        trim_blocks=True)
    for f, _ in inspect.getmembers(ffig.filters.capi_filter):
        # for f in ['to_output_ctype', 'to_ctype']:
        env.filters[f] = getattr(ffig.filters.capi_filter, f)
    return env


def run(args):
    cwd = os.getcwd()

    # FIXME: Remove the need for this constraint.
    if len(args.inputs) > 1:
        raise Exception("Multiple input files are currently not supported.")

    # FIXME: Loop over files and extend the model once we can handle multiple
    # input files.
    input_file = os.path.join(cwd, args.inputs[0])
    m = build_model_from_source(input_file, args.module_name)
    classes = m.classes
    api_classes = collect_api_and_obj_classes(classes, 'FFIG:EXPORT')

    make_output_dir(cwd, args.output_dir)
    env = set_template_env(args.template_dir)
    write_bindings_to_disk(
        args.module_name,
        list(args.bindings),
        api_classes,
        env,
        args.output_dir)


def main():
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
        default=[],
        dest='inputs',
        required=True)
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
        default=os.path.join(ffig_dir, 'templates'),
        dest='template_dir')
    parser.add_argument(
        '-m', '--module-name',
        help='module name for generated files',
        dest='module_name',
        required=True)

    args = parser.parse_args()

    run(args)
