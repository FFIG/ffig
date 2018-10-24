// FIXME(jbcoe): Use a proper Swift test framework.
import Foundation                                                                                                                                                                
import Shape

var c = try! Circle(2)

//
// Test that area and perimeter are related as expected
//
if c.area() != c.perimeter() {
  print("A circle with radius 2.0 should have area == perimeter (ignoring units)")
  exit(-1)
}

//
// Test that name is as expected
//
if c.name() != "Circle" { 
  print("Circle name is not \"Circle\"")
  print(c.name())
  exit(-1)
}

//
// Test that equality is implemented
//
if c.is_equal(c) != 1 { 
  print("Any shape should be equal to itself")
  exit(-1)
}

//
// Test that inequality is implemented
//
var p = try! Pentagon(1)
if p.is_equal(c) != 0 { 
  print("Shapes of different kind should not be considered equal to one another")
  exit(-1)
}

//
// Test exception
// 

let cc = try? Circle(-5) 
if cc != nil {
  print("Constructing a circle with a negative radius should be an exception")
  exit(-1)
}

