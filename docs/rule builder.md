# Rule Builder

This document describes the API provided for the rule builder. Using this API prvoides you with with a simple interface to define rules and the following advantages:

- Automatic result caching
- Logic optimization
- Serialize/deserialize to JSON
- Human-readable logic explanations

## Usage

The rule builder provides a `RuleWorldMixin` for your `World` class that provides some helpers for you.

```python
class MyWorld(RuleWorldMixin, World):
    game = "My Game"
```

The rule builder comes with a few rules by default:

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

When assigning the rule you must use the `set_rule` helper added by the rule mixin to correctly resolve and register the rule.

```python
self.set_rule(location_or_entrance, rule)
```

There is also a `create_entrance` helper that will resolve the rule, check if it's `False`, and if not create the entrance and set the rule. This allows you to skip creating entrances that will never be valid.

```python
self.create_entrance(from_region, to_region, rule)
```

> ⚠️ If you use a `CanReachLocation` rule on an entrance, you will either have to create the locations first, or specify the location's parent region name with the `parent_region_name` argument of `CanReachLocation`.

You can also set a rule for your world's completion condition:

```python
self.set_completion_rule(rule)
```

If your rules use `CanReachLocation`, `CanReachEntrance` or a custom rule that depends on locations or entrances, you must call `self.register_dependencies()` after all of your locations and entrances exist to setup the caching system.

### Restricting options

Every rule allows you to specify which options it's applicable for. You can provide the argument `options` which is an iterable of `OptionFilter` instances. If you want a comparison that isn't equals, you can specify with the `operator` arguemnt.

The following operators are allowed:

- `eq`: `==`
- `ne`: `!=`
- `gt`: `>`
- `lt`: `<`
- `ge`: `>=`
- `le`: `<=`
- `contains`: `in`

To check if the player can reach a switch, or if they've receieved the switch item if switches are randomized:

```python
rule = (
    Has("Red switch", options=[OptionFilter(SwitchRando, 1)])
    | CanReachLocation("Red switch", options=[OptionFilter(SwitchRando, 0)])
)
```

To add an extra logic requirement on the easiest difficulty:

```python
rule = (
    # ...the rest of the logic
    & (
        Has("QoL item", options=[OptionFilter(Difficulty, Difficulty.option_easy)])
        | True_(options=[OptionFilter(Difficulty, Difficulty.option_medium, operator="ge")])
    )
)
```

If you would like to provide option filters when composing rules, you can use the `And` and `Or` rules directly:

```python
rule = Or(
    And(Has("A"), HasAny("B", "C"), options=[OptionFilter(Opt, 0)]),
    Or(Has("X"), CanReachRegion("Y"), options=[OptionFilter(Opt, 1)]),
)
```

### Disabling caching

If your world's logic is very simple and you don't have many nested rules, the caching system may have more overhead cost than time it saves. You can disable the caching system entirely by setting the `rule_caching_enabled` class property to `False` on your world:

```python
class MyWorld(RuleWorldMixin, World):
    rule_caching_enabled = False
```

You'll have to benchmark your own world to see if it should be disabled or not.

### Item name mapping

If you have multiple real items that map to a single logic item, add a `item_mapping` class dict to your world that maps actual item names to real item names so the cache system knows what to invalidate.

For example, if you have multiple `Currecy x<num>` items on locations, but your rules only check a singlular logical `Currency` item, eg `Has("Currency", 1000)`, you'll want to map each numerical currency item to the single logical `Currency`.

```python
class MyWorld(RuleWorldMixin, World):
    item_mapping = {
        "Currency x10": "Currency",
        "Currency x50": "Currency",
        "Currency x100": "Currency",
        "Currency x500": "Currency",
    }
```

## Defining custom rules

You can create a custom rule by creating a class that inherits from `Rule` or any of the default rules. You must provide the game name as an argument to the class. It's recommended to use the `@dataclass` decorator to reduce boilerplate to provide your world as a type argument to add correct type checking to the `_instantiate` method.

