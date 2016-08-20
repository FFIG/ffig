#!/usr/bin/env bash

export PYTHONPATH=$(pwd)/externals/clang_cpp_code_model:$PYTHONPATH
export PYTHONPATH=$(pwd)/output:$PYTHONPATH

export LD_LIBRARY_PATH="$(pwd)/output:${LD_LIBRARY_PATH}"

echo -n Cleaning output
rm -rf output || exit 1
mkdir output
echo " [OK]" 

HEADERS=Shape.h
for HEADER in input/*
  do echo -n Generating bindings for ${HEADER}
  ./_build.sh ${HEADER} || exit 1
  echo " [OK]" 
done

echo Running tests
python -m nose -v tests/ || exit 1

echo Running CPP tests
mkdir -p tests/build
pushd tests/build > /dev/null
cmake -DCMAKE_INSTALL_PREFIX:PATH=.. ../src/ 
make && make install 
popd > /dev/null
pushd tests/bin > /dev/null
for var in Test* ; do ./$var; done
popd > /dev/null

