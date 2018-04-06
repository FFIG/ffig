# FIXME: Work out which CMake version we actually need.
cmake_minimum_required(VERSION 3.5)

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

include_directories(externals/catch2/single_include)
include_directories(externals/variant/include)
# FIXME: Use FFIG to get this path.
include_directories(ffig/include)

# Check that the found version of Python==3 on Windows.
# Trust the user if they have supplied their own.
# FIXME: Get to the bottom of the libclang/ctypes issues with Python2 on Windows.
if(NOT PYTHON_EXECUTABLE)
  find_package(PythonInterp REQUIRED)
  if(WIN32)
    execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; assert sys.version_info[0] == 3" 
                    RESULT_VARIABLE result 
                    OUTPUT_QUIET 
                    ERROR_QUIET)
    if(result)
      message(FATAL_ERROR "CMake failed: Python 3 is required for Windows.")
    endif()
  endif()
else()
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import this" 
                  RESULT_VARIABLE result 
                  OUTPUT_QUIET 
                  ERROR_QUIET)
  if(result)
    message(FATAL_ERROR "CMake failed: ${PYTHON_EXECUTABLE} cannot execute a simple Python script.")
  endif()
endif()

# FFIG won't work without Python and a C++ compiler so we can assume
# support for Python and C++ must exist.
set(all_ffig_bindings "PYTHON;CPP;CPP_MOCKS")

# Look for Go
# FIXME: Make this less hacky, ideally using a real CMake module
execute_process(COMMAND go version 
                RESULT_VARIABLE result 
                OUTPUT_QUIET 
                ERROR_QUIET)
if(result)
  set(Go_FOUND FALSE)
else()
  set(Go_FOUND True)
  list(APPEND all_ffig_bindings "GO")
endif()

# Look for Ruby
find_package(Ruby)
if(NOT Ruby_FOUND)
  message(STATUS "Ruby tests disabled: Ruby interpreter not found.")
