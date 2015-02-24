#!/usr/bin/env bash

./generate.py Shape.h h.tmpl > c_shape.h
./generate.py Shape.h cpp.tmpl > c_shape.cpp
./generate.py Shape.h py.tmpl > Shape.py

clang++ -std=c++11 -shared -Wl, -o shape.dylib -fPIC c_shape.cpp
