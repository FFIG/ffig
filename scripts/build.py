#!/usr/bin/env python
import sys
import os
import platform
import subprocess


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t', help='run tests', action='store_true', dest='run_tests')
    parser.add_argument(
        '-v', help='verbose', action='store_true', dest='verbose')
    parser.add_argument(
        '-o',
        help='output dir (relative to source dir)',
        default='build',
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
    args = parser.parse_args()
    args.platform = platform.system()
    
    src_dir = os.path.dirname(os.path.dirname(__file__))

    cmake_invocation = ['cmake', '.','-B{}'.format(args.out_dir)]
    if args.platform == 'Windows':
        cmake_invocation.extend(['-G', '"Visual Studio 14 2015 Win64"'])
    else:
        cmake_invocation.append('-DCMAKE_BUILD_TYPE={}'.format(args.config))

    if args.verbose:
        cmake_invocation.append('-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON')
    if args.python_path:
        cmake_invocation.append('-DPYTHON_EXECUTABLE={}'.format(args.python_path))

    subprocess.check_call(cmake_invocation, cwd=src_dir)
    subprocess.check_call(
        'cmake --build ./{}'.format(args.out_dir).split(), cwd=src_dir)

    if args.run_tests:
        rc = subprocess.call(
            'ctest . --output-on-failure -C {}'.format(args.config).split(),
            cwd=os.path.join(src_dir, args.out_dir))
        if rc != 0:
            sys.exit(1)


if __name__ == '__main__':
    main()
