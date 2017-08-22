#define CATCH_CONFIG_MAIN // This tells Catch to provide a main() - only do this
                          // in one cpp file
#include "Tree_c.h"
#include <catch.hpp>
#include <string>

TEST_CASE("Test data mutability", "[Tree_CAPI]")
{
  Tree_Tree root = Tree_Tree_create_noexcept(3);

  Tree_Tree_set_data_noexcept(root, 42);

  REQUIRE(Tree_Tree_data_noexcept(root) == 42);

  Tree_Tree_dispose(root);
}

TEST_CASE("Test left subtree access", "[Tree_CAPI]")
{
  Tree_Tree root = Tree_Tree_create_noexcept(3);
  Tree_Tree left = Tree_Tree_left_subtree_noexcept(root);

  Tree_Tree_set_data_noexcept(left, 42);
  REQUIRE(Tree_Tree_data_noexcept(left) == 42);

  Tree_Tree_dispose(root);
  Tree_Tree_dispose(left);
}

TEST_CASE("Test right subtree access", "[Tree_CAPI]")
{
  Tree_Tree root = Tree_Tree_create_noexcept(3);
  Tree_Tree right = Tree_Tree_right_subtree_noexcept(root);

  Tree_Tree_set_data_noexcept(right, 42);
  REQUIRE(Tree_Tree_data_noexcept(right) == 42);


  Tree_Tree_dispose(root);
  Tree_Tree_dispose(right);
}

TEST_CASE("Test left subtree lifetime extension", "[Tree_CAPI]")
{
  Tree_Tree root = Tree_Tree_create_noexcept(3);
  Tree_Tree left = Tree_Tree_left_subtree_noexcept(root);

  // this will invalidate `left` unless the `root` object created above has had
  // its lifetime extended by the creation of `left`.
  Tree_Tree_dispose(root);

  Tree_Tree_set_data_noexcept(left, 42);
  REQUIRE(Tree_Tree_data_noexcept(left) == 42);


  Tree_Tree_dispose(left);
}

TEST_CASE("Test right subtree lifetime extension", "[Tree_CAPI]")
{
  Tree_Tree root = Tree_Tree_create_noexcept(3);
  Tree_Tree right = Tree_Tree_right_subtree_noexcept(root);

  // this will invalidate `right` unless the `root` object created above has had
  // its lifetime extended by the creation of `right`.
  Tree_Tree_dispose(root);

  Tree_Tree_set_data_noexcept(right, 42);
  REQUIRE(Tree_Tree_data_noexcept(right) == 42);


  Tree_Tree_dispose(right);
}
