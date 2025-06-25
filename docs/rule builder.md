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

The rule builder comes with a few by default:

- `True_`: Always returns true
- `False_`: Always returns false
- `And`: Checks that all child rules are true (also provided by `&` operator)
- `Or`: Checks that at least one child rule is true (also provided by `|` operator)
- `Has`: Checks that the player has the given item with the given count (default 1)
- `HasAll`: Checks that the player has all given items
- `HasAny`: Checks that the player has at least one of the given items
- `CanReachLocation`: Checks that the player can logically reach the given location
- `CanReachRegion`: Checks that the player can logically reach the given region
- `CanReachEntrance`: Checks that the player can logically reach the given entrance

You can combine these rules together to describe the logic required for something. For example, to check if a player either has `Movement ability` or they have both `Key 1` and `Key 2`, you can do:

```python
rule = Has("Movement ability") | HasAll("Key 1", "Key 2")
```

> ⚠️ Composing rules with the `and` and `or` keywords will not work. You must use the bitwise `&` and `|` operators. In order to catch mistakes, the rule builder will not let you do boolean operations. As a consequence, in order to check if a rule is defined you must use `if rule is not None`.

When assigning the rule you must use the `set_rule` helper added by the rule mixin to correctly resolve and register the rule.

```python
self.set_rule(location_or_entrance, rule)
```

There is also a `create_entrance` helper that will resolve the rule, check if it's `False`, and if not create the entrance and set the rule. This allows you to skip creating entrances that will never be valid.

```python
self.create_entrance(from_region, to_region, rule)
```

You can also set a rule for your world's completion condition:

```python
self.set_completion_rule(rule)
```

If your rules use `CanReachLocation` or a custom rule that depends on locations, you must call `self.register_location_dependencies()` after all of your locations exist to setup the caching system.

## Restricting options

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

## Defining custom rules

You can create a custom rule by creating a class that inherits from `Rule` or any of the default rules. You must provide the game name as an argument to the class. It's recommended to use the `@dataclass` decorator to reduce boilerplate to provide your world as a type argument to add correct type checking to the `_instantiate` method.

You must provide or inherit a `Resolved` child class that defines an `_evaluate` method. This class will automatically be converted into a frozen `dataclass`. You may need to also define an `item_dependencies` or `region_dependencies` function.

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

The default `Has`, `HasAll`, and `HasAny` rules define this function already.

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

## JSON serialization

The rule builder is intended to be written first in Python for optimization and type safety. To export the rules to a client or tracker, there is a default JSON serializer implementation for all rules. By default the rules will export with the following format:

```json
{
    "rule": "<name of rule>",
    "args": {
        "options": {...},
        "<field>": <value> // for each field the rule defines
    }
}
```

The `And` and `Or` rules have a slightly different format:

```json
{
    "rule": "And",
    "options": {...},
    "children": [
        {<each serialized rule>}
    ]
}
```

To define a custom format, override the `to_json` function:

```python
class MyRule(Rule, game="My Game"):
    def to_json(self) -> Mapping[str, Any]:
        return {
            "rule": "my_rule",
            "custom_logic": [...]
        }
```

If your logic has been done in custom JSON first, you can define a `from_json` class method on your rules to parse it correctly:

```python
class MyRule(Rule, game="My Game"):
    @classmethod
    def from_json(cls, data: Mapping[str, Any]) -> Self:
        return cls(data.get("custom_logic"))
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
