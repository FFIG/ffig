#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT h.tmpl > ${OUTPUT}_c.h
./generate.py $INPUT cpp.tmpl > ${OUTPUT}_c.cpp
./generate.py $INPUT py.tmpl > ${OUTPUT}.py

clang++ -std=c++11 -shared -Wl, -o ${OUTPUT}.dylib -fPIC ${OUTPUT}_c.cpp

