import static org.junit.Assert.assertEquals;
import org.junit.Test;
import Number.Number;

public class TestNumber {
    @Test
    public void Value()
    {
      Number number = new Number(8);

      assertEquals(number.value(), 8);
    }
    
    @Test
    public void NextNumberHasNextValue()
    {
      Number number = new Number(8);
      Number next = number.next();

      assertEquals(next.value(), 9);
    }
}
