# Generator module for Rust.

import ffig.generators
import os


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    output_dir = os.path.join(output_dir, 'rust')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    o = os.path.join(output_dir, module_name + '.rust')
    ffig.generators.generate_single_output_file(
        module_name, 'rust.tmpl', api_classes, env, o)
    outputs.append(o)
    
    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('rust', 'Rust generator using c-api')
            ])


