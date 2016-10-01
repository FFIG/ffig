from Asset import *
import os
import sys

if sys.platform == 'darwin':
    # OS X doesn't use DYLD_LIBRARY_PATH if System Integrity Protection is
    # enabled. Set the library path manually.
    script_dir = os.path.dirname(os.path.realpath(__file__))
    output_dir = script_dir + '/../output'
    Config.set_library_path(output_dir)

def test_no_argument_constructor():
    # Lack of exception is all we need to test.
    cdo = CDO()

