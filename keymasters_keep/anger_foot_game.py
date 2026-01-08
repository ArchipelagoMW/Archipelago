from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class AngerFootArchipelagoOptions:
    pass


class AngerFootGame(Game):
    name = "Anger Foot"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = None

    is_adult_only_or_unrated = False

    options_cls = AngerFootArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play with 1 of the following Anger Shoes: SHOES",
                data={"SHOES": (self.shoes, 3)},
            ),
            GameObjectiveTemplate(
                label="Play with random Anger Shoes",
                data=dict()
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Finish LEVEL",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the 2nd objective on LEVEL",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete the 3rd objective on LEVEL",
                data={"LEVEL": (self.levels, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete all objectives on 1 of: LEVELS",
                data={"LEVELS": (self.levels, 3)},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Defeat BOSS",
                data={"BOSS": (self.bosses, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def shoes() -> List[str]:
        return [
            "Boomers",
            "Brain Expanders",
            "Chargers",
            "Clown Shoes",
            "Detonators",
            "Feet",
            "Firefighters",
            "Flash Kickers",
            "Floaties",
            "Fly Whisperers",
            "Gamblers",
            "Holy Sandals",
            "Plakkies",
            "Pumped Kicks",
            "Rage Runners",
            "Revengers",
            "Scavengers",
            "Size Threes",
            "Slide Kickers",
            "Soul Suckers",
            "Stilettos",
            "Thrusters",
            "Timestoppers",
            "Uppercutters",
        ]

    @staticmethod
    def levels() -> List[str]:
        return [
            "Violence Gang #1 (Sneaker Shakedown)",
            "Violence Gang #2 (The Chase Begins)",
            "Violence Gang #3 (Sunny Hill Apartments)",
            "Violence Gang #4 (Petrol Party)",
            "Violence Gang #5 (Barksdale Manor)",
            "Violence Gang #6 (Pine Tree Heights)",
            "Violence Gang #7 (Riot Control)",
            "Violence Gang #8 (Bombing Run)",
            "Violence Gang #9 (Hothead Hotel)",
            "Violence Gang #10 (Eastbrooke Suites)",
            "Violence Gang #11 (Corridor Crunch)",
            "Violence Gang #12 (Going Up)",
            "Violence Gang #13 (Narcotomi Towers)",
            "Violence Gang #14 (Rooftop Rampage)",
            "Violence Gang #15 (Potshots)",
            "Pollution Gang #1 (Down the Drain)",
            "Pollution Gang #2 (Pipe City)",
            "Pollution Gang #3 (The Deep End)",
            "Pollution Gang #4 (Steam Sewer)",
            "Pollution Gang #5 (The Slime Pits)",
            "Pollution Gang #6 (Slithering Canals)",
            "Pollution Gang #7 (Pollution Penitentiary)",
            "Pollution Gang #8 (The Septic Pools)",
            "Pollution Gang #9 (Clogged)",
            "Pollution Gang #10 (Poo Gutter)",
            "Pollution Gang #11 (Containment Breach)",
            "Pollution Gang #12 (Experimental Facility)",
            "Pollution Gang #13 (Tentacle Teardown)",
            "Business Gang #1 (Transit Hub)",
            "Business Gang #2 (The Trainyard)",
            "Business Gang #3 (Derailed)",
            "Business Gang #4 (Entry Level Position)",
            "Business Gang #5 (Glass Ceilings)",
            "Business Gang #6 (The Bullpen)",
            "Business Gang #7 (Bear Market)",
            "Business Gang #8 (Elevator Hell)",
            "Business Gang #9 (Market Forces)",
            "Business Gang #10 (Supply Chain)",
            "Business Gang #11 (Booming Industry)",
            "Business Gang #12 (Corporate Takeover)",
            "Business Gang #13 (Import Extort)",
            "Business Gang #14 (Glock Exchange)",
            "Business Gang #15 (Executive Order)",
            "Debauchery Gang #1 (Club Debauchery)",
            "Debauchery Gang #2 (Deep Dish Depravity)",
            "Debauchery Gang #3 (High Stakes)",
            "Debauchery Gang #4 (Deplorable Dungeon)",
            "Debauchery Gang #5 (Sinful Celebration)",
            "Debauchery Gang #6 (Crawlspace)",
            "Debauchery Gang #7 (The Firepit)",
            "Debauchery Gang #8 (Pie in the Sky)",
            "Debauchery Gang #9 (Pit Party)",
            "Debauchery Gang #10 (Mozzarella Riviera)",
            "Debauchery Gang #11 (Dancefloor Decadence)",
            "Debauchery Gang #12 (Sensual Delights)",
            "Debauchery Gang #13 (Unholy Halls)",
            "Crime Tower #1 (Put Foot)",
            "Crime Tower #2 (Crime Tower)",
            "Crime Tower #3 (Municipal Mayhem)",
            "Crime Tower #4 (The Final Kick)",
        ]

    @staticmethod
    def bosses() -> List[str]:
        return [
            "Goocopkopter",
            "The Sludge Baron",
            "The CEO",
            "Pizza Pig",
        ]


# Archipelago Options
# ...
