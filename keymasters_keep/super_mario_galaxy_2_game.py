from __future__ import annotations

from typing import List

from Options import OptionSet

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperMarioGalaxy2ArchipelagoOptions:
    super_mario_galaxy_2_game_modes: SuperMarioGalaxy2GameModes


class SuperMarioGalaxy2Game(Game):
    name = "Super Mario Galaxy 2"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.WIIU,
    ]
    
    is_adult_only_or_unrated = False

    options_cls = SuperMarioGalaxy2ArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Play as Luigi",
                data=dict(),
            ),

            GameObjectiveTemplate(
                label="Beat the level without JUMP",
                data={"JUMP": (self.actions, 1)},
            ),

            GameObjectiveTemplate(
                label="Beat the level without collecting Star Bits or Coins",
                data=dict(),
            ),

            GameObjectiveTemplate(
                label="Beat the level without any jumps",
                data=dict(),
            ),

            GameObjectiveTemplate(
                label="Beat the level without spinning (except for Launch Stars)",
                data=dict(),
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        templates: List[GameObjectiveTemplate] = list()
        
        if "Power Star Hunt" in self.game_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="In World 1, complete LEVEL",
                    data={"LEVEL": (self.world_1_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 2, complete LEVEL",
                    data={"LEVEL": (self.world_2_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 3, complete LEVEL",
                    data={"LEVEL": (self.world_3_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 4, complete LEVEL",
                    data={"LEVEL": (self.world_4_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 5, complete LEVEL",
                    data={"LEVEL": (self.world_5_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 5, complete Squizzard's Daredevil Run (Star 3) in Slipsand Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World 5, complete The Star in the Sinking Swamp (Star 3) in Boo Moon Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World 6, complete LEVEL",
                    data={"LEVEL": (self.world_6_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 6, complete A Stroll Down Rolling Lane (Star 2) in Melty Monster Galaxy",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World 6, complete The Adventure of the Purple Coins (Star 2) in Clockwork Ruins Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World 6, complete Bowser's Fortified Fortress (Star 1) in Bowser's Galaxy Generator",
                    data=dict(),
                    is_time_consuming=True,
                    is_difficult=False,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World S, complete LEVEL",
                    data={"LEVEL": (self.world_s_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World S, complete Cosmic Clone Wall Jumpers (Star 2) in Flip-Out Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World S, complete LEVEL",
                    data={"LEVEL": (self.world_s_hard_levels, 1)},
                    is_time_consuming=True,
                    is_difficult=True,
                    weight=2,
                )
            ])
        
        if "Green Star Hunt" in self.game_modes:
            templates.extend([
                GameObjectiveTemplate(
                    label="In World 1, find LEVEL",
                    data={"LEVEL": (self.world_1_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 2, find LEVEL",
                    data={"LEVEL": (self.world_2_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 3, find LEVEL",
                    data={"LEVEL": (self.world_3_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 4, find LEVEL",
                    data={"LEVEL": (self.world_4_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 5, find LEVEL",
                    data={"LEVEL": (self.world_5_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World 5, find Green Star 1 in Boo Moon Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
                GameObjectiveTemplate(
                    label="In World 6, find LEVEL",
                    data={"LEVEL": (self.world_6_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World S, find LEVEL",
                    data={"LEVEL": (self.world_s_green_levels, 1)},
                    is_time_consuming=False,
                    is_difficult=False,
                    weight=3,
                ),
                GameObjectiveTemplate(
                    label="In World S, find Green Star 2 in Flip-Out Galaxy",
                    data=dict(),
                    is_time_consuming=False,
                    is_difficult=True,
                    weight=1,
                ),
            ])

        return templates

    @property
    def game_modes(self):
        return sorted(self.archipelago_options.super_mario_galaxy_2_game_modes.value)

    @staticmethod
    def actions() -> List[str]:
        return [
            "Double or Triple jump",
            "Backward or Side somersault",
            "Wall or Long jump",
        ]

    @staticmethod
    def world_1_levels() -> List[str]:
        return [
            "Peewee Piranha's Temper Tantrum (Star 1) in Sky Station Galaxy",
            "Storming the Sky Fleet (Star 2) in Sky Station Galaxy",
            "Peewee Piranha's Speed Run (Star 3) in Sky Station Galaxy",
            "Saddle Up with Yoshi (Star 1) in Yoshi Star Galaxy",
            "Spiny Control (Star 2) in Yoshi Star Galaxy",
            "Spiny Rainbow Romp (Star 3) in Yoshi Star Galaxy",
            "Digga-Leg's Planet (Star 1) in Spin-Dig Galaxy",
            "Silver Stars Down Deep (Star 2) in Spin-Dig Galaxy",
            "Digga-Leg's Daredevil Run (Star 3) in Spin-Dig Galaxy",
            "Search for the Toad Brigade Captain (Star 1) in Fluffy Bluff Galaxy",
            "The Chimp's Stomp Challenge (Star 2) in Fluffy Bluff Galaxy",
            "Every Planet Has Its Price (Star 3) in Fluffy Bluff Galaxy",
            "Think Before You Shake (Star 1) in Flip-Swap Galaxy",
            "Purple Coin Flip 'n' Sprint (Star 2) in Flip-Swap Galaxy",
            "Breaking the Laws of Gravity (Star 1) in Rightside Down Galaxy",
            "The Great Crate Incinerator (Star 2) in Rightside Down Galaxy",
            "Gobblegut's Aching Belly (Star 1) in Bowser Jr.'s Fiery Flotilla",
            "Fiery Flotilla Speed Run (Star 2) in Bowser Jr.'s Fiery Flotilla",
        ]
    
    @staticmethod
    def world_2_levels() -> List[str]:
        return [
            "The Puzzling Picture Block (Star 1) in Puzzle Plank Galaxy",
            "Purple Coin Shadow Vault (Star 2) in Puzzle Plank Galaxy",
            "Bugaboom's Back (Star 3) in Puzzle Plank Galaxy",
            "Hot-Stepping Dash Pepper (Star 1) in Hightail Falls Galaxy",
            "Hightail Falls Speed Run (Star 2) in Hightail Falls Galaxy",
            "Silver Stars in Hightail Falls (Star 3) in Hightail Falls Galaxy",
            "Rock and Rollodillo (Star 1) in Boulder Bowl Galaxy",
            "Rolling Crabber Romp (Star 2) in Boulder Bowl Galaxy",
            "C'mere, Goomba (Star 3) in Boulder Bowl Galaxy",
            "Twin Falls Hideaway (Star 1) in Cosmic Cove Galaxy",
            "Exploring the Cosmic Cavern (Star 2) in Cosmic Cove Galaxy",
            "Catch That Star Bunny (Star 3) in Cosmic Cove Galaxy",
            "Fluzzard's First Flight (Star 1) in Wild Glide Galaxy",
            "Jungle Fluzzard Race (Star 2) in Wild Glide Galaxy",
            "Bumble Beginnings (Star 1) in Honeybloom Galaxy",
            "The Secret Wall Jump (Star 2) in Honeybloom Galaxy",
            "Bowser's Big Lava Power Party (Star 1) in Bowser's Lava Lair",
            "Lava Lair Speed Run (Star 2) in Bowser's Lava Lair",
        ]
    
    @staticmethod
    def world_3_levels() -> List[str]:
        return [
            "The Flotacious Blimp Fruit (Star 1) in Tall Trunk Galaxy",
            "Tall Trunk's Big Slide (Star 2) in Tall Trunk Galaxy",
            "Tall Trunk's Purple Coin Slide (Star 3) in Tall Trunk Galaxy",
            "Head in the Clouds (Star 1) in Cloudy Court Galaxy",
            "The Shadow Lining (Star 2) in Cloudy Court Galaxy",
            "Silver Stars in the Purple Pond (Star 3) in Cloudy Court Galaxy",
            "A Glimmer of Bulb Berry (Star 1) in Haunty Halls Galaxy",
            "Sneaking Down the Creepy Corridor (Star 2) in Haunty Halls Galaxy",
            "Spooky Cosmic Clone Chase (Star 3) in Haunty Halls Galaxy",
            "Bowser on Ice (Star 1) in Freezy Flake Galaxy",
            "Sorbetti's Chilly Reception (Star 2) in Freezy Flake Galaxy",
            "The Chimp's Skating Challenge (Star 3) in Freezy Flake Galaxy",
            "Silver Chomp Grudge Match (Star 1) in Rolling Masterpiece Galaxy",
            "Masterpiece Speed Run (Star 2) in Rolling Masterpiece Galaxy",
            "Step to the Beep (Star 1) in Beat Block Galaxy",
            "Silver Stars in Double Time (Star 2) in Beat Block Galaxy",
            "Bowser Jr.'s Mighty Megahammer (Star 1) in Bowser Jr.'s Fearsome Fleet",
            "Megahammer's Daredevil Bash (Star 2) in Bowser Jr.'s Fearsome Fleet",
        ]
    
    @staticmethod
    def world_4_levels() -> List[str]:
        return [
            "Huge Trouble with Big Wigglers (Star 1) in Supermassive Galaxy",
            "Big Wigglers Speed Run (Star 2) in Supermassive Galaxy",
            "In Full Bloom (Star 3) in Supermassive Galaxy",
            "Flip-Flopping in Flipsville (Star 1) in Flipsville Galaxy",
            "Flipsville's New Digs (Star 2) in Flipsville Galaxy",
            "Purple Coin Spin Speed Run (Star 3) in Flipsville Galaxy",
            "Surf, Sand, and Silver Stars (Star 1) in Starshine Beach Galaxy",
            "Climbing the Cloudy Tower (Star 2) in Starshine Beach Galaxy",
            "Purple Coin Beach Dash (Star 3) in Starshine Beach Galaxy",
            "Where the Chomps Are Made of Gold (Star 1) in Chompworks Galaxy",
            "Spring into the Chompworks (Star 2) in Chompworks Galaxy",
            "Cosmic Clones in the Chompworks (Star 3) in Chompworks Galaxy",
            "Bulb Berry's Mysterious Glow (Star 1) in Sweet Mystery Galaxy",
            "Bulb Berry's Purple Coin Glow (Star 2) in Sweet Mystery Galaxy",
            "The Sweetest Silver Stars (Star 1) in Honeyhop Galaxy",
            "The Chimp's Score Challenge (Star 2) in Honeyhop Galaxy",
            "Breaking into Bowser's Castle (Star 1) in Bowser's Gravity Gauntlet",
            "Gravity Star Speed Run (Star 2) in Bowser's Gravity Gauntlet",
        ]
    
    @staticmethod
    def world_5_levels() -> List[str]:
        return [
            "Follow Me, Bob-omb (Star 1) in Space Storm Galaxy",
            "To the Top of Topman's Tower (Star 2) in Space Storm Galaxy",
            "C'mere, Topman (Star 3) in Space Storm Galaxy",
            "Squizzard's Sandy Sinkhole (Star 1) in Slipsand Galaxy",
            "Sailing the Sandy Seas (Star 2) in Slipsand Galaxy",
            "Prince Pikante's Peppery Mood (Star 1) in Shiverburn Galaxy",
            "Octo-Army Icy Rainbow Romp (Star 2) in Shiverburn Galaxy",
            "The Chimp's Ultimate Skating Challenge (Star 3) in Shiverburn Galaxy",
            "Silver Stars Pop-Up (Star 1) in Boo Moon Galaxy",
            "Haunting the Howling Tower (Star 2) in Boo Moon Galaxy",
            "A Walk on the Weird Side (Star 1) in Upside Dizzy Galaxy",
            "Burning Upside Dizzy (Star 2) in Upside Dizzy Galaxy",
            "Fluzzard's Wild Battlefield Glide (Star 1) in Fleet Glide Galaxy",
            "Fastest Feathers in the Galaxy (Star 2) in Fleet Glide Galaxy",
            "Bowser Jr.'s Boomsday Machine (Star 1) in Bowser Jr.'s Boom Bunker",
            "Boomsday Machine Daredevil Run (Star 2) in Bowser Jr.'s Boom Bunker",
        ]
    
    @staticmethod
    def world_6_levels() -> List[str]:
        return [
            "The Magnificent Magma Sea (Star 1) in Melty Monster Galaxy",
            "The Chimp's Bowling Challenge (Star 3) in Melty Monster Galaxy",
            "Time for Adventure (Star 1) in Clockwork Ruins Galaxy",
            "The Ledge Hammer Trap (Star 3) in Clockwork Ruins Galaxy",
            "Return of the Whomp King (Star 1) in Throwback Galaxy",
            "Silver Stars in the Whomp Fortress (Star 2) in Throwback Galaxy",
            "Whomp Silver Star Speed Run (Star 3) in Throwback Galaxy",
            "Mini-Planet Mega-Run (Star 1) in Battle Belt Galaxy",
            "Mini-Planet Daredevil Run (Star 2) in Battle Belt Galaxy",
            "Snacktime for Gobblegut (Star 3) in Battle Belt Galaxy",
            "Jumping Around in the Dark (Star 1) in Flash Black Galaxy",
            "Dark Octo-Army Romp (Star 2) in Flash Black Galaxy",
            "The Deep Shell Well (Star 1) in Slimy Spring Galaxy",
            "The Chimp's Coin Challenge (Star 2) in Slimy Spring Galaxy",
            "Bowser's Big Bad Speed Run (Star 2) in Bowser's Galaxy Generator",
        ]
    
    @staticmethod
    def world_s_levels() -> List[str]:
        return [
            "Make Mario a Star (Star 1) in Mario Squared Galaxy",
            "Luigi's Purple Coin Chaos (Star 2) in Mario Squared Galaxy",
            "The Rainbow Road Roll (Star 1) in Rolling Coaster Galaxy",
            "Purple Coins on the Rainbow Road (Star 2) in Rolling Coaster Galaxy",
            "Spinning and Spinning and Spinning (Star 1) in Twisty Trials Galaxy",
            "Turning Turning Double Time (Star 2) in Twisty Trials Galaxy",
            "Silver Stars on the Cyclone (Star 1) in Stone Cyclone Galaxy",
            "Tox Box Speed Run (Star 2) in Stone Cyclone Galaxy",
            "Throwback Throwdown (Star 1) in Boss Blitz Galaxy",
            "Throwback Throwdown Speed Run (Star 2) in Boss Blitz Galaxy",
            "Wicked Wall Jumps (Star 1) in Flip-Out Galaxy",
        ]
    
    @staticmethod
    def world_s_hard_levels() -> List[str]:
        return [
            "The Ultimate Test (Star 1) in Grandmaster Galaxy",
            "The Perfect Run (Star 2) in Grandmaster Galaxy",
        ]
    
    @staticmethod
    def world_1_green_levels() -> List[str]:
        return [
            "Green Star 1 in Sky Station Galaxy",
            "Green Star 2 in Sky Station Galaxy",
            "Green Star 3 in Sky Station Galaxy",
            "Green Star 1 in Yoshi Star Galaxy",
            "Green Star 2 in Yoshi Star Galaxy",
            "Green Star 3 in Yoshi Star Galaxy",
            "Green Star 1 in Spin-Dig Galaxy",
            "Green Star 2 in Spin-Dig Galaxy",
            "Green Star 3 in Spin-Dig Galaxy",
            "Green Star 1 in Fluffy Bluff Galaxy",
            "Green Star 2 in Fluffy Bluff Galaxy",
            "Green Star 3 in Fluffy Bluff Galaxy",
            "Green Star 1 in Flip-Swap Galaxy",
            "Green Star 2 in Flip-Swap Galaxy",
            "Green Star 1 in Rightside Down Galaxy",
            "Green Star 2 in Rightside Down Galaxy",
            "Green Star 1 in Bowser Jr.'s Fiery Flotilla",
            "Green Star 2 in Bowser Jr.'s Fiery Flotilla",
        ]
    
    @staticmethod
    def world_2_green_levels() -> List[str]:
        return [
            "Green Star 1 in Puzzle Plank Galaxy",
            "Green Star 2 in Puzzle Plank Galaxy",
            "Green Star 3 in Puzzle Plank Galaxy",
            "Green Star 1 in Hightail Falls Galaxy",
            "Green Star 2 in Hightail Falls Galaxy",
            "Green Star 3 in Hightail Falls Galaxy",
            "Green Star 1 in Boulder Bowl Galaxy",
            "Green Star 2 in Boulder Bowl Galaxy",
            "Green Star 3 in Boulder Bowl Galaxy",
            "Green Star 1 in Cosmic Cove Galaxy",
            "Green Star 2 in Cosmic Cove Galaxy",
            "Green Star 3 in Cosmic Cove Galaxy",
            "Green Star 1 in Wild Glide Galaxy",
            "Green Star 2 in Wild Glide Galaxy",
            "Green Star 1 in Honeybloom Galaxy",
            "Green Star 2 in Honeybloom Galaxy",
            "Green Star 1 in Bowser's Lava Lair",
            "Green Star 2 in Bowser's Lava Lair",
        ]
    
    @staticmethod
    def world_3_green_levels() -> List[str]:
        return [
            "Green Star 1 in Tall Trunk Galaxy",
            "Green Star 2 in Tall Trunk Galaxy",
            "Green Star 3 in Tall Trunk Galaxy",
            "Green Star 1 in Cloudy Court Galaxy",
            "Green Star 2 in Cloudy Court Galaxy",
            "Green Star 3 in Cloudy Court Galaxy",
            "Green Star 1 in Haunty Halls Galaxy",
            "Green Star 2 in Haunty Halls Galaxy",
            "Green Star 3 in Haunty Halls Galaxy",
            "Green Star 1 in Freezy Flake Galaxy",
            "Green Star 2 in Freezy Flake Galaxy",
            "Green Star 3 in Freezy Flake Galaxy",
            "Green Star 1 in Rolling Masterpiece Galaxy",
            "Green Star 2 in Rolling Masterpiece Galaxy",
            "Green Star 1 in Beat Block Galaxy",
            "Green Star 2 in Beat Block Galaxy",
            "Green Star 1 in Bowser Jr.'s Fearsome Fleet",
            "Green Star 2 in Bowser Jr.'s Fearsome Fleet",
        ]
    
    @staticmethod
    def world_4_green_levels() -> List[str]:
        return [
            "Green Star 1 in Supermassive Galaxy",
            "Green Star 2 in Supermassive Galaxy",
            "Green Star 3 in Supermassive Galaxy",
            "Green Star 1 in Flipsville Galaxy",
            "Green Star 2 in Flipsville Galaxy",
            "Green Star 3 in Flipsville Galaxy",
            "Green Star 1 in Starshine Beach Galaxy",
            "Green Star 2 in Starshine Beach Galaxy",
            "Green Star 3 in Starshine Beach Galaxy",
            "Green Star 1 in Chompworks Galaxy",
            "Green Star 2 in Chompworks Galaxy",
            "Green Star 3 in Chompworks Galaxy",
            "Green Star 1 in Sweet Mystery Galaxy",
            "Green Star 2 in Sweet Mystery Galaxy",
            "Green Star 1 in Honeyhop Galaxy",
            "Green Star 2 in Honeyhop Galaxy",
            "Green Star 1 in Bowser's Gravity Gauntlet",
            "Green Star 2 in Bowser's Gravity Gauntlet",
        ]
    
    @staticmethod
    def world_5_green_levels() -> List[str]:
        return [
            "Green Star 1 in Space Storm Galaxy",
            "Green Star 2 in Space Storm Galaxy",
            "Green Star 3 in Space Storm Galaxy",
            "Green Star 1 in Slipsand Galaxy",
            "Green Star 2 in Slipsand Galaxy",
            "Green Star 3 in Slipsand Galaxy",
            "Green Star 1 in Shiverburn Galaxy",
            "Green Star 2 in Shiverburn Galaxy",
            "Green Star 3 in Shiverburn Galaxy",
            "Green Star 2 in Boo Moon Galaxy",
            "Green Star 3 in Boo Moon Galaxy",
            "Green Star 1 in Upside Dizzy Galaxy",
            "Green Star 2 in Upside Dizzy Galaxy",
            "Green Star 1 in Fleet Glide Galaxy",
            "Green Star 2 in Fleet Glide Galaxy",
            "Green Star 1 in Bowser Jr.'s Boom Bunker",
            "Green Star 2 in Bowser Jr.'s Boom Bunker",
        ]
    
    @staticmethod
    def world_6_green_levels() -> List[str]:
        return [
            "Green Star 1 in Melty Monster Galaxy",
            "Green Star 2 in Melty Monster Galaxy",
            "Green Star 3 in Melty Monster Galaxy",
            "Green Star 1 in Clockwork Ruins Galaxy",
            "Green Star 2 in Clockwork Ruins Galaxy",
            "Green Star 3 in Clockwork Ruins Galaxy",
            "Green Star 1 in Throwback Galaxy",
            "Green Star 2 in Throwback Galaxy",
            "Green Star 3 in Throwback Galaxy",
            "Green Star 1 in Battle Belt Galaxy",
            "Green Star 2 in Battle Belt Galaxy",
            "Green Star 3 in Battle Belt Galaxy",
            "Green Star 1 in Flash Black Galaxy",
            "Green Star 2 in Flash Black Galaxy",
            "Green Star 1 in Slimy Spring Galaxy",
            "Green Star 2 in Slimy Spring Galaxy",
            "Green Star 1 in Bowser's Galaxy Generator",
            "Green Star 2 in Bowser's Galaxy Generator",
        ]
    
    @staticmethod
    def world_s_green_levels() -> List[str]:
        return [
            "Green Star 1 in Mario Squared Galaxy",
            "Green Star 2 in Mario Squared Galaxy",
            "Green Star 1 in Rolling Coaster Galaxy",
            "Green Star 2 in Rolling Coaster Galaxy",
            "Green Star 1 in Twisty Trials Galaxy",
            "Green Star 2 in Twisty Trials Galaxy",
            "Green Star 1 in Stone Cyclone Galaxy",
            "Green Star 2 in Stone Cyclone Galaxy",
            "Green Star 1 in Boss Blitz Galaxy",
            "Green Star 2 in Boss Blitz Galaxy",
            "Green Star 1 in Flip-Out Galaxy",
        ]


# Archipelago Options
class SuperMarioGalaxy2GameModes(OptionSet):
    """
    Indicates which Super Mario Galaxy 2 Game Modes the player wants to include when generating objectives.
    """

    display_name = "Super Mario Galaxy 2 Game Modes"
    valid_keys = [
        "Power Star Hunt",
        "Green Star Hunt",
    ]

    default = valid_keys
