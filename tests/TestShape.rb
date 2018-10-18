require "test/unit"
# FIXME: Remove this hardcoded path
require_relative "../build_out/generated/Shape"

class TestShape < Test::Unit::TestCase
  def test_name
    assert_equal("Circle", Circle.new(3).name)
  end
  
  def test_area
    assert_equal(100.0, Square.new(10).area)
  end
  
  def test_perimeter
    assert_equal(40, Square.new(10).perimeter)
  end

  def test_error
    assert_raise(ShapeError) { Circle.new(-1) }
  end
end

