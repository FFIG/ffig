cmake_minimum_required(VERSION 2.8)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

if(MSVC)
  add_compile_options("/EHsc")
else()
  add_compile_options("-std=c++14")
endif()

set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)
include(ffig)

include_directories(externals/catch/include)
include_directories(externals/variant/include)

# Check that the found version of Python==3 on Windows.
# Trust the user if they have supplied their own.
# FIXME: Get to the botton of the libclang/ctypes issues with Python2.
if(NOT PYTHON_EXECUTABLE)
  find_package(PythonInterp REQUIRED)
  if(WIN32)
    execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; assert sys.version_info[0] == 3" RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
    if(result)
      message(FATAL_ERROR "CMake failed: Python 3 is required for Windows.")
    endif()
  endif()
else()
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import this" RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
  if(result)
    message(FATAL_ERROR "CMake failed: ${PYTHON_EXECUTABLE} cannot execute a simple Python script.")
  endif()
endif()

if(Ruby_FOUND)
  ffig_add_library(NAME Shape INPUTS input/Shape.h PYTHON CPP_MOCKS CPP GO RUBY)
else()
  ffig_add_library(NAME Shape INPUTS input/Shape.h PYTHON CPP_MOCKS CPP GO)
endif()
ffig_add_library(NAME Tree INPUTS input/Tree.h PYTHON CPP)
ffig_add_library(NAME Asset INPUTS input/Asset.h PYTHON)

add_subdirectory(tests/src)
add_subdirectory(tests/go)

enable_testing()

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/ffig)

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_SOURCE_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)

if(Ruby_FOUND)
  add_test(
    NAME test_ruby_bindings
    COMMAND ${RUBY_EXECUTABLE} ${CMAKE_SOURCE_DIR}/tests/TestShape.rb ${CMAKE_SOURCE_DIR}/tests/TestShape.rb
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
endif()

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

add_test(
    NAME test_Shape
    COMMAND ${CMAKE_BINARY_DIR}/tests/go/test_Shape
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}/generated)
