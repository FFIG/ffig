from Tree import *

def test_root_node_is_non_null():
    t = Tree(2)
    assert(t)
    assert(t.data)

def test_left_node_is_non_null():
    t = Tree(2)
    lt = t.left
    assert(lt)
    assert(lt.data)

def test_right_node_is_non_null():
    t = Tree(2)
    rt = t.right
    assert(rt)
    assert(rt.data)

def test_right_3_node_is_null():
    t = Tree(2)
    r3t = t.right.right.right
    assert(r3t==None)

def test_use_of_null_node_is_caught():
    t = Tree(2)
    r3t = t.right.right.right
    error_thrown = False
    try:
        r3t.data
    except Exception as e:
        error_thrown = True
    assert(error_thrown)

def test_subtree_handle_keeps_tree_alive():
    t = Tree(1)
    st = t.left
    x = st.data
    del t
    assert(st.data==x)

def test_tree_count_incremented_on_construction():
    assert(Tree.count() == 0)
    t = Tree(0)
    print "test_tree_count_decremented_on_destruction {}".format(Tree.count())
    assert(Tree.count() == 1)

def test_tree_count_decremented_on_destruction():
    t = Tree(0)
    assert(Tree.count() == 1)
    del t
    assert(Tree.count() == 0) # this depends on Python using reference counting

def test_subtree_handle_does_not_change_count():
    t = Tree(1)
    assert(Tree.count() == 3)
    rt = t.right
    assert(Tree.count() == 3)

def test_tree_count_is_preserved_by_active_subtree_handle():
    t = Tree(1)
    assert(Tree.count() == 3)
    rt = t.right
    del t
    assert(Tree.count() == 3)

