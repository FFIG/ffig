from Asset import *


def test_no_argument_constructor():
    # Lack of exception is all we need to test.
    cdo = CDO()


def test_id_is_renamed_to_name_and_is_a_property():
    cdo = CDO()

    assert cdo.name == "CDO"


def test_PV_is_renamed_to_value():
    cdo = CDO()

    assert cdo.value() == 0
