# Developers Guide

Welcome to the FFIG development guide.  This document provides an overview of FFIG.  This includes an outline of what FFIG is, how it does works, how to use it and finally and how finally to extend it.

## What is FFIG

FFIG (Foreign Function Interface Generator) is a toolkit for automatically generating language bindings from C++ code to a range of programming languages (including C++, see [C++ binding generation](MISSING LINK<PROVIDE ME>) for why you may want to do this).

## How does FFIG work?

FFIG aims to take all of the hard work out of generating a solution to interop C++ code with other high-level programming languages.  Other existing widely used solutions such as [SWIG](http://www.swig.org/) require manual intervention, in the form of an interface definition language for the tool to generate resulting language binding.  FFIG aims to remove the need for this by using the [abstract syntax tree](https://en.wikipedia.org/wiki/Abstract_syntax_tree) generate by the Clang compiler front-end to generate the information required to automate the binding generation for you.  

FFIG differs further to [SWIG](http://www.swig.org/), where [SWIG](http://www.swig.org/) would generate from bindings from your C++ code to a language such as Python FFIG provides a level of abstraction in the form of generators which provides a means of selecting between multiple bindings implementations.  In the case of Python this allows FFIG to generate multiple types of Python bindings, allowing for binding generated which are based upon:
* [ctypes](https://docs.python.org/2/library/ctypes.html)
* [Boost Python](https://www.boost.org/doc/libs/1_66_0/libs/python/doc/html/index.html)
* [pybind11](https://github.com/pybind/pybind11)

This provides a number of benefits.  It allows for rapid prototyping of code and language bindings in unison without the need to update interface definition language files.  It allows you test multiple bindings, for instance, if you have a large code base the compile time of bindings may vary across underlying frameworks (think [Boost Python](https://www.boost.org/doc/libs/1_66_0/libs/python/doc/html/index.html) vs [pybind11's](https://github.com/pybind/pybind11) significantly reduced build times).  It allows you to move from a framework bound to a particular version of Python to a binding supporting multiple Python implementations (such as [ctypes](https://docs.python.org/2/library/ctypes.html)).   Or if you are just interested in comparing the performance or easy of debugability of an interface layer you can generate multiple bindings simultaneously via just selecting the appropriate configuration and compare the resulting bindings side by side.


