# Archipelago Options API

This document covers some of the generic options available using Archipelago's options handling system.

For more information on where these options go in your world please refer to:
 - [world api.md](/docs/world%20api.md)

Archipelago will be abbreviated as "AP" from now on.

## Option Definitions
Option parsing in AP is done using different Option classes. For each option you would like to have in your game, you
need to create:
- A new option class with a docstring detailing what the option will do to your user.
- A `display_name` to be displayed on the webhost.
- A new entry in the `option_definitions` dict for your World.
By style and convention, the internal names should be snake_case.

### Option Creation
- If the option supports having multiple sub_options, such as Choice options, these can be defined with
`option_value1`. Any attributes of the class with a preceding `option_` is added to the class's `options` lookup. The
`option_` is then stripped for users, so will show as `value1` in yaml files. If `auto_display_name` is True, it will
display as `Value1` on the webhost.
- An alternative name can be set for any specific option by setting an alias attribute
(i.e. `alias_value_1 = option_value1`) which will allow users to use either `value_1` or `value1` in their yaml
files, and both will resolve as `value1`. This should be used when changing options around, i.e. changing a Toggle to a
Choice, and defining `alias_true = option_full`.
- All options support `random` as a generic option. `random` chooses from any of the available values for that option,
and is reserved by AP. You can set this as your default value, but you cannot define your own `option_random`.

As an example, suppose we want an option that lets the user start their game with a sword in their inventory. Let's
create our option class (with a docstring), give it a `display_name`, and add it to our game's options dataclass:

```python
# options.py
from dataclasses import dataclass

from Options import Toggle, PerGameCommonOptions


class StartingSword(Toggle):
    """Adds a sword to your starting inventory."""
    display_name = "Start With Sword"


@dataclass
class ExampleGameOptions(PerGameCommonOptions):
    starting_sword: StartingSword
```

This will create a `Toggle` option, internally called `starting_sword`. To then submit this to the multiworld, we add it
to our world's `__init__.py`:

```python
from worlds.AutoWorld import World
from .Options import ExampleGameOptions


class ExampleWorld(World):
    # this gives the generator all the definitions for our options
    options_dataclass = ExampleGameOptions
    # this gives us typing hints for all the options we defined
    options: ExampleGameOptions
```

### Option Checking
Options are parsed by `Generate.py` before the worlds are created, and then the option classes are created shortly after
world instantiation. These are created as attributes on the MultiWorld and can be accessed with
`self.options.my_option_name`. This is an instance of the option class, which supports direct comparison methods to
relevant objects (like comparing a Toggle class to a `bool`). If you need to access the option result directly, this is
the option class's `value` attribute. For our example above we can do a simple check:
```python
if self.options.starting_sword:
    do_some_things()
```

or if I need a boolean object, such as in my slot_data I can access it as:
```python
start_with_sword = bool(self.options.starting_sword.value)
```

## Generic Option Classes
These options are generically available to every game automatically, but can be overridden for slightly different
behavior, if desired. See `worlds/soe/Options.py` for an example.

### Accessibility
Sets rules for availability of locations for the player. `Items` is for all items available but not necessarily all
locations, such as self-locking keys, but needs to be set by the world for this to be different from locations access.

### ProgressionBalancing
Algorithm for moving progression items into earlier spheres to make the gameplay experience a bit smoother. Can be
overridden if you want a different default value.

### LocalItems
Forces the players' items local to their world.

### NonLocalItems
Forces the players' items outside their world.

### StartInventory
Allows the player to define a dictionary of starting items with item name and quantity.

### StartHints
Gives the player starting hints for where the items defined here are.

### StartLocationHints
Gives the player starting hints for the items on locations defined here.

### ExcludeLocations
Marks locations given here as `LocationProgressType.Excluded` so that progression items can't be placed on them.

### PriorityLocations
Marks locations given here as `LocationProgressType.Priority` forcing progression items on them.

### ItemLinks
Allows users to share their item pool with other players. Currently item links are per game. A link of one game between
two players will combine their items in the link into a single item, which then gets replaced with `World.create_filler()`.

## Basic Option Classes
### Toggle
The example above. This simply has 0 and 1 as its available results with 0 (false) being the default value. Cannot be
compared to strings but can be directly compared to True and False.

### DefaultOnToggle
Like Toggle, but 1 (true) is the default value.

### Choice
A numeric option allowing you to define different sub options. Values are stored as integers, but you can also do
comparison methods with the class and strings, so if you have an `option_early_sword`, this can be compared with:
```python
if self.options.sword_availability == "early_sword":
    do_early_sword_things()
```

or:
```python
from .Options import SwordAvailability

if self.options.sword_availability == SwordAvailability.option_early_sword:
    do_early_sword_things()
```

### Range
A numeric option allowing a variety of integers including the endpoints. Has a default `range_start` of 0 and default
`range_end` of 1. Allows for negative values as well. This will always be an integer and has no methods for string
comparisons.

### SpecialRange
Like range but also allows you to define a dictionary of special names the user can use to equate to a specific value.
For example:
```python
special_range_names: {
    "normal": 20,
    "extreme": 99,
}
```

will let users use the names "normal" or "extreme" in their options selections, but will still return those as integers
to you. Useful if you want special handling regarding those specified values.

## More Advanced Options
### FreeText
This is an option that allows the user to enter any possible string value. Can only be compared with strings, and has
no validation step, so if this needs to be validated, you can either add a validation step to the option class or
within the world.

### TextChoice
Like choice allows you to predetermine options and has all of the same comparison methods and handling. Also accepts any
user defined string as a valid option, so will either need to be validated by adding a validation step to the option
class or within world, if necessary. Value for this class is `Union[str, int]` so if you need the value at a specified
point, `self.options.my_option.current_key` will always return a string.

### PlandoBosses
An option specifically built for handling boss rando, if your game can use it. Is a subclass of TextChoice so supports
everything it does, as well as having multiple validation steps to automatically support boss plando from users. If
using this class, you must define `bosses`, a set of valid boss names, and `locations`, a set of valid boss location
names, and `def can_place_boss`, which passes a boss and location, allowing you to check if that placement is valid for
your game. When this function is called, `bosses`, `locations`, and the passed strings will all be lowercase. There is
also a `duplicate_bosses` attribute allowing you to define if a boss can be placed multiple times in your world. False
by default, and will reject duplicate boss names from the user. For an example of using this class, refer to
`worlds.alttp.options.py`

### OptionDict
This option returns a dictionary. Setting a default here is recommended as it will output the dictionary to the
template. If you set a [Schema](https://pypi.org/project/schema/) on the class with `schema = Schema()`, then the
options system will automatically validate the user supplied data against the schema to ensure it's in the correct
format.

### ItemDict
Like OptionDict, except this will verify that every key in the dictionary is a valid name for an item for your world.

### OptionList
This option defines a List, where the user can add any number of strings to said list, allowing duplicate values. You
can define a set of keys in `valid_keys`, and a default list if you want certain options to be available without editing
for this. If `valid_keys_casefold` is true, the verification will be case-insensitive; `verify_item_name` will check
that each value is a valid item name; and`verify_location_name` will check that each value is a valid location name.

### OptionSet
Like OptionList, but returns a set, preventing duplicates.

### ItemSet
Like OptionSet, but will verify that all the items in the set are a valid name for an item for your world.
