# Generator module that provides aliases for other generators.
# This is used to alias ruby -> rb.tmpl, for example.

import ffig.generators

aliases = {
    'dotnet': ('cs.tmpl', 'dotnet (C#) bindings'),
    'lua': ('lua.tmpl', 'Lua bindings'),
    'ruby': ('rb.tmpl', 'Ruby bindings'),
}


def aliased_generator(module_name, binding, api_classes, env, output_dir):
    try:
        binding = aliases[binding][0]
    except KeyError:
        raise Exception('No alias for {0}'.format(binding))

    return ffig.generators.default_generator(
        module_name, binding, api_classes, env, output_dir)


def setup_plugin(context):
    bindings = [(key, value[1]) for key, value in aliases.items()]
    context.register(aliased_generator, bindings)
