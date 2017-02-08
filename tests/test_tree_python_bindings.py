from Tree import *

def test_root_node_is_non_null():
    t = Tree(2)
    assert(t)
    assert(t.data())

def test_left_node_is_non_null():
    t = Tree(2)
    lt = t.left_subtree()
    assert(lt)
    assert(lt.data())

def test_right_node_is_non_null():
    t = Tree(2)
    rt = t.right_subtree()
    assert(rt)
    assert(rt.data())

def test_right_3_node_is_null():
    t = Tree(2)
    r3t = t.right_subtree().right_subtree().right_subtree()
    assert(r3t==None)

def test_use_of_null_node_is_caught():
    t = Tree(2)
    r3t = t.right_subtree().right_subtree().right_subtree()
    error_thrown = False
    try:
        r3t.data()
    except Exception as e:
        error_thrown = True
    assert(error_thrown)

def test_subtree_handle_keeps_tree_alive():
    t = Tree(1)
    st = t.left_subtree()
    x = st.data()
    del t
    assert(st.data()==x)

def test_tree_set_data():
    t = Tree(0)
    t.set_data(77)
    assert t.data() == 77
