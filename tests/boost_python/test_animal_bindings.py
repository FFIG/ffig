import Animal_py as animal


def test_animals_are_defined():
    assert hasattr(animal, "Cat")
    assert hasattr(animal, "Duck")
    assert hasattr(animal, "Squirrel")


def test_animals_make_noises():
    assert animal.Cat().noise() == "Miaow"
    assert animal.Duck().noise() == "Quack"
    assert animal.Squirrel().noise() == "<deafening silence>"
