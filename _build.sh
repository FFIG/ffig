#!/usr/bin/env bash
INPUT=$1
DYLIB_EXT="so"

#FIXME: Find a more idiomatic way to detect the OS.
if [[ $OSTYPE =~ .*darwin.* ]] ; then DYLIB_EXT="dylib"; fi

# Use clang++-3.8 explicitly, if available. Fall back on available clang++
# otherwise.
CLANG=clang++-3.8
which ${CLANG} > /dev/null || CLANG=clang++

./generate.py $INPUT templates output || exit 1
cp $INPUT output/

pushd output > /dev/null
INPUT_FILE=$(basename $INPUT)
OUTPUT=${INPUT_FILE%.h}
${CLANG} -fvisibility=hidden -g -std=c++14 -shared -Wl, -o lib${OUTPUT}_c.${DYLIB_EXT} -fPIC ${OUTPUT}_c.cpp || exit 1
strip -x lib${OUTPUT}_c.${DYLIB_EXT}
popd > /dev/null
