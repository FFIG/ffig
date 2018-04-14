# Generator module for Python 2 and 3.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    # Module name should be lowercase to conform with PEP-8:
    module_dir = os.path.join(output_dir, module_name.lower())
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    o = os.path.join(module_dir, '__init__.py')
    ffig.generators.generate_single_output_file(
        module_name, '__init__.py.tmpl', api_classes, env, o)

    o = os.path.join(module_dir, '_py2.py')
    ffig.generators.generate_single_output_file(
        module_name, 'py2.tmpl', api_classes, env, o)

    o = os.path.join(module_dir, '_py3.py')
    ffig.generators.generate_single_output_file(
        module_name, 'py3.tmpl', api_classes, env, o)

    return [
        os.path.join(module_dir, x) for x in [
            '__init__.py',
            '_py2.py',
            '_py3.py']]


def setup_plugin(context):
    context.register(
            generator,
            [
                ('python', 'Python2 and Python3 generator using ctypes')
            ])
