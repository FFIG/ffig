package gotests

import (
    "Shape"
    "math"
    "testing"
)

const tolerance = 1e-11

func Test_Circle(t *testing.T) {
    s, err := Shape.Shape_Circle_create(5.0)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    area, err := Shape.Shape_area(s)
    if (err) {
        t.Error(`Failed to call Shape.Shape_area()`)
    }
    if math.Abs(area - (5.0 * 5.0 * math.Pi)) > tolerance {
        t.Error(`Shape.Shape_area() does not match expectation`)
    }
}

