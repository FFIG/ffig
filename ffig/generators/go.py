# Generator module for Golang.

# Currently, this forwards to the default generator as an example / testcase
# for generator plugins. Ultimately, it will generate Go packages in the
# correct structure.

import generators

def go_generator(binding, api_classes, env, args, output_dir):
    return generators.default_generator(binding, api_classes, env, args, output_dir)

def setup_plugin(context):
    context.register(go_generator, ['go.tmpl'])
