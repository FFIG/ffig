#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include <catch.hpp>
#include <string>
#include "Tree_cpp.h"

using CPP_API::Tree;

TEST_CASE("Test subtree access", "[cpp_api::tree]")
{
  auto root = Tree(3);
  auto left = root.left_subtree();
  
  REQUIRE(left.data());
}

TEST_CASE("Test lifetime extension", "[cpp_api::tree]")
{
  auto root = Tree(3);
  auto left = root.left_subtree();
  
  // this will invalidate left unless the object created above has had its lifetime extended.
  root = Tree(1); 

  REQUIRE(left.data());
}

TEST_CASE("Test move", "[cpp_api::tree]")
{
  auto root = Tree(3);
  auto data = root.left_subtree().data();
  
  auto uprooted = std::move(root);

  REQUIRE(uprooted.left_subtree().data() == data);
}

