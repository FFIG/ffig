# Generator module for Golang.

# Currently, this forwards to the default generator as an example / testcase
# for generator plugins. Ultimately, it will generate Go packages in the
# correct structure.

import os
import os.path

import generators
import logging

log = logging.getLogger(__name__)

def go_generator(module_name, binding, api_classes, env, output_dir):
    ''' Create Go bindings in an appropriate Go package.

        This generator produces a directory src/modulename inside the output
        directory, into which it writes a single Go file containing the
        bindings for this module.
    '''
    module_directory = os.path.realpath(os.path.join(output_dir, 'src', module_name))
    if not os.path.isdir(module_directory):
        log.info('Creating Go package directory {}'.format(module_directory))
        os.makedirs(module_directory)

    log.info('Generating Go bindings for module {0}'.format(module_name))
    template = env.get_template(binding)
    generated_code = generators.render_api_and_obj_classes(api_classes, template)

    output_file_name = os.path.join(module_directory,
            generators.get_template_output(module_name,
                generators.get_template_name(binding)))
    with open(output_file_name, 'w') as f:
        f.write(generated_code)
        log.info('Wrote Go bindings for module {0} to {1}'.format(
            module_name, output_file_name))

    return [output_file_name]

def setup_plugin(context):
    context.register(go_generator, ['go.tmpl'])
