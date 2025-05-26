# Rule Builder

This document describes the API provided for the rule builder. Using this API prvoides you with with a simple interface to define rules and the following advantages:

- Automatic result caching
- Branch pruning based on selected options
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

When assigning the rule you must resolve the rule against the current world, and then assign the `.test` method as the `access_rule`.

```python
resolved_rule = self.resolve_rule(rule)
set_rule(location, resolved_rule.test)
```

## Restricting options

Every rule allows you to specify which options it's applicable for. You can provide the argument `options` which is a dictionary of option name to expected value. If you want a comparison that isn't equals, you can add the operator name after a double underscore after the option name.

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
