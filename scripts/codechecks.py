#!/usr/bin/env python

import argparse
import collections
import logging
import subprocess
import sys
import os

logging.basicConfig(level=logging.ERROR, format='%(message)s')
log = logging.getLogger('codechecks')

ProcessResult = collections.namedtuple('ProcessResult',
                                       ['stdout', 'stderr', 'returncode'])


def _capture_output(command):
    '''Run command and capture the output and return code.'''
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if len(stdout):
        log.info(stdout)
    if len(stderr):
        log.error(stderr)
    return True if process.returncode == 0 else False


def is_python_file(filename):
    return filename.endswith('.py')


def python_checks(files, reformat=False):
    ''' Run pep8 checks.
        If reformat=True, run autopep8 first.
    '''
    ignored = [
        'E265',  # Block comment should start with '#'
        'E266',  # Too many leading '#' for block comment
        'E402',  # Module level import not at top of file
        'E501',  # Line too long
    ]

    if reformat:
        command = ['python', '-m', 'autopep8', '--aggressive', '--aggressive', '--in-place']
        command.extend(files)
        if not _capture_output(command):
            return False

    command = ['python', '-m', 'autopep8', '--ignore={0}'.format(','.join(ignored))]
    return all([_capture_output(command + [f]) for f in files])


def main():
    parser = argparse.ArgumentParser(
        description='Run codechecks and optionally reformat the code.')
    parser.add_argument(
        '--reformat',
        dest='reformat',
        action='store_true',
        default=False,
        help='Reformat the code.')
    args = parser.parse_args()

    # Get a list of all the files in this repository:
    files = subprocess.check_output(['git', 'ls-files']).split('\n')

    # Ignore files taken and modified from llvm/clang as reformatting makes
    # upstreaming changes hard.
    ignored_directories = [os.path.join('ffig', 'clang')]
    files = [f for f in files if os.path.dirname(f) not in ignored_directories]

    # Collect the result of each stage.
    results = []

    # Run language-specific checks on subsets of the file list:
    results.append(
        python_checks(
            filter(
                is_python_file,
                files),
            reformat=args.reformat))

    if False in results:
        log.error('Checks failed')
        sys.exit(1)
    else:
        log.info('Checks passed')
        sys.exit(0)

if __name__ == '__main__':
    main()