else()
  execute_process(COMMAND ${RUBY_EXECUTABLE} -rffi -e "puts FFI"
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    message(WARNING "CMake failed: Ruby FFI dependencies is required.  Run 'gem install ffi' to install FFI dependency")
  else()
    list(APPEND all_ffig_bindings "RUBY")
  endif()
endif()

# Look for Java
find_package(Java)
find_package(Java COMPONENTS Runtime)
find_package(Java COMPONENTS Development)
if(NOT Java_FOUND)
  message(STATUS "Java tests disabled: Java SDK not found.")
else()
  include(UseJava)
  # FIXME: append JAVA to all_ffig_bindings once we have a test.
endif()

# Look for Lua
# FIXME: Make this less hacky, ideally using a real CMake module
execute_process(COMMAND luajit -e "print('testing')" 
                RESULT_VARIABLE result 
                OUTPUT_QUIET 
                ERROR_QUIET)
if(result)
  message(STATUS "Lua tests disabled: luajit cannot execute a simple Lua script.")
else()
  set(LuaJIT_FOUND 1)
  set(LuaJIT_EXECUTABLE "luajit")
  # FIXME: Get Lua bindings working well enough to work with Shape classes and 
  # add LUA to all_ffig_bindings.
endif()

# Look for C#
# FIXME: Make this less hacky, ideally using a real CMake module
execute_process(COMMAND dotnet --version 
                RESULT_VARIABLE result 
                OUTPUT_QUIET 
                ERROR_QUIET)
if(result)
  message(STATUS "Dotnet tests disabled: dotnet executable not found.")
else()
  set(dotnet_FOUND 1)
  configure_file(${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/ffig.net.csproj.in 
                 ${CMAKE_CURRENT_BINARY_DIR}/generated/ffig.net.csproj)
  list(APPEND all_ffig_bindings "DOTNET")
endif()


# Set FFIG_SOURCE so that FFIG-targets are sensitive to changes in FFIG code and templates.
# The variable FFIG_SOURCE is used by ffig.cmake and is only needed when developing FFIG.
file(GLOB_RECURSE FFIG_SOURCE ${CMAKE_CURRENT_LIST_DIR}/ffig/*)

# Add FFIG build targets
ffig_add_library(NAME Shape 
                 INPUTS tests/input/Shape.h 
                 ${all_ffig_bindings})

ffig_add_library(NAME Tree 
                 INPUTS tests/input/Tree.h 
                 CPP 
                 D 
                 DOTNET
                 NOEXCEPT 
                 PYTHON 
                 SWIFT)

ffig_add_library(NAME Asset 
                 INPUTS tests/input/Asset.h 
                 LUA
                 PYTHON
                 JAVA)

ffig_add_library(NAME Animal 
                 INPUTS tests/input/Animal.h 
                 PYTHON)

ffig_add_library(NAME Number
                 INPUTS tests/input/Number.h
                 DOTNET
                 PYTHON)

enable_testing()
add_subdirectory(tests/src)

# FIXME: Run custom clang tests until clang 5 is commonly available.
# clang 5 has our changes to cindex.py that enable Python3 support.

add_test(
  NAME test_cppmodel
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_CURRENT_LIST_DIR}/tests/cppmodel
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/ffig)
set_property(TEST test_cppmodel 
  PROPERTY LABELS INFRASTRUCTURE)

add_test(
  NAME test_python_bindings
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_CURRENT_LIST_DIR}/tests
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_python_bindings 
             PROPERTY LABELS PYTHON)

add_test(
  NAME test_cpp_mocks
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestShapeMocks
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_mocks 
             PROPERTY LABELS MOCKS)

add_test(
  NAME test_cpp_circle
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestCppCircle
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_circle 
             PROPERTY LABELS CPP)

add_test(
  NAME test_tree_capi
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestTreeCAPI
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_tree_capi 
             PROPERTY LABELS C)

add_test(
  NAME test_number_capi
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestNumberCAPI
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_number_capi 
             PROPERTY LABELS C)

add_test(
  NAME test_cpp_tree
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestCppTree
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_cpp_tree 
             PROPERTY LABELS CPP)

if(dotnet_FOUND)
  include(dotnet)
  set(CMAKE_DOTNET_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  add_dotnet_library(NAME ffig.net 
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated
    SOURCES 
      ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestNumber.cs 
      ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestShape.cs 
      ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestTree.cs 
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Number.cs 
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.cs
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.cs 
  )

  add_test(
    NAME test_dotnet_shape_output
    COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Shape.cs.expected
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.cs)
  set_property(TEST test_dotnet_shape_output 
               PROPERTY LABELS DOTNET TEXT)

  add_test(
    NAME test_dotnet_tree_output
    COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
    ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.cs.expected
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.cs)
  set_property(TEST test_dotnet_tree_output 
               PROPERTY LABELS DOTNET TEXT)

  add_test(
    NAME test_dotnet
    COMMAND dotnet test --no-build --no-restore -o .
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_dotnet 
               PROPERTY LABELS DOTNET)
  set_property(TEST test_dotnet 
               PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

if(Java_FOUND)
  set(FFIG_JAR_PATH ${CMAKE_CURRENT_SOURCE_DIR}/externals/ffig-jars)

  find_jar(JNA_JAR NAMES jna jna-4.5.1 PATHS ${FFIG_JAR_PATH})
  if(NOT JNA_JAR)
    message(FATAL_ERROR 
      "Could NOT find JNA library. "
      "Run git submodules update --init to get JARs")
  endif()
  
  find_jar(JUNIT_JAR NAMES junit junit-4.12 PATHS ${FFIG_JAR_PATH})
  if(NOT JUNIT_JAR)
    message(FATAL_ERROR 
      "Could NOT find JUnit library. "
      "Run git submodules update --init to get JARs")
  endif()
  
  find_jar(HAMCREST_JAR NAMES hamcrest hamcrest-all-1.3 PATHS ${FFIG_JAR_PATH})
  if(NOT HAMCREST_JAR)
    message(FATAL_ERROR 
      "Could NOT find Hamcrest library. "
      "Run git submodules update --init to get JARs")
  endif()

  # FIXME: Move JAR creation to ffig.cmake - requires passing JAR_PATH.
  add_jar(Asset 
          ${CMAKE_CURRENT_BINARY_DIR}/generated/Asset.java 
          OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated
          INCLUDE_JARS ${JNA_JAR})

  add_jar(TestAsset 
          tests/java/TestAsset.java 
          OUTPUT_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated
          INCLUDE_JARS 
            ${JNA_JAR} 
            ${JUNIT_JAR} 
            ${CMAKE_CURRENT_BINARY_DIR}/generated/Asset.jar)

  set(JAVA_JARS "")
  list(APPEND JAVA_JARS
       ${JNA_JAR}
       ${JUNIT_JAR}
       ${HAMCREST_JAR}
       ${CMAKE_CURRENT_BINARY_DIR}/generated/Asset.jar
       ${CMAKE_CURRENT_BINARY_DIR}/generated/TestAsset.jar)

  if(WIN32)
    set(SEPARATOR ";")
  else()
    set(SEPARATOR ":")
  endif()

  set(JAVA_CLASSPATH $<JOIN:${JAVA_JARS},${SEPARATOR}>)

  add_test(
    NAME test_java_asset
    COMMAND echo ${Java_JAVA_EXECUTABLE} -classpath ${JAVA_CLASSPATH} org.junit.runner.JUnitCore TestAsset
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_java_asset 
    PROPERTY LABELS JAVA)
  set_property(TEST test_java_asset 
                PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

add_test(
  NAME test_d_tree_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.d.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.d)
set_property(TEST test_d_tree_output 
             PROPERTY LABELS D TEXT)

add_test(
  NAME test_swift_tree_output
  COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/scripts/pydiff.py
  ${CMAKE_CURRENT_LIST_DIR}/tests/expected_output/Tree.swift.expected
  ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.swift)
set_property(TEST test_swift_tree_output 
             PROPERTY LABELS SWIFT TEXT)
             

if(LuaJIT_FOUND)
  # FIXME: The relative paths here (and in the lua test file) are very brittle.
  add_test(
    NAME test_asset_lua
    COMMAND ${LuaJIT_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/tests/test_asset_bindings.lua
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_asset_lua 
               PROPERTY LABELS LUA)
  set_property(TEST test_asset_lua 
               PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

if(Ruby_FOUND)
  add_test(
    NAME test_ruby_bindings
    COMMAND ${RUBY_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/tests/TestShape.rb
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_ruby_bindings PROPERTY LABELS RUBY)
endif()

if(Go_FOUND AND NOT WIN32)
  add_subdirectory(tests/go)
endif()
