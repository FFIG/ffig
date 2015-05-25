#!/usr/bin/env bash

INPUT=${1:-Shape.h}
OUTPUT=${INPUT%.h}

./generate.py $INPUT templates/*

clang++ -std=c++11 -shared -Wl, -o ${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp

