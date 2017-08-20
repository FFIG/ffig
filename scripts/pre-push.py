#!/usr/bin/env python

from __future__ import print_function

import os
import subprocess
import sys

this_dir = os.path.dirname(os.path.realpath(__file__))
check_script = os.path.join(this_dir, 'codechecks.py')

try:
    subprocess.check_call([check_script])
    sys.exit(0)
except subprocess.CalledProcessError:
    print('\n****')
    print(
        'The code checks failed. Please run\n  {0} --reformat'.format(check_script))
    print('and commit the changes before pushing.')
    print('****\n')
    sys.exit(1)
