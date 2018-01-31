cmake_minimum_required(VERSION 3.5)

# FIXME: This silences a warning but I'm not sure why its needed.
set(CMAKE_MACOSX_RPATH 1)

project(test_ffig)

if(MSVC)
  add_compile_options("/EHsc")
else()
  add_compile_options("-std=c++14")
endif()

if(NOT WIN32)
  set(CMAKE_CXX_FLAGS_ASAN "-g -fno-omit-frame-pointer -O0 -fsanitize=address")
  set(CMAKE_C_FLAGS_ASAN "-g -fno-omit-frame-pointer -O0 -fsanitize=address")
  set(CMAKE_EXE_LINKER_FLAGS_ASAN "-fsanitize=address")
  set(CMAKE_SHARED_LINKER_FLAGS_ASAN "-fsanitize=address")
endif()

set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/cmake)
include(ffig)

include_directories(externals/catch/include)
include_directories(externals/variant/include)
# FIXME: Use FFIG to get this path.
include_directories(ffig/include)

# Check that the found version of Python==3 on Windows.
# Trust the user if they have supplied their own.
# FIXME: Get to the bottom of the libclang/ctypes issues with Python2.
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

# Look for Go
# FIXME: Make this less hacky, ideally using a real CMake module
execute_process(COMMAND go version RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
if(result)
  set(Go_FOUND FALSE)
else()
  set(Go_FOUND True)
endif()

# Look for Ruby
find_package(Ruby)
if(NOT Ruby_FOUND)
  message(STATUS "Ruby tests disabled: Ruby interpreter not found.")
endif()


# Look for Lua
# FIXME: Make this less hacky.
execute_process(COMMAND luajit -e "print('testing')" RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
if(result)
  message(STATUS "Lua tests disabled: luajit cannot execute a simple Lua script.")
else()
  set(LuaJIT_FOUND 1)
  set(LuaJIT_EXECUTABLE "luajit")
endif()

# Look for C#
# FIXME: Make this less hacky, ideally using a real CMake module
execute_process(COMMAND dotnet --version RESULT_VARIABLE result OUTPUT_QUIET ERROR_QUIET)
if(result)
  message(STATUS "Dotnet tests disabled: dotnet executable not found.")
else()
  set(dotnet_FOUND 1)
  configure_file(${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestTree.cs.in ${CMAKE_CURRENT_BINARY_DIR}/generated/TestTree.cs)
  configure_file(${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestShape.cs.in ${CMAKE_CURRENT_BINARY_DIR}/generated/TestShape.cs)
  configure_file(${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/ffig.net.csproj.in ${CMAKE_CURRENT_BINARY_DIR}/generated/ffig.net.csproj)
endif()

set(all_ffig_bindings "PYTHON;CPP;CPP_MOCKS;DOTNET")
if(Ruby_FOUND)
  list(APPEND all_ffig_bindings "RUBY")
endif()

if(Go_FOUND)
  list(APPEND all_ffig_bindings "GO")
endif()

file(GLOB_RECURSE FFIG_SOURCE ${CMAKE_CURRENT_LIST_DIR}/ffig/*)

# Add FFIG build targets
ffig_add_library(NAME Shape INPUTS tests/input/Shape.h ${all_ffig_bindings})
ffig_add_library(NAME Tree INPUTS tests/input/Tree.h NOEXCEPT PYTHON CPP D SWIFT DOTNET)
ffig_add_library(NAME Asset INPUTS tests/input/Asset.h PYTHON LUA)
ffig_add_library(NAME Animal INPUTS tests/input/Animal.h PYTHON)

# build dotnet test dll
# FIXME: Work out how to get dependencies calculated more robustly
if(dotnet_FOUND)
  file(GLOB TEST_INPUT ${CMAKE_CURRENT_LIST_DIR}/tests/input/*.h)
  add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/generated/ffig.net.dll
    COMMAND dotnet build ffig.net.csproj -o .
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.cs;${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.cs
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated
    COMMENT "Building DOTNET assembly ffig.net.dll")
  add_custom_target(ffig.net ALL
    DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/generated/ffig.net.dll)
endif()

add_subdirectory(tests/src)

enable_testing()

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_CURRENT_LIST_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/ffig)

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_CURRENT_LIST_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_python_bindings PROPERTY LABELS PYTHON)

add_test(
  NAME test_cpp_mocks
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestShapeMocks
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_mocks PROPERTY LABELS MOCKS)

add_test(
  NAME test_cpp_circle
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestCppCircle
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_circle PROPERTY LABELS CPP)

add_test(
  NAME test_tree_capi
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestTreeCAPI
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_tree_capi PROPERTY LABELS C)

add_test(
  NAME test_cpp_tree
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestCppTree
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_tree PROPERTY LABELS CPP)

add_test(
  NAME test_d_tree_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.d.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.d)
set_property(TEST test_d_tree_output PROPERTY LABELS D TEXT)

add_test(
  NAME test_dotnet_shape_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Shape.cs.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.cs)
set_property(TEST test_dotnet_shape_output PROPERTY LABELS DOTNET TEXT)

add_test(
  NAME test_dotnet_tree_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.cs.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.cs)
set_property(TEST test_dotnet_tree_output PROPERTY LABELS DOTNET TEXT)

add_test(
  NAME test_swift_tree_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.swift.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.swift)
set_property(TEST test_swift_tree_output PROPERTY LABELS SWIFT TEXT)

if(dotnet_FOUND)
  add_test(
    NAME test_dotnet
    COMMAND dotnet test --no-build --no-restore -o .
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_dotnet PROPERTY LABELS DOTNET)
  set_property(TEST test_dotnet PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

if(LuaJIT_FOUND)
  # FIXME: The relative paths here (and in the lua test file) are very brittle.
  add_test(
    NAME test_asset_lua
    COMMAND ${LuaJIT_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/tests/test_asset_bindings.lua
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_asset_lua PROPERTY LABELS LUA)
  set_property(TEST test_asset_lua PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

if(Ruby_FOUND)
  add_test(
    NAME test_ruby_bindings
    COMMAND ${RUBY_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/tests/TestShape.rb ${CMAKE_CURRENT_LIST_DIR}/tests/TestShape.rb
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_ruby_bindings PROPERTY LABELS RUBY)
endif()

if(Go_FOUND AND NOT WIN32)
  add_subdirectory(tests/go)
endif()

