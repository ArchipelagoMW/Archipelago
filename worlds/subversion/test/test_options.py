from typing import Iterator

from Utils import parse_yaml
from worlds.subversion.options import SubversionCustomLogic, SubversionShortGame
import worlds.subversion.options as options_module

from subversion_rando.location_data import pullCSV
from subversion_rando.trick_data import Tricks


def test_location_names() -> None:
    """ make sure all the names in these lists are valid location names """
    locations = pullCSV()

    for op, loc_list in SubversionShortGame.location_lists.items():
        for loc_name in loc_list:
            assert loc_name in locations, f"{loc_name} invalid location name in list {op}"


def test_parse_custom_logic_string() -> None:
    """ yaml parser can see a string that's all digits and interpret it as int or octal """
    LENGTH = 12
    assert len(SubversionCustomLogic.default) == LENGTH, "test needs to be updated for new string length?"
    logic_strings = [
        "000000000000",
        "000000000101",
        "000000200500",
        "007000000000",
        "077777777777",
        "099999999999",
        "100000000000",
        "777777777777",
        "999999999999",
        "a0b9a3f79350"
    ]

    def gen() -> Iterator[str]:
        yield from logic_strings

        for i in range(0x1000):
            yield f"{hex(i)[2:]:03}000000000"
            yield f"{hex(i)[2:]:03}111111111"
            yield f"{hex(i)[2:]:03}777777777"
            yield f"{hex(i)[2:]:03}999999999"
            yield f"{hex(i)[2:]:03}fffffffff"

    for logic_string in gen():
        assert len(logic_string) == LENGTH, f"{len(logic_string)=}"
        yaml_text = f"custom_logic: {logic_string}"
        parsed_yaml = parse_yaml(yaml_text)
        # print(parsed_yaml)
        option = SubversionCustomLogic.from_any(parsed_yaml["custom_logic"])
        assert logic_string == option.value, f"{logic_string=} == {option.value=}"


def test_parse_tricks_from_yaml_string() -> None:
    """ one example of custom logic tricks that would be messed up if octal parsing isn't fixed """
    parsed_yaml = parse_yaml("custom_logic: 007000000000")
    option = SubversionCustomLogic.from_any(parsed_yaml["custom_logic"])
    make_custom = getattr(options_module, "_make_custom")
    tricks = make_custom(option.value)
    assert len(tricks) == 3, f"{len(tricks)=}"
    assert Tricks.hell_run_easy in tricks, "easy not in tricks"
    assert Tricks.hell_run_medium in tricks, "medium not in tricks"
    assert Tricks.hell_run_hard in tricks, "hard not in tricks"
