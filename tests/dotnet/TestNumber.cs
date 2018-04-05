using Number_c;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace TestFFIG
{
    [TestClass]
    public class TestNumber
    {
        [TestMethod]
        public void NumberValue()
        {
          var number = new Number(8);
          
          Assert.AreEqual(number.value(), 8);
        }
        
        [TestMethod]
        public void NumberNext()
        {
          var number = new Number(8);
          var next_number = number.next();
          
          Assert.AreEqual(next_number.value(), 9);
        }
    }
}


