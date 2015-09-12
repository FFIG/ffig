#!/usr/bin/env bash
cp ../output/libShape_c.dylib .
cp ../output/Shape_c.h .
clang -framework Foundation -I. Circle.m main.m -o CircleTest -L. -lShape_c
./CircleTest $RANDOM
