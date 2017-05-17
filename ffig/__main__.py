import sys
import os

from FFIG import main as ffig_main

if sys.argv[0].endswith('__main__.py'):
    sys.argv[0] = '%s -m ffig' % sys.executable

ffig_main()
