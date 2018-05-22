import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class TestShape {
    @Test
    public void CircleHasNameCircle()
    {
        Shape.Circle circle = new Shape.Circle(2);

        assertEquals(circle.name(), "Circle");
    }
    
    @Test
    public void SquareArea()
    {
        Shape.Square square = new Shape.Square(3);

        assertEquals(square.area(), 9.0, 0.0);
    }
    
    @Test
    public void SquarePerimeter()
    {
        Shape.Square square = new Shape.Square(3);

        assertEquals(square.perimeter(), 12.0, 0.0);
    }
    
    @Test
    public void SquareIsEqualToIdenticalSquare()
    {
        Shape.Square square = new Shape.Square(3);
        Shape.Square identicalSquare = new Shape.Square(3);

        assertEquals(square.is_equal(identicalSquare), 1);
    }
    
    @Test
    public void SquareIsNotEqualToCircle()
    {
        Shape.Square square = new Shape.Square(3);
        Shape.Circle circle = new Shape.Circle(2);

        assertEquals(square.is_equal(circle), 0);
    }
    
    @Test
    public void SquareIsEqualToDifferentSquare()
    {
        Shape.Square square = new Shape.Square(3);
        Shape.Square differentSquare = new Shape.Square(4);

        assertEquals(square.is_equal(differentSquare), 0);
    }
}
