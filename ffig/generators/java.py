# Generator module for Java.

import ffig.generators
import os


def _render_template_to_file(filename, template_name, env, data):
    template = env.get_template(template_name)
    with open(filename, 'w') as output_file:
        output_file.write(template.render(data))


def generator(module_name, binding, api_classes, env, output_dir):
    outputs = []

    output_dir = os.path.join(output_dir, 'java', 'src', module_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    o = os.path.join(output_dir, module_name + 'CLibrary.java')
    d = {'module': {'name': module_name}, 'classes': api_classes}
    _render_template_to_file(o, 'java.interop.tmpl', env, d)
    outputs.append(o)

    o = os.path.join(output_dir, module_name + 'Exception.java')
    d = {'module': {'name': module_name}, 'classes': api_classes}
    _render_template_to_file(o, 'java.exception.tmpl', env, d)
    outputs.append(o)

    for cls in api_classes:
        o = os.path.join(output_dir, cls.name + '.java')
        d = {'module': {'name': module_name}, 'class': cls}
        _render_template_to_file(o, 'java.tmpl', env, d)
        outputs.append(o)

        for impl in cls.impls:
            o = os.path.join(output_dir, impl.name + '.java')
            d = {'module': {'name': module_name},
                 'base_class': cls, 'class': impl}
            _render_template_to_file(o, 'java.derived.tmpl', env, d)
            outputs.append(o)

    return outputs


def setup_plugin(context):
    context.register(
        generator,
        [
            ('java', 'Java generator using JNA and a c-api')
        ])
