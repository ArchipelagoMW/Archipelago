from __future__ import annotations

from typing import List

import functools
from dataclasses import dataclass

from Options import OptionSet

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RealmOfTheMadGodArchipelagoOptions:
    realm_of_the_mad_god_dungeon_packs: RealmOfTheMadGodDungeonPacks


class RealmOfTheMadGodGame(Game):
    name = "Realm of the Mad God"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = RealmOfTheMadGodArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as CLASS (unless otherwise specified)",
                data={
                    "CLASS": (self.classes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Unequip your pet",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Unequip your potions",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Unbind your nexus key",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="As a CATEGORY class, clear DUNGEON",
                data={
                    "CATEGORY": (self.class_categories, 1),
                    "DUNGEON": (self.dungeons, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Clear DUNGEON as the following class: CLASS",
                data={
                    "DUNGEON": (self.dungeons, 1),
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Start a new CLASS and reach Level 20",
                data={
                    "CLASS": (self.classes, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Find a UT or ST Item in DUNGEON",
                data={
                    "DUNGEON": (self.dungeons, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Find an ST Item for a Set belonging to a CATEGORY class",
                data={
                    "CATEGORY": (self.class_categories, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find a UT CATEGORY",
                data={
                    "CATEGORY": (self.ut_categories, 1),
                },
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="As a CATEGORY class, activate COUNT Beacon(s)",
                data={
                    "CATEGORY": (self.class_categories, 1),
                    "COUNT": (self.beacon_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Complete COUNT Quests in a single realm",
                data={
                    "COUNT": (self.quest_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat HERO",
                data={
                    "HERO": (self.heroes_of_oryx, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=6,
            ),
            GameObjectiveTemplate(
                label="Play the MINIGAME minigame",
                data={
                    "MINIGAME": (self.minigames, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Find a Stat-Increasing Potion in DROP",
                data={
                    "DROP": (self.potion_drops, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
        ]

    @property
    def dungeon_packs(self) -> List[str]:
        return sorted(self.archipelago_options.realm_of_the_mad_god_dungeon_packs.value)

    @property
    def has_dungeons_lategame(self) -> bool:
        return "Lategame" in self.dungeon_packs

    @property
    def has_dungeons_endgame(self) -> bool:
        return "Endgame" in self.dungeon_packs

    @property
    def has_dungeons_aliens(self) -> bool:
        return "Aliens" in self.dungeon_packs

    @staticmethod
    def classes() -> List[str]:
        return [
            "Rogue",
            "Archer",
            "Wizard",
            "Priest",
            "Warrior",
            "Knight",
            "Paladin",
            "Assassin",
            "Necromancer",
            "Huntress",
            "Mystic",
            "Trickster",
            "Sorcerer",
            "Ninja",
            "Samurai",
            "Bard",
            "Summoner",
        ]

    @staticmethod
    def class_categories() -> List[str]:
        return [
            "Dagger",
            "Bow",
            "Sword",
            "Katana",
            "Staff",
            "Wand",
            "Robe",
            "Leather Armor",
            "Heavy Armor",
        ]

    @staticmethod
    def other_item_categories() -> List[str]:
        return [
            "Ability item",
            "Ring",
        ]

    def ut_categories(self) -> List[str]:
        return sorted(self.class_categories() + self.other_item_categories())

    @functools.cached_property
    def dungeons_base(self) -> List[str]:
        return [
            "The Realm",
            "a Snake Pit",
            "a Sprite World",
            "The Cave of a Thousand Treasures",
            "an Ancient Ruins",
            "a Magic Woods",
            "an Undead Lair",
            "a Puppet Master's Theatre",
            "a Toxic Sewers",
            "a Cursed Library",
            "a Mad Lab",
            "an Abyss of Demons",
            "The Manor of the Immortals",
            "a Haunted Cemetery",
            "Davy Jones' Locker",
            "an Ice Cave",
            "an Ocean Trench",
            "The Crawling Depths",
            "a Woodland Labyrinth",
            "a Deadwater Docks",
            "a Parasite Chambers",
            "a Sulfurous Wetlands",
            "a Mountain Temple",
            "The Tavern",
            "The Lair of Draconis",
            "The Tomb of the Ancients",
            "The Third Dimension",
            "a Puppet Master's Encore",
            "a Cnidarian Reef",
            "a Lair of Shaitan",
            "a Secluded Thicket",
            "a High Tech Terror",
            "Oryx's Castle",
            "Oryx's Wine Cellar",
        ]

    @functools.cached_property
    def dungeons_potless(self) -> List[str]:
        return [
            "a Pirate Cave",
            "a Forest Maze",
            "a Spider Den",
            "a Forbidden Jungle",
            "The Hive",            
        ]
    
    @functools.cached_property
    def dungeons_rare(self) -> List[str]:
        return [
            "a Candyland Hunting Grounds",
            "The Machine",
        ]

    @functools.cached_property
    def dungeons_rare_potless(self) -> List[str]:
        return [
            "The Beachzone",
        ]

    @functools.cached_property
    def dungeons_lategame(self) -> List[str]:
        return [
            "a Fungal Cavern",
            "a Crystal Cavern",
            "The Nest",
            "The Lost Halls",
            "a Cultist Hideout",
            "The Void",
            "a Spectral Penitentiary",
            "a Kogbold Steamworks",
        ]

    @functools.cached_property
    def dungeons_endgame(self) -> List[str]:
        return [
            "an Advanced Kogbold Steamworks",
            "an Advanced Nest",
            "The Shatters",
            "Oryx's Sanctuary",
            "a Moonlight Village",
        ]

    @functools.cached_property
    def dungeons_aliens(self) -> List[str]:
        return [
            "Malogia",
            "Katalund",
            "Untaris",
            "Forax",
        ]

    def dungeons_with_pots(self) -> List[str]:
        dungeons = self.dungeons_base[:]

        if self.include_time_consuming_objectives:
            dungeons.extend(self.dungeons_rare)
        if self.has_dungeons_lategame:
            dungeons.extend(self.dungeons_lategame)
        if self.has_dungeons_endgame:
            dungeons.extend(self.dungeons_endgame)
        if self.has_dungeons_aliens:
            dungeons.extend(self.dungeons_aliens)

        return sorted(dungeons)

    def dungeons(self) -> List[str]:
        dungeons = self.dungeons_with_pots()[:]

        dungeons.extend(self.dungeons_potless)

        if self.include_time_consuming_objectives:
            dungeons.extend(self.dungeons_rare_potless)

        return sorted(dungeons)

    @staticmethod
    def advanced_biomes() -> List[str]:
        return [
            "the Coral Reefs biome",
            "the Haunted Hallows biome",
            "the Shipwreck Cove biome",
            "the Dead Church biome",
            "the Risen Hell biome",
            "the Abandoned City biome",
            "the Deep Sea Abyss biome",
            "the Carboniferous biome",
            "the Sanguine Forest biome",
            "the Runic Tundra biome",
            "the Floral Escape biome",
        ]

    def potion_drops(self) -> List[str]:
        potion_drops: List[str] = self.dungeons_with_pots()[:]

        potion_drops.extend(self.advanced_biomes())
        potion_drops.extend(self.advanced_biomes())
        potion_drops.extend(self.advanced_biomes())

        return sorted(potion_drops)

    @staticmethod
    def beacon_count_range() -> range:
        return range(1, 6)

    @staticmethod
    def quest_count_range() -> range:
        return range(4, 11)

    @staticmethod
    def heroes_of_oryx() -> List[str]:
        return [
            "a Cube God",
            "an Astral Rift",
            "The Daughter of Limon",
            "a Pentaract",
            "The Lich King",
            "The Plague Doctor",
            "The Well of Souls",
            "a Skull Shrine",
            "a Possessed Pumpkin",
            "a Sigma Werewolf",
            "a Skull Knight",
            "a Crab Soverign",
            "a Beer God",
            "The Eye of the Storm",
            "a Ghost Ship",
            "Bilgewater's Galleon",
            "a Hermit God",
            "The World's Oyster",
            "a Grand Sphinx",
            "The Jade/Garnet Statues",
            "a Rock Dragon",
            "a Goblin Patriarch",
            "a Maze Minotaur",
            "a Legion General",
            "an Adult Baneserpent",
            "an Ancient Kaiju",
            "a Flying Behemoth",
            "an Ethereal Shrine",
            "a Dwarf Miner",
            "a Corrupted Bramblethorn",
            "a Kogbold Expedition Engine",
            "a Killer Bee's Nest",
            "The Avatar of the Forgotten King",
            "a Ravenous Rot",
            "a Bloodroot Heart",
            "a Skeletal Centipede",
            "a Lost Sentry",
            "a Lord of the Lost Lands",
            "an Aerial Warship",
            "a Sentient Monolith",
            "a Lich",
            "an Ent Ancient",
            "an Oasis Giant",
            "a Ghost King",
            "a Phoenix Lord",
            "a Cosmic Sprite",
            "a Celestial Sprite",
            "a Red Demon",
            "an Elder Sprite Tree",
            "an Artificial Sprite",
            "a Maiden of the Sea",
            "an Alpha Werewolf",
            "a Sinister Scarecrow",
            "an Animal Merchant",
            "a Washed-up Captain",
            "a Death Knight",
            "a Lantern Holder",
            "a Shady Sect Leader",
            "a Demonic Effigy",
            "an Eternal Tormentor",
            "an Infernal Ironsmith",
            "an Insurgent Rebel Commander",
            "a Sword in the Stone",
            "a Slumbering Dragon",
            "a Sea Dragon",
            "a Sunken Treasure Shipwreck",
            "a Critter Brood",
            "an Alluring Blossom",
            "an Elder Ent Ancient",
            "a Hornet's Nest",
            "an Organ Harvester",
            "an Assembled Giant",
            "a Monstrous Grizzly",
            # "a Dread Angler",
            # "a Cyclops God",
        ]

    @staticmethod
    def minigames() -> List[str]:
        return [
            "Fishing",
            "Rat Extermination",
        ]


# Archipelago Options
class RealmOfTheMadGodDungeonPacks(OptionSet):
    """
    Indicates which optional dungeon packs to include when generating objectives for Realm of the Mad God.
    """

    display_name = "Realm of the Mad God Dungeon Packs"
    default = [
        "Lategame",
        "Endgame",
        "Aliens",
    ]
