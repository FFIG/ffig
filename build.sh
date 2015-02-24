#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT h.tmpl > c_${OUTPUT}.h
./generate.py $INPUT cpp.tmpl > c_${OUTPUT}.cpp
./generate.py $INPUT py.tmpl > ${OUTPUT}.py

clang++ -std=c++11 -shared -Wl, -o ${OUTPUT}.dylib -fPIC c_${OUTPUT}.cpp
