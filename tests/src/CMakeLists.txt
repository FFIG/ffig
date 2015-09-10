cmake_minimum_required (VERSION 3.1)
set(CMAKE_CXX_STANDARD 14) 

project (TestCppCircle)
add_executable(TestCppCircle TestCppCircle.cpp)
include_directories(../../externals/catch/include/ ../../output/)

find_library(SHAPE_C_LIBRARY NAMES Shape_c PATHS ../../output/)

target_link_libraries(TestCppCircle ${SHAPE_C_LIBRARY})

install(TARGETS TestCppCircle DESTINATION bin)
install(FILES ${SHAPE_C_LIBRARY} DESTINATION bin)
