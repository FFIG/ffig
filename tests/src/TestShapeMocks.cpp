#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this
                          // in one cpp file
#include <catch.hpp>
#include <string>
#include "Shape_mocks.h"

TEST_CASE("MockShape", "[mocks::Shape]")
{
  GIVEN("A mock shape with no expected values set")
  {
    mocks::Shape shape;

    THEN("All method invocations lead to exceptions")
    {
      REQUIRE_THROWS_AS(shape.name(),
                        mocks::Shape::MockMethodResultNotSpecified);

      REQUIRE_THROWS_AS(shape.area(),
                        mocks::Shape::MockMethodResultNotSpecified);

      REQUIRE_THROWS_AS(shape.perimeter(),
                        mocks::Shape::MockMethodResultNotSpecified);

      REQUIRE_THROWS_AS(shape.is_equal(&shape),
                        mocks::Shape::MockMethodResultNotSpecified);
    }
  }

  GIVEN("A mock shape with expected values set")
  {
    mocks::Shape shape;
    shape.area_ = 10;
    shape.perimeter_ = 25;
    shape.name_ = "Mock";
    shape.is_equal_ = false;

    THEN("All method invocations return expected values")
    {
      REQUIRE(shape.area() == 10);
      REQUIRE(shape.is_equal(nullptr) == false);
      REQUIRE(strcmp(shape.name(), "Mock")==0);
      REQUIRE(shape.perimeter() == 25);
    }
  }
}
