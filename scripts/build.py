#!/usr/bin/env python
import sys
import os
import platform
import shutil
import subprocess


def check_for_executable(exe_name, args=['--version']):
    try:
        cmd = [exe_name]
        cmd.extend(args)
        subprocess.check_output(cmd)
        return True
    except (subprocess.CalledProcessError, IOError):
        return False


def process_optional_bindings(required, disabled):
    output = []

    for lang in required:
        output.append('-DFFIG_REQUIRE_{}=1'.format(lang.upper()))
    for lang in disabled:
        output.append('-DFFIG_DISABLE_{}=1'.format(lang.upper()))

    return output


def main():
    optional_languages = ('dotnet', 'go', 'lua', 'java',
                          'swift', 'ruby', 'boost_python',
                          'julia')

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--clean',
        help='remove build directory before build',
        action='store_true',
        dest='clean')

    test_options = parser.add_mutually_exclusive_group()
    test_options.add_argument(
        '-t', help='run tests', action='store_true', dest='run_tests')
    test_options.add_argument(
        '-T', help='run labelled tests', dest='labelled_tests')

    parser.add_argument(
        '-v', help='verbose', action='store_true', dest='verbose')
    parser.add_argument(
        '-o',
        help='output dir (relative to source dir)',
        default='build_out',
        dest='out_dir')
    parser.add_argument(
        '-c',
        help='config (Debug or Release)',
        default='Debug',
        dest='config')
    parser.add_argument(
        '--python-path',
        help='path to python executable ie "/usr/local/bin/python3"',
        dest='python_path')
    parser.add_argument(
        '--venv',
        help='Use a python virtualenv, installing modules from requirements.txt',
        action="store_true",
        dest='venv')

    if platform.system() == "Windows":
        parser.add_argument(
            '--win32',
            help='Build 32-bit libraries',
            action='store_true',
            dest='win32')

    for lang in optional_languages:
        group = parser.add_mutually_exclusive_group()
        group.add_argument(
            '--disable_{}'.format(lang),
            dest='disabled_bindings',
            action='append_const',
            const=lang,
            help='Disable generation of bindings for {}'.format(lang))
        group.add_argument(
            '--require_{}'.format(lang),
            dest='required_bindings',
            action='append_const',
            const=lang,
            help='Require generation of bindings for {}'.format(lang))

    parser.add_argument(
        '--nodetect',
        action='store_true',
        help='Disable generation of all optional bindings not explicitly activated')

    args = parser.parse_args()
    args.platform = platform.system()

    src_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    if args.clean and os.path.exists(args.out_dir):
        shutil.rmtree(args.out_dir)

    cmake_invocation = ['cmake', '.', '-B{}'.format(args.out_dir)]
    if args.platform == 'Windows':
        if not args.win32:
            cmake_invocation.extend(['-A', 'x64'])
    else:
        # Use Ninja instead of Make, if available.
        if check_for_executable('ninja'):
            cmake_invocation.extend(['-GNinja'])
        cmake_invocation.extend(['-DCMAKE_BUILD_TYPE={}'.format(args.config)])

    if args.verbose:
        cmake_invocation.append('-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON')

    if not os.path.exists(os.path.join(src_dir, args.out_dir)):
        os.makedirs(os.path.join(src_dir, args.out_dir))

    if args.venv:
        python_executable = args.python_path if args.python_path else 'python'
        subprocess.check_call(
            '{} -m virtualenv pyenv'.format(python_executable).split(),
            cwd=os.path.join(src_dir,
                             args.out_dir))
        subprocess.check_call(
            '{}/pyenv/bin/pip install -r requirements.txt'.format(
                os.path.join(
                    src_dir,
                    args.out_dir)).split(),
            cwd=src_dir)
        args.python_path = os.path.join(
            src_dir, args.out_dir, 'pyenv', 'bin', 'python')

    if args.python_path:
        cmake_invocation.append(
            '-DPYTHON_EXECUTABLE={}'.format(args.python_path))

    # Add required / disabled binding options
    required_bindings = args.required_bindings or []
    disabled_bindings = args.disabled_bindings or []

    if args.nodetect:
        disabled_bindings += [o for o in optional_languages
                              if o not in required_bindings]

    cmake_invocation.extend(
        process_optional_bindings(required_bindings, disabled_bindings))

    cmake_cache_valid = True

    try:
        with open(os.path.join(src_dir, args.out_dir, "build.py.cache.txt"), "r") as cachefile:
            if cachefile.readline() != " ".join(cmake_invocation):
                print("CMake invocation has changed. Rebuilding CMakeCache.txt")
                cmake_cache_valid = False
    except IOError:
        cmake_cache_valid = False
        pass

    if not cmake_cache_valid:
        try:
            os.remove(os.path.join(src_dir, args.out_dir, "CMakeCache.txt"))
        except OSError:
            pass
        subprocess.check_call(cmake_invocation, cwd=src_dir)
        with open(os.path.join(src_dir, args.out_dir, "build.py.cache.txt"), "w") as cachefile:
            cachefile.write(" ".join(cmake_invocation))

    subprocess.check_call(
        'cmake --build ./{}'.format(args.out_dir).split(), cwd=src_dir)

    rc = 0
    if args.run_tests:
        rc = subprocess.call(
            'ctest . --output-on-failure -C {}'.format(args.config).split(),
            cwd=os.path.join(src_dir, args.out_dir))
    elif args.labelled_tests:
        rc = subprocess.call(
            'ctest . --output-on-failure -C {} -L {}'.format(
                args.config, args.labelled_tests).split(),
            cwd=os.path.join(src_dir, args.out_dir))
    if rc != 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
