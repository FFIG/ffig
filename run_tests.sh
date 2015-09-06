#!/usr/bin/env bash

HEADERS=Shape.h
for HEADER in ${HEADERS}
  do echo -n Generating bindings for ${HEADER}
  ./build.sh ${HEADER} && echo " [OK]"
done


echo

echo Running tests
python -m unittest discover -v tests/
