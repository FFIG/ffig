using NUnit.Framework;
using Tree_c;

namespace TestFFIG
{
    [TestFixture]
    public class TestTree
    {
        [Test]
        public void DepthIsAsConstructed()
        {
          var tree = new Tree(1);
          
          Assert.IsNotNull(tree.left_subtree());
          Assert.IsNull(tree.left_subtree().left_subtree());
        }
        
        [Test]
        public void DataIsAsSet()
        {
          var tree = new Tree(1);
                            
          tree.set_data(42);

          Assert.AreEqual(tree.data(), 42);
        }
        
        [Test]
        public void LifetimeExtension()
        {
          var tree = new Tree(1);
          var left = tree.left_subtree();
          
          tree = null;
          left.set_data(42);

          Assert.AreEqual(left.data(), 42);
        }
    }
}

