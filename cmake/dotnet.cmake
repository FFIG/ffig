function(add_dotnet_project)
  set(oneValueArgs NAME DIRECTORY)
  set(multiValueArgs SOURCES)
  cmake_parse_arguments(add_dotnet_project "${options}" "${oneValueArgs}" "${multiValueArgs}" ${ARGN})

  set(NAME ${add_dotnet_project_NAME})
  set(DIRECTORY ${add_dotnet_project_DIRECTORY})
  set(SOURCES ${add_dotnet_project_SOURCES})

  if(NOT CMAKE_DOTNET_OUTPUT_DIRECTORY)
    set(CMAKE_DOTNET_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/dotnet.output)
  endif() 
  file(MAKE_DIRECTORY ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME})

  set(OUTPUT ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME}/${NAME}.dll)
  set(CSPROJ ${NAME}.csproj)

  set(DEPENDENCIES
    ${SOURCES}
    ${DIRECTORY}/${CSPROJ}
  )

  add_custom_command(OUTPUT ${OUTPUT} 
    COMMAND ${CMAKE_COMMAND} -E copy
      ${DIRECTORY}/${CSPROJ}
      ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME}
    COMMAND ${CMAKE_COMMAND} -E copy
      ${SOURCES}
      ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME}
    COMMAND dotnet build ${CSPROJ} -o .
    DEPENDS ${DEPENDENCIES}
    WORKING_DIRECTORY ${CMAKE_DOTNET_OUTPUT_DIRECTORY}/${NAME}
    COMMENT "Building DOTNET assembly ${NAME}.dll"
  )

  add_custom_target(${NAME} ALL 
    DEPENDS ${OUTPUT})

endfunction()
