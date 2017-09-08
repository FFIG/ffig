import logging
import os
import os.path
import re
import sys

log = logging.getLogger(__name__)


def dso_extension():
    extensions = {
        'darwin': 'dylib',
        'win32': 'dll',
        'cygwin': 'dll',
        'linux2': 'so',
        'linux': 'so',
    }
    return extensions[sys.platform]


def render_api_and_obj_classes(module_name, api_classes, template):
    '''Render a template.'''
    return str(template.render({"module": {"name": module_name},
                                "classes": api_classes,
                                "dso_extension": dso_extension()}))


def get_template_name(template_path):
    '''Get the template name from the binding name.'''
    template_name = os.path.basename(template_path)
    return re.sub(".tmpl$", "", template_name)


def get_template_output(class_name, template_name):
    '''Determine the output filename from the template name.'''
    split_name = template_name.split('.')
    suffix_name = '.'.join(split_name[:-1])
    extension = split_name[-1]
    return "{}{}.{}".format(class_name, suffix_name, extension)


def generate_single_output_file(
        module_name,
        binding,
        api_classes,
        env,
        output_file_name):
    '''Generate a single named output file. Used by the default generator.'''
    with open(output_file_name, 'w') as output_file:
        template = env.get_template(binding)
        output_string = render_api_and_obj_classes(
            module_name, api_classes, template)
        output_file.write(output_string)


def default_generator(module_name, binding, api_classes, env, output_dir):
    '''
    Default generator.

    Used when there are no custom generators registered for a binding. This
    generator is appropriate for simple bindings that produce a single output
    file.

    Input:
     - module_name: The name of the module to generate.
     - binding: The name of the binding to generate.
     - api_classes: The classes to generate bindings for.
     - env: The jinja2 environment.
     - output_dir: The base directory for generator output.
    '''
    template = env.get_template(binding)
    output_string = render_api_and_obj_classes(
        module_name, api_classes, template)

    output_file_name = os.path.join(
        output_dir, get_template_output(
            module_name, get_template_name(binding)))
    generate_single_output_file(
        module_name,
        binding,
        api_classes,
        env,
        output_file_name)
    return [output_file_name]


class GeneratorContext(object):
    '''Holds a mapping of bindings to custom generators.'''

    def __init__(self):
        '''Initialise with no custom generators'''
        self._generator_map = {}

    def register(self, generator_function, bindings):
        '''
        Register a generation function.

        Input:
         - generator_function: f(module_name, binding, api_classes, env, output_dir).
         - bindings: List of bindings that this function generates.
        '''
        for binding in bindings:
            self._generator_map[binding] = generator_function

    def generate(self, module_name, binding, api_classes, env, output_dir):
        '''
        Generate a set of bindings.

        Input:
          - module_name: The name of the module to generate.
          - binding: The type of binding to generate.
          - api_classes: Classes to generate bindings for.
          - env: The template environment.
          - output_dir: Directory to write generated bindings to.
        '''
        log.info('Finding generator for {}'.format(binding))
        if binding in self._generator_map:
            log.info('  found in map')
            return self._generator_map[binding](
                module_name, binding, api_classes, env, output_dir)
        else:
            log.info('  using default')
            return default_generator(
                module_name, binding, api_classes, env, output_dir)

# This is the default generator context.
generator_context = GeneratorContext()


def generate(module_name, binding, api_classes, env, output_dir):
    '''Forward the request to the default generator context.'''
    return generator_context.generate(
        module_name, binding, api_classes, env, output_dir)


def _activate_plugin(module_name):
    '''Internal function used to activate a plugin that has been found.'''
    log.info('Importing {}'.format(module_name))
    module = __import__(
        'ffig.generators.{0}'.format(module_name),
        fromlist=['setup_plugin'])
    module.setup_plugin(generator_context)


def _scan_plugins():
    ''' Internal function used to search the generators directory for plugins.

        Plugins may be written as a module (a single python file in the
        generators directory) or as a package (a subdirectory of generators,
        containing an __init__.py).

        In either case, plugins must define a function to register one or more
        generator functions against a list of one or more binding names:

            def setup_plugin(context):
                context.register(generator_func, [binding, ...])

        where generator_func is a function of the form

            f(module_name, binding, api_classes, env, output_dir)
    '''
    basedir = os.path.realpath(os.path.dirname(__file__))
    log.info('Scanning for plugins in {}'.format(basedir))
    excluded_files = ['__init__.py', '__pycache__']
    for entry in os.listdir(basedir):
        log.info('Checking {}'.format(entry))
        if entry in excluded_files:
            log.info('Skipping excluded file {}'.format(entry))
            continue
        filepath = os.path.join(basedir, entry)
        if os.path.isdir(filepath):
            log.info('Found plugin package {}'.format(entry))
            # This is a generator package. Import it.
            _activate_plugin(os.path.basename(entry))
        elif os.path.isfile(filepath) and entry.endswith('.py'):
            log.info('Found plugin module {}'.format(entry))
            _activate_plugin(os.path.basename(entry)[:-3])

# Scan the generators directory for plugins and register them on
# initialisation.
_scan_plugins()
