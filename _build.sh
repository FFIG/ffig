#!/usr/bin/env bash
INPUT=$1

./generate.py $INPUT templates output || exit 1
cp $INPUT output/

pushd output > /dev/null
INPUT_FILE=$(basename $INPUT)
OUTPUT=${INPUT_FILE%.h}
clang++-3.6 -std=c++14 -shared -Wl, -o lib${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp || exit 1
popd > /dev/null
