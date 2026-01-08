from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from Options import Toggle

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class Bomberman64ArchipelagoOptions:
    bomberman_64_allow_rainbow_palace: Bomberman64AllowRainbowPalace


class Bomberman64Game(Game):
    # Initial implementation by @delcake on Discord

    name = "Bomberman 64"
    platform = KeymastersKeepGamePlatforms.N64

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = Bomberman64ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete objectives on DIFF difficulty where applicable",
                data={"DIFF": (self.difficulties, 1)},
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete STAGE",
                data={"STAGE": (self.base_stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete STAGE",
                data={"STAGE": (self.deep_stages, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Earn CARDS gold cards from STAGE",
                data={"CARDS": (self.stage_gold_card_range, 1), "STAGE": (self.base_stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn CARDS gold cards from STAGE",
                data={"CARDS": (self.stage_gold_card_range, 1), "STAGE": (self.deep_stages, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn the Target Time gold card from STAGE",
                data={"STAGE": (self.base_stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Earn the Target Time gold card from STAGE",
                data={"STAGE": (self.deep_stages, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Earn the Enemies Defeated gold card from STAGE",
                data={"STAGE": (self.enemy_eligible_base_stages, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Earn the Enemies Defeated gold card from STAGE",
                data={"STAGE": (self.enemy_eligible_deep_stages, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT stages in WORLD",
                data={"COUNT": (self.stage_count_range, 1), "WORLD": (self.base_worlds, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT stages in WORLD",
                data={"COUNT": (self.stage_count_range, 1), "WORLD": (self.deep_worlds, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete all stages in WORLD, earning at least CARDS gold cards from the set",
                data={"WORLD": (self.base_worlds, 1), "CARDS": (self.world_gold_card_range, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete all stages in WORLD, earning at least CARDS gold cards from the set",
                data={"WORLD": (self.deep_worlds, 1), "CARDS": (self.world_gold_card_range, 1)},
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find the PART costume item",
                data={"PART": (self.findable_custom_parts, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Earn the PART costume item",
                data={"PART": (self.earnable_custom_parts, 1)},
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def base_stages() -> List[str]:
        return [
            "Blue Resort Stage 1 - Switches and Bridges",
            "Blue Resort Stage 2 - VS Artemis",
            "Blue Resort Stage 3 - Pump it Up!",
            "Blue Resort Stage 4 - Sewer Savage",
            "Green Garden Stage 1 - Untouchable Treasure",
            "Green Garden Stage 2 - Friend or Foe?",
            "Green Garden Stage 3 - To Have or Have Not",
            "Green Garden Stage 4 - Winged Guardian",
            "Red Mountain Stage 1 - Hot on the Trail",
            "Red Mountain Stage 2 - VS Orion",
            "Red Mountain Stage 3 - On the Right Track",
            "Red Mountain Stage 4 - Hot Avenger",
            "White Glacier Stage 1 - Blizzard Peaks",
            "White Glacier Stage 2 - VS Regulus",
            "White Glacier Stage 3 - Shiny Slippy Icy Floor",
            "White Glacier Stage 4 - Cold Killers",
        ]

    @functools.cached_property
    def late_stages(self) -> List[str]:
        return [
            "Black Fortress Stage 1 - Go for Broke",
            "Black Fortress Stage 2 - High-Tech Harvester",
            "Black Fortress Stage 3 - Trap Tower",
            "Black Fortress Stage 4 - VS Altair",
        ]

    @functools.cached_property
    def secret_stages(self) -> List[str]:
        return [
            "Rainbow Palace Stage 1 - Beyond the Clouds",
            "Rainbow Palace Stage 2 - VS Spellmaker",
            "Rainbow Palace Stage 3 - Doom Castle",
            "Rainbow Palace Stage 4 - The Final Battle!",
        ]

    def deep_stages(self) -> List[str]:
        deep_stages: List[str] = self.late_stages[:]

        if self.archipelago_options.bomberman_64_allow_rainbow_palace:
            deep_stages.extend(self.secret_stages[:])

        return deep_stages

    def enemy_eligible_base_stages(self) -> List[str]:
        ignore_stages = ["Stage 2", "Stage 4"]

        return [stage for stage in self.base_stages() if not any(entry in stage for entry in ignore_stages)]
    
    def enemy_eligible_deep_stages(self) -> List[str]:
        ignore_stages = ["Stage 2", "Stage 4"]

        return [stage for stage in self.deep_stages() if not any(entry in stage for entry in ignore_stages)]

    @staticmethod
    def base_worlds() -> List[str]:
        return [
            "Blue Resort",
            "Green Garden",
            "Red Mountain",
            "White Glacier",
        ]

    @functools.cached_property
    def late_worlds(self) -> List[str]:
        return [
            "Black Fortress",
        ]

    def deep_worlds(self) -> List[str]:
        deep_worlds: List[str] = self.late_worlds[:]

        if self.archipelago_options.bomberman_64_allow_rainbow_palace:
            deep_worlds.append("Rainbow Palace")

        return deep_worlds

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Hard",
            "Normal",
        ]

    @staticmethod
    def stage_count_range() -> range:
        return range(2,5)
    
    @staticmethod
    def stage_gold_card_range() -> range:
        return range(2,6)

    @staticmethod
    def world_gold_card_range() -> range:
        return range(5,16)
    
    def findable_custom_parts(self) -> List[str]:
        findable_custom_parts = [
            # HEAD Costume Pieces
            "Dragon Head",
            "Iron Goggles",
            "Cat Hood",
            "Sunglasses",
            "Chicken Head",
            # BODY Costume Pieces
            "Dragon Mail",
            "Iron Armor",
            "Cat Suit",
            "Dress",
            "Rocking Horse",
            # ARMS Costume Pieces
            "Dragon Gloves",
            "Iron Nuckles",
            "Slash Claws",
            "Drill Arms",
            "Chicken Wings",
            # FEET Costume Pieces
            "Dragon Spikes",
            "Iron Sneakers",
            "Cat Paws (Legs)",
            "High Tops",
            "Bubby Socks",
        ]

        rainbow_palace_custom_parts = [
            "Pony Tails",
            "Duck Float",
            "Cat Paws (Arms)",
            "Duck Feet",
        ]

        if self.archipelago_options.bomberman_64_allow_rainbow_palace:
            findable_custom_parts.extend(rainbow_palace_custom_parts)

        return sorted(findable_custom_parts)

    def earnable_custom_parts(self) -> List[str]:
        earnable_custom_parts = [
            "Clown Smile",
            "Karate Ware",
            "Boxing Gloves",
            "Clogs",
        ]

        rainbow_palace_earnable_custom_parts = [
            "Samurai Head",
            "Gold Visor",
            "Shogun Kimono",
            "Gold Armor",
            "Fans",
            "Gold Gloves",
            "High Heels",
            "Gold Boots",
        ]

        if self.archipelago_options.bomberman_64_allow_rainbow_palace:
            earnable_custom_parts.extend(rainbow_palace_earnable_custom_parts)

        return sorted(earnable_custom_parts)


# Archipelago Options
class Bomberman64AllowRainbowPalace(Toggle):
    """
    Whether objectives are allowed to require accessing the secret Rainbow Palace stages.
    """
    display_name = "Bomberman 64 Allow Rainbow Palace"
