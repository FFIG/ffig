add_custom_target(test_Shape
    ALL
    SOURCES test_Shape.go
    COMMAND ${CMAKE_COMMAND} -E env "GOPATH=${CMAKE_BINARY_DIR}/generated" go build ${CMAKE_CURRENT_SOURCE_DIR}/test_Shape.go)

