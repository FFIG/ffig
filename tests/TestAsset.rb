require "test/unit"
# FIXME: Remove this hardcoded path
require_relative "../build/generated/Asset"

class TestAsset < Test::Unit::TestCase
  def test_CDO_name
    assert_equal("CDO", CDO.new.name)
  end
  
  def test_CDO_PV
    assert_equal(CDO.new.PV, 0.0)
  end
end


