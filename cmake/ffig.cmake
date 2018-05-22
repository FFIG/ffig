# ffig_add_library
# ----------------
#
# This module defines a function that allows the user to add a build target
# that constructs a shared library with a C-API and optional language bindings
# that make use of the C-API. 
#
# FIXME: Make output directory user-configurable.
# Currently the generated bindings and libraries go into ${ffig_output_dir}.
#
# Usage:
#
# ffig_add_library(NAME myModuleName INPUTS myHeader.h RUBY PYTHON)
#
# This will create a build target called myModuleName_c which creates a shared library:
# * libmyModuleName.so on Linux
# * libmyModuleName.dylib on macOS
# * myModuleName.dll on Windows
#
# NAME is required, 
# FIXME: relax constraints on INPUTS
# INPUTS currently supports only a single header file (which must have only standard library includes).
#
# Optional bindings can be created by passing in any of the optional arguments:
# * RUBY - creates myModuleName.rb
# * PYTHON - creates myModuleName/{_py3.py,_py2.py,__init__.py}
# * LUA - creates myModuleName.lua (needs luajit)
# * CPP - creates myModuleName_cpp.h
# * CPP_MOCKS - creates myModuleName_mocks.h

function(ffig_add_library)
  set(options BOOST_PYTHON RUBY PYTHON CPP CPP_MOCKS GO LUA DOTNET D SWIFT JAVA)
  set(oneValueArgs NAME INPUTS)
  cmake_parse_arguments(ffig_add_library "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(module ${ffig_add_library_NAME})
  string(TOLOWER "${module}" module_lower)
  set(input ${ffig_add_library_INPUTS})

  # Always generate c-api bindings as all other bindings use them.
  set(ffig_output_dir "${CMAKE_CURRENT_BINARY_DIR}/generated")
  set(ffig_invocation "-i;${input};-m;${module};-o;${ffig_output_dir};-b;_c.h.tmpl;_c.cpp.tmpl")
  set(ffig_outputs "${ffig_output_dir}/${module}_c.h;${ffig_output_dir}/${module}_c.cpp")  

  if(ffig_add_library_DOTNET)
    set(ffig_invocation "${ffig_invocation};dotnet")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.cs")
  endif()
  if(ffig_add_library_CPP_MOCKS)
    set(ffig_invocation "${ffig_invocation};_mocks.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_mocks.h")
  endif()
  if(ffig_add_library_CPP)
    set(ffig_invocation "${ffig_invocation};_cpp.h.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}_cpp.h")
  endif()
  if(ffig_add_library_GO)
    set(ffig_invocation "${ffig_invocation};go")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/src/${module}/${module}.go")
  endif()
  if(ffig_add_library_D)
    set(ffig_invocation "${ffig_invocation};d.tmpl")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.d")
  endif()
  if(ffig_add_library_SWIFT)
    set(ffig_invocation "${ffig_invocation};swift")
    set(ffig_outputs "${ffig_outputs};${ffig_output_dir}/${module}.swift;${ffig_output_dir}/${module}-Bridging-Header.h")
  endif()

  add_custom_command(OUTPUT ${ffig_outputs}
    COMMAND ${PYTHON_EXECUTABLE} -m ffig ${ffig_invocation}
    DEPENDS ${input} ${FFIG_SOURCE}
    WORKING_DIRECTORY ${CMAKE_CURRENT_LIST_DIR}
    COMMENT "Generating FFIG bindings for ${module}: ${ffig_outputs}")

  # FIXME: This is a bit ugly. The header is copied next to the generated bindings.
  file(COPY ${input} DESTINATION ${ffig_output_dir}/)
  
  add_library(${module}_c SHARED ${input} ${ffig_output_dir}/${module}_c.h ${ffig_output_dir}/${module}_c.cpp)
  set_target_properties(${module}_c PROPERTIES 
    LIBRARY_OUTPUT_DIRECTORY ${ffig_output_dir})
  
  # FIXME: This is a bit ugly. The shared library is copied next to the generated bindings.
  # Currently needed for Windows where library goes into a Debug/Release subdirectory.
  if(WIN32)
    add_custom_command(TARGET ${module}_c
      POST_BUILD
      COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_FILE:${module}_c> ${ffig_output_dir}/)
  endif()

  #
  # Ruby bindings
  #
  if(ffig_add_library_RUBY)
    add_custom_command(
      OUTPUT ${ffig_output_dir}/${module}.rb
      COMMAND ${PYTHON_EXECUTABLE} -m ffig -i ${input} -m ${module} -o ${ffig_output_dir} -b ruby
      DEPENDS ${input} ${FFIG_SOURCE}
      WORKING_DIRECTORY ${FFIG_ROOT}
      COMMENT "Generating Ruby bindings for ${module}")
    
    add_custom_target(${module}.ffig.ruby ALL DEPENDS ${ffig_outputs};${ffig_output_dir}/${module}.rb)
  endif()
  
  #
  # Lua bindings
  #
  if(ffig_add_library_LUA)
    add_custom_command(
      OUTPUT ${ffig_output_dir}/${module}.lua
      COMMAND ${PYTHON_EXECUTABLE} -m ffig -i ${input} -m ${module} -o ${ffig_output_dir} -b lua
      DEPENDS ${input} ${FFIG_SOURCE}
      WORKING_DIRECTORY ${FFIG_ROOT}
      COMMENT "Generating LuaJIT bindings for ${module}")
    
    add_custom_target(${module}.ffig.lua ALL DEPENDS ${ffig_outputs};${ffig_output_dir}/${module}.lua)
  endif()
  
  #
  # Python bindings
  #
  if(ffig_add_library_PYTHON)
    # Run FFIG to generate Python bindings,
    # Run pycodestyle on generated Python. Ignore line-length errors,
    # as with generated code we have no control over the length of
    # type or function names supplied as input.
    add_custom_command(
      OUTPUT ${ffig_output_dir}/${module_lower}/__init__.py 
             ${ffig_output_dir}/${module_lower}/_py2.py 
             ${ffig_output_dir}/${module_lower}/_py3.py
      COMMAND ${PYTHON_EXECUTABLE} -m ffig -i ${input} -m ${module} -o ${ffig_output_dir} -b python
      COMMAND ${PYTHON_EXECUTABLE} -m pycodestyle --ignore=E501 ${ffig_output_dir}/${module_lower}
      DEPENDS ${input} ${FFIG_SOURCE}
      WORKING_DIRECTORY ${FFIG_ROOT}
      COMMENT "Generating Python bindings for ${module}")
    
    add_custom_target(${module}.ffig.python ALL 
      DEPENDS ${ffig_output_dir}/${module_lower}/__init__.py 
              ${ffig_output_dir}/${module_lower}/_py2.py 
              ${ffig_output_dir}/${module_lower}/_py3.py)
  endif()

  #
  # Java bindings
  #
  # FIXME: Do not check Java_FOUND. 
  # Requesting Java bindings with no Java SDK is user-error.
  if(ffig_add_library_JAVA AND Java_FOUND)  
    FILE(MAKE_DIRECTORY "${ffig_output_dir}/java/classes/${module}")
    
    add_custom_command(
      OUTPUT ${ffig_output_dir}/java/src/${module}/${module}CLibrary.java
      COMMAND ${PYTHON_EXECUTABLE} -m ffig -i ${input} -m ${module} 
              -o ${ffig_output_dir} -b java
      DEPENDS ${input} ${FFIG_SOURCE}
      WORKING_DIRECTORY ${FFIG_ROOT}
      COMMENT "Generating java source for ${module}")
    
    add_custom_target(${module}.ffig.java.source 
      DEPENDS ${ffig_output_dir}/java/src/${module}/${module}CLibrary.java)
  
    add_custom_command(
      OUTPUT ${ffig_output_dir}/${module}.jar
      COMMAND ${Java_JAVAC_EXECUTABLE} 
              -d ${ffig_output_dir}/java/classes/${module} 
              -cp ${FFIG_JNA_JAR_PATH}
              ${ffig_output_dir}/java/src/${module}/*.java
      COMMAND ${Java_JAR_EXECUTABLE} -cfM ${module}.jar 
              -C ${ffig_output_dir}/java/classes/${module} .
      WORKING_DIRECTORY ${ffig_output_dir}
      DEPENDS ${module}.ffig.java.source
      COMMENT "Building ${module}.jar from FFIG source bindings.")
    
    add_custom_target(${module}.ffig.java ALL 
      DEPENDS ${ffig_output_dir}/${module}.jar)
  endif()
  
  #
  # boost::python bindings
  #
  # FIXME: Do not check BOOST_PYTHON_FOUND. 
  # Requesting boost::python bindings with no boost::python libs is user-error.
  if(ffig_add_library_BOOST_PYTHON AND BOOST_PYTHON_Found)
    add_custom_command(
      OUTPUT ${ffig_output_dir}/${module}_py.cpp
      COMMAND ${PYTHON_EXECUTABLE} -m ffig -i ${input} -m ${module} 
              -o ${ffig_output_dir} -b boost_python
      DEPENDS ${input} ${FFIG_SOURCE}
      WORKING_DIRECTORY ${FFIG_ROOT}
      COMMENT "Generating boost::python source for ${module}")
    
    add_custom_target(${module}.ffig.boost_python.source 
      DEPENDS ${ffig_output_dir}/${module}_py.cpp)
  
    add_library(${module}_py SHARED 
      ${CMAKE_CURRENT_BINARY_DIR}/generated/${module}_py.cpp)
    target_include_directories(${module}_py 
      PRIVATE ${PYTHON_INCLUDE_DIRS} ${Boost_INCLUDE_DIRS})
    target_link_libraries(${module}_py ${PYTHON_LIBRARIES})
    target_link_libraries(${module}_py ${Boost_LIBRARIES})
    set_property(TARGET ${module}_py PROPERTY PREFIX "")
    if(WIN32)
      set_property(TARGET ${module}_py PROPERTY SUFFIX ".dll")
    else()
      set_property(TARGET ${module}_py PROPERTY SUFFIX ".so")
    endif()

    set_target_properties(${module}_py PROPERTIES 
      LIBRARY_OUTPUT_DIRECTORY ${ffig_output_dir})
  endif()

endfunction()

