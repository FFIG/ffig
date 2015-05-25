#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT _c.h.tmpl ${OUTPUT}_c.h _c.cpp.tmpl ${OUTPUT}_c.cpp py.tmpl ${OUTPUT}.py

clang++ -std=c++11 -shared -Wl, -o ${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp

