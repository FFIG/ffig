# Description

FFIG is a Foreign Function Interface Generator.

This project uses libclang to read existing C++ class definitions and create
equivalent classes in other languages (primarily Python for now) and binds them
to the C++ implementation.

While similar to SWIG, <http://www.swig.org>, FFIG does not need an interface
generation language to be used nor do the bindings it generates depend on any
binary details of an interpreter. FFIG Python bindings will run on PyPy,
Python2 Python3 without requiring changes.

FFIG is in early development. We welcome feedback from users but would
encourage anyone looking to generate language bindings to look at SWIG.


# Setup (Linux)

You will need libclang >=3.8.

libclang can be installed from here: <http://llvm.org/releases/>

Set `LD_LIBRARY_PATH` so that libclang can be found.


# Setup (macOS)

Install Xcode. FFIG will use the version of libclang distributed with Xcode.


# Setup (Windows)

Work in progress, minor issues expected.


## Submodules
Tests use the 'catch' test framework: <https://github.com/philsquared/Catch.git>

To get the submodule run:

```
git submodule update --init
```


## Building
The build uses cmake driven by a simple Python script. To build and run tests, run the following from the console:

```
./scripts/build.py -t
```

# Continuous integration

**Build status (on Travis-CI):** [![Build Status](https://travis-ci.org/FFIG/ffig.svg?branch=master)](https://travis-ci.org/FFIG/ffig)


# Issues

Please raise github issues if code cannot be generated where expected or if generated code does not behave as expected.


# Contributing

Contributions are very welcome, please look at unassigned github issues or raise issues for suggested improvements.


# Attribution

We've made considerable use of the following in putting this together:

* <http://szelei.me/code-generator>
* <http://blog.glehmann.net/2014/12/29/Playing-with-libclang>
* <http://eli.thegreenplace.net/tag/llvm-clang>

Design of the python bindings is taken from clang's cindex.

* <https://github.com/llvm-mirror/clang/tree/master/bindings/python>

Mistakes are our own.

