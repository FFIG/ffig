#!/usr/bin/env python

from __future__ import print_function

import os

this_dir = os.path.dirname(os.path.realpath(__file__))
git_dir = os.path.realpath(os.path.join(this_dir, '..', '.git'))

hook_scripts = ['pre-push.py']

for hook_script in hook_scripts:
    target = os.path.join(this_dir, hook_script)
    link_name = os.path.join(git_dir, 'hooks', hook_script.replace('.py', ''))
    if os.path.exists(link_name):
        print(
            'Skipping {0} because {1} already exists'.format(
                target, link_name))
    else:
        print('Installing symbolic link {0} --> {1}'.format(link_name, target))
        os.symlink(target, link_name)
