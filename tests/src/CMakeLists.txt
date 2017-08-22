include_directories(
  ${CMAKE_SOURCE_DIR}/externals/catch/include/ 
  ${CMAKE_SOURCE_DIR}/externals/variant/include 
  ${CMAKE_BINARY_DIR}/generated
)

add_executable(TestCppTree TestCppTree.cpp)
target_link_libraries(TestCppTree Tree_c)

add_executable(TestTreeCAPI TestTreeCAPI.cpp)
target_link_libraries(TestTreeCAPI Tree_c)

add_executable(TestCppCircle TestCppCircle.cpp)
target_link_libraries(TestCppCircle Shape_c)

add_executable(TestShapeMocks TestShapeMocks.cpp)
add_dependencies(TestShapeMocks Shape_c)
