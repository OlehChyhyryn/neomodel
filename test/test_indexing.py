from pytest import raises

from neomodel import (
    IntegerProperty,
    StringProperty,
    StructuredNode,
    UniqueProperty,
    install_labels,
)


class Human(StructuredNode):
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True)


def test_unique_error():
    install_labels(Human)
    Human(name="j1m", age=13).save()
    try:
        Human(name="j1m", age=14).save()
    except UniqueProperty as e:
        assert str(e).find("j1m")
        assert str(e).find("name")
    else:
        assert False, "UniqueProperty not raised."


def test_optional_properties_dont_get_indexed():
    Human(name="99", age=99).save()
    h = Human.nodes.get(age=99)
    assert h
    assert h.name == "99"

    Human(name="98", age=98).save()
    h = Human.nodes.get(age=98)
    assert h
    assert h.name == "98"


def test_escaped_chars():
    _name = "sarah:test"
    Human(name=_name, age=3).save()
    r = Human.nodes.filter(name=_name)
    assert r
    assert r[0].name == _name


def test_does_not_exist():
    with raises(Human.DoesNotExist):
        Human.nodes.get(name="XXXX")


def test_custom_label_name():
    class Giraffe(StructuredNode):
        __label__ = "Giraffes"
        name = StringProperty(unique_index=True)

    jim = Giraffe(name="timothy").save()
    node = Giraffe.nodes.get(name="timothy")
    assert node.name == jim.name

    class SpecialGiraffe(Giraffe):
        power = StringProperty()

    # custom labels aren't inherited
    assert SpecialGiraffe.__label__ == "SpecialGiraffe"
