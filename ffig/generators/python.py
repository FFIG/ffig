# Generator module for Python 2 and 3.

import generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    module_dir = os.path.join(output_dir, module_name)
    if not os.path.exists(module_dir):
        os.makedirs(module_dir)

    o = os.path.join(module_dir, '__init__.py')
    generators.generate_single_output_file(
        module_name, '__init__.py.tmpl', api_classes, env, o)

    o = os.path.join(module_dir, '_py2.py')
    generators.generate_single_output_file(
        module_name, 'py2.tmpl', api_classes, env, o)

    o = os.path.join(module_dir, '_py3.py')
    generators.generate_single_output_file(
        module_name, 'py3.tmpl', api_classes, env, o)

    return [
        os.path.join(module_dir, x) for x in [
            '__init__.py',
            'interop_py2.py',
            'interop_py3.py']]


def setup_plugin(context):
    context.register(generator, ['python'])
