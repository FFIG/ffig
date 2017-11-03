using Xunit;
using Tree_c;

namespace TestFFIG
{
    public class TestTree
    {
        [Fact]
        public void DepthIsAsConstructed()
        {
          var tree = new Tree(1);
          
          Assert.NotNull(tree.left_subtree());
          Assert.Null(tree.left_subtree().left_subtree());
        }
        
        [Fact]
        public void DataIsAsSet()
        {
          var tree = new Tree(1);
                            
          tree.set_data(42);

          Assert.Equal(tree.data(), 42);
        }
        
        [Fact]
        public void LifetimeExtension()
        {
          var tree = new Tree(1);
          var left = tree.left_subtree();
          
          tree = null;
          left.set_data(42);

          Assert.Equal(left.data(), 42);
        }
    }
}

