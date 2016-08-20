#!/usr/bin/env bash
INPUT=$1
DYLIB_EXT="so"

#FIXME: Find a more idiomatic way to detect the OS.
if [[ $OSTYPE =~ .*darwin.* ]] ; then DYLIB_EXT="dylib"; fi

./generate.py $INPUT templates output || exit 1
cp $INPUT output/

pushd output > /dev/null
INPUT_FILE=$(basename $INPUT)
OUTPUT=${INPUT_FILE%.h}
clang++-3.8 -fvisibility=hidden -g -std=c++14 -shared -Wl, -o lib${OUTPUT}_c.${DYLIB_EXT} -fPIC ${OUTPUT}_c.cpp || exit 1
strip -x lib${OUTPUT}_c.${DYLIB_EXT}
popd > /dev/null
