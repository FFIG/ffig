using Xunit;
using Shape_c;

namespace TestFFIG
{
    public class TestShape
    {
        [Fact]
        public void CircleName()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.Equal(circle.name(), "Circle");
        }
        
        [Fact]
        public void CircleArea()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.Equal(circle.area(), 12.56637061436, 10);
        }
        
        [Fact]
        public void CirclePerimeter()
        {
          double radius = 2.0;
          var circle = new Circle(radius);
          
          Assert.Equal(circle.perimeter(), 12.5663706144, 10);
        }
        
        [Fact]
        public void CircleEquality()
        {
          var circle1 = new Circle(3);
          var circle2 = new Circle(3);
          
          Assert.Equal(circle1.is_equal(circle2), 1);
        }
        
        [Fact]
        public void CircleInequality()
        {
          var circle1 = new Circle(3);
          var circle2 = new Circle(4);
          
          Assert.Equal(circle1.is_equal(circle2), 0);
        }
    }
}

