package gotests

import (
    "Shape"
    "math"
    "testing"
)

const tolerance = 1e-11

func Test_Circle_Area(t *testing.T) {
    r := 5.0
    s, err := Shape.Circle_create(r)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    area, err := s.Area()
    if (err) {
        t.Error(`Failed to call Circle.Area()`)
    }
    if math.Abs(area - (math.Pi * r * r)) > tolerance {
        t.Error(`Circle.Area() does not match expectation`)
    }
}

func Test_Circle_Perimeter(t *testing.T) {
    r := 5.0
    s, err := Shape.Circle_create(r)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    perim, err := s.Perimeter()
    if (err) {
        t.Error(`Failed to call Circle.Perimeter()`)
    }
    if math.Abs(perim - (2.0 * math.Pi * r)) > tolerance {
        t.Error(`Circle.Perimeter() does not match expectation`)
    }
}

func Test_Circle_Is_equal(t *testing.T) {
    r := 5.0
    s, err := Shape.Circle_create(r)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    s2, err := Shape.Circle_create(r)
    if (err) {
        t.Error(`Failed to create a Circle`)
    }

    result, err := s.Is_equal(s2)
    if (err) {
        t.Error(`Failed to call Circle.Is_equal()`)
    }
    if result == 0 {
        t.Error(`Circle.Is_equal() does not match expectation (expected non-zero)`)
    }

    s3, err := Shape.Circle_create(2.0 * r)
    if err {
        t.Error(`Failed to create a Circle`)
    }

    result, err = s.Is_equal(s3)
    if result != 0 {
        t.Error(`Circle.Is_equal() does not match expectation (expected zero)`)
    }
}
