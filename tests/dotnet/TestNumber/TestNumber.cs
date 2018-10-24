using Number_c;
using NUnit.Framework;

namespace TestFFIG
{
    [TestFixture]
    public class TestNumber
    {
        [Test]
        public void NumberValue()
        {
          var number = new Number(8);
          
          Assert.AreEqual(number.value(), 8);
        }
        
        [Test]
        public void NumberNext()
        {
          var number = new Number(8);
          var next_number = number.next();
          
          Assert.AreEqual(next_number.value(), 9);
        }
    }
}


