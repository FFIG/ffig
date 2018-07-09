# Generator module for dotnet.

import ffig.generators
import os
import shutil

def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    output_dir = os.path.join(output_dir, module_name + '.net')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    o = os.path.join(output_dir, module_name + '.cs')
    ffig.generators.generate_single_output_file(
        module_name, 'cs.tmpl', api_classes, env, o)
    outputs.append(o)

    o = os.path.join(output_dir, module_name + '.net.csproj')
    ffig.generators.generate_single_output_file(
        module_name, 'csproj.tmpl', api_classes, env, o)
    outputs.append(o)
    
    return outputs


def setup_plugin(context):
    context.register(
            generator,
            [
                ('dotnet', 'dotnet generator using PInvoke')
            ])

