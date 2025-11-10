from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.AutoWorld import World

from . import Technologies
from .InternalItem import all_ingredients, recipes

if TYPE_CHECKING:
    from . import FactorioBobs, InternalItem, Recipe
    from BaseClasses import CollectionState


class Rule:
    def eval(self, world: World, state: "CollectionState") -> bool:
        raise NotImplementedError("You must implement this method")

    def optimize(self) -> Rule:
        return self

    def needed_items(self) -> set[str]:
        return set()


class AndRule(Rule):
    def __init__(self, *rules: Rule):
        super().__init__()
        self.rules = rules

    def eval(self, world: World, state: "CollectionState") -> bool:
        return all(rule.eval(world, state) for rule in self.rules)

    def optimize(self) -> AndRule:
        new_rule_set = set()
        for rule in self.rules:
            optimized_rule = rule.optimize()
            if isinstance(rule, AndRule):
                rule: AndRule # makes the type checker happy
                new_rule_set = new_rule_set.union(optimized_rule.rules)
            else:
                new_rule_set.add(optimized_rule)
        return AndRule(*new_rule_set)

    def needed_items(self) -> set[str]:
        return set(x for rule in self.rules for x in rule.needed_items())


class OrRule(Rule):
    def __init__(self, *rules: Rule):
        super().__init__()
        self.rules = rules

    def eval(self, world: World, state: "CollectionState") -> bool:
        return any(rule.eval(world, state) for rule in self.rules)

    def optimize(self) -> OrRule:
        new_rule_set = set()
        for rule in self.rules:
            optimized_rule = rule.optimize()
            if isinstance(rule, OrRule):
                rule: OrRule # makes the type checker happy
                new_rule_set = new_rule_set.union(optimized_rule.rules)
            else:
                new_rule_set.add(optimized_rule)
        return OrRule(*new_rule_set)

    def needed_items(self) -> set[str]:
        return set(x for rule in self.rules for x in rule.needed_items())

class FactorioRule(Rule):
    def eval(self, world: "FactorioBobs", state: "CollectionState") -> bool:
        raise NotImplementedError("You must implement this method")

class TechRule(FactorioRule):
    made_rules: dict[str, TechRule] = {}
    def __new__(cls, tech: str | Technologies.Technology):
        if tech is Technologies.Technology:
            tech = tech.name

        if tech in cls.made_rules:
            return cls.made_rules[tech]
        return super(TechRule, cls).__new__(cls)

    def __init__(self, tech: str | Technologies.Technology):
        super().__init__()
        if type(tech) is str:
            assert tech in Technologies.base_technology_table, f"{tech} is not a valid tech for rules"
            self.tech_name = tech
        else:
            self.tech_name = tech.name

    def eval(self, world: "FactorioBobs", state: "CollectionState") -> bool:
        return state.has(self.tech_name, world.player)

    def needed_items(self) -> set[str]:
        return {self.tech_name,}

class InternalItemRule(AndRule, FactorioRule):
    def __init__(self, internal_item: InternalItem | str):
        if type(internal_item) is str:
            assert internal_item in all_ingredients, f"{InternalItem} is not a valid item for rules"
            self.internalItem = all_ingredients[internal_item]
        else:
            self.internalItem = internal_item
        super().__init__(*(TechRule(tech) for tech in self.internalItem.all_unlocking_technologies()))

class RecipeRule(AndRule, FactorioRule):
    def __init__(self, recipe: Recipe | str):
        if type(recipe) is str:
            assert recipe in recipes, f"{recipe} is not a valid recipe for rules"
            self.recipe = recipes[recipe]
        else:
            self.recipe = recipe
        super().__init__(*(TechRule(tech) for tech in self.recipe.all_unlocking_technologies()))