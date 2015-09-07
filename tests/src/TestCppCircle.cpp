#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"
#include "Shape_cpp.h"
#include <string>

using CPP_API::Circle;
using namespace std::string_literals;

static const double pi = 3.14159265359;

TEST_CASE( "Unit radius circle has area pi * r * r", "[circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.area() == pi * r * r);
}

TEST_CASE( "Unit radius circle has circumference 2 * pi * r", "[circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.perimeter() == 2 * pi * r);
}

TEST_CASE( "circle has name 'circle'", "[circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.name() == "Circle"s);
}
