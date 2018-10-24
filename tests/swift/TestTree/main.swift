// FIXME(jbcoe): Use a proper Swift test framework.
import Foundation                                                                                                                                                                
import Tree

var t = Tree(1)

//
// Test that depth is as constructed
//
if t.left_subtree() == nil { 
  print("Tree is missing a left subtree")
  exit(-1)
}

if t.left_subtree()!.left_subtree() != nil { 
  print("Tree has an unexpected a left-left sub-subtree")
  exit(-1)
}

if t.right_subtree() == nil { 
  print("Tree is missing a right subtree")
  exit(-1)
}

if t.right_subtree()!.right_subtree() != nil { 
  print("Tree has an unexpected a right-right sub-subtree")
  exit(-1)
}

//
// Test that data is as set
//
t.set_data(82)

if t.data() != 82 {
  print("Tree data is not as set")
  exit(-1)
}

//
// Test lifetime extension
//
let left = t.left_subtree()!
t = Tree(1)

// If root lifetime was not extended then this would access invalid memory
left.set_data(42);
if left.data() != 42 {
  print("Left subtree data is not as set")
  exit(-1)
}
