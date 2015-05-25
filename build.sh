#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT _c.h.tmpl _c.cpp.tmpl py.tmpl

clang++ -std=c++11 -shared -Wl, -o ${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp

