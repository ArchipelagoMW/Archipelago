from __future__ import annotations
import typing
import random

from schema import Schema, And, Or


class AssembleOptions(type):
    def __new__(mcs, name, bases, attrs):
        options = attrs["options"] = {}
        name_lookup = attrs["name_lookup"] = {}
        # merge parent class options
        for base in bases:
            if getattr(base, "options", None):
                options.update(base.options)
                name_lookup.update(base.name_lookup)
        new_options = {name[7:].lower(): option_id for name, option_id in attrs.items() if
                       name.startswith("option_")}
        if "random" in new_options:
            raise Exception("Choice option 'random' cannot be manually assigned.")
        attrs["name_lookup"].update({option_id: name for name, option_id in new_options.items()})
        options.update(new_options)

        # apply aliases, without name_lookup
        options.update({name[6:].lower(): option_id for name, option_id in attrs.items() if
                        name.startswith("alias_")})

        # auto-validate schema on __init__
        if "schema" in attrs.keys():

            if "__init__" in attrs:
                def validate_decorator(func):
                    def validate(self, *args, **kwargs):
                        ret = func(self, *args, **kwargs)
                        self.value = self.schema.validate(self.value)
                        return ret

                    return validate
                attrs["__init__"] = validate_decorator(attrs["__init__"])
            else:
                # construct an __init__ that calls parent __init__

                cls = super(AssembleOptions, mcs).__new__(mcs, name, bases, attrs)

                def meta__init__(self, *args, **kwargs):
                    super(cls, self).__init__(*args, **kwargs)
                    self.value = self.schema.validate(self.value)

                cls.__init__ = meta__init__
                return cls

        return super(AssembleOptions, mcs).__new__(mcs, name, bases, attrs)


class Option(metaclass=AssembleOptions):
    value: int
    name_lookup: typing.Dict[int, str]
    default = 0

    # convert option_name_long into Name Long as display_name, otherwise name_long is the result.
    # Handled in get_option_name()
    auto_display_name = False

    # can be weighted between selections
    supports_weighting = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.get_current_option_name()})"

    def __hash__(self):
        return hash(self.value)

    @property
    def current_key(self) -> str:
        return self.name_lookup[self.value]

    def get_current_option_name(self) -> str:
        """For display purposes."""
        return self.get_option_name(self.value)

    @classmethod
    def get_option_name(cls, value: typing.Any) -> str:
        if cls.auto_display_name:
            return cls.name_lookup[value].replace("_", " ").title()
        else:
            return cls.name_lookup[value]

    def __int__(self) -> int:
        return self.value

    def __bool__(self) -> bool:
        return bool(self.value)

    @classmethod
    def from_any(cls, data: typing.Any):
        raise NotImplementedError


class Toggle(Option):
    option_false = 0
    option_true = 1
    default = 0

    def __init__(self, value: int):
        assert value == 0 or value == 1
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Toggle:
        if text.lower() in {"off", "0", "false", "none", "null", "no"}:
            return cls(0)
        else:
            return cls(1)

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == str:
            return cls.from_text(data)
        else:
            return cls(data)

    def __eq__(self, other):
        if isinstance(other, Toggle):
            return self.value == other.value
        else:
            return self.value == other

    def __gt__(self, other):
        if isinstance(other, Toggle):
            return self.value > other.value
        else:
            return self.value > other

    def __bool__(self):
        return bool(self.value)

    def __int__(self):
        return int(self.value)

    @classmethod
    def get_option_name(cls, value):
        return ["No", "Yes"][int(value)]

    __hash__ = Option.__hash__  # see https://docs.python.org/3/reference/datamodel.html#object.__hash__


class DefaultOnToggle(Toggle):
    default = 1


class Choice(Option):
    auto_display_name = True

    def __init__(self, value: int):
        self.value: int = value

    @classmethod
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "random":
            return cls(random.choice(list(cls.name_lookup)))
        for option_name, value in cls.options.items():
            if option_name == text:
                return cls(value)
        raise KeyError(
            f'Could not find option "{text}" for "{cls.__name__}", '
            f'known options are {", ".join(f"{option}" for option in cls.name_lookup.values())}')

    @classmethod
    def from_any(cls, data: typing.Any) -> Choice:
        if type(data) == int and data in cls.options.values():
            return cls(data)
        return cls.from_text(str(data))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.value == self.value
        elif isinstance(other, str):
            assert other in self.options
            return other == self.current_key
        elif isinstance(other, int):
            assert other in self.name_lookup
            return other == self.value
        elif isinstance(other, bool):
            return other == bool(self.value)
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return other.value != self.value
        elif isinstance(other, str):
            assert other in self.options
            return other != self.current_key
        elif isinstance(other, int):
            assert other in self.name_lookup
            return other != self.value
        elif isinstance(other, bool):
            return other != bool(self.value)
        elif other is None:
            return False
        else:
            raise TypeError(f"Can't compare {self.__class__.__name__} with {other.__class__.__name__}")

    __hash__ = Option.__hash__  # see https://docs.python.org/3/reference/datamodel.html#object.__hash__


