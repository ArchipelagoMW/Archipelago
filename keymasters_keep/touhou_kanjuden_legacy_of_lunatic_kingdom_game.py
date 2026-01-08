from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class TouhouKanjudenLegacyOfLunaticKingdomArchipelagoOptions:
    pass


class TouhouKanjudenLegacyOfLunaticKingdomGame(Game):
    name = "Touhou Kanjuden: Legacy of Lunatic Kingdom"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = TouhouKanjudenLegacyOfLunaticKingdomArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play on Pointdevice Mode",
                data=dict(),
            ),
            GameObjectiveTemplate(
                label="Cannot use Bombs",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_lunatic, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Lunatic as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_lunatic, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_only, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_lunatic_only, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_extra, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Score SCORE points or greater on SPELL_CARDS on Lunatic as CHARACTER",
                data={
                    "SCORE": (self.score_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_easy_normal_hard, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_lunatic, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Lunatic as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_lunatic, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_hard_only, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_lunatic_only, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_extra, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Easy as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Normal as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Hard as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Graze GRAZE times or greater on SPELL_CARDS on Lunatic as CHARACTER",
                data={
                    "GRAZE": (self.graze_range, 1),
                    "SPELL_CARDS": (self.spell_cards_all, 1),
                    "CHARACTER": (self.player_characters, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat BOSS as CHARACTER with POWER or greater power remaining in Point Device mode",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "POWER": (self.power_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat BOSS as CHARACTER with POWER or greater power remaining in Legacy mode",
                data={
                    "BOSS": (self.bosses, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "POWER": (self.power_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE as CHARACTER with POWER or greater power remaining in Point Device mode",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "POWER": (self.power_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Beat STAGE as CHARACTER with POWER or greater power remaining in Legacy mode",
                data={
                    "STAGE": (self.stages, 1),
                    "CHARACTER": (self.player_characters, 1),
                    "POWER": (self.power_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def player_characters() -> List[str]:
        return [
            "Reimu Hakurei",
            "Marisa Kirisame",
            "Sanae Kochiya",
            "Reisen Udongein Inaba",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Seiran",
            "Ringo",
            "Doremy Sweet",
            "Sagume Kishin",
            "Clownpiece",
            "Junko",
            "Hecatia Lapislazuli",
        ]

    @staticmethod
    def spell_cards_easy_normal() -> List[str]:
        return [
            "Rabbit Sign 'Strawberry Dango'",
            "Dream Sign 'Scarlet Nightmare'",
            "Dream Sign 'Indigo Dream of Anxiety'",
            "Dream Sign 'Ochre Confusion'",
            "Dream Sign 'Dream Catcher'",
            "Orb Sign 'Disorderly Flock's Curse'",
            "Orb Sign 'Impure Body Detection Mines'",
            "Orb Sign 'Shotgun Coronation of the Gods'",
            "Hell Sign 'Hell Eclipse'",
            "Hell Sign 'Flash and Stripe'",
            "'Fake Apollo'",
            "'Primordial Divine Spirit World'",
            "Pure Sign 'Purely Bullet Hell'",
        ]

    @staticmethod
    def spell_cards_easy_normal_hard() -> List[str]:
        return [
            "Bullet Sign 'Eagle Shooting'",
            "Moon-Viewing 'September Full Moon'",
            "Hellfire 'Graze Inferno'",
            "'Overflowing Blemishes'",
        ]

    @staticmethod
    def spell_cards_hard_lunatic() -> List[str]:
        return [
            "Assassin's Bullet 'Speed Strike'",
            "Rabbit Sign 'Berry Berry Dango'",
            "Dream Sign 'Scarlet Oppressive Nightmare'",
            "Dream Sign 'Ochre Labyrinthine Confusion'",
            "Orb Sign 'Impure Body Detection Mines V2'",
            "Orb Sign 'Shining Shotgun Coronation of the Gods'",
            "Hell Sign 'Eclipse of Hell'",
            "Hell Sign 'Star and Stripe'",
            "'Apollo Hoax Theory'",
            "'Modern Divine Spirit World'",
            "'Pure Sign' A Pristine Danmaku Hell",
        ]

    @staticmethod
    def spell_cards_hard_only() -> List[str]:
        return [
            "Dream Sign 'Indigo Three-Layered Dream of Anxiety'",
            "Dream Sign 'Azure Dream Catcher'",
            "Orb Sign 'Disorderly Flock's Reverse Curse'",
            "Inferno 'Striped Abyss'",
        ]

    @staticmethod
    def spell_cards_lunatic_only() -> List[str]:
        return [
            "Bullet Sign 'The Eagle Has Shot Its Target'",
            "Moon-Viewing Sake 'Lunatic September'",
            "Dream Sign 'Eternally Anxious Dream'",
            "Dream Sign 'Losing Oneself in a Dream'",
            "Orb Sign 'Disorderly Flock's Duplex Curse'",
            "'Refinement of Earthen Impurity'",
        ]

    @staticmethod
    def spell_cards_all() -> List[str]:
        return [
            "Gun Sign 'Lunatic Gun'",
            "Rabbit Sign 'Dango Influence'",
            "Moon Sign 'Ultramarine Lunatic Dream'",
            "'One-Winged White Heron'",
            "'Pure Light of the Palm'",
            "'Lilies of Murderous Intent'",
            "'Trembling, Shivering Star'",
            "'Pristine Lunacy'",
        ]

    @staticmethod
    def spell_cards_extra() -> List[str]:
        return [
            "Butterfly 'Butterfly Supplantation'",
            "Super-Express 'Dream Express'",
            "Crawling Dream 'Creeping Bullet'",
            "Otherworld 'Oumagatoki'",
            "Earth 'Impurity Within One's Body'",
            "Moon 'Apollo Reflection Mirror'",
            "'Simple Danmaku for Cornering a Trapped Rat'",
            "Otherworld 'Hell's Non-Ideal Danmaku'",
            "Earth 'Rain Falling in Hell'",
            "Moon 'Lunatic Impact'",
            "'Pristine Danmaku for Killing a Person'",
            "'Trinitarian Rhapsody'",
            "'First and Last Nameless Danmaku'",
        ]

    @staticmethod
    def difficulties() -> List[str]:
        return [
            "Easy",
            "Normal",
            "Hard",
            "Lunatic",
        ]

    @staticmethod
    def stages() -> List[str]:
        return [
            "1",
            "2",
            "3",
            "4",
            "5",
            "Extra",
        ]

    @staticmethod
    def graze_range() -> range:
        return range(25, 101, 5)

    @staticmethod
    def power_range() -> List[float]:
        return [round(x / 100.0, 2) for x in range(0, 401, 5)]

    @staticmethod
    def score_range() -> range:
        return range(1000, 650001, 1000)


# Archipelago Options
# ...
