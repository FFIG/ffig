package gotests

import (
    "Shape"
    "math"
    "testing"
)

const tolerance = 1e-11

func Test_Circle(t *testing.T) {
    s, err := Shape.AbstractShape_Circle_create(5.0)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    area, err := Shape.AbstractShape_area(s)
    if (err) {
        t.Error(`Failed to call Shape.AbstractShape_area()`)
    }
    if math.Abs(area - (5.0 * 5.0 * math.Pi)) > tolerance {
        t.Error(`Shape.AbstractShape_area() does not match expectation`)
    }
}

