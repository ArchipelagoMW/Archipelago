from __future__ import annotations

from typing import NamedTuple, Optional, Sequence

from BaseClasses import Region

from .options import Difficulty, Goal, Logic
from .rules import *


normal = Difficulty.option_normal
hard = Difficulty.option_hard
s_hard = Difficulty.option_s_hard
advanced = Logic.option_advanced


class LevelData(NamedTuple):
    regions: Sequence[RegionData]
    use_entrance_region: bool = True


class RegionData(NamedTuple):
    name: str
    exits: Sequence[ExitData]
    locations: Sequence[LocationData] = ()


class ExitData(NamedTuple):
    destination: str
    access_rule: Optional[Requirement] = None  # Forward and reverse


class LocationData(NamedTuple):
    name: str
    access_rule: Optional[Requirement] = None
    difficulties: Sequence[int] = [normal, hard, s_hard]
    event: bool = False


class BossData(NamedTuple):
    name: str
    kill_rule: Requirement
    quick_kill_rule: Optional[Requirement] = None


passage_levels = {
    Passage.ENTRY: ["Hall of Hieroglyphs"],
    Passage.EMERALD: ["Palm Tree Paradise", "Wildflower Fields", "Mystic Lake", "Monsoon Jungle"],
    Passage.RUBY: ["The Curious Factory", "The Toxic Landfill", "40 Below Fridge", "Pinball Zone"],
    Passage.TOPAZ: ["Toy Block Tower", "The Big Board", "Doodle Woods", "Domino Row"],
    Passage.SAPPHIRE: ["Crescent Moon Village", "Arabian Night", "Fiery Cavern", "Hotel Horror"],
    Passage.GOLDEN: ["Golden Passage"],
}


