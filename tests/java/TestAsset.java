import static org.junit.Assert.assertEquals;
import org.junit.Test;
//import org.ffig.Asset;

public class TestAsset {
    @Test
    public void CDOhasPVofZero()
    {
        Asset cdo = Asset.Asset_CDO_create();

        assertEquals(99.99, cdo.value(), 0.0);
    }

    @Test
    public void CDOisCalledCDO()
    {
        Asset cdo = Asset.Asset_CDO_create();

        assertEquals(cdo.name(), "CDO");
    }
}