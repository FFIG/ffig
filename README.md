# Description

A proof-of-concept clang-ast-powered code-generator.

This project uses libclang to read existing C++ class definitions and create
equivalent classes in other languages (primarily Python for now) and binds them
to the C++ implementation.


# Setup (Linux and macOS)

You will need libclang 3.8 and clang python bindings.

libclang can be installed from homebrew on mac or here: <http://llvm.org/releases/>

You can use pip to install python bindings for libclang:

`pip install clang version==3.8`

Set `LD_LIBRARY_PATH` so that libclang can be found.

Update submodules with `git submodule update --init --recursive`.


# Setup (Windows)

Untested, minor issues expected.


# Using the API generator

Currently little more than an extensible proof of concept, the method for running API generation is due revision.

For now:

Add code to the 'input' directory in a similar vein to the existing 'Shape.h' class and run:
    
`./run_tests.sh`

this populates 'output' with generated files and runs the simple existing tests.

Adding django templates to the 'templates' directory in a similar vein to the
existing templates will generate extra output files.

New input files and templates are picked up automatically.


# Output

The 'output' directory is populated with C++, C and Python bindings files along with a dynamic library.

Setting `LD_LIBRARY_PATH` so that the C-API bindings shared libraries in `output` can be found and
running the following in `ipython` will exercise the generated python bindings.

    from YOUR_BASE_CLASS_NAME import *

    x = DERIVED_CLASS_NAME(CONSTRUCTOR_ARGUMENTS)
    x.MEMBER_FUNCTION_1(MEMBER_FUNCTION_ARGUMENTS_1)
    x.MEMBER_FUNCTION_2(MEMBER_FUNCTION_ARGUMENTS_2)


#Continuous integration

**Build status (on Travis-CI):** [![Build Status](https://travis-ci.org/jbcoe/C_API_generation.svg?branch=master)](https://travis-ci.org/jbcoe/C_API_generation)


# Issues

Please raise github issues if code cannot be generated where expected or if generated code does not behave as expected.


# Contributing

Contributions are very welcome, please look at unassigned github issues or raise issues for suggested improvements.


# Attribution

I've made considerable use of the following in putting this together:

* <http://szelei.me/code-generator>
* <http://blog.glehmann.net/2014/12/29/Playing-with-libclang>
* <http://eli.thegreenplace.net/tag/llvm-clang>

Design of the python bindings is taken from clang's cindex.

* <https://github.com/llvm-mirror/clang/tree/master/bindings/python>

Mistakes are my own.

