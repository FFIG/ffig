add_test(
    NAME test_go_Shape
    COMMAND ${CMAKE_COMMAND} -E env "GOPATH=${CMAKE_BINARY_DIR}/generated" go test
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})
set_property(TEST test_go_Shape PROPERTY LABELS GO)
