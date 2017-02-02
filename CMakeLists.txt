cmake_minimum_required(VERSION 2.8)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

set(CMAKE_CXX_FLAGS "-std=c++14")

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(ffig)

include_directories(externals/catch/include)
include_directories(externals/variant/include)

find_package(PythonInterp REQUIRED)
find_package(Ruby REQUIRED)

ffig_add_library(NAME Shape INPUTS input/Shape.h PYTHON RUBY CPP CPP_MOCKS)
ffig_add_library(NAME Tree INPUTS input/Tree.h PYTHON RUBY CPP CPP_MOCKS)
ffig_add_library(NAME Asset INPUTS input/Asset.h PYTHON RUBY CPP CPP_MOCKS)

add_subdirectory(tests/src)

enable_testing()

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_ruby_bindings
  COMMAND ${RUBY_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tests/TestShape.rb ${CMAKE_SOURCE_DIR}/tests/TestShape.rb
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_mocks
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestShapeMocks
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_circle
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppCircle
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

add_test(
  NAME test_cpp_tree
  COMMAND ${CMAKE_BINARY_DIR}/tests/src/TestCppTree
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

