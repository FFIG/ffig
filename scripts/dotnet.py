#!/usr/bin/env python
import sys
import os
import platform
import shutil
import subprocess

src_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
if len(sys.argv) > 1:
    gen_dir = os.path.abspath(sys.argv[1])

testEnv = os.environ.copy()
testEnv['LD_LIBRARY_PATH'] = gen_dir

subprocess.check_call("dotnet restore", cwd=gen_dir, shell=True, env=testEnv)
subprocess.check_call("dotnet test -v diag -o .",
                      cwd=gen_dir, shell=True, env=testEnv)
