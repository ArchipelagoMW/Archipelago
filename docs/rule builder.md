# Rule Builder

This document describes the API provided for the rule builder. Using this API provides you with with a simple interface to define rules and the following advantages:

- Rule classes that avoid all the common pitfalls
- Logic optimization
- Automatic result caching (opt-in)
- Serialization/deserialization
- Human-readable logic explanations for players

## Overview

The rule builder consists of 3 main parts:

1. The rules, which are classes that inherit from `rule_builder.rules.Rule`. These are what you write for your logic. They can be combined and take into account your world's options. There are a number of default rules listed below, and you can create as many custom rules for your world as needed. When assigning the rules to a location or entrance they must be resolved.
1. Resolved rules, which are classes that inherit from `rule_builder.rules.Rule.Resolved`. These are the optimized rules specific to one player that are set as a location or entrance's access rule. You generally shouldn't be directly creating these but they'll be created when assigning rules to locations or entrances. These are what power the human-readable logic explanations.
1. The optional rule builder world subclass `CachedRuleBuilderWorld`, which is a class your world can inherit from instead of `World`. It adds a caching system to the rules that will lazy evaluate and cache the result.

## Usage

For the most part the only difference in usage is instead of writing lambdas for your logic, you write static Rule objects. You then must use `world.set_rule` to assign the rule to a location or entrance.

```python
# In your world's create_regions method
location = MyWorldLocation(...)
self.set_rule(location, Has("A Big Gun"))
```

The rule builder comes with a number of rules by default:

- `True_`: Always returns true
- `False_`: Always returns false
- `And`: Checks that all child rules are true (also provided by `&` operator)
- `Or`: Checks that at least one child rule is true (also provided by `|` operator)
- `Has`: Checks that the player has the given item with the given count (default 1)
- `HasAll`: Checks that the player has all given items
- `HasAny`: Checks that the player has at least one of the given items
- `HasAllCounts`: Checks that the player has all of the counts for the given items
- `HasAnyCount`: Checks that the player has any of the counts for the given items
- `HasFromList`: Checks that the player has some number of given items
- `HasFromListUnique`: Checks that the player has some number of given items, ignoring duplicates of the same item
- `HasGroup`: Checks that the player has some number of items from a given item group
- `HasGroupUnique`: Checks that the player has some number of items from a given item group, ignoring duplicates of the same item
- `CanReachLocation`: Checks that the player can logically reach the given location
- `CanReachRegion`: Checks that the player can logically reach the given region
- `CanReachEntrance`: Checks that the player can logically reach the given entrance

You can combine these rules together to describe the logic required for something. For example, to check if a player either has `Movement ability` or they have both `Key 1` and `Key 2`, you can do:

```python
rule = Has("Movement ability") | HasAll("Key 1", "Key 2")
```

> ⚠️ Composing rules with the `and` and `or` keywords will not work. You must use the bitwise `&` and `|` operators. In order to catch mistakes, the rule builder will not let you do boolean operations. As a consequence, in order to check if a rule is defined you must use `if rule is not None`.

### Assigning rules

When assigning the rule you must use the `set_rule` helper to correctly resolve and register the rule.

```python
self.set_rule(location_or_entrance, rule)
```

There is also a `create_entrance` helper that will resolve the rule, check if it's `False`, and if not create the entrance and set the rule. This allows you to skip creating entrances that will never be valid. You can also specify `force_creation=True` if you would like to create the entrance even if the rule is `False`.

```python
self.create_entrance(from_region, to_region, rule)
```

> ⚠️ If you use a `CanReachLocation` rule on an entrance, you will either have to create the locations first, or specify the location's parent region name with the `parent_region_name` argument of `CanReachLocation`.

You can also set a rule for your world's completion condition:

```python
self.set_completion_rule(rule)
```

### Restricting options

Every rule allows you to specify which options it's applicable for. You can provide the argument `options` which is an iterable of `OptionFilter` instances. Rules that pass the options check will be resolved as normal, and those that fail will be resolved as `False`.

If you want a comparison that isn't equals, you can specify with the `operator` argument. The following operators are allowed:

- `eq`: `==`
- `ne`: `!=`
- `gt`: `>`
- `lt`: `<`
- `ge`: `>=`
- `le`: `<=`
- `contains`: `in`

By default rules that are excluded by their options will default to `False`. If you want to default to `True` instead, you can specify `filtered_resolution=True` on your rule.

To check if the player can reach a switch, or if they've received the switch item if switches are randomized:

