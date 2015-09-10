# Description

A very simple clang-ast-powered code-generator.


# Usage

Add code to the 'input' directory in a similar vein to the existing 'Shape.h' class and run:
    ./run_tests.sh

This populates 'output' with generated files and runs the simple existing tests.

# Output

The 'output' directory is populated with c++, c and python bindings files along with a dynamic library.

running the following in `ipython` will exercise the generated python bindings.
   
    from YOUR_BASE_CLASS_NAME import *

    x = DERIVED_CLASS_NAME(CONSTRUCTOR_ARGUMENTS)
    x.MEMBER_FUNCTION_1(MEMBER_FUNCTION_ARGUMENTS_1)
    x.MEMBER_FUNCTION_2(MEMBER_FUNCTION_ARGUMENTS_2)
