#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include <catch.hpp>
#include <string>
#include "Shape_cpp.h"

using CPP_API::Circle;
using CPP_API::Square;
using namespace std::string_literals;

static const double pi = 3.14159265359;

TEST_CASE( "Unit radius circle has area pi * r * r", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.area() == pi * r * r);
}

TEST_CASE( "Unit radius circle has circumference 2 * pi * r", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.perimeter() == 2 * pi * r);
}

TEST_CASE( "circle has name 'circle'", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.name() == "Circle"s);
}

TEST_CASE( "circle is_equal to self", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);

  REQUIRE(c.is_equal(&c));
}

TEST_CASE( "circle is_equal to circle with same radius", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);
  const Circle c2(r);

  REQUIRE(c.is_equal(&c2));
}

TEST_CASE( "circle is not equal to circle with different radius", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);
  const Circle c2(r+1.0);

  REQUIRE(!c.is_equal(&c2));
}

TEST_CASE( "circle is not equal to square", "[cpp_api::circle]" ) {
  const double r = 1.0;
  const Circle c(r);
  const Square s(r);
  REQUIRE(!c.is_equal(&s));
}

TEST_CASE( "circle with negative radius raises exception", "[cpp_api::circle]" ) {
  REQUIRE_THROWS_AS(Circle(-1), Circle::exception);
}

