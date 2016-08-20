#!/usr/bin/env bash
INPUT=$1

./generate.py $INPUT templates output || exit 1
cp $INPUT output/

pushd output > /dev/null
INPUT_FILE=$(basename $INPUT)
OUTPUT=${INPUT_FILE%.h}
clang++-3.8 -fvisibility=hidden -g -std=c++14 -stdlib=libc++ -shared -Wl, -o lib${OUTPUT}_c.dylib -fPIC ${OUTPUT}_c.cpp || exit 1
strip -x lib${OUTPUT}_c.dylib
popd > /dev/null
