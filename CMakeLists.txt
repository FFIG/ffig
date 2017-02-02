cmake_minimum_required(VERSION 2.8)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

set(CMAKE_CXX_FLAGS "-std=c++14")

include_directories(externals/catch/include)
include_directories(externals/variant/include)

find_package(PythonInterp REQUIRED)
find_package(Ruby REQUIRED)

function(add_ffig_library)
  set(options RUBY PYTHON CPP CPP_MOCKS)
  set(oneValueArgs NAME INPUTS)
  cmake_parse_arguments(add_ffig_library "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(module ${add_ffig_library_NAME})
  set(input ${add_ffig_library_INPUTS})

  set(ffig_invocation "-i;${input};-m;${module};-t;${CMAKE_SOURCE_DIR}/templates;-o;${CMAKE_BINARY_DIR}/generated;-b;_c.h.tmpl;_c.cpp.tmpl")
  set(ffig_outputs "${CMAKE_BINARY_DIR}/generated/${module}_c.h;${CMAKE_BINARY_DIR}/generated/${module}_c.cpp")  
  set(ffig_output_dir "${CMAKE_BINARY_DIR}/generated")

  if(add_ffig_library_RUBY)
    set(ffig_invocation "${ffig_invocation};rb.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.rb")
  endif()
  if(add_ffig_library_PYTHON)
    set(ffig_invocation "${ffig_invocation};py.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.py")
  endif()
  if(add_ffig_library_CPP_MOCKS)
    set(ffig_invocation "${ffig_invocation};_mocks.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_mocks.h")
  endif()
  if(add_ffig_library_CPP)
    set(ffig_invocation "${ffig_invocation};_cpp.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_cpp.h")
  endif()

  add_custom_command(OUTPUT ${ffig_outputs}
    COMMAND ${PYTHON_EXECUTABLE} FFIG.py ${ffig_invocation}
    DEPENDS ${input}
    WORKING_DIRECTORY ${CMAKE_SOURCE_DIR})

  # FIXME: This is a bit ugly. The header is copied next to the generated bindings.
  file(COPY ${input} DESTINATION ${ffig_output_dir}/)

  add_library(${module}_c SHARED ${input} ${ffig_output_dir}/${module}_c.h ${ffig_output_dir}/${module}_c.cpp)

  # FIXME: This is a bit ugly. The shared library is copied next to the generated bindings.
  add_custom_command(TARGET ${module}_c
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${module}_c> ${ffig_output_dir}/)
endfunction()

add_ffig_library(NAME Shape INPUTS input/Shape.h PYTHON RUBY CPP CPP_MOCKS)
add_ffig_library(NAME Tree INPUTS input/Tree.h PYTHON RUBY CPP CPP_MOCKS)
add_ffig_library(NAME Asset INPUTS input/Asset.h PYTHON RUBY CPP CPP_MOCKS)

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