```python
rule = (
    Has("Red switch", options=[OptionFilter(SwitchRando, 1)])
    | CanReachLocation("Red switch", options=[OptionFilter(SwitchRando, 0)])
)
```

To add an extra logic requirement on the easiest difficulty which is ignored for other difficulties:

```python
rule = (
    # ...the rest of the logic
    & Has("QoL item", options=[OptionFilter(Difficulty, Difficulty.option_easy)], filtered_resolution=True)
)
```

If you would like to provide option filters when reusing or composing rules, you can use the `Filtered` helper rule:

```python
common_rule = Has("A") | HasAny("B", "C")
...
rule = (
    Filtered(common_rule, options=[OptionFilter(Opt, 0)]),
    | Filtered(Has("X") | CanReachRegion("Y"), options=[OptionFilter(Opt, 1)]),
)
```

You can also use the & and | operators to apply options to rules:

```python
common_rule = Has("A")
easy_filter = [OptionFilter(Difficulty, Difficulty.option_easy)]
common_rule_only_on_easy = common_rule & easy_filter
common_rule_skipped_on_easy = common_rule | easy_filter
```

## Enabling caching

The rule builder provides a `CachedRuleBuilderWorld` base class for your `World` class that enables caching on your rules.

```python
class MyWorld(CachedRuleBuilderWorld):
    game = "My Game"
```

If your world's logic is very simple and you don't have many nested rules, the caching system may have more overhead cost than time it saves. You'll have to benchmark your own world to see if it should be enabled or not.

### Item name mapping

If you have multiple real items that map to a single logic item, add a `item_mapping` class dict to your world that maps actual item names to real item names so the cache system knows what to invalidate.

For example, if you have multiple `Currency x<num>` items on locations, but your rules only check a singular logical `Currency` item, eg `Has("Currency", 1000)`, you'll want to map each numerical currency item to the single logical `Currency`.

```python
class MyWorld(CachedRuleBuilderWorld):
    item_mapping = {
        "Currency x10": "Currency",
        "Currency x50": "Currency",
        "Currency x100": "Currency",
        "Currency x500": "Currency",
    }
```

## Defining custom rules

You can create a custom rule by creating a class that inherits from `Rule` or any of the default rules. You must provide the game name as an argument to the class. It's recommended to use the `@dataclass` decorator to reduce boilerplate, and to also provide your world as a type argument to add correct type checking to the `_instantiate` method.

You must provide or inherit a `Resolved` child class that defines an `_evaluate` method. This class will automatically be converted into a frozen `dataclass`. If your world has caching enabled you may need to define one or more dependencies functions as outlined below.

To add a rule that checks if the user has enough mcguffins to goal, with a randomized requirement:

```python
@dataclasses.dataclass()
class CanGoal(Rule["MyWorld"], game="My Game"):
    @override
    def _instantiate(self, world: "MyWorld") -> Rule.Resolved:
        # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
        return self.Resolved(world.required_mcguffins, player=world.player, caching_enabled=True)

    class Resolved(Rule.Resolved):
        goal: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has("McGuffin", self.player, count=self.goal)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            # this function is only required if you have caching enabled
            return {"McGuffin": {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            # this method can be overridden to display custom explanations
            return [
                {"type": "text", "text": "Goal with "},
                {"type": "color", "color": "green" if state and self(state) else "salmon", "text": str(self.goal)},
                {"type": "text", "text": " McGuffins"},
            ]
```

Your custom rule can also resolve to builtin rules instead of needing to define your own:

```python
@dataclasses.dataclass()
class ComplicatedFilter(Rule["MyWorld"], game="My Game"):
    def _instantiate(self, world: "MyWorld") -> Rule.Resolved:
        if world.some_precalculated_bool:
            return Has("Item 1").resolve(world)
        if world.options.some_option:
            return CanReachRegion("Region 1").resolve(world)
        return False_().resolve(world)
```

### Item dependencies

If your world inherits from `CachedRuleBuilderWorld` and there are items that when collected will affect the result of your rule evaluation, it must define an `item_dependencies` function that returns a mapping of the item name to the id of your rule. These dependencies will be combined to inform the caching system. It may be worthwhile to define this function even when caching is disabled as more things may use it in the future.

```python
@dataclasses.dataclass()
class MyRule(Rule["MyWorld"], game="My Game"):
    class Resolved(Rule.Resolved):
        item_name: str

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}
```

All of the default `Has*` rules define this function already.

### Region dependencies

If your custom rule references other regions, it must define a `region_dependencies` function that returns a mapping of region names to the id of your rule regardless of if your world inherits from `CachedRuleBuilderWorld`. These dependencies will be combined to register indirect connections when you set this rule on an entrance and inform the caching system if applicable.

