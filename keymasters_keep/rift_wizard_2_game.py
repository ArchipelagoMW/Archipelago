from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class RiftWizard2ArchipelagoOptions:
    pass


class RiftWizard2Game(Game):
    name = "Rift Wizard 2"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = RiftWizard2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play the Improviser trial",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="You YODA buy perks that cost X",
                data={
                    "YODA": (self.yoda, 1),
                    "X": (self.perkcosts, 1),
                },
            ),
            GameObjectiveTemplate(
                label="The majority of the skills you purchase must have the SKILLTYPE tag",
                data={
                    "SKILLTYPE": (self.skilltype, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Buy exactly X spells",
                data={
                    "X": (self.spellnum, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Once you equip an item, you cannot swap it for a different one",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Win a run using a majority of SPELLTYPE Spells",
                data={
                    "SPELLTYPE": (self.spelltype, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Win a run with one of: BIGSKILL",
                data={
                    "BIGSKILL": (self.bigskill, 2),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Defeat Rift 10 while BIGCHALLENGE",
                data={
                    "BIGCHALLENGE": (self.bigchallenge, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Reach Mordred in the TRIAL Archmage Trial",
                data={
                    "TRIAL": (self.trials, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def spelltype() -> List[str]:
        return [
            "Fire",
            "Lightning",
            "Ice",
            "Nature",
            "Arcane",
            "Dark",
            "Holy",
            "Sorcery",
            "Conjuration",
            "Enchantment",
            "Metallic",
        ]

    @staticmethod
    def skilltype() -> List[str]:
        return [
            "Fire",
            "Lightning",
            "Ice",
            "Nature",
            "Arcane",
            "Dark",
            "Holy",
            "Sorcery",
            "Conjuration",
        ]

    @staticmethod
    def spellnum() -> range:
        return range(3, 12)

    @staticmethod
    def perkcosts() -> range:
        return range(4, 7)

    @staticmethod
    def yoda() -> List[str]:
        return [
            "can only",
            "cannot",
        ]

    @staticmethod
    def bigskill() -> List[str]:
        return [
            "Soul Harvest",
            "Serpents of Chaos",
            "Orb Lord",
            "Arch Conjurer",
            "Arch Enchanter",
            "Arch Sorcerer",
            "Ice Tap",
            "Inferno Engines",
            "Lightning Frenzy",
            "Moonspeaker",
            "Chaos Familiar and Deathchill Familiar",
            "two Poison-related skills",
            "Arcane Combustion and Master of Space",
            "Steam Anima",
            "Necrostatics",
            "Storm Caller",
            "Scent of Blood",
            "Hypocrisy",
            "Unblinking Eye",
            "Master of Memories and Arcane Accounting",
            "Voidflame Lantern and Lifespark Lantern",
            ">9SP of Fire skills",
            ">9SP of Lightning skills",
            ">9SP of Ice skills",
            ">9SP of Nature skills",
            ">9SP of Arcane skills",
            ">9SP of Dark skills",
            ">9SP of Holy skills",
        ]
    
    @staticmethod
    def bigchallenge() -> List[str]:
        return [
            "only using Blood spells",
            "upgrading each spell you buy before buying anything else",
            "only using spells below level 3",
            "only using Enchantment spells",
            "only picking up SP and consumables",
            "only using spells that can damage you",
            "passing your first 2 turns in each rift",
            "only using Metallic spells after rift 1",
            "only using Holy spells",
            "purchasing 4 Eye spells",
            "never boosting your spells' damage or minion damage",
        ]
        
    @staticmethod
    def trials() -> List[str]:
        return [
            "Menagerist",
            "Mutant Masher",
            "Giant Slayer",
            "Staff Abuser",
            "Ogre Mage",
        ]

# Archipelago Options
# ...