You must provide or inherit a `Resolved` child class that defines an `_evaluate` method. This class will automatically be converted into a frozen `dataclass`. You may need to also define one or more dependencies functions as outlined below.

To add a rule that checks if the user has enough mcguffins to goal, with a randomized requirement:

```python
@dataclasses.dataclass()
class CanGoal(Rule["MyWorld"], game="My Game"):
    def _instantiate(self, world: "MyWorld") -> "Resolved":
        return self.Resolved(world.required_mcguffins, player=world.player)

    class Resolved(Rule.Resolved):
        goal: int

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has("McGuffin", self.player, count=self.goal)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {"McGuffin": {id(self)}}
```

### Item dependencies

If there are items that when collected will affect the result of your rule evaluation, it must define an `item_dependencies` function that returns a mapping of the item name to the id of your rule. These dependencies will be combined to inform the caching system.

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

If your custom rule references other regions, it must define an `region_dependencies` function that returns a mapping of region names to the id of your rule. These will be combined to inform the caching system and indirect connections will be registered when you set this rule on an entrance.

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

If your custom rule references other locations, it must define a `location_dependencies` function that returns a mapping of the location name to the id of your rule. These dependencies will be combined to inform the caching system.

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

If your custom rule references other entrances, it must define a `entrance_dependencies` function that returns a mapping of the entrance name to the id of your rule. These dependencies will be combined to inform the caching system.

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
    def from_dict(cls, data: Mapping[str, Any]) -> Self:
        items = data.get("items", ())
        return cls(*items)
```

## Rule explanations

Resolved rules have a default implementation for `explain_json` and `explain_str` functions. The former returns a list of `JSONMessagePart` appropriate for `print_json` in a client. It will display a human-readable message that explains what the rule requires. The latter returns similar information but as a string. It is useful when debugging.

To implement a custom message with a custom rule, override the `explain_json` and/or `explain_str` method on your `Resolved` class:

```python
class MyRule(Rule, game="My Game"):
    class Resolved(Rule.Resolved):
        @override
        def explain_json(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            has_item = state and state.has("growth spurt", self.player)
            color = "yellow"
            start = "You must be "
            if has_item:
                start = "You are "
                color = "green
            elif state is not None:
                start = "You are not "
                color = "salmon"
            return [
                {"type": "text", "text": start},
                {"type": "color", "color": color, "text": "THIS"},
                {"type": "text", "text": " tall to beat the game"},
            ]

        @override
        def explain_str(self, state: "CollectionState | None" = None) -> str:
            if state is None:
                return str(self)
            if state.has("growth spurt", self.player):
                return "You ARE this tall and can beat the game"
            return "You are not THIS tall and cannot beat the game"

        @override
        def __str__(self) -> str:
            return "You must be THIS tall to beat the game"
```

## APIs

This section is provided for reference, refer to the above sections for examples.

### World API

These are properties and helpers that are available to you in your world.

#### Properties

- `completion_rule: Rule.Resolved | None`: The resolved rule used for the completion condition of this world as set by `set_completion_rule`
- `true_rule: Rule.Resolved`: A pre-resolved rule for this player that is equal to `True_()`
- `false_rule: Rule.Resolved`: A pre-resolved rule for this player that is equal to `False_()`
- `item_mapping: dict[str, str]`: A mapping of actual item name to logical item name
- `rule_caching_enabled: bool`: A boolean value to enable or disable rule caching for this world

#### Methods

- `rule_from_dict(data)`: Create a rule instance from a deserialized dict representation
- `register_dependencies()`: Register all rules that depend on location or entrance access with the inherited dependencies
- `set_rule(spot: Location | Entrance, rule: Rule)`: Resolve a rule, register its dependencies, and set it on the given location or entrance
- `create_entrance(from_region: Region, to_rengion: Region, rule: Rule | None, name: str | None = None)`: Attempt to create an entrance from `from_region` to `to_rengion`, skipping creation if `rule` is defined and evaluates to `False_()`
- `set_completion_rule(rule: Rule)`: Sets the completion condition for this world

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