```python
@dataclasses.dataclass()
class MyRule(Rule["MyWorld"], game="My Game"):
    class Resolved(Rule.Resolved):
        region_name: str

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {self.region_name: {id(self)}}
```

The default `CanReachLocation`, `CanReachRegion`, and `CanReachEntrance` rules define this function already.

### Location dependencies

If your custom rule references other locations, it must define a `location_dependencies` function that returns a mapping of the location name to the id of your rule regardless of if your world inherits from `CachedRuleBuilderWorld`. These dependencies will be combined to register indirect connections when you set this rule on an entrance and inform the caching system if applicable.

```python
@dataclasses.dataclass()
class MyRule(Rule["MyWorld"], game="My Game"):
    class Resolved(Rule.Resolved):
        location_name: str

        @override
        def location_dependencies(self) -> dict[str, set[int]]:
            return {self.location_name: {id(self)}}
```

The default `CanReachLocation` rule defines this function already.

### Entrance dependencies

If your custom rule references other entrances, it must define a `entrance_dependencies` function that returns a mapping of the entrance name to the id of your rule regardless of if your world inherits from `CachedRuleBuilderWorld`. These dependencies will be combined to register indirect connections when you set this rule on an entrance and inform the caching system if applicable.

```python
@dataclasses.dataclass()
class MyRule(Rule["MyWorld"], game="My Game"):
    class Resolved(Rule.Resolved):
        entrance_name: str

        @override
        def entrance_dependencies(self) -> dict[str, set[int]]:
            return {self.entrance_name: {id(self)}}
```

The default `CanReachEntrance` rule defines this function already.

### Rule explanations

Resolved rules have a default implementation for `explain_json` and `explain_str` functions. The former optionally accepts a `CollectionState` and returns a list of `JSONMessagePart` appropriate for `print_json` in a client. It will display a human-readable message that explains what the rule requires. The latter is similar but returns a string. It is useful when debugging. There is also a `__str__` method defined to check what a rule is without a state.

To implement a custom message with a custom rule, override the `explain_json` and/or `explain_str` method on your `Resolved` class:

```python
class MyRule(Rule, game="My Game"):
    class Resolved(Rule.Resolved):
        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            has_item = state and state.has("growth spurt", self.player)
            color = "yellow"
            start = "You must be "
            if has_item:
                start = "You are "
                color = "green"
            elif state is not None:
                start = "You are not "
                color = "salmon"
            return [
                {"type": "text", "text": start},
                {"type": "color", "color": color, "text": "THIS"},
                {"type": "text", "text": " tall to beat the game"},
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            if state.has("growth spurt", self.player):
                return "You ARE this tall and can beat the game"
            return "You are not THIS tall and cannot beat the game"

        @override
        def __str__(self) -> str:
            return "You must be THIS tall to beat the game"
```

### Cache control

By default your custom rule will work through the cache system as any other rule if caching is enabled. There are two class attributes on the `Resolved` class you can override to change this behavior.

- `force_recalculate`: Setting this to `True` will cause your custom rule to skip going through the caching system and always recalculate when being evaluated. When a rule with this flag enabled is composed with `And` or `Or` it will cause any parent rules to always force recalculate as well. Use this flag when it's difficult to determine when your rule should be marked as stale.
- `skip_cache`: Setting this to `True` will also cause your custom rule to skip going through the caching system when being evaluated. However, it will **not** affect any other rules when composed with `And` or `Or`, so it must still define its `*_dependencies` functions as required. Use this flag when the evaluation of this rule is trivial and the overhead of the caching system will slow it down.

### Caveats

- Ensure you are passing `caching_enabled=True` in your `_instantiate` function when creating resolved rule instances if your world has opted into caching.
- Resolved rules are forced to be frozen dataclasses. They and all their attributes must be immutable and hashable.
- If your rule creates child rules ensure they are being resolved through the world rather than creating `Resolved` instances directly.

## Serialization

The rule builder is intended to be written first in Python for optimization and type safety. To facilitate exporting the rules to a client or tracker, rules have a `to_dict` method that returns a JSON-compatible dict. Since the location and entrance logic structure varies greatly from world to world, the actual JSON dumping is left up to the world dev.

The dict contains a `rule` key with the name of the rule, an `options` key with the rule's list of option filters, and an `args` key that contains any other arguments the individual rule has. For example, this is what a simple `Has` rule would look like:

