# Utility functions for CMake used by FFIG.

# Set the shared library path for test execution.
function(set_test_shared_library_path)
  set(options)
  set(multiValueArgs)
  set(oneValueArgs TEST_NAME DLL_PATH)
  cmake_parse_arguments(set_test_shared_library_path "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(TEST_NAME ${set_test_shared_library_path_TEST_NAME})
  set(DLL_PATH ${set_test_shared_library_path_DLL_PATH})

  if(WIN32)
    set_property(TEST ${TEST_NAME} 
      PROPERTY ENVIRONMENT "PATH=${DLL_PATH}\;%PATH%")
  else()
    set_property(TEST ${TEST_NAME} 
      PROPERTY ENVIRONMENT "LD_LIBRARY_PATH=${DLL_PATH}:$LD_LIBRARY_PATH")
  endif()
endfunction()

