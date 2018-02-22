function(add_dotnet_library)
  set(oneValueArgs NAME DIRECTORY)
  set(multiValueArgs SOURCES)
  cmake_parse_arguments(add_dotnet_library "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(NAME ${add_dotnet_library_NAME})
  set(DIRECTORY ${add_dotnet_library_DIRECTORY})
  set(SOURCES ${add_dotnet_library_SOURCES})

  if(NOT DOTNET_OUTPUT_DIRECTORY)
    set(_DOTNET_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dotnet.output)
    set(DOTNET_OUTPUT_DIRECTORY ${_DOTNET_OUTPUT_DIRECTORY}/${NAME})
  endif() 
  file(MAKE_DIRECTORY ${DOTNET_OUTPUT_DIRECTORY})
  
  # FIXME: make this customizable
  # FIXME: avoid the need to copy source to a special location by redirecting obj output
  set(_DOTNET_INTERMEDIATE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dotnet.intermediate)
  set(DOTNET_INTERMEDIATE_DIRECTORY ${_DOTNET_INTERMEDIATE_DIRECTORY}/${NAME})
  file(MAKE_DIRECTORY ${DOTNET_INTERMEDIATE_DIRECTORY})

  set(OUTPUT ${DOTNET_OUTPUT_DIRECTORY}/${NAME}.dll)
  set(CSPROJ ${NAME}.csproj)

  set(DEPENDENCIES
    ${SOURCES}
    ${DIRECTORY}/${CSPROJ}
  )

  add_custom_command(OUTPUT ${OUTPUT} 
    COMMAND ${CMAKE_COMMAND} -E copy
      ${DIRECTORY}/${CSPROJ}
      ${DOTNET_INTERMEDIATE_DIRECTORY}
    COMMAND ${CMAKE_COMMAND} -E copy
      ${SOURCES}
      ${DOTNET_INTERMEDIATE_DIRECTORY}
    COMMAND dotnet build ${CSPROJ} -o ${DOTNET_OUTPUT_DIRECTORY}
    DEPENDS ${DEPENDENCIES}
    WORKING_DIRECTORY ${DOTNET_INTERMEDIATE_DIRECTORY}
    COMMENT "Building DOTNET assembly ${NAME}.dll"
  )

  add_custom_target(${NAME} ALL 
    DEPENDS ${OUTPUT})

endfunction()
