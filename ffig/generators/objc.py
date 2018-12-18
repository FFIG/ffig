# Generator module for Objective-C.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    o = os.path.join(output_dir, module_name + '_objc.h')
    ffig.generators.generate_single_output_file(
        module_name, '_objc.h.tmpl', api_classes, env, o)
    outputs.append(o)

    o = os.path.join(output_dir, module_name + '_objc.m')
    ffig.generators.generate_single_output_file(
        module_name, '_objc.m.tmpl', api_classes, env, o)
    outputs.append(o)

    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('objc', 'Objective-C generator using c-api')
            ])

