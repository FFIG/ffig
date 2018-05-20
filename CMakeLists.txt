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
include(utils)

include_directories(externals/catch2/single_include)
include_directories(externals/variant/include)
# FIXME: Use FFIG to get this path.
include_directories(ffig/include)

# Detect Python if it's not user-specified.
if(NOT PYTHON_EXECUTABLE)
  find_package(PythonInterp REQUIRED)
else()
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import this"
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    message(FATAL_ERROR "CMake failed: ${PYTHON_EXECUTABLE} cannot execute a simple Python script.")
  endif()
endif()

# Robustly detect Python version
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import sys; sys.exit(sys.version_info[0])"
  RESULT_VARIABLE result
  OUTPUT_QUIET
  ERROR_QUIET)
set(PYTHON_VERSION_MAJOR ${result})
# Check that the found version of Python==3 on Windows.
# FIXME: Get to the bottom of the libclang/ctypes issues with Python2 on Windows.
if(WIN32)
  if(NOT ${PYTHON_VERSION_MAJOR} STREQUAL 3)
    message(FATAL_ERROR "CMake failed: Python 3 is required for Windows.")
  endif()
endif()

# FFIG won't work without Python and a C++ compiler so we can assume
# support for Python and C++ must exist.
set(all_ffig_bindings "PYTHON;CPP;CPP_MOCKS;BOOST_PYTHON")

