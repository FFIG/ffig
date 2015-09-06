#!/usr/bin/env bash

echo -n Cleaning output
rm -rf output || exit 1
mkdir output
echo " [OK]" 

HEADERS=Shape.h
for HEADER in ${HEADERS}
  do echo -n Generating bindings for ${HEADER}
  ./build.sh ${HEADER} templates || exit 1
  echo " [OK]" 
done


echo

echo Running tests
python -m unittest discover -v tests/
