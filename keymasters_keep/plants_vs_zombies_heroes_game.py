from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class PlantsVSZombiesHeroesArchipelagoOptions:
    plants_vs_zombies_heroes_non_starter_heroes_owned: PlantsVSZombiesHeroesNonStarterHeroesOwned


class PlantsVSZombiesHeroesGame(Game):
    name = "Plants vs. Zombies: Heroes"
    platform = KeymastersKeepGamePlatforms.IOS

    platforms_other = [
        KeymastersKeepGamePlatforms.AND,
    ]

    is_adult_only_or_unrated = False

    options_cls = PlantsVSZombiesHeroesArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play Ranked Matches only",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Don't use any Legendary cards",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Use 'Finish for Me' to create your decks after including the mandatory cards",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a game with a CLASS Plant Hero",
                data={
                    "CLASS": (self.plant_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Win a game with a CLASS Zombie Hero",
                data={
                    "CLASS": (self.zombie_classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play COUNT TRIBE Card(s)",
                data={
                    "COUNT": (self.entity_range, 1),
                    "TRIBE": (self.plant_tribes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play COUNT TRIBE Card(s)",
                data={
                    "COUNT": (self.entity_range, 1),
                    "TRIBE": (self.zombie_tribes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play COUNT Plant(s) that cost MANA or less",
                data={
                    "COUNT": (self.entity_range, 1),
                    "MANA": (self.mana_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play COUNT Plant(s) that cost MANA or more",
                data={
                    "COUNT": (self.entity_range, 1),
                    "MANA": (self.mana_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Play COUNT Zombie(s) that cost MANA or less",
                data={
                    "COUNT": (self.entity_range, 1),
                    "MANA": (self.mana_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play COUNT Zombie(s) that cost MANA or more",
                data={
                    "COUNT": (self.entity_range, 1),
                    "MANA": (self.mana_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Deal 20 Damage to Heroes as HERO",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play 2 of HERO's Superpowers",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Play all 4 of HERO's Superpowers",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Deal 300 Damage to Heroes",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win 3 Multiplayer Games with HERO",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Win a game with HERO without it ever taking damage",
                data={
                    "HERO": (self.heroes, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @property
    def non_starter_heroes_owned(self) -> List[str]:
        return sorted(self.archipelago_options.plants_vs_zombies_heroes_non_starter_heroes_owned.value)

    @functools.cached_property
    def plant_classes_base(self) -> List[str]:
        return [
            "Mega-Grow",
            "Smarty",
        ]

    def plant_classes(self) -> List[str]:
        plant_classes: List[str] = self.plant_classes_base[:]

        heroes_guardian: List[str] = [
            "Wall-Knight",
            "Spudow",
            "Citron",
            "Grass Knuckles",
            "Beta-Carrotina",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_guardian]):
            plant_classes.append("Guardian")

        heroes_kabloom: List[str] = [
            "Solar Flare",
            "Spudow",
            "Grass Knuckles",
            "Night Cap",
            "Captain Combustible",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_kabloom]):
            plant_classes.append("Kabloom")

        heroes_solar: List[str] = [
            "Solar Flare",
            "Chompzilla",
            "Rose",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_solar]):
            plant_classes.append("Solar")

        return sorted(plant_classes)

    @functools.cached_property
    def zombie_classes_base(self) -> List[str]:
        return [
            "Brainy",
            "Sneaky",
        ]

    def zombie_classes(self) -> List[str]:
        zombie_classes: List[str] = self.zombie_classes_base[:]

        heroes_beastly: List[str] = [
            "The Smash",
            "Electric Boogaloo",
            "Brain Freeze",
            "Immorticia",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_beastly]):
            zombie_classes.append("Beastly")

        heroes_crazy: List[str] = [
            "Impfinity",
            "Electric Boogaloo",
            "Professor Brainstorm",
            "Z-Mech",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_crazy]):
            zombie_classes.append("Crazy")

        heroes_hearty: List[str] = [
            "The Smash",
            "Rustbolt",
            "Z-Mech",
            "Neptuna",
        ]

        if any([hero in self.non_starter_heroes_owned for hero in heroes_hearty]):
            zombie_classes.append("Hearty")

        return sorted(zombie_classes)

    def heroes(self) -> List[str]:
        heroes: List[str] = [
            "Green Shadow",
            "Super Brainz",
        ]

        if len(self.non_starter_heroes_owned):
            heroes.extend(self.non_starter_heroes_owned)

        return sorted(heroes)

    @staticmethod
    def plant_tribes() -> List[str]:
        return [
            "Pea",
            "Bean",
            "Nut",
            "Berry",
            "Flower",
            "Mushroom",
        ]

    @staticmethod
    def zombie_tribes() -> List[str]:
        return [
            "Imp",
            "Gargantuar",
            "Pet",
            "Dancing",
            "Science",
            "History",
        ]

    @staticmethod
    def entity_range() -> range:
        return range(1, 6)

    @staticmethod
    def mana_range() -> range:
        return range(2, 5)


# Archipelago Options
class PlantsVSZombiesHeroesNonStarterHeroesOwned(OptionSet):
    """
    Indicates which non-starter heroes in Plants vs. Zombies: Heroes the player owns, if any.
    """

    display_name = "Plants vs. Zombies: Heroes Non-Starter Heroes Owned"
    valid_keys = [
        "Solar Flare",
        "Wall-Knight",
        "Chompzilla",
        "Spudow",
        "Citron",
        "Grass Knuckles",
        "Night Cap",
        "Rose",
        "Captain Combustible",
        "Beta-Carrotina",
        "The Smash",
        "Impfinity",
        "Rustbolt",
        "Electric Boogaloo",
        "Brain Freeze",
        "Professor Brainstorm",
        "Immorticia",
        "Z-Mech",
        "Neptuna",
        "Huge-Gigantacus",
    ]

    default = valid_keys
