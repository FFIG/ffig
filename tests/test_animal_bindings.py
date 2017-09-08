import Animal


def test_animals_are_defined():
    assert hasattr(Animal, "Cat")
    assert hasattr(Animal, "Duck")
    assert hasattr(Animal, "Squirrel")


def test_animals_make_noises():
    assert Animal.Cat().noise() == "Miaow"
    assert Animal.Duck().noise() == "Quack"
    assert Animal.Squirrel().noise() == "<deafening silence>"
