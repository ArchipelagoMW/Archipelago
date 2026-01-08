from __future__ import annotations

import functools
from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class NeonWhiteArchipelagoOptions:
    pass


class NeonWhiteGame(Game):
    # Initial Proposal by @pitchouli on Discord

    name = "Neon White"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.PS5,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
        KeymastersKeepGamePlatforms.XSX,
    ]

    is_adult_only_or_unrated = False

    options_cls = NeonWhiteArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return list()

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Complete LEVEL and earn: MEDAL medal",
                data={
                    "LEVEL": (self.levels_standard, 1),
                    "MEDAL": (self.medals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=5,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL and earn: MEDAL medal",
                data={
                    "LEVEL": (self.levels_standard, 1),
                    "MEDAL": (self.medals_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS and earn at least COUNT MEDAL medal(s)",
                data={
                    "LEVELS": (self.levels_standard, 3),
                    "COUNT": (self.medal_count_range_low, 1),
                    "MEDAL": (self.medals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS and earn at least COUNT MEDAL medal(s)",
                data={
                    "LEVELS": (self.levels_standard, 3),
                    "COUNT": (self.medal_count_range_low, 1),
                    "MEDAL": (self.medals_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS and earn at least COUNT MEDAL medal(s)",
                data={
                    "LEVELS": (self.levels_standard, 5),
                    "COUNT": (self.medal_count_range_high, 1),
                    "MEDAL": (self.medals, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS and earn at least COUNT MEDAL medal(s)",
                data={
                    "LEVELS": (self.levels_standard, 5),
                    "COUNT": (self.medal_count_range_high, 1),
                    "MEDAL": (self.medals_hard, 1),
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete LEVEL",
                data={"LEVEL": (self.levels_sidequest, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Complete LEVELS",
                data={"LEVELS": (self.levels_sidequest, 3)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete every stage in MISSION",
                data={"MISSION": (self.missions, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Complete RUSH's Heaven Rush",
                data={"RUSH": (self.rushes, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Complete RUSH's Hell Rush",
                data={"RUSH": (self.rushes, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
        ]

    @staticmethod
    def medals() -> List[str]:
        return [
            "Bronze",
            "Silver",
            "Silver",
            "Gold",
            "Gold",
            "Gold",
        ]

    @staticmethod
    def medals_hard() -> List[str]:
        return [
            "Ace",
            "Ace",
            "Ace",
            "Red",
        ]

    @staticmethod
    def medal_count_range_low() -> range:
        return range(1, 3)

    @staticmethod
    def medal_count_range_high() -> range:
        return range(1, 5)

    @staticmethod
    def levels_standard() -> List[str]:
        return [
            "Movement (1-1)",
            "Pummel (1-2)",
            "Gunner (1-3)",
            "Cascade (1-4)",
            "Elevate (1-5)",
            "Bounce (1-6)",
            "Purify (1-7)",
            "Climb (1-8)",
            "Fasttrack (1-9)",
            "Glass Port (1-10)",
            "Take Flight (2-1)",
            "Godspeed (2-2)",
            "Dasher (2-3)",
            "Thrasher (2-4)",
            "Outstretched (2-5)",
            "Smackdown (2-6)",
            "Catwalk (2-7)",
            "Fastlane (2-8)",
            "Distinguish (2-9)",
            "Dancer (2-10)",
            "Guardian (3-1)",
            "Stomp (3-2)",
            "Jumper (3-3)",
            "Dash Tower (3-4)",
            "Descent (3-5)",
            "Driller (3-6)",
            "Canals (3-7)",
            "Sprint (3-8)",
            "Mountain (3-9)",
            "Superkinetic (3-10)",
            "Arrival (4-1)",
            "Forgotten City (4-2)",
            "The Clocktower (4-3)",
            "Fireball (5-1)",
            "Ringer (5-2)",
            "Cleaner (5-3)",
            "Warehouse (5-4)",
            "Boom (5-5)",
            "Streets (5-6)",
            "Steps (5-7)",
            "Demolition (5-8)",
            "Arcs (5-9)",
            "Apartment (5-10)",
            "Hanging Gardens (6-1)",
            "Tangled (6-2)",
            "Waterworks (6-3)",
            "Killswitch (6-4)",
            "Falling (6-5)",
            "Shocker (6-6)",
            "Bouquet (6-7)",
            "Prepare (6-8)",
            "Triptrack (6-9)",
            "Race (6-10)",
            "Bubble (7-1)",
            "Shield (7-2)",
            "Overlook (7-3)",
            "Pop (7-4)",
            "Minefield (7-5)",
            "Mimic (7-6)",
            "Trigger (7-7)",
            "Greenhouse (7-8)",
            "Sweep (7-9)",
            "Fuse (7-10)",
            "Heaven's Edge (8-1)",
            "Zipline (8-2)",
            "Swing (8-3)",
            "Chute (8-4)",
            "Crash (8-5)",
            "Ascent (8-6)",
            "Straightaway (8-7)",
            "Firecracker (8-8)",
            "Streak (8-9)",
            "Mirror (8-10)",
            "Escalation (9-1)",
            "Bolt (9-2)",
            "Godstreak (9-3)",
            "Plunge (9-4)",
            "Mayhem (9-5)",
            "Barrage (9-6)",
            "Estate (9-7)",
            "Tripwire (9-8)",
            "Ricochet (9-9)",
            "Fortress (9-10)",
            "Holy Ground (10-1)",
            "The Third Temple (10-2)",
            "Spree (11-1)",
            "Breakthrough (11-2)",
            "Glide (11-3)",
            "Closer (11-4)",
            "Hike (11-5)",
            "Switch (11-6)",
            "Access (11-7)",
            "Congregation (11-8)",
            "Sequence (11-9)",
            "Marathon (11-10)",
            "Sacrifice (12-1)",
            "Absolution (12-2)",
        ]

    @staticmethod
    def levels_sidequest() -> List[str]:
        return [
            "Elevate Traversal I (Red-1)",
            "Elevate Traversal II (Red-2)",
            "Purify Traversal (Red-3)",
            "Godspeed Traversal (Red-4)",
            "Stomp Traversal (Red-5)",
            "Fireball Traversal (Red-6)",
            "Dominion Traversal (Red-7)",
            "Book of Life Traversal (Red-8)",
            "Doghouse (Purple-1)",
            "Choker (Purple-2)",
            "Chain (Purple-3)",
            "Hellevator (Purple-4)",
            "Razor (Purple-5)",
            "All-Seeying Eye (Purple-6)",
            "Resident Saw I (Purple-7)",
            "Resident Saw II (Purple-8)",
            "Sunset Flip Powerbomb (Yellow-1)",
            "Balloon Mountain (Yellow-2)",
            "Climbing Gym (Yellow-3)",
            "Fisherman Suplex (Yellow-4)",
            "STF (Yellow-5)",
            "Arena (Yellow-6)",
            "Attitude Adjustment (Yellow-7)",
            "Rocket (Yellow-8)",
        ]

    @functools.cached_property
    def missions_short(self) -> List[str]:
        return [
            "The Old City (Mission 4)",
            "The Third Temple (Mission 10)",
            "Hand of God (Mission 12)",
        ]

    @functools.cached_property
    def missions_long(self) -> List[str]:
        return [
            "Rebirth (Mission 1)",
            "Killer Inside (Mission 2)",
            "Only Shallow (Mission 3)",
            "The Burn That Cures (Mission 5)",
            "Covenant (Mission 6)",
            "Reckoning (Mission 7)",
            "Benediction (Mission 8)",
            "Apocrypha (Mission 9)",
            "Thousand Pound Butterfly (Mission 11)",
        ]

    def missions(self) -> List[str]:
        return sorted(self.missions_short[:] + self.missions_long[:])

    @staticmethod
    def rushes() -> List[str]:
        return [
            "Yellow",
            "Red",
            "Purple",
        ]


# Archipelago Options
# ...