class Range(Option, int):
    range_start = 0
    range_end = 1

    def __init__(self, value: int):
        if value < self.range_start:
            raise Exception(f"{value} is lower than minimum {self.range_start} for option {self.__class__.__name__}")
        elif value > self.range_end:
            raise Exception(f"{value} is higher than maximum {self.range_end} for option {self.__class__.__name__}")
        self.value = value

    @classmethod
    def from_text(cls, text: str) -> Range:
        text = text.lower()
        if text.startswith("random"):
            if text == "random-low":
                return cls(int(round(random.triangular(cls.range_start, cls.range_end, cls.range_start), 0)))
            elif text == "random-high":
                return cls(int(round(random.triangular(cls.range_start, cls.range_end, cls.range_end), 0)))
            elif text == "random-middle":
                return cls(int(round(random.triangular(cls.range_start, cls.range_end), 0)))
            elif text.startswith("random-range-"):
                textsplit = text.split("-")
                try:
                    random_range = [int(textsplit[len(textsplit) - 2]), int(textsplit[len(textsplit) - 1])]
                except ValueError:
                    raise ValueError(f"Invalid random range {text} for option {cls.__name__}")
                random_range.sort()
                if random_range[0] < cls.range_start or random_range[1] > cls.range_end:
                    raise Exception(
                        f"{random_range[0]}-{random_range[1]} is outside allowed range "
                        f"{cls.range_start}-{cls.range_end} for option {cls.__name__}")
                if text.startswith("random-range-low"):
                    return cls(int(round(random.triangular(random_range[0], random_range[1], random_range[0]))))
                elif text.startswith("random-range-middle"):
                    return cls(int(round(random.triangular(random_range[0], random_range[1]))))
                elif text.startswith("random-range-high"):
                    return cls(int(round(random.triangular(random_range[0], random_range[1], random_range[1]))))
                else:
                    return cls(int(round(random.randint(random_range[0], random_range[1]))))
            else:
                return cls(random.randint(cls.range_start, cls.range_end))
        return cls(int(text))

    @classmethod
    def from_any(cls, data: typing.Any) -> Range:
        if type(data) == int:
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return str(value)

    def __str__(self):
        return str(self.value)


class VerifyKeys:
    valid_keys = frozenset()
    valid_keys_casefold: bool = False
    verify_item_name = False
    verify_location_name = False
    value: typing.Any

    @classmethod
    def verify_keys(cls, data):
        if cls.valid_keys:
            data = set(data)
            dataset = set(word.casefold() for word in data) if cls.valid_keys_casefold else set(data)
            extra = dataset - cls.valid_keys
            if extra:
                raise Exception(f"Found unexpected key {', '.join(extra)} in {cls}. "
                                f"Allowed keys: {cls.valid_keys}.")

    def verify(self, world):
        if self.verify_item_name:
            for item_name in self.value:
                if item_name not in world.item_names:
                    raise Exception(f"Item {item_name} from option {self} "
                                    f"is not a valid item name from {world.game}")
        elif self.verify_location_name:
            for location_name in self.value:
                if location_name not in world.world_types[world.game].location_names:
                    raise Exception(f"Location {location_name} from option {self} "
                                    f"is not a valid location name from {world.game}")


class OptionDict(Option, VerifyKeys):
    default = {}
    supports_weighting = False
    value: typing.Dict[str, typing.Any]

    def __init__(self, value: typing.Dict[str, typing.Any]):
        self.value = value

    @classmethod
    def from_any(cls, data: typing.Dict[str, typing.Any]) -> OptionDict:
        if type(data) == dict:
            cls.verify_keys(data)
            return cls(data)
        else:
            raise NotImplementedError(f"Cannot Convert from non-dictionary, got {type(data)}")

    def get_option_name(self, value):
        return ", ".join(f"{key}: {v}" for key, v in value.items())

    def __contains__(self, item):
        return item in self.value


class ItemDict(OptionDict):
    # implemented by Generate
    verify_item_name = True

    def __init__(self, value: typing.Dict[str, int]):
        if any(item_count < 1 for item_count in value.values()):
            raise Exception("Cannot have non-positive item counts.")
        super(ItemDict, self).__init__(value)


