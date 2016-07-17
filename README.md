# Description

A very simple clang-ast-powered code-generator.

# Setup

Set LD_LIBRARY_PATH so that libclang can be found.

Set LLVM_SRC_DIR to the root of LLVM source with clang.
OR install clang modules for python using pip.

libclang and the python bindings will need to be compatible (libclang will need to be new enough).
As of writing the pip clang bindings required clang-3.5.

You can use homebrew (on OS X) to install clang-3.6.

Update submodules with `git submodule update --init --recursive`.

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

# Issues 

Please raise github issues if code cannot be generated where expected or if generated code does not behave as expected.


# Contributing

Contributions are very welcome, please look at unassigned github issues or raise issues for suggested improvements.
