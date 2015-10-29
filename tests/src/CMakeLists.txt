cmake_minimum_required (VERSION 3.1)
set(CMAKE_CXX_STANDARD 14) 

project (TestCppGeneratedOutput)

include_directories(../../externals/catch/include/ ../../output/)

add_executable(TestCppCircle TestCppCircle.cpp)
add_executable(TestShapeMocks TestShapeMocks.cpp)

find_library(SHAPE_C_LIBRARY NAMES Shape_c PATHS ../../output/)

target_link_libraries(TestCppCircle ${SHAPE_C_LIBRARY})

install(TARGETS TestCppCircle TestShapeMocks DESTINATION bin)
install(FILES ${SHAPE_C_LIBRARY} DESTINATION bin)
