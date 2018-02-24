function(add_dotnet_library)
  set(oneValueArgs NAME DIRECTORY)
  set(multiValueArgs SOURCES)
  cmake_parse_arguments(add_dotnet_library "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(NAME ${add_dotnet_library_NAME})
  set(DIRECTORY ${add_dotnet_library_DIRECTORY})
  set(SOURCES ${add_dotnet_library_SOURCES})

  if(NOT CMAKE_DOTNET_OUTPUT_DIRECTORY)
    set(CMAKE_DOTNET_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dotnet.output/${NAME})
  endif() 
  file(MAKE_DIRECTORY ${CMAKE_DOTNET_OUTPUT_DIRECTORY})
  
  # FIXME: avoid the need to copy source to a special location by redirecting obj output
  set(CMAKE_DOTNET_INTERMEDIATE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dotnet.intermediate/${NAME})
  file(MAKE_DIRECTORY ${CMAKE_DOTNET_INTERMEDIATE_DIRECTORY})

  set(OUTPUT ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME}.dll)
  set(CSPROJ ${NAME}.csproj)

  set(DEPENDENCIES
    ${SOURCES}
    ${DIRECTORY}/${CSPROJ}
  )

  add_custom_command(OUTPUT ${OUTPUT} 
    COMMAND ${CMAKE_COMMAND} -E copy
      ${DIRECTORY}/${CSPROJ}
      ${CMAKE_DOTNET_INTERMEDIATE_DIRECTORY}
    COMMAND ${CMAKE_COMMAND} -E copy
      ${SOURCES}
      ${CMAKE_DOTNET_INTERMEDIATE_DIRECTORY}
    COMMAND dotnet build ${CSPROJ} -o ${CMAKE_DOTNET_OUTPUT_DIRECTORY}
    DEPENDS ${DEPENDENCIES}
    WORKING_DIRECTORY ${CMAKE_DOTNET_INTERMEDIATE_DIRECTORY}
    COMMENT "Building DOTNET assembly ${NAME}.dll"
  )

  add_custom_target(${NAME} ALL 
    DEPENDS ${OUTPUT})

endfunction()
