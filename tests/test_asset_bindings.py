from Asset import *
import common

common.set_library_path(Config)

def test_no_argument_constructor():
    # Lack of exception is all we need to test.
    cdo = CDO()

