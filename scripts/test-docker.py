#!/usr/bin/env python
import subprocess
import sys


def main(args):
    if '--local' in args:
        args = [a for a in args if a != '--local']
    else:
        subprocess.check_call("docker pull ffig/ffig-base".split())
    subprocess.check_call("docker build -t ffig_local .".split())
    subprocess.check_call(['docker',
                           'run',
                           'ffig_local',
                           '/bin/bash',
                           '-c',
                           './scripts/build.py {}'.format(' '.join(args[1:]))])


if __name__ == '__main__':
    main(sys.argv)
