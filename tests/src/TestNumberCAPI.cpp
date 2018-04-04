#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this
                          // in one cpp file
#include "Number_c.h"
#include <catch.hpp>
#include <string>

TEST_CASE("Test hoist-to heap of objects returned by value", "[Number_CAPI]")
{
  Number_Number p;
  auto rc = Number_Number_create(8, &p);
  REQUIRE(rc == Number_RC_SUCCESS);

  int v = 0;
  Number_Number_value(p, &v);
  CHECK(v == 8);

  Number_Number p_next;
  rc = Number_Number_next(p, &p_next);
  REQUIRE(rc == Number_RC_SUCCESS);
  
  v = 0;
  Number_Number_value(p_next, &v);
  CHECK(v == 9);

  Number_Number_dispose(p);
  Number_Number_dispose(p_next);
}


