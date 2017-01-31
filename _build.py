#!/usr/bin/env python

import distutils.spawn
import os
import platform
import shutil
import subprocess
import sys

def find_clang(binary='clang++', version='3.8'):
    ''' Search for a suitable clang binary.
        Returns the path to the executable, or None if not found.
    '''
    versioned_name = '{0}-{1}'.format(binary, version)
    bin_path = distutils.spawn.find_executable(versioned_name)
    if not bin_path:
        # Fall back to unversioned binary.
        bin_path = distutils.spawn.find_executable(binary)
        if not bin_path:
            raise Exception('Could not find {0} or {1}'.format(versioned_name, binary))
    return bin_path

def find_dylib_extension():
    ''' Detect the current platform and return the appropriate file extension for
        dynamic libraries on that platform.
    '''
    dso_extensions = {
            'Darwin': 'dylib',
            'Linux': 'so',
            'Windows': 'dll'
            }
    platform_name = platform.system()
    try:
        return dso_extensions[platform_name]
    except KeyError:
        raise Exception('Unsupported platform: {0}'.format(platform_name))

def strip_extension(filename):
    ''' Remove the path and extension from a filename.
    '''
    return os.path.splitext(os.path.basename(filename))[0]

def build(input_file):
    ''' Build the bindings for a given input file.
    '''
    # Detect system properties.
    clang = find_clang()
    dylib_extension = find_dylib_extension()

    # TODO: These paths probably shouldn't be hard-coded.
    root_dir = os.path.abspath(os.path.dirname(__file__))
    template_dir = os.path.join(root_dir, 'templates')
    output_dir = os.path.join(root_dir, 'output')

    # Call the FFIG generator in the same way that a user would.
    all_templates = [x for x in os.listdir(template_dir) if x.endswith('.tmpl')]
    generator_call = 'python FFIG.py -m {} -i {} -o output -b {}'.format(
            strip_extension(input_file), input_file, ' '.join(all_templates))
    subprocess.check_call(generator_call.split(), cwd=root_dir)
    
    shutil.copy(input_file, output_dir)
    
    # Compile the generated bindings.
    original_dir = os.getcwd()
    try:
        os.chdir(output_dir)
        output_basename = strip_extension(input_file)

        # Compile:
        dylib_filename = 'lib{0}_c.{1}'.format(output_basename, dylib_extension)
        source_filename = '{0}_c.cpp'.format(output_basename)
        clang_cmd = [clang, '-fvisibility=hidden', '-g', '-std=c++14', '-shared',
                '-Wl,', '-o', dylib_filename, '-fPIC', source_filename]
        subprocess.check_call(clang_cmd)

        # Strip:
        strip_cmd = ['strip', '-x', dylib_filename]
        subprocess.check_call(strip_cmd)
    finally:
        os.chdir(original_dir)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception('Usage: {0} input_file'.format(sys.argv[0]))

    build(sys.argv[1])