class OptionList(Option, VerifyKeys):
    default = []
    supports_weighting = False
    value: list

    def __init__(self, value: typing.List[typing.Any]):
        self.value = value or []
        super(OptionList, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == list:
            cls.verify_keys(data)
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(map(str, value))

    def __contains__(self, item):
        return item in self.value


class OptionSet(Option, VerifyKeys):
    default = frozenset()
    supports_weighting = False
    value: set

    def __init__(self, value: typing.Union[typing.Set[str, typing.Any], typing.List[str, typing.Any]]):
        self.value = set(value)
        super(OptionSet, self).__init__()

    @classmethod
    def from_text(cls, text: str):
        return cls([option.strip() for option in text.split(",")])

    @classmethod
    def from_any(cls, data: typing.Any):
        if type(data) == list:
            cls.verify_keys(data)
            return cls(data)
        elif type(data) == set:
            cls.verify_keys(data)
            return cls(data)
        return cls.from_text(str(data))

    def get_option_name(self, value):
        return ", ".join(value)

    def __contains__(self, item):
        return item in self.value


local_objective = Toggle  # local triforce pieces, local dungeon prizes etc.


class Accessibility(Choice):
    """Set rules for reachability of your items/locations.
    Locations: ensure everything can be reached and acquired.
    Items: ensure all logically relevant items can be acquired.
    Minimal: ensure what is needed to reach your goal can be acquired."""
    display_name = "Accessibility"
    option_locations = 0
    option_items = 1
    option_minimal = 2
    alias_none = 2
    default = 1


class ProgressionBalancing(DefaultOnToggle):
    """A system that moves progression earlier, to try and prevent the player from getting stuck and bored early."""
    display_name = "Progression Balancing"


common_options = {
    "progression_balancing": ProgressionBalancing,
    "accessibility": Accessibility
}


class ItemSet(OptionSet):
    # implemented by Generate
    verify_item_name = True


class LocalItems(ItemSet):
    """Forces these items to be in their native world."""
    display_name = "Local Items"


class NonLocalItems(ItemSet):
    """Forces these items to be outside their native world."""
    display_name = "Not Local Items"


class StartInventory(ItemDict):
    """Start with these items."""
    verify_item_name = True
    display_name = "Start Inventory"


class StartHints(ItemSet):
    """Start with these item's locations prefilled into the !hint command."""
    display_name = "Start Hints"


class StartLocationHints(OptionSet):
    """Start with these locations and their item prefilled into the !hint command"""
    display_name = "Start Location Hints"


class ExcludeLocations(OptionSet):
    """Prevent these locations from having an important item"""
    display_name = "Excluded Locations"
    verify_location_name = True


class PriorityLocations(OptionSet):
    """Prevent these locations from having an unimportant item"""
    display_name = "Priority Locations"
    verify_location_name = True


class DeathLink(Toggle):
    """When you die, everyone dies. Of course the reverse is true too."""
    display_name = "Death Link"


class ItemLinks(OptionList):
    """Share part of your item pool with other players."""
    default = []
    schema = Schema([
        {
            "name": And(str, len),
            "item_pool": [And(str, len)],
            "replacement_item": Or(And(str, len), None)
        }
    ])

    def verify(self, world):
        super(ItemLinks, self).verify(world)
        for link in self.value:
            for item_name in link["item_pool"]:
                if item_name not in world.item_names and item_name not in world.item_name_groups:
                    raise Exception(f"Item {item_name} from option {self} "
                                    f"is not a valid item name from {world.game}")
            if link["replacement_item"] not in world.item_names:
                raise Exception(f"Item {link['replacement_item']} from option {self} "
                                f"is not a valid item name from {world.game}")


per_game_common_options = {
    **common_options,  # can be overwritten per-game
    "local_items": LocalItems,
    "non_local_items": NonLocalItems,
    "start_inventory": StartInventory,
    "start_hints": StartHints,
    "start_location_hints": StartLocationHints,
    "exclude_locations": ExcludeLocations,
    "priority_locations": PriorityLocations,
    "item_links": ItemLinks
}


if __name__ == "__main__":

    from worlds.alttp.Options import Logic
    import argparse

    map_shuffle = Toggle
    compass_shuffle = Toggle
    key_shuffle = Toggle
    big_key_shuffle = Toggle
    hints = Toggle
    test = argparse.Namespace()
    test.logic = Logic.from_text("no_logic")
    test.map_shuffle = map_shuffle.from_text("ON")
    test.hints = hints.from_text('OFF')
    try:
        test.logic = Logic.from_text("overworld_glitches_typo")
    except KeyError as e:
        print(e)
    try:
        test.logic_owg = Logic.from_text("owg")
    except KeyError as e:
        print(e)
    if test.map_shuffle:
        print("map_shuffle is on")
    print(f"Hints are {bool(test.hints)}")
    print(test)
