using NUnit.Framework;
using Shape_c;

namespace TestFFIG
{
    [TestFixture]
    public class TestShape
    {
        [Test]
        public void CircleName()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.AreEqual(circle.name, "Circle");
        }
        
        [Test]
        public void CircleArea()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.AreEqual(circle.area, 12.56637061436, 10);
        }
        
        [Test]
        public void CirclePerimeter()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.AreEqual(circle.perimeter, 12.5663706144, 10);
        }
        
        [Test]
        public void CircleEquality()
        {
          var circle1 = new Circle(3);
          var circle2 = new Circle(3);
          
          Assert.AreEqual(circle1.is_equal(circle2), 1);
        }
        
        [Test]
        public void CircleInequality()
        {
          var circle1 = new Circle(3);
          var circle2 = new Circle(4);
          
          Assert.AreEqual(circle1.is_equal(circle2), 0);
        }
    }
}