level_table = {
    "Hall of Hieroglyphs": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        None,
                        has_all(['Dash Attack', 'Grab', 'Super Ground Pound'])
                    ),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("First Jewel Box"),
                    LocationData("Second Jewel Box"),
                    LocationData("Full Health Item Box"),
                    LocationData("Third Jewel Box"),
                    LocationData("Fourth Jewel Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),

    "Palm Tree Paradise": LevelData(
        [
            RegionData(
                None,
                [],
                [
                    LocationData("First Box", difficulties=[normal]),
                    LocationData("Ledge Box", difficulties=[hard]),
                    LocationData("Dead End Box", difficulties=[s_hard]),
                    LocationData("Box Before Cave", difficulties=[normal]),
                    LocationData("Hidden Box", difficulties=[hard, s_hard]),
                    LocationData("Platform Cave Jewel Box"),
                    LocationData("Ladder Cave Box"),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "Wildflower Fields": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Giant Sunflower", has_all(['Super Ground Pound', 'Swim'])),
                ],
                [
                    LocationData(
                        "8-Shaped Cave Box",
                        access_rule=has('Super Ground Pound') & ((difficulty(hard) & has('Grab')) | (difficulty(s_hard) & has('Heavy Grab'))),
                        difficulties=[hard, s_hard]
                    ),
                    LocationData("CD Box"),
                ]
            ),
            RegionData(
                "Giant Sunflower",
                [],
                [
                    LocationData("Current Cave Box"),
                    LocationData("Sunflower Jewel Box", difficulties=[normal]),
                    LocationData("Sunflower Box", difficulties=[hard, s_hard]),
                    LocationData("Slope Room Box", difficulties=[normal]),
                    LocationData("Beezley Box"),
                    LocationData("Full Health Item Box", difficulties=[normal]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Mystic Lake": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Rock Cave", has('Grab')),
                    ExitData("Shallows", has('Swim')),
                ],
                []
            ),
            RegionData(
                "Rock Cave",
                [],
                [
                    LocationData("Rock Cave Box", difficulties=[s_hard]),
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                ]
            ),
            RegionData(
                "Shallows",
                [
                    ExitData("Depths", has('Head Smash')),
                ],
                [
                    LocationData("Air Pocket Box", difficulties=[normal]),
                    LocationData("Large Cave Box", access_rule=has('Head Smash'), difficulties=[hard, s_hard]),
                ]
            ),
            RegionData(
                "Depths",
                [],
                [
                    LocationData("Hill Room Box", difficulties=[normal]),
                    LocationData("Small Cave Box", access_rule=has('Dash Attack'), difficulties=[hard]),
                    LocationData("Cavern Box", difficulties=[normal]),
                    LocationData("Spring Cave Box", difficulties=[hard, s_hard]),
                    LocationData("Box Before Bridge", difficulties=[normal]),
                    LocationData("Lake Exit Bubble Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", access_rule=has('Dash Attack')),
                    LocationData("Full Health Item Box", access_rule=has('Dash Attack'), difficulties=[s_hard]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Monsoon Jungle": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Deeps", access_rule=has('Ground Pound')),
                ],
                [
                    LocationData("Fat Plummet Box", access_rule=difficulty(normal) | has('Ground Pound')),
                    LocationData("CD Box", access_rule=has('Ground Pound')),
                    LocationData("Full Health Item Box", access_rule=has('Swim')),
                ]
            ),
            RegionData(
                "Deeps",
                [],
                [
                    LocationData("Spiky Box", difficulties=[normal]),
                    LocationData("Escape Climb Box", difficulties=[hard]),
                    LocationData("Brown Pipe Cave Box", difficulties=[s_hard]),
                    LocationData("Descent Box", difficulties=[normal]),
                    LocationData("Puffy Hallway Box", access_rule=has('Dash Attack'), difficulties=[hard, s_hard]),
                    LocationData("Buried Cave Box", access_rule=difficulty(normal) | has('Grab')),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),

    "The Curious Factory": LevelData(
        [
            RegionData(
                None,
                [],
                [
                    LocationData("First Drop Box", difficulties=[normal]),
                    LocationData('Thin Gap Box', difficulties=[hard, s_hard]),
                    LocationData("Early Escape Box", difficulties=[normal]),
                    LocationData("Conveyor Room Box", difficulties=[hard, s_hard]),
                    LocationData("Late Escape Box", difficulties=[normal]),
                    LocationData("Underground Chamber Box", difficulties=[hard, s_hard]),
                    LocationData("Frog Switch Room Box", difficulties=[normal]),
                    LocationData("Gear Elevator Box", access_rule=has('Dash Attack'), difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "The Toxic Landfill": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has_all(['Dash Attack', 'Super Ground Pound', 'Head Smash'])),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("Portal Room Box", difficulties=[normal]),
                    LocationData("Box Above Portal", difficulties=[hard, s_hard]),
                    LocationData("Fat Room Box"),
                    LocationData("Spring Room Box", difficulties=[normal]),
                    LocationData("Current Circle Box", access_rule=has('Swim'), difficulties=[hard, s_hard]),
                    LocationData("Ledge Box", difficulties=[normal]),
                    LocationData(
                        "Transformation Puzzle Box",
                        access_rule=has_any(['Heavy Grab', 'Enemy Jump']),
                        difficulties=[hard, s_hard]
                    ),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "40 Below Fridge": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has('Super Ground Pound')),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("Looping Room Box"),
                    LocationData("Maze Room Box"),
                    LocationData("Snowman Puzzle Lower Box"),
                    LocationData("Snowman Puzzle Upper Box"),
                    LocationData("CD Box", access_rule=has('Head Smash')),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Pinball Zone": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Early Rooms", has('Grab')),
                ]
            ),
            RegionData(
                "Early Rooms",
                [
                    ExitData("Jungle Room", has('Ground Pound') | logic(advanced)),
                ],
                [
                    LocationData("Rolling Room Box", difficulties=[normal, hard]),
                    LocationData("Fruit Room Box"),
                    LocationData("Rolling Room Full Health Item Box", difficulties=[s_hard]),
                ]
            ),
            RegionData(
                "Jungle Room",
                [
                    ExitData("Late Rooms", has('Ground Pound') | logic(advanced) & has('Heavy Grab')),
                ],
                [
                    LocationData("Jungle Room Box"),
                ]
            ),
            RegionData(
                "Late Rooms",
                [
                    ExitData("Scienstein Puzzle Pink Room", has('Super Ground Pound')),
                    ExitData("Escape", has_all(['Ground Pound', 'Head Smash'])),
                ],
                [
                    LocationData("Switch Room Box", difficulties=[s_hard]),
                    LocationData("Snow Room Box"),
                    LocationData("CD Box"),
                ]
            ),
            RegionData(
                "Scienstein Puzzle Pink Room",
                [],
                [
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                    LocationData("Pink Room Full Health Item Box", difficulties=[s_hard]),
                ]
            ),
            RegionData(
                "Escape",
                [],
                [
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),

    "Toy Block Tower": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, has('Heavy Grab')),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("Toy Car Overhang Box", difficulties=[normal, hard]),
                    LocationData("Tower Exterior Top Box", difficulties=[s_hard]),
                    LocationData("Hidden Tower Room Box", difficulties=[normal]),
                    LocationData("Digging Room Box", access_rule=has('Dash Attack'), difficulties=[hard, s_hard]),
                    LocationData("Fire Box", difficulties=[normal]),
                    LocationData("Hidden Falling Block Door Box", difficulties=[hard]),
                    LocationData("Bonfire Block Box", difficulties=[s_hard]),
                    LocationData("Red Pipe Box", difficulties=[normal, hard]),
                    LocationData("Escape Ledge Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box", access_rule=has('Dash Attack'), difficulties=[normal, hard]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "The Big Board": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(None, access_rule=has('Ground Pound')),
                ]
            ),
            RegionData(
                None,
                [],
                [
                    LocationData("First Box", difficulties=[normal]),
                    LocationData("Hard Fire Room Box", difficulties=[hard, s_hard]),
                    LocationData("Normal Fire Room Box", difficulties=[normal]),
                    LocationData("Hard Enemy Room Box", access_rule=has('Grab'), difficulties=[hard, s_hard]),
                    LocationData("Normal Enemy Room Box", difficulties=[normal]),
                    LocationData("Fat Room Box", difficulties=[hard, s_hard]),
                    LocationData("Toy Car Box", difficulties=[normal]),
                    LocationData("Flat Room Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData(
                        "Full Health Item Box",
                        access_rule=has_all(['Grab', 'Enemy Jump']),
                        difficulties=[normal, hard]
                    ),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Doodle Woods": LevelData(
        [
            RegionData(
                None,
                [
                    ExitData(
                        "Gray Square Room",
                        has('Ground Pound') | not_difficulty(normal) & logic(advanced) & has('Grab')
                    ),
                ],
                [
                    LocationData("Box Behind Wall", difficulties=[normal]),
                    LocationData("Orange Escape Box", difficulties=[normal]),
                    LocationData("Pink Circle Box", access_rule=has('Ground Pound'), difficulties=[hard, s_hard]),
                    LocationData("Buried Door Box", difficulties=[normal]),
                    LocationData("Purple Square Box", difficulties=[hard, s_hard]),
                    LocationData("Blue Escape Box", difficulties=[normal]),
                    LocationData("Blue Circle Box", access_rule=has('Enemy Jump'), difficulties=[hard, s_hard]),
                    LocationData("CD Box", difficulties=[hard, s_hard]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
            RegionData(
                "Gray Square Room",
                [],
                [
                    LocationData("Gray Square Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", difficulties=[normal]),
                ]
            ),
        ],
        use_entrance_region=False
    ),
    "Domino Row": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        "Lake Area",
                        has('Swim') & (has('Ground Pound') | logic(advanced) & has_any(['Head Smash', 'Grab']))
                    ),
                ],
                [
                    LocationData("Racing Box"),
                ]
            ),
            RegionData(
                "Lake Area",
                [],
                [
                    LocationData("Rolling Box"),
                    LocationData("Swimming Detour Box", access_rule=has('Head Smash'), difficulties=[normal, hard]),
                    LocationData("Swimming Room Escape Box", access_rule=has('Ground Pound'), difficulties=[s_hard]),
                    LocationData("Keyzer Room Box", access_rule=has('Ground Pound')),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),

    "Crescent Moon Village": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Upper", access_rule=has('Head Smash'))
                ]
            ),
            RegionData(
                "Upper",
                [
                    ExitData("Lower", access_rule=has('Dash Attack')),
                ],
                [
                    LocationData("Agile Bat Box", difficulties=[normal]),
                    LocationData(
                        "Agile Bat Hidden Box",
                        access_rule=has_all(['Ground Pound', 'Grab']),
                        difficulties=[hard, s_hard]
                    ),
                ]
            ),
            RegionData(
                "Lower",
                [],
                [
                    LocationData("Metal Platform Box", difficulties=[normal]),
                    LocationData("Metal Platform Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("Rolling Box", difficulties=[normal]),
                    LocationData("!-Switch Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("Sewer Box", access_rule=has('Swim')),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Arabian Night": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Sewer", has('Swim')),
                ],
                [
                    LocationData("Onomi Box", access_rule=difficulty(normal) | has_any(['Ground Pound', 'Head Smash'])),
                    LocationData("Flying Carpet Overhang Box", difficulties=[normal]),
                    LocationData(
                        "Flying Carpet Dash Attack Box",
                        access_rule=has('Dash Attack'),
                        difficulties=[hard, s_hard]
                    ),
                    LocationData("Zombie Plummet Box", difficulties=[normal]),
                    LocationData("Kool-Aid Box", access_rule=has('Dash Attack'), difficulties=[hard, s_hard]),
                    LocationData("Keyzer", event=True),
                ]
            ),
            RegionData(
                "Sewer",
                [],
                [
                    LocationData("Sewer Box", access_rule=difficulty(normal) | has('Super Ground Pound')),
                    LocationData("CD Box"),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Fiery Cavern": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Frozen", has_all(['Ground Pound', 'Dash Attack', 'Head Smash'])),
                ],
                [
                    LocationData("Lava Dodging Box", difficulties=[normal]),
                    LocationData("Long Lava Geyser Box")
                ]
            ),
            RegionData(
                "Frozen",
                [],
                [
                    LocationData("Ice Beyond Door Box", difficulties=[hard, s_hard]),
                    LocationData("Ice Detour Box"),
                    LocationData("Snowman Box"),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),
    "Hotel Horror": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Switch Room", access_rule=has('Heavy Grab') | difficulty(s_hard)),
                ],
                [
                    LocationData("1F Hallway Box", difficulties=[normal]),
                    LocationData("Room 102 Box", difficulties=[hard, s_hard]),
                    LocationData("2F Hallway Box", difficulties=[normal]),
                    LocationData("Room 303 Box", difficulties=[hard, s_hard]),
                    LocationData("3F Hallway Box", difficulties=[normal]),
                    LocationData("Room 402 Box", difficulties=[hard, s_hard]),
                    LocationData("4F Hallway Box", difficulties=[normal]),
                    LocationData("Exterior Box", difficulties=[hard, s_hard]),
                    LocationData("Keyzer", event=True),
                ]
            ),
            RegionData(
                "Switch Room",
                [],
                [
                    LocationData("CD Box"),
                    LocationData("Frog Switch", event=True),
                ]
            ),
        ]
    ),

    "Golden Passage": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Passage", has('Swim')),
                ],
                [
                    LocationData("Frog Switch", event=True),
                ]
            ),
            RegionData(
                "Passage",
                [
                    ExitData("Scienstein Area", has('Ground Pound')),
                ],
                [
                    LocationData("Current Puzzle Box"),
                    LocationData("River Box"),
                    LocationData("Bat Room Box"),
                ]
            ),
            RegionData(
                "Scienstein Area",
                [
                    ExitData("Keyzer Area", has('Grab')),
                ],
                [
                    LocationData("Mad Scienstein Box"),
                ]
            ),
            RegionData(
                "Keyzer Area",
                [],
                [
                    LocationData("Keyzer", event=True),
                ]
            ),
        ]
    ),
}


passage_boss_table = {
    Passage.EMERALD: BossData("Cractus", has('Ground Pound'), not_difficulty(s_hard) | has('Enemy Jump') | logic(advanced)),
    Passage.RUBY: BossData("Cuckoo Condor", has('Grab')),
    Passage.TOPAZ: BossData("Aerodent", has('Grab')),
    Passage.SAPPHIRE: BossData(
        "Catbat",
        has('Ground Pound') & (has('Enemy Jump') | logic(advanced)),
        has('Enemy Jump') | logic(advanced) & not_difficulty(s_hard)
    ),
}

golden_diva = BossData(
    "Golden Diva",
    has('Heavy Grab') & (option('goal', Goal.option_golden_diva) | has_treasures())
)
