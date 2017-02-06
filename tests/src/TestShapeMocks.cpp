#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this
                          // in one cpp file
#include <catch.hpp>
#include <string>
#include <type_traits>
#include "Shape_mocks.h"

TEST_CASE("MockShape", "[mocks::MockShape]")
{
  static_assert(std::is_base_of<Shape,mocks::MockShape>::value,"");

  GIVEN("A mock shape with no expected values set")
  {
    mocks::MockShape shape;

    THEN("All method invocations lead to exceptions")
    {
      REQUIRE_THROWS_AS(shape.name(),
                        mocks::MockShape::MockMethodResultNotSpecified);

      REQUIRE_THROWS_AS(shape.area(),
                        mocks::MockShape::MockMethodResultNotSpecified);

      REQUIRE_THROWS_AS(shape.perimeter(),
                        mocks::MockShape::MockMethodResultNotSpecified);

      //REQUIRE_THROWS_AS(shape.is_equal(&shape),
      //                  mocks::MockShape::MockMethodResultNotSpecified);
    }
  }

  GIVEN("A mock shape with expected values set")
  {
    mocks::MockShape shape;
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
  
  GIVEN("A mock shape with function objects returning values")
  {
    mocks::MockShape shape;
    int area_f_count = 0;
    shape.area_ = [&area_f_count]{ ++area_f_count; return 0.0;};

    THEN("All method invocations return expected values through function invocations")
    {
      REQUIRE(shape.area() == 0.0);
      REQUIRE(area_f_count == 1);
    }
  }
}