```python
{
    "rule": "Has",
    "options": [],
    "args": {
        "item_name": "Some item",
        "count": 1,
    },
}
```

For `And` and `Or` rules, instead of an `args` key, they have a `children` key containing a list of their child rules in the same serializable format:

```python
{
    "rule": "And",
    "options": [],
    "children": [
        ...,  # each serialized rule
    ]
}
```

A full example is as follows:

```python
rule = And(
    Has("a", options=[OptionFilter(ToggleOption, 0)]),
    Or(Has("b", count=2), CanReachRegion("c"), options=[OptionFilter(ToggleOption, 1)]),
)
assert rule.to_dict() == {
    "rule": "And",
    "options": [],
    "children": [
        {
            "rule": "Has",
            "options": [
                {
                    "option": "worlds.my_world.options.ToggleOption",
                    "value": 0,
                    "operator": "eq",
                },
            ],
            "args": {
                "item_name": "a",
                "count": 1,
            },
        },
        {
            "rule": "Or",
            "options": [
                {
                    "option": "worlds.my_world.options.ToggleOption",
                    "value": 1,
                    "operator": "eq",
                },
            ],
            "children": [
                {
                    "rule": "Has",
                    "options": [],
                    "args": {
                        "item_name": "b",
                        "count": 2,
                    },
                },
                {
                    "rule": "CanReachRegion",
                    "options": [],
                    "args": {
                        "region_name": "c",
                    },
                },
            ],
        },
    ],
}
```

### Custom serialization

To define a different format for your custom rules, override the `to_dict` function:

```python
class BasicLogicRule(Rule, game="My Game"):
    items = ("one", "two")

    def to_dict(self) -> dict[str, Any]:
        # Return whatever format works best for you
        return {
            "logic": "basic",
            "items": self.items,
        }
```

If your logic has been done in custom JSON first, you can define a `from_dict` class method on your rules to parse it correctly:

```python
class BasicLogicRule(Rule, game="My Game"):
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: type[World]) -> Self:
        items = data.get("items", ())
        return cls(*items)
```

## APIs

This section is provided for reference, refer to the above sections for examples.

### World API

These are properties and helpers that are available to you in your world.

#### Methods

- `rule_from_dict(data)`: Create a rule instance from a deserialized dict representation
- `register_rule_builder_dependencies()`: Register all rules that depend on location or entrance access with the inherited dependencies, gets called automatically after set_rules
- `set_rule(spot: Location | Entrance, rule: Rule)`: Resolve a rule, register its dependencies, and set it on the given location or entrance
- `set_completion_rule(rule: Rule)`: Sets the completion condition for this world
- `create_entrance(from_region: Region, to_region: Region, rule: Rule | None, name: str | None = None, force_creation: bool = False)`: Attempt to create an entrance from `from_region` to `to_region`, skipping creation if `rule` is defined and evaluates to `False_()` unless force_creation is `True`

#### CachedRuleBuilderWorld Properties

The following property is only available when inheriting from `CachedRuleBuilderWorld`

- `item_mapping: dict[str, str]`: A mapping of actual item name to logical item name

### Rule API

These are properties and helpers that you can use or override for custom rules.

- `_instantiate(world: World)`: Create a new resolved rule instance, override for custom rules as required
- `to_dict()`: Create a JSON-compatible dict representation of this rule, override if you want to customize your rule's serialization
- `from_dict(data, world_cls: type[World])`: Return a new rule instance from a deserialized representation, override if you've overridden `to_dict`
- `__str__()`: Basic string representation of a rule, useful for debugging

#### Resolved rule API

- `player: int`: The slot this rule is resolved for
- `_evaluate(state: CollectionState)`: Evaluate this rule against the given state, override this to define the logic for this rule
- `item_dependencies()`: A mapping of item name to set of ids, override this if your custom rule depends on item collection
- `region_dependencies()`: A mapping of region name to set of ids, override this if your custom rule depends on reaching regions
- `location_dependencies()`: A mapping of location name to set of ids, override this if your custom rule depends on reaching locations
- `entrance_dependencies()`: A mapping of entrance name to set of ids, override this if your custom rule depends on reaching entrances
- `explain_json(state: CollectionState | None = None)`: Return a list of printJSON messages describing this rule's logic (and if state is defined its evaluation) in a human readable way, override to explain custom rules
- `explain_str(state: CollectionState | None = None)`: Return a string describing this rule's logic (and if state is defined its evaluation) in a human readable way, override to explain custom rules, more useful for debugging
- `__str__()`: A string describing this rule's logic without its evaluation, override to explain custom rules
