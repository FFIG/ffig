import nose
import number

def test_number_8_has_value_8():
    n = number.Number(8)
    assert n.value() == 8

def test_number_9_comes_after_8():
    n8 = number.Number(8)
    n9 = n8.next()

    assert n9.value() == 9

