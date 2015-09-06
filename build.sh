#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT templates || exit 1

clang++ -std=c++14 -shared -Wl, -o ${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp

