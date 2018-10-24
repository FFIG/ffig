import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.junit.Assert.assertNotNull;
import org.junit.Test;

public class TestTree {
    @Test
    public void Depth()
    {
        Tree.Tree tree = new Tree.Tree(1);

        assertNotNull(tree.left_subtree());
        assertNull(tree.left_subtree().left_subtree());
    }
    
    @Test
    public void GetSetData()
    {
        Tree.Tree tree = new Tree.Tree(2);

        tree.set_data(42);
        assertEquals(tree.data(), 42);
    }
    
    @Test
    public void LifetimeExtension()
    {
        Tree.Tree tree = new Tree.Tree(2);
        Tree.Tree left = tree.left_subtree();

        tree = null;

        left.set_data(42);
        assertEquals(left.data(), 42);
    }
}
