from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class UniversalStudiosExperienceMinecraftBedrockArchipelagoOptions:
    pass


class UniversalStudiosExperienceMinecraftBedrockGame(Game):
    name = "Universal Studios Experience (Minecraft Bedrock)"
    platform = KeymastersKeepGamePlatforms.MOD

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = UniversalStudiosExperienceMinecraftBedrockArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Return COUNT Golden Letters to the Universal Globe",
                data={
                    "COUNT": (self.golden_letter_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find / Interact with the following Character: CHARACTER",
                data={
                    "CHARACTER": (self.characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Experience the following Attraction: ATTRACTION",
                data={
                    "ATTRACTION": (self.attractions, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete the following Minigame: MINIGAME",
                data={
                    "MINIGAME": (self.minigames, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="At the Discovering Dinosaurs exhibit, find the following Dinosaur: DINOSAUR",
                data={
                    "DINOSAUR": (self.dinosaurs, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Correctly guess COUNT Eggs at the Hatchery",
                data={
                    "COUNT": (self.egg_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Set the Holoscape to display the following Dinosaur: DINOSAUR",
                data={
                    "DINOSAUR": (self.holoscape, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="At the DNA Sequencing Lab, create a Dinosaur with the following Traits: TRAIT1, TRAIT2, TRAIT3, TRAIT4",
                data={
                    "TRAIT1": (self.dna_traits_1, 1),
                    "TRAIT2": (self.dna_traits_2, 1),
                    "TRAIT3": (self.dna_traits_3, 1),
                    "TRAIT4": (self.dna_traits_4, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def attractions() -> List[str]:
        return [
            "E.T. Adventure",
            "Revenge of the Mummy",
            "The World-Famous Studio Tour (First Car)",
            "The World-Famous Studio Tour (Second Car)",
            "The World-Famous Studio Tour (Third Car)",
            "JAWS",
            "Back to the Future: The Ride",
            "Jurassic World - The Ride",
            "Amber Mines",
            "Skull Island: Reign of Kong",
            "Hatchery Show in the Innovation Center",
        ]

    @staticmethod
    def minigames() -> List[str]:
        return [
            "Revenge of the Mummy PVE Battle",
            "Studio Tour Quiz",
            "JAWS Treasure Dive",
            "Back to the future Hoverboard Chase",
            "Raptor Encounter",
            "Skull Island Reign of Kong Temple Minigame",
            "Far Far Away Theater",
        ]

    @staticmethod
    def dinosaurs() -> List[str]:
        return [
            "Apatosaurus",
            "Gallinimus",
            "Pteranodon",
            "Pachycephalosaurus",
        ]

    @staticmethod
    def egg_count_range() -> range:
        return range(2, 6)

    @staticmethod
    def holoscape() -> List[str]:
        return [
            "Ankylosaurus",
            "Brachiosaurus",
            "Indominus Rex",
            "Dilophosaurus",
            "Mosasaurus",
            "Parasaurolophus",
            "Stegosaurus",
            "Tyrannosarus Rex",
            "Triceratops",
            "Velociraptor",
        ]

    @staticmethod
    def dna_traits_1() -> List[str]:
        return [
            "Carnivore",
            "Herbivore",
        ]

    @staticmethod
    def dna_traits_2() -> List[str]:
        return [
            "Strong",
            "Fast",
        ]

    @staticmethod
    def dna_traits_3() -> List[str]:
        return [
            "Large",
            "Small",
        ]

    @staticmethod
    def dna_traits_4() -> List[str]:
        return [
            "Solo",
            "Pack",
        ]

    @staticmethod
    def characters() -> List[str]:
        return [
            "Claire",
            "Triceratops",
            "Baby Triceratops",
            "Raptor",
            "Female (outside of Reign of Kong)",
            "Sleeping Kong",
            "Donkey",
            "Shrek",
            "Kitty Softpaws",
            "Perrito",
            "Puss in boots",
            "Far Far Away Castle Characters",
            "Frankenstein",
            "Bride of Frankenstein",
            "Dracula",
            "Rick O'Connell",
            "The Mummy",
            "Worried Studio person (near the Mummy attraction)",
            "JAWS statue",
            "Dean (outside of JAWS ride)",
            "Doc Brown",
            "Einstein",
            "Marty Mcfly",
            "Biff",
            "Woody Woodpecker",
            "Princess Fiona",
            "Magic Mirror",
            "Ghost of Lord Farquad",
            "Drago",
        ]

    @staticmethod
    def golden_letter_count_range() -> range:
        return range(2, 9)

# Archipelago Options
# ...
