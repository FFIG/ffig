# Generator module that provides aliases for other generators.
# This is used to alias ruby -> rb.tmpl, for example.

import ffig.generators

aliases = {
    'lua': 'lua.tmpl',
    'ruby': 'rb.tmpl',
}


def aliased_generator(module_name, binding, api_classes, env, output_dir):
    try:
        binding = aliases[binding]
    except KeyError:
        raise Exception('No alias for {0}'.format(binding))

    return ffig.generators.default_generator(
        module_name, binding, api_classes, env, output_dir)


def setup_plugin(context):
    context.register(aliased_generator, aliases.keys())
