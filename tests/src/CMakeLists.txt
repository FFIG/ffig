cmake_minimum_required (VERSION 3.1)
set(CMAKE_CXX_STANDARD 14) 

project (TestCppGeneratedOutput)

include_directories(../../externals/catch/include/ ../../externals/variant/include ../../output/)

add_executable(TestCppTree TestCppTree.cpp)
add_executable(TestCppCircle TestCppCircle.cpp)
add_executable(TestShapeMocks TestShapeMocks.cpp)

find_library(SHAPE_C_LIBRARY NAMES Shape_c PATHS ../../output/)
find_library(TREE_C_LIBRARY NAMES Tree_c PATHS ../../output/)

target_link_libraries(TestCppCircle ${SHAPE_C_LIBRARY})

target_link_libraries(TestCppTree ${TREE_C_LIBRARY})

install(TARGETS TestCppCircle TestShapeMocks DESTINATION bin)
install(FILES ${SHAPE_C_LIBRARY} DESTINATION bin)
