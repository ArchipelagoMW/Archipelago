from __future__ import annotations

from typing import TYPE_CHECKING

import BaseClasses
from worlds.AutoWorld import World

if TYPE_CHECKING:
    from . import FactorioBobs, InternalItem, all_ingredients, Technology, Recipe, recipes


class Rule:
    def __init__(self, world: World):
        self.world = world

    def eval(self, state: BaseClasses.CollectionState) -> bool:
        raise NotImplementedError("You must implement this method")


class AndRule(Rule):
    def __init__(self, world: World, *rules: Rule):
        super().__init__(world)
        self.rules = rules

    def eval(self, state: BaseClasses.CollectionState) -> bool:
        return all(rule.eval(state) for rule in self.rules)


class OrRule(Rule):
    def __init__(self, world: World, *rules: Rule):
        super().__init__(world)
        self.rules = rules

    def eval(self, state: BaseClasses.CollectionState) -> bool:
        return any(rule.eval(state) for rule in self.rules)

class FactorioRule(Rule):
    def __init__(self, world: "FactorioBobs"):
        super().__init__(world)

class TechRule(FactorioRule):
    made_rules: dict[str, TechRule] = {}
    def __new__(cls, world: "FactorioBobs", tech: str | Technology):
        if tech is Technology:
            tech = tech.name

        if tech in cls.made_rules:
            return cls.made_rules[tech]
        return super(TechRule, cls).__new__(cls)

    def __init__(self, world: "FactorioBobs", tech: str | Technology):
        super().__init__(world)
        if type(tech) is str:
            assert tech in self.world.technologies, f"{tech} is not a valid tech for rules"
            self.tech_name = tech
        else:
            self.tech_name = tech.name

    def eval(self, state: BaseClasses.CollectionState) -> bool:
        return state.has(self.tech_name, self.world.player)

class InternalItemRule(AndRule, FactorioRule):
    def __init__(self, world: "FactorioBobs", internal_item: InternalItem | str):
        if type(internal_item) is str:
            assert internal_item in all_ingredients, f"{InternalItem} is not a valid item for rules"
            self.internalItem = all_ingredients[internal_item]
        else:
            self.internalItem = internal_item
        super().__init__(world, *(TechRule(world, tech) for tech in self.internalItem.all_unlocking_technologies()))
        # self.rules = tuple(TechRule(world, tech) for tech in self.internal_item.all_unlocking_technologies())

class RecipeRule(AndRule, FactorioRule):
    def __init__(self, world: "FactorioBobs", recipe: Recipe | str):
        if type(recipe) is str:
            assert recipe in recipes, f"{recipe} is not a valid recipe for rules"
            self.recipe = recipes[recipe]
        else:
            self.recipe = recipe
        super().__init__(world, *(TechRule(world, tech) for tech in self.recipe.all_unlocking_technologies()))