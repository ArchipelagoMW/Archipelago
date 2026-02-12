from __future__ import annotations

from typing import TYPE_CHECKING

from worlds.AutoWorld import World

from . import Technologies, FactorioModpack
from .RecipeEngine import GameItem, GameRecipe

if TYPE_CHECKING:
    from . import FactorioBobs
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
            self.tech_name = tech
        else:
            self.tech_name = tech.name

    def eval(self, world: "FactorioBobs", state: "CollectionState") -> bool:
        return state.has(self.tech_name, world.player)

    def needed_items(self) -> set[str]:
        return {self.tech_name,}

class InternalItemRule(AndRule, FactorioRule):
    def __init__(self, internal_item: GameItem):
        self.internalItem = internal_item
        super().__init__(*(TechRule(tech) for tech in self.internalItem.get_req_techs()))

class RecipeRule(AndRule, FactorioRule):
    def __init__(self, recipe: GameRecipe):
        self.recipe = recipe

        super().__init__(*(TechRule(tech) for tech in self.recipe.get_req_techs()))


def process_yaml_rule(rule_pair: dict[str, str | list], modpack: FactorioModpack) -> Rule:
    rule_type, rule_value = next(iter(rule_pair.items()))
    if rule_type == "and":
        return AndRule(*(process_yaml_rule(rule, modpack) for rule in rule_value))
    if rule_type == "or":
        return OrRule(*(process_yaml_rule(rule, modpack) for rule in rule_value))
    if rule_type == "tech":
        assert rule_value in modpack.base_technology_table.keys(), f"{rule_value} is not a valid tech for rules"
        return TechRule(rule_value)
    if rule_type == "item":
        assert rule_value in modpack.recipe_engine.all_ingredients.keys(), f"{rule_value} is not a valid item in rules"
        return InternalItemRule(modpack.recipe_engine.all_ingredients[rule_value])
    if rule_type == "recipe":
        assert rule_value in modpack.recipe_engine.recipes.keys(), f"{rule_value} is not a valid recipe in rules"
        return RecipeRule(modpack.recipe_engine.recipes[rule_value])
    raise ValueError(f"Unknown rule type {rule_type}")