# Look for Go
# FIXME: Make this less hacky, ideally using a real CMake module
if(NOT FFIG_DISABLE_GO)
  execute_process(COMMAND go version
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    if(FFIG_REQUIRE_GO)
      message(FATAL_ERROR "CMake failed: Go not found but is required by this build.")
    endif()
    set(Go_FOUND FALSE)
    message(STATUS "Go tests disabled: Go compiler not found.")
  else()
    if(NOT FFIG_REQUIRE_GO)
      message(STATUS "Found Go. Generating Go bindings.")
    endif()
    set(Go_FOUND True)
    list(APPEND all_ffig_bindings "GO")
  endif()
endif()

# Look for Swift
if(NOT FFIG_DISABLE_SWIFT)
  execute_process(COMMAND swiftc --version
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    if(FFIG_REQUIRE_SWIFT)
      message(FATAL_ERROR "CMake failed: swiftc not found but is required by this build.")
    endif()
    set(Swift_FOUND FALSE)
    message(STATUS "Swift tests disabled: Swift compiler not found.")
  else()
    if(NOT FFIG_REQUIRE_SWIFT)
      message(STATUS "Found Swift. Generating Swift bindings.")
    endif()
    set(Swift_FOUND True)
    list(APPEND all_ffig_bindings "SWIFT")
  endif()
endif()

# Look for Ruby
if(NOT FFIG_DISABLE_RUBY)
  find_package(Ruby)
  if(NOT Ruby_FOUND)
    if(FFIG_REQUIRE_RUBY)
      message(FATAL_ERROR "CMake failed: Ruby not found but is required by this build.")
    endif()
    message(STATUS "Ruby tests disabled: Ruby interpreter not found.")
  else()
    execute_process(COMMAND ${RUBY_EXECUTABLE} -rffi -e "puts FFI"
                    RESULT_VARIABLE result
                    OUTPUT_QUIET
                    ERROR_QUIET)
    if(result)
      message(WARNING "CMake failed: Ruby FFI dependencies is required.  Run 'gem install ffi' to install FFI dependency")
    else()
      if(NOT FFIG_REQUIRE_RUBY)
        message(STATUS "Found Ruby. Generating Ruby bindings.")
      endif()
      list(APPEND all_ffig_bindings "RUBY")
    endif()
  endif()
endif()

# Look for Java
if(NOT FFIG_DISABLE_JAVA)
  find_package(Java)
  find_package(Java COMPONENTS Runtime)
  find_package(Java COMPONENTS Development)
  if(NOT Java_FOUND)
    if(FFIG_REQUIRE_JAVA)
      message(FATAL_ERROR "CMake failed: Java SDK not found but is required by this build.")
    endif()
    message(STATUS "Java tests disabled: Java SDK not found.")
  else()
    if(NOT FFIG_REQUIRE_JAVA)
      message(STATUS "Found Java SDK. Generating Java bindings.")
    endif()
    include(UseJava)
    # FIXME: append JAVA to all_ffig_bindings once we have a test.
  endif()
endif()

# Look for Lua
# FIXME: Make this less hacky, ideally using a real CMake module
if(NOT FFIG_DISABLE_LUA)
  execute_process(COMMAND luajit -e "print('testing')"
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    if(FFIG_REQUIRE_LUA)
      message(FATAL_ERROR "CMake failed: luajit not found but is required by this build.")
    endif()
    message(STATUS "Lua tests disabled: luajit cannot execute a simple Lua script.")
  else()
    if(NOT FFIG_REQUIRE_LUA)
      message(STATUS "Found luajit. Generating Lua bindings.")
    endif()
    set(LuaJIT_FOUND 1)
    set(LuaJIT_EXECUTABLE "luajit")
    # FIXME: Get Lua bindings working well enough to work with Shape classes and
    # add LUA to all_ffig_bindings.
  endif()
endif()

# Look for C#
# FIXME: Make this less hacky, ideally using a real CMake module
if(NOT FFIG_DISABLE_DOTNET)
  execute_process(COMMAND dotnet --version
                  RESULT_VARIABLE result
                  OUTPUT_QUIET
                  ERROR_QUIET)
  if(result)
    if(FFIG_REQUIRE_DOTNET)
      message(FATAL_ERROR "CMake failed: dotnet executable not found but is required by this build.")
    endif()
    message(STATUS "Dotnet tests disabled: dotnet executable not found.")
  else()
    if(NOT FFIG_REQUIRE_DOTNET)
      message(STATUS "Found dotnet executable. Generating dotnet bindings.")
    endif()
    set(dotnet_FOUND 1)
    list(APPEND all_ffig_bindings "DOTNET")
  endif()
endif()

# Look for Boost Python - needs Python libs and Boost.
if(NOT FFIG_DISABLE_BOOST_PYTHON)
  find_package(PythonLibs)
  if(NOT PythonLibs_FOUND)
    if(FFIG_REQUIRE_BOOST_PYTHON)
      message(FATAL_ERROR "CMake failed: Python libraries not found but are required by this build.")
    else()  
      message(STATUS "boost::python tests disabled: Python libraries not found.")
    endif()
  else()
    if(${PYTHON_VERSION_MAJOR} STREQUAL "3")
      find_package(Boost COMPONENTS python36)
    else()
      find_package(Boost COMPONENTS python)
    endif()
    if(NOT Boost_FOUND)
      if(FFIG_REQUIRE_BOOST_PYTHON)
        message(FATAL_ERROR "CMake failed: Boost libraries not found but are required by this build.")
      else()  
        message(STATUS "boost::python tests disabled: Boost libraries not found.")
      endif()
    else()
      message(STATUS "Found boost::python. Generating boost::python bindings.")
      list(APPEND all_ffig_bindings "BOOST_PYTHON")
      set(BOOST_PYTHON_Found 1)
    endif()
  endif()
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
  NAME test_ffig
  COMMAND ${PYTHON_EXECUTABLE} -m nose -v ${CMAKE_CURRENT_LIST_DIR}/tests/ffig
  WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/ffig)
set_property(TEST test_ffig
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
  NAME test_capi_tree
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestTreeCAPI
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_capi_tree
             PROPERTY LABELS C)

add_test(
  NAME test_capi_number
  COMMAND ${CMAKE_CURRENT_BINARY_DIR}/tests/src/TestNumberCAPI
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
set_property(TEST test_capi_number
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

  add_dotnet_project(NAME Shape.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/Shape
    SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.cs
  )

  add_dotnet_project(NAME Tree.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/Tree
    SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.cs
  )

  add_dotnet_project(NAME Number.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/Number
    SOURCES
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Number.cs
  )

  add_dotnet_project(NAME TestShape.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestShape
    SOURCES
    ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestShape/TestShape.cs
  )
  add_dependencies(TestShape.net Shape.net)

  add_dotnet_project(NAME TestNumber.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestNumber
    SOURCES
    ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestNumber/TestNumber.cs
  )
  add_dependencies(TestNumber.net Number.net)

  add_dotnet_project(NAME TestTree.net
    DIRECTORY ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestTree
    SOURCES
    ${CMAKE_CURRENT_LIST_DIR}/tests/dotnet/TestTree/TestTree.cs
  )
  add_dependencies(TestTree.net Tree.net)

  add_test(
    NAME test_dotnet_shape
    COMMAND dotnet test --no-build --no-restore -o .
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/TestShape.net)
  set_property(TEST test_dotnet_shape
               PROPERTY LABELS DOTNET)
  set_test_shared_library_path(
    TEST_NAME test_dotnet_shape 
    DLL_PATH ${CMAKE_CURRENT_BINARY_DIR}/generated)

  add_test(
    NAME test_dotnet_number
    COMMAND dotnet test --no-build --no-restore -o .
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/TestNumber.net)
  set_property(TEST test_dotnet_number
               PROPERTY LABELS DOTNET)
  set_test_shared_library_path(
    TEST_NAME test_dotnet_number 
    DLL_PATH ${CMAKE_CURRENT_BINARY_DIR}/generated)

  add_test(
    NAME test_dotnet_tree
    COMMAND dotnet test --no-build --no-restore -o .
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/TestTree.net)
  set_property(TEST test_dotnet_tree
               PROPERTY LABELS DOTNET)
  set_test_shared_library_path(
    TEST_NAME test_dotnet_tree 
    DLL_PATH ${CMAKE_CURRENT_BINARY_DIR}/generated)

endif()

if(Swift_FOUND)

  set(SWIFT_TREE_MODULE ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Tree)
  add_custom_command(
    OUTPUT ${SWIFT_TREE_MODULE}
    COMMAND swiftc ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.swift
      -import-objc-header ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree-Bridging-Header.h
      -Xcc -I${CMAKE_CURRENT_LIST_DIR}/ffig/include/
      -L${CMAKE_CURRENT_BINARY_DIR}/generated/
      -lTree_c
      -emit-module
      -emit-module-path ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Tree.swiftmodule
      -emit-library
      -module-name Tree
      -o ${SWIFT_TREE_MODULE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated
    DEPENDS Tree_c
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree-Bridging-Header.h
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Tree.swift)
  add_custom_target(SwiftTree ALL DEPENDS ${SWIFT_TREE_MODULE})

  set(SWIFT_TREE_TEST ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/TreeTest)
  add_custom_command(
    OUTPUT ${SWIFT_TREE_TEST}
    COMMAND swiftc ${CMAKE_CURRENT_LIST_DIR}/tests/swift/TestTree/main.swift
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Tree
    -I${CMAKE_CURRENT_BINARY_DIR}/generated/Swift
    -L${CMAKE_CURRENT_BINARY_DIR}/generated
    -lTree_c
    -o ${SWIFT_TREE_TEST}
    DEPENDS Tree_c ${SWIFT_TREE_MODULE}
      ${CMAKE_CURRENT_LIST_DIR}/tests/swift/TestTree/main.swift)
  add_custom_target(SwiftTreeTest ALL DEPENDS ${SWIFT_TREE_TEST})

  add_test(
    NAME test_swift_tree
    COMMAND ./TreeTest
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift)
  set_property(TEST test_swift_tree
    PROPERTY LABELS SWIFT)
  set_property(TEST test_swift_tree
               PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")


  set(SWIFT_SHAPE_MODULE ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Shape)
  add_custom_command(
    OUTPUT ${SWIFT_SHAPE_MODULE}
    COMMAND swiftc ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.swift
      -import-objc-header ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape-Bridging-Header.h
      -Xcc -I${CMAKE_CURRENT_LIST_DIR}/ffig/include/
      -L${CMAKE_CURRENT_BINARY_DIR}/generated/
      -lShape_c
      -emit-module
      -emit-module-path ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Shape.swiftmodule
      -emit-library
      -module-name Shape
      -o ${SWIFT_SHAPE_MODULE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated
    DEPENDS Shape_c
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape-Bridging-Header.h
      ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape.swift)
  add_custom_target(SwiftShape ALL DEPENDS ${SWIFT_SHAPE_MODULE})

  set(SWIFT_SHAPE_TEST ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/ShapeTest)
  add_custom_command(
    OUTPUT ${SWIFT_SHAPE_TEST}
    COMMAND swiftc ${CMAKE_CURRENT_LIST_DIR}/tests/swift/TestShape/main.swift
    ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift/Shape
    -I${CMAKE_CURRENT_BINARY_DIR}/generated/Swift
    -L${CMAKE_CURRENT_BINARY_DIR}/generated
    -lShape_c
    -o ${SWIFT_SHAPE_TEST}
    DEPENDS Shape_c ${SWIFT_SHAPE_MODULE}
      ${CMAKE_CURRENT_LIST_DIR}/tests/swift/TestShape/main.swift)
  add_custom_target(SwiftShapeTest ALL DEPENDS ${SWIFT_SHAPE_TEST})

  add_test(
    NAME test_swift_shape
    COMMAND ./ShapeTest
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated/Swift)
  set_property(TEST test_swift_shape
    PROPERTY LABELS SWIFT)
  set_property(TEST test_swift_shape
               PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${CMAKE_CURRENT_BINARY_DIR}/generated")
endif()

if(Java_FOUND)
  set(FFIG_JAR_PATH ${CMAKE_CURRENT_SOURCE_DIR}/externals/ffig-jars)

  find_jar(JNA_JAR NAMES jna jna-4.5.1 PATHS ${FFIG_JAR_PATH})
  if(NOT JNA_JAR)
    message(FATAL_ERROR
      "Could NOT find JNA library. "
      "Run git submodule update --init to get JARs")
  endif()

  find_jar(JUNIT_JAR NAMES junit junit-4.12 PATHS ${FFIG_JAR_PATH})
  if(NOT JUNIT_JAR)
    message(FATAL_ERROR
      "Could NOT find JUnit library. "
      "Run git submodule update --init to get JARs")
  endif()

  find_jar(HAMCREST_JAR NAMES hamcrest hamcrest-all-1.3 PATHS ${FFIG_JAR_PATH})
  if(NOT HAMCREST_JAR)
    message(FATAL_ERROR
      "Could NOT find Hamcrest library. "
      "Run git submodule update --init to get JARs")
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

if(LuaJIT_FOUND)
  # FIXME: The relative paths here (and in the lua test file) are very brittle.
  add_test(
    NAME test_lua_asset
    COMMAND ${LuaJIT_EXECUTABLE} ${CMAKE_CURRENT_LIST_DIR}/tests/test_asset_bindings.lua
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_lua_asset
               PROPERTY LABELS LUA)
  set_property(TEST test_lua_asset
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

if(BOOST_PYTHON_Found)
  add_library(Shape_py SHARED ${CMAKE_CURRENT_BINARY_DIR}/generated/Shape_py.cpp)
  target_include_directories(Shape_py PRIVATE ${PYTHON_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})
  target_link_libraries(Shape_py ${PYTHON_LIBRARIES})
  target_link_libraries(Shape_py ${Boost_LIBRARIES})
  set_property(TARGET Shape_py PROPERTY PREFIX "")
  if(WIN32)
    set_property(TARGET Shape_py PROPERTY SUFFIX ".dll")
  else()
    set_property(TARGET Shape_py PROPERTY SUFFIX ".so")
  endif()

  add_custom_command(TARGET Shape_py
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:Shape_py> ${CMAKE_CURRENT_BINARY_DIR}/generated)

  # FIXME: Use the existing Python tests with boost::python.
  add_test(
    NAME test_boost_python_bindings
    COMMAND python -c "import Shape_py; c = Shape_py.Circle(3); print('A %s with radius 3 has area %f' % (c.name, c.area))"
    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/generated)
  set_property(TEST test_boost_python_bindings PROPERTY LABELS BOOST_PYTHON)
endif()

