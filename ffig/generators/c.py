# Generator module for Boost-Python.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    o = os.path.join(output_dir, module_name + '_c.h')
    ffig.generators.generate_single_output_file(
        module_name, '_c.h.tmpl', api_classes, env, o)
    outputs.append(o)
    
    o = os.path.join(output_dir, module_name + '_c.cpp')
    ffig.generators.generate_single_output_file(
        module_name, '_c.cpp.tmpl', api_classes, env, o)
    outputs.append(o)
    
    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('c', "C API bindings to be used from other languages' FFI facilities.")
            ])


