import static org.junit.Assert.assertEquals;
import org.junit.Test;

public class TestAsset {
    @Test
    public void CDOhasPVofZero()
    {
        Asset.Asset cdo = new Asset.CDO();

        assertEquals(99.99, cdo.value(), 0.0);
    }

    @Test
    public void CDOisCalledCDO()
    {
        Asset.Asset cdo = new Asset.CDO();

        assertEquals(cdo.name(), "CDO");
    }
}
