from __future__ import annotations

from typing import NamedTuple, Optional, Sequence

from .data import Passage
from .options import Difficulty, Goal
from .rules import Requirement, has, has_all, has_any, has_treasures, option, difficulty, not_difficulty, advanced_logic


normal = Difficulty.option_normal
hard = Difficulty.option_hard
s_hard = Difficulty.option_s_hard


class LevelData(NamedTuple):
    regions: Sequence[RegionData]
    use_entrance_region: bool = True


class RegionData(NamedTuple):
    name: str
    exits: Sequence[ExitData]
    locations: Sequence[LocationData] = ()
    diamonds: Sequence[LocationData] = ()


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
                ],
                diamonds=[
                    LocationData("Stone Block Diamond"),
                    LocationData("Grab Tutorial Diamond", difficulties=[s_hard]),
                    LocationData("Diamond Above Jewel Box", difficulties=[normal]),
                    LocationData("Alcove Diamond", difficulties=[normal, hard]),
                    LocationData("Ground Pound Tutorial Diamond"),
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
                ],
                diamonds=[
#                   LocationData("Unused Cave Diamond")
                    LocationData("Ledge Diamond", difficulties=[s_hard]),
                    LocationData("Hidden Tunnel Diamond", difficulties=[normal]),
                    LocationData("Platform Cave Hidden Diamond", difficulties=[normal]),
                    LocationData("Submerged Diamond", access_rule=has('Swim')),
                    LocationData(
                        "Switch Staircase Diamond",
                        access_rule=has('Grab') | advanced_logic() & has('Stomp Jump')
                    ),
                    LocationData("Scienstein Throw Diamond", access_rule=has('Grab')),
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
                    ExitData("8-Shaped Cave", has('Super Ground Pound')),
                    ExitData("Sunflower Roots", has('Super Ground Pound')),
                ],
                [
                    LocationData("CD Box"),
                ]
            ),
            RegionData(
                "8-Shaped Cave",
                [],
                [
                    LocationData(
                        "8-Shaped Cave Box",
                        access_rule=(difficulty(hard) & has('Grab')) | (difficulty(s_hard) & has('Heavy Grab')),
                        difficulties=[hard, s_hard]
                    ),
                ],
                diamonds=[
                    LocationData("8-Shaped Cave Diamond", has('Grab'), difficulties=[normal]),
                ]
            ),
            RegionData(
                "Sunflower Roots",
                [
                    ExitData("Giant Sunflower", has('Swim')),
                ],
                diamonds=[
                    LocationData("Scienstein Stomp Diamond", access_rule=has('Grab') & has('Stomp Jump'))
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
                ],
                diamonds=[
                    LocationData("Hidden Tunnel Diamond"),
                    LocationData("Escape Detour Diamond"),
                    LocationData("Escape Detour Corner Diamond"),
                    LocationData("Current Cave Diamond"),
                    LocationData("Sunflower Diamond", difficulties=[normal]),
                    LocationData("Switch Puzzle Diamond", access_rule=has('Grab')),
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
                    ExitData("Large Cave", has('Head Smash')),
                    ExitData("Depths", has('Head Smash')),
                ],
                [
                    LocationData("Air Pocket Box", difficulties=[normal]),
                ],
                diamonds=[
                    LocationData("Air Pocket Diamond", difficulties=[hard, s_hard]),
                ]
            ),
            RegionData(
                "Large Cave",
                [],
                [
                    LocationData("Large Cave Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Large Cave Diamond", difficulties=[normal]),
                    LocationData("Shallow Pool Puzzle Diamond", access_rule=has_all(['Super Ground Pound', 'Grab'])),
                ]
            ),
            RegionData(
                "Depths",
                [
                    ExitData("Utsuboanko Hidden Cave", access_rule=has('Dash Attack')),
                ],
                [
                    LocationData("Hill Room Box", difficulties=[normal]),
                    LocationData("Cavern Box", difficulties=[normal]),
                    LocationData("Spring Cave Box", difficulties=[hard, s_hard]),
                    LocationData("Box Before Bridge", difficulties=[normal]),
                    LocationData("Lake Exit Bubble Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box", access_rule=has('Dash Attack')),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Eel Cave Underwater Diamond"),
                    LocationData("Bubble Path Diamond", difficulties=[normal]),
                    LocationData("Deep Pool Puzzle Diamond", access_rule=has('Grab')),
                ]
            ),
            RegionData(
                "Utsuboanko Hidden Cave",
                [],
                [
                    LocationData("Small Cave Box", difficulties=[hard]),
                    LocationData("Full Health Item Box", difficulties=[s_hard]),
                ],
                diamonds=[
                    LocationData("Small Cave Diamond", difficulties=[normal]),
                ]
            ),
        ]
    ),
    "Monsoon Jungle": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Fat Plummet Extra Area", access_rule=has('Ground Pound')),
                    ExitData("Deeps", access_rule=has('Ground Pound')),
                ],
                [
                    LocationData("Fat Plummet Box", difficulties=[normal]),
                    LocationData("CD Box", access_rule=has('Ground Pound')),
                    LocationData("Full Health Item Box", access_rule=has('Swim')),
                ],
                diamonds=[
                    LocationData("Archer Pink Room Diamond"),
                    LocationData("Rock Catching Diamond", access_rule=has('Grab')),
                ]
            ),
            RegionData(
                "Fat Plummet Extra Area",
                [],
                [
                    LocationData("Fat Plummet Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Fat Plummet Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Deeps",
                [
                    ExitData("Puffy Hallway", access_rule=has('Dash Attack')),
                    ExitData("Buried Cave", access_rule=has('Grab')),
                ],
                [
                    LocationData("Spiky Box", difficulties=[normal]),
                    LocationData("Escape Climb Box", difficulties=[hard]),
                    LocationData("Brown Pipe Cave Box", difficulties=[s_hard]),
                    LocationData("Descent Box", difficulties=[normal]),
                    LocationData("Buried Cave Box", difficulties=[normal]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ]
            ),
            RegionData(
                "Puffy Hallway",
                [],
                [
                    LocationData("Puffy Hallway Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Puffy Hallway Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Buried Cave",
                [],
                [
                    LocationData("Buried Cave Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Buried Cave Diamond", difficulties=[normal]),
                ]
            ),
        ]
    ),

    "The Curious Factory": LevelData(
        [
            RegionData(
                None,
                [
                    ExitData("Gear Elevator", access_rule=has('Dash Attack')),
                ],
                [
                    LocationData("First Drop Box", difficulties=[normal]),
                    LocationData('Thin Gap Box', difficulties=[hard, s_hard]),
                    LocationData("Early Escape Box", difficulties=[normal]),
                    LocationData("Conveyor Room Box", difficulties=[hard, s_hard]),
                    LocationData("Late Escape Box", difficulties=[normal]),
                    LocationData("Underground Chamber Box", difficulties=[hard, s_hard]),
                    LocationData("Frog Switch Room Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("T-Tunnel Diamond", difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", access_rule=has('Grab')),
                    LocationData("Rock Puzzle Diamond", access_rule=has('Grab')),
                    LocationData("Underground Chamber Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Gear Elevator",
                [],
                [
                    LocationData("Gear Elevator Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Gear Elevator Diamond", difficulties=[normal]),
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
                [
                    ExitData("Current Circle Room", access_rule=has('Swim')),
                    ExitData("Transformation Puzzle", access_rule=has_any(['Heavy Grab', 'Stomp Jump'])),
                ],
                [
                    LocationData("Portal Room Box", difficulties=[normal]),
                    LocationData("Box Above Portal", difficulties=[hard, s_hard]),
                    LocationData("Fat Room Box"),
                    LocationData("Spring Room Box", difficulties=[normal]),
                    LocationData("Ledge Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Full Health Item Box", difficulties=[normal]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Trash Plummet Diamond", difficulties=[normal]),
                    LocationData("Spike Ceiling Diamond"),
                    LocationData("Sewage Pool Diamond", access_rule=has('Swim')),
                    LocationData("Trash Sprint Diamond"),
                    LocationData(
                        "Transformation Puzzle Lower Diamond",
                        access_rule=has('Swim') & (advanced_logic() | has('Heavy Grab'))
                    ),
                    LocationData("Rock Throwing Diamond", access_rule=has('Grab')),
                ]
            ),
            RegionData(
                "Current Circle Room",
                [],
                [
                    LocationData("Current Circle Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Current Circle Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Transformation Puzzle",
                [],
                [
                    LocationData("Transformation Puzzle Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Transformation Puzzle Upper Diamond", difficulties=[normal]),
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
                ],
                diamonds=[
                    LocationData("Conveyor Room Diamond"),
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
                ],
                diamonds=[
                    LocationData("Maze Cage Diamond", difficulties=[normal]),
                    LocationData("Maze Pit Diamond"),
                    LocationData("Looping Room Diamond", difficulties=[normal]),
                    LocationData("Ice Block Diamond"),
                    LocationData("Snowman Puzzle Left Diamond", difficulties=[normal]),
                    LocationData("Snowman Puzzle Bottom Diamond", difficulties=[normal]),
                    LocationData("Snowman Puzzle Diamond Under Door"),
                    LocationData("Snowman Puzzle Right Diamond"),
                    LocationData(
                        "Glass Ball Puzzle Diamond",
                        access_rule=has('Grab') | advanced_logic() & has_all(['Stomp Jump', 'Ground Pound'])
                    ),
                    LocationData("Yeti Puzzle Diamond", access_rule=has('Heavy Grab')),
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
                    ExitData("Jungle Room", has('Ground Pound') | advanced_logic()),
                ],
                [
                    LocationData("Rolling Room Box", difficulties=[normal, hard]),
                    LocationData("Fruit Room Box"),
                    LocationData("Rolling Room Full Health Item Box", difficulties=[s_hard]),
                ],
                diamonds=[
                    LocationData("Fruit Room Diamond", difficulties=[normal]),
                    LocationData("Flaming Wario Diamond"),
                ]
            ),
            RegionData(
                "Jungle Room",
                [
                    ExitData("Late Rooms", has('Ground Pound') | advanced_logic() & has('Heavy Grab')),
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
                ],
                diamonds=[
                    LocationData("Switch Room Diamond", difficulties=[hard, s_hard]),
                    LocationData("Snow Room Diamond", difficulties=[normal]),
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
                ],
                diamonds=[
                    LocationData("Robot Room Diamond", access_rule=has('Dash Attack')),
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
                [
                    ExitData("Block Catch Pink Room", access_rule=has('Dash Attack')),
                ],
                [
                    LocationData("Toy Car Overhang Box", difficulties=[normal, hard]),
                    LocationData("Tower Exterior Top Box", difficulties=[s_hard]),
                    LocationData("Hidden Tower Room Box", difficulties=[normal]),
                    LocationData("Digging Room Box", access_rule=has('Dash Attack'), difficulties=[hard, s_hard]),
                    LocationData("Fire Box", difficulties=[normal]),
                    LocationData("Hidden Falling Block Door Box", difficulties=[hard]),
                    LocationData("Bonfire Block Box", difficulties=[s_hard]),
                    LocationData("Red Pipe Box", difficulties=[normal]),
                    LocationData("Escape Ledge Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Tower Diamond", difficulties=[hard]),
                    LocationData("Digging Room Diamond", access_rule=has('Dash Attack')),
                    LocationData("Escape Ledge Diamond", difficulties=[normal]),
                    LocationData("Cage Diamond", access_rule=has('Stomp Jump'), difficulties=[normal]),
                    LocationData("Circle Block Diamond", access_rule=has_all(['Super Ground Pound', 'Dash Attack'])),
                ]
            ),
            RegionData(
                "Block Catch Pink Room",
                [],
                [
                    LocationData("Full Health Item Box", difficulties=[normal, hard]),
                ],
                diamonds=[
                    LocationData("Dash Puzzle Diamond", difficulties=[s_hard]),
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
                        access_rule=has_all(['Grab', 'Stomp Jump']),
                        difficulties=[normal, hard]
                    ),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Fire Room Diamond", difficulties=[normal]),
                    LocationData("Enemy Room Diamond", access_rule=has('Grab'), difficulties=[normal]),
                    LocationData("Fat Room Diamond", difficulties=[normal]),
                    LocationData("Bouncy Room Diamond", difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", access_rule=has('Grab')),
                ]
            ),
        ]
    ),
    "Doodle Woods": LevelData(
        [
            RegionData(
                None,
                [
                    ExitData("Blue Circle Room", has('Stomp Jump')),
                    ExitData("Pink Circle Room", has('Ground Pound')),
                    ExitData(
                        "Gray Square Room",
                        has('Ground Pound') | not_difficulty(normal) & advanced_logic() & has('Grab')
                    ),
                ],
                [
                    LocationData("Box Behind Wall", difficulties=[normal]),
                    LocationData("Orange Escape Box", difficulties=[normal]),
                    LocationData("Buried Door Box", difficulties=[normal]),
                    LocationData("Purple Square Box", difficulties=[hard, s_hard]),
                    LocationData("Blue Escape Box", difficulties=[normal]),
                    LocationData("CD Box", difficulties=[hard, s_hard]),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Platform Staircase Diamond", difficulties=[normal, hard]),
                    LocationData("Hidden Platform Puzzle Diamond"),
                    LocationData("Rolling Room Diamond"),
                ]
            ),
            RegionData(
                "Blue Circle Room",
                [],
                [
                    LocationData("Blue Circle Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Blue Circle Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Pink Circle Room",
                [],
                [
                    LocationData("Pink Circle Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Pink Circle Diamond", difficulties=[normal]),
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
                    ExitData("Lake Entrance", has('Ground Pound') | advanced_logic() & has_any(['Head Smash', 'Grab'])),
                ],
                [
                    LocationData("Racing Box"),
                ]
            ),
            RegionData(
                "Lake Entrance",
                [
                    ExitData("Lake Area", has('Swim')),
                ],
                diamonds=[
                    LocationData(
                        "Toy Car Tower Diamond",
                        access_rule=has_all(['Grab', 'Stomp Jump']),
                        difficulties=[normal, hard]
                    ),
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
                ],
                diamonds=[
                    LocationData("Switch Ladder Diamond", difficulties=[normal, hard], access_rule=has('Super Ground Pound')),
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
                ],
                diamonds=[
                    LocationData("First Village Diamond"),
                ]
            ),
            RegionData(
                "Upper",
                [
                    ExitData("Agile Bat Rock Puzzle", access_rule=has_all(['Ground Pound', 'Grab'])),
                    ExitData("Lower", access_rule=has('Dash Attack')),
                ],
                [
                    LocationData("Agile Bat Box", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Agile Bat Rock Puzzle",
                [],
                [
                    LocationData("Agile Bat Hidden Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Agile Bat Hidden Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Lower",
                [
                    ExitData("Sewer", access_rule=has('Swim'))
                ],
                [
                    LocationData("Metal Platform Box", difficulties=[normal]),
                    LocationData("Metal Platform Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("Rolling Box", difficulties=[normal]),
                    LocationData("!-Switch Rolling Box", difficulties=[hard, s_hard]),
                    LocationData("CD Box"),
                    LocationData("Keyzer", event=True),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Dropdown Diamond"),
                    LocationData("Candle Dodging Diamond"),
                    LocationData("Glass Ball Puzzle Diamond", access_rule=has('Grab')),
                ]
            ),
            RegionData(
                "Sewer",
                [],
                [
                    LocationData("Sewer Box"),
                ],
                diamonds=[
                    LocationData("Sewer Diamond", difficulties=[normal]),
                ]
            ),
        ]
    ),
    "Arabian Night": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        "Onomi Room Bottom",
                        has_any(['Ground Pound', 'Head Smash']) | advanced_logic() & has('Grab')
                    ),
                    ExitData("Flying Carpet Dash Attack Puzzle", has('Dash Attack')),
                    ExitData("Kool-Aid Man", has('Dash Attack')),
                    ExitData("Sewer", has('Swim')),
                ],
                [
                    LocationData("Onomi Box", difficulties=[normal]),
                    LocationData("Flying Carpet Overhang Box", difficulties=[normal]),
                    LocationData("Zombie Plummet Box", difficulties=[normal]),
                    LocationData("Keyzer", event=True),
                ],
                diamonds=[
                    LocationData("City Ledge Diamond"),
                ]
            ),
            RegionData(
                "Onomi Room Bottom",
                [],
                [
                    LocationData("Onomi Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Onomi Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Flying Carpet Dash Attack Puzzle",
                [],
                [
                    LocationData("Flying Carpet Dash Attack Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Flying Carpet Dash Attack Diamond", difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", access_rule=has('Grab')),
                ]
            ),
            RegionData(
                "Kool-Aid Man",
                [],
                [
                    LocationData("Kool-Aid Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Kool-Aid Diamond", difficulties=[normal]),
                ]
            ),
            RegionData(
                "Sewer",
                [
                    ExitData("Sewer Underwater", access_rule=has('Super Ground Pound'))
                ],
                [
                    LocationData("Sewer Box", difficulties=[normal]),
                    LocationData("CD Box"),
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Left Sewer Ceiling Diamond"),
                    LocationData("Right Sewer Ceiling Diamond"),
                ]
            ),
            RegionData(
                "Sewer Underwater",
                [],
                [
                    LocationData("Sewer Box", difficulties=[hard, s_hard]),
                ],
                diamonds=[
                    LocationData("Sewer Air Pocket Diamond", difficulties=[normal]),
                    LocationData("Sewer Submerged Diamond"),
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
                    LocationData("Long Lava Geyser Box"),
                ],
                diamonds=[
                    LocationData("Long Lava Geyser Diamond", difficulties=[normal]),
                    LocationData("Scienstein Puzzle Diamond", access_rule=has('Grab')),
                    LocationData("Spring Puzzle Diamond", access_rule=has('Ground Pound')),
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
                ],
                diamonds=[
                    LocationData("Ice Jump Diamond", access_rule=has('Stomp Jump'), difficulties=[normal, hard]),
                    LocationData("Corner Diamond", difficulties=[normal, hard]),
                    LocationData("Hidden Ice Diamond", difficulties=[normal]),
                    LocationData("Frozen Diamond"),
                ]
            ),
        ]
    ),
    "Hotel Horror": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData(
                        "Switch Room",
                        access_rule=(
                            has('Heavy Grab')
                            | difficulty(hard) & advanced_logic() & has_all(['Grab', 'Stomp Jump', 'Super Ground Pound'])
                            | difficulty(s_hard)
                        )
                    ),
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
                    LocationData("Keyzer", difficulties=[normal, hard], event=True),
                ],
                diamonds=[
                    LocationData("Room 102 Diamond", difficulties=[normal]),
                    LocationData("Room 402 Diamond", difficulties=[normal]),
                    LocationData("Bonfire Block Diamond", difficulties=[s_hard]),
                    LocationData("Exterior Diamond"),
                    LocationData("Transformation Puzzle Fat Diamond"),
                    LocationData("Transformation Puzzle Spring Diamond"),
                ]
            ),
            RegionData(
                "Switch Room",
                [],
                [
                    LocationData("CD Box"),
                    LocationData("Frog Switch", event=True),
                    LocationData("Keyzer", difficulties=[s_hard], event=True),
                ]
            ),
        ]
    ),

    "Golden Passage": LevelData(
        [
            RegionData(
                "Entrance",
                [
                    ExitData("Current Puzzle", has('Swim')),
                    ExitData("Passage", advanced_logic()),
                ],
                [
                    LocationData("Frog Switch", event=True),
                ],
                diamonds=[
                    LocationData("Long Hall Left Diamond"),
                    LocationData("Long Hall Right Diamond"),
                ]
            ),
            RegionData(
                "Current Puzzle",
                [
                    ExitData("Passage"),
                ],
                [
                    LocationData("Current Puzzle Box"),
                ],
                diamonds=[
                    LocationData("Current Puzzle Diamond"),
                ]
            ),
            RegionData(
                "Passage",
                [
                    # Trick undocumented due to being currently not doable in practice: Reaching Golden Passage always
                    # requires Ground Pound because of Cractus and Catbat
                    ExitData("Scienstein Area", has('Ground Pound') | advanced_logic() & has('Grab')),
                ],
                [
                    LocationData("River Box"),
                    LocationData("Bat Room Box"),
                ],
                diamonds=[
                    LocationData("Spring Shaft Diamond"),
                    LocationData("Zombie Hall Left Diamond"),
                    LocationData("Zombie Hall Right Diamond"),
                    LocationData("Digging Diamond"),
                    LocationData("Slope Diamond"),
                    LocationData("Scienstein Escape Diamond", access_rule=has('Swim')),
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
                ],
                diamonds=[
                    LocationData("Scienstein Roll Diamond"),
                ]
            ),
        ]
    ),
}


passage_boss_table = {
    Passage.EMERALD: BossData(
        "Cractus",
        has('Ground Pound'),
        not_difficulty(s_hard) | has('Stomp Jump') | advanced_logic()
    ),
    Passage.RUBY: BossData("Cuckoo Condor", has('Grab')),
    Passage.TOPAZ: BossData("Aerodent", has('Grab')),
    Passage.SAPPHIRE: BossData(
        "Catbat",
        has('Ground Pound') & (has('Stomp Jump') | advanced_logic()),
        has('Stomp Jump') | advanced_logic() & not_difficulty(s_hard)
    ),
}

golden_diva = BossData(
    "Golden Diva",
    has('Heavy Grab') & (option('goal', Goal.option_golden_diva) | has_treasures())
)
