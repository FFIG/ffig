# Generator module for Swift.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    o = os.path.join(output_dir, module_name + '.swift')
    ffig.generators.generate_single_output_file(
        module_name, 'swift.tmpl', api_classes, env, o)
    outputs.append(o)

    o = os.path.join(output_dir, module_name + '-Bridging-Header.h')
    ffig.generators.generate_single_output_file(
        module_name, 'swift.bridging-header.tmpl', api_classes, env, o)
    outputs.append(o)
    
    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('swift', 'Swift generator using c-api')
            ])

