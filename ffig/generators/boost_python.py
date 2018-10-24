# Generator module for Boost-Python.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    o = os.path.join(output_dir, module_name + '_py.cpp')
    ffig.generators.generate_single_output_file(
        module_name, 'boost_python.tmpl', api_classes, env, o)
    outputs.append(o)
    
    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('boost_python', 'Python bindings using Boost Python.')
            ])


