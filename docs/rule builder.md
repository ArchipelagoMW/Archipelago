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
- `And`: Checks that all child rules are true
- `Or`: Checks that at least one child rule is true
- `Has`: Checks that the player has the given item with the given count (default 1)
- `HasAll`: Checks that the player has all given items
- `HasAny`: Checks that the player has at least one of the given items
- `CanReachLocation`: Checks that the player can reach the given location
- `CanReachRegion`: Checks that the player can reach the given region
- `CanReachEntrance`: Checks that the player can reach the given entrance

You can combine these rules together to describe the logic required for something. For example, to check if a player either has `Movement ability` or they have both `Key 1` and `Key 2`, you can do:

```python
rule = Or(
    Has("Movement ability"),
    HasAll("Key 1", "Key 2"),
)
```

When assigning the rule you must use the `set_rule` helper added by the rule mixin to correctly resolve and register the rule.

```python
self.set_rule(location_or_entrance, rule)
```

## Restricting options

Every rule allows you to specify which options it's applicable for. You can provide the argument `options` which is a dictionary of option name to expected value. If you want a comparison that isn't equals, you can add the operator name after a double underscore after the option name.

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
Or(
    Has("Red switch", options={"switch_rando": 1}),
    CanReachLocation("Red switch", options={"switch_rando": 0}),
)
```

To add an extra logic requirement on the easiest difficulty:

```python
And(
    # the rest of the logic
    Or(
        Has("QoL item", options={"difficulty": 0}),
        True_(options={"difficulty__ge": 1}),
    ),
)
```

## Defining custom rules

You can create a custom rule by creating a class that inherits from `Rule` or any of the default rules. You must provide a `Resolved` child class that defines an `_evaluate` method. You may need to also define an `item_dependencies` or `indirect_regions` function.

To add a rule that checks if the user has enough mcguffins to goal, with a randomized requirement:

```python
@dataclasses.dataclass()
class CanGoal(Rule):
    def _instantiate(self, world: "RuleWorldMixin") -> "Resolved":
        return self.Resolved(world.required_mcguffins, player=world.player)

    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        goal: int

        def _evaluate(self, state: "CollectionState") -> bool:
            return state.has("McGuffin", self.player, count=self.goal)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {"McGuffin": {id(self)}}
```

If you want to use the serialization, you must add a `custom_rule_classes` class var to your world that points to the custom rules you've defined.

```python
class MyWorld(RuleWorldMixin, World):
    game = "My Game"
    custom_rule_classes = {
        "CanGoal": CanGoal,
    }
```

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
@dataclasses.dataclass()
class MyRule(Rule):
    def to_json(self) -> Any:
        return {
            "rule": "my_rule",
            "custom_logic": [...]
        }
```

If your logic has been done in custom JSON first, you can define a `from_json` class method on your rules to parse it correctly:

```python
@dataclasses.dataclass()
class MyRule(Rule):
    @classmethod
    def from_json(cls, data: Any) -> Self:
        return cls(data.get("custom_logic"))
```

## Rule explanations

Resolved rules have a default implementation for an `explain` message, which returns a list of `JSONMessagePart` appropriate for `print_json` in a client. It will display a human-readable message that explains what the rule requires.

To implement a custom message with a custom rule, override the `explain` method on your `Resolved` class:

```python
@dataclasses.dataclass()
class MyRule(Rule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        @override
        def explain(self, state: "CollectionState | None" = None) -> "list[JSONMessagePart]":
            return [
                {"type": "text", "text": "You must be "},
                {"type": "color", "color": "green", "text": "THIS"},
                {"type": "text", "text": " tall to beat the game"},
            ]
```

## Item dependencies

If there are items that when collected will affect the result of your rule evaluation, it must define an `item_dependencies` function that returns a mapping of the item name to the id of your rule. These dependencies will be combined to inform the caching system.

```python
@dataclasses.dataclass()
class MyRule(Rule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        item_name: str

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.item_name: {id(self)}}
```

The default `Has`, `HasAll`, and `HasAny` rules define this function already.

## Indirect connections

If your custom rule references other regions, it must define an `indirect_regions` function that returns a tuple of region names. These will be collected and indirect connections will be registered when you set this rule on an entrance.

```python
@dataclasses.dataclass()
class MyRule(Rule):
    @dataclasses.dataclass(frozen=True)
    class Resolved(Rule.Resolved):
        region_name: str

        @override
        def indirect_regions(self) -> tuple[str, ...]:
            return (self.region_name,)
```

The default `CanReachLocation` and `CanReachRegion` rules define this function already.
