from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class SuperMarioGalaxyArchipelagoOptions:
    pass


class SuperMarioGalaxyGame(Game):
    name = "Super Mario Galaxy"
    platform = KeymastersKeepGamePlatforms.WII

    platforms_other = [
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.WIIU,
    ]
    
    is_adult_only_or_unrated = False

    options_cls = SuperMarioGalaxyArchipelagoOptions

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
        return [
            GameObjectiveTemplate(
                label="In the Terrace, complete LEVEL",
                data={"LEVEL": (self.terrace_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Terrace, complete The Honeyhive's Purple Coins (Star 5) in Honeyhive Galaxy",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Next to the Terrace, complete Rocky Road in Sweet Sweet Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Fountain, complete LEVEL",
                data={"LEVEL": (self.fountain_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="Next to the Fountain, complete A Very Sticky Situation in Sling Pod Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Kitchen, complete LEVEL",
                data={"LEVEL": (self.kitchen_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Kitchen, complete Bouldergeist's Daredevil Run (Star 4) in Ghostly Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Next to the Kitchen, complete Giant Ell Outbreak in Drip Drop Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Bedroom, complete LEVEL",
                data={"LEVEL": (self.bedroom_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Bedroom, complete Purple Coins on the Summit (Star 5) in Freezeflame Galaxy",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Next to the Bedroom, complete Bigmouth's Gold Bait in Bigmouth Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Engine Room, complete LEVEL",
                data={"LEVEL": (self.engine_room_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Engine Room, complete Purple Coins by the Seaside (Star 5) in Sea Slide Galaxy",
                data=dict(),
                is_time_consuming=True,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Next to the Engine Room, complete Choosing a Favorite Snack in Sand Spiral Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Garden, complete LEVEL",
                data={"LEVEL": (self.garden_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=4,
            ),
            GameObjectiveTemplate(
                label="In the Garden, complete Ghost Ship Daredevil Run (Star 4) in Deep Dark Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Garden, complete Battlestation's Purple Coins (Star 5) in Dreadnought Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Garden, complete Lava Spire Daredevil Run (Star 4) in Melty Molten Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Next to the Garden, complete Star Bunnies in the Snow in Snow Cap Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="In the Gate, complete LEVEL",
                data={"LEVEL": (self.gateway_levels, 1)},
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Next to the Gate, complete Racing the Spooky Speedster in Boo's Boneyard Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="At the Planet of Trials, complete LEVEL",
                data={"LEVEL": (self.planet_of_trials_levels, 1)},
                is_time_consuming=False,
                is_difficult=True,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Beat either The Fate of the Universe in Bowser's Galaxy Reactor or The Star Festival in Grand Finale Galaxy",
                data=dict(),
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
        ]

    @staticmethod
    def actions() -> List[str]:
        return [
            "Double or Triple jump",
            "Backward or Side somersault",
            "Wall or Long jump",
        ]

    @staticmethod
    def terrace_levels() -> List[str]:
        return [
            "Dino Piranha (Star 1) in Good Egg Galaxy",
            "A Snack of Cosmic Proportions (Star 2) in Good Egg Galaxy",
            "King Kaliente's Battle Fleet (Star 3) in Good Egg Galaxy",
            "Dino Piranha Speed Run (Star 4) in Good Egg Galaxy",
            "Purple Coin Omelet (Star 5) in Good Egg Galaxy",
            "Luigi on the Roof (Star 6) in Good Egg Galaxy",
            "Bee Mario Takes Flight (Star 1) in Honeyhive Galaxy",
            "Trouble on the Tower (Star 2) in Honeyhive Galaxy",
            "Big Bad Bugaboom (Star 3) in Honeyhive Galaxy",
            "Honeyhive Cosmic Race (Star 4) in Honeyhive Galaxy",
            "Luigi in the Honeyhive Kingdom (Star 6) in Honeyhive Galaxy",
            "Surfing 101 in Loopdeeloop Galaxy",
            "Painting the Planet Yellow in Flipswitch Galaxy",
            "Megaleg's Moon in Bowser Jr.'s Robot Reactor",
        ]
    
    @staticmethod
    def fountain_levels() -> List[str]:
        return [
            "Pull Star Path (Star 1) in Space Junk Galaxy",
            "Kamella's Airship Attack (Star 2) in Space Junk Galaxy",
            "Tarantox's Tangled Web (Star 3) in Space Junk Galaxy",
            "Pull Star Path Speed Run (Star 4) in Space Junk Galaxy",
            "Purple Coin Spacewalk (Star 5) in Space Junk Galaxy",
            "Yoshi's Unexpected Apperance (Star 6) in Space Junk Galaxy",
            "Rolling in the Clouds in Rolling Green Galaxy",
            "Battlerock Barrage (Star 1) in Battlerock Galaxy",
            "Breaking into the Battlerock (Star 2) in Battlerock Galaxy",
            "Topmaniac and the Topman Tribe (Star 3) in Battlerock Galaxy",
            "Topmaniac's Daredevil Run (Star 4) in Battlerock Galaxy",
            "Purple Coins on the Battlerock (Star 5) in Battlerock Galaxy",
            "Battlerock's Garbage Dump (Star 6) in Battlerock Galaxy",
            "Luigi under the Saucer (Star 7) in Battlerock Galaxy",
            "Shrinking Satellite in Hurry-Scurry Galaxy",
            "The Fiery Stronghold in Bowser's Star Reactor",
        ]
    
    @staticmethod
    def kitchen_levels() -> List[str]:
        return [
            "Sunken Treasure (Star 1) in Beach Bowl Galaxy",
            "Passing the Swim Test (Star 2) in Beach Bowl Galaxy",
            "The Secret Undersea Cavern (Star 3) in Beach Bowl Galaxy",
            "Fast Foes on the Cyclone Stone (Star 4) in Beach Bowl Galaxy",
            "Beachcombing for Purple Coins (Star 5) in Beach Bowl Galaxy",
            "Wall Jumping up Waterfalls (Star 6) in Beach Bowl Galaxy",
            "Through the Poison Swamp in Bubble Breeze Galaxy",
            "Luigi and the Haunted Mansion (Star 1) in Ghostly Galaxy",
            "A Very Spooky Sprint (Star 2) in Ghostly Galaxy",
            "Beware of the Bouldergeist (Star 3) in Ghostly Galaxy",
            "Purple Coins in the Bone Pen (Star 5) in Ghostly Galaxy",
            "Matter Splatter Mansion (Star 6) in Ghostly Galaxy",
            "The Floating Fortress (Star 1) in Buoy Base Galaxy",
            "The Secret of Buoy Base (Star 2) in Buoy Base Galaxy",
            "Sinking the Airships in Bowser Jr.'s Airship Armada",
        ]
    
    @staticmethod
    def bedroom_levels() -> List[str]:
        return [
            "Bunnies in the Wind (Star 1) in Gusty Garden Galaxy",
            "The Dirty Tricks of Major Burrows (Star 2) in Gusty Garden Galaxy",
            "Gusty Garden's Gravity Scramble (Star 3) in Gusty Garden Galaxy",
            "Major Burrows's Daredevil Run (Star 4) in Gusty Garden Galaxy",
            "Purple Coins on the Puzzle Cube (Star 5) in Gusty Garden Galaxy",
            "The Golden Chomp (Star 6) in Gusty Garden Galaxy",
            "The Frozen Peak of Baron Brrr (Star 1) in Freezeflame Galaxy",
            "Freezeflame's Blistering Core (Star 2) in Freezeflame Galaxy",
            "Hot and Cold Collide (Star 3) in Freezeflame Galaxy",
            "Frosty Cosmic Race (Star 4) in Freezeflame Galaxy",
            "Conquering the Summit (Star 6) in Freezeflame Galaxy",
            "Soaring on the Desert Winds (Star 1) in Dusty Dune Galaxy",
            "Blasting through the Sand (Star 2) in Dusty Dune Galaxy",
            "Sunbaked Sand Castle (Star 3) in Dusty Dune Galaxy",
            "Sandblast Speed Run (Star 4) in Dusty Dune Galaxy",
            "Purple Coins in the Desert (Star 5) in Dusty Dune Galaxy",
            "Bullet Bill on Your Back (Star 6) in Dusty Dune Galaxy",
            "Treasure of the Pyramid (Star 7) in Dusty Dune Galaxy",
            "Scaling the Sticky Wall in Honeyclimb Galaxy",
            "Darkness on the Horizon in Bowser's Dark Matter Plant",
        ]
    
    @staticmethod
    def engine_room_levels() -> List[str]:
        return [
            "Star Bunnies on the Hunt (Star 1) in Gold Leaf Galaxy",
            "Cataquack to the Skies (Star 2) in Gold Leaf Galaxy",
            "When It Rains, It Pours (Star 3) in Gold Leaf Galaxy",
            "Cosmic Forest Race (Star 4) in Gold Leaf Galaxy",
            "Purple Coins in the Woods (Star 5) in Gold Leaf Galaxy",
            "The Bell on the Big Tree (Star 6) in Gold Leaf Galaxy",
            "Going after Guppy (Star 1) in Sea Slide Galaxy",
            "Faster Than a Speeding Penguin (Star 2) in Sea Slide Galaxy",
            "The Silver Stars of Sea Slide (Star 3) in Sea Slide Galaxy",
            "Underwater Cosmic Race (Star 4) in Sea Slide Galaxy",
            "Hurry, He's Hungry (Star 6) in Sea Slide Galaxy",
            "Heavy Metal Mecha-Bowser (Star 1) in Toy Time Galaxy",
            "Mario/Luigi Meets Mario (Star 2) in Toy Time Galaxy",
            "Bouncing Down Cake Lane (Star 3) in Toy Time Galaxy",
            "Fast Foes of Toy Time (Star 4) in Toy Time Galaxy",
            "Luigi's Purple Coins (Star 5) in Toy Time Galaxy",
            "The Flipswitch Chain (Star 6) in Toy Time Galaxy",
            "Kingfin's Fearsome Waters in Bonefin Galaxy",
            "King Kaliente's Spicy Return in Bowser Jr.'s Lava Reactor",
        ]
    
    @staticmethod
    def garden_levels() -> List[str]:
        return [
            "The Underground Ghost Ship (Star 1) in Deep Dark Galaxy",
            "Bubble Blastoff (Star 2) in Deep Dark Galaxy",
            "Guppy and the Underground Lake (Star 3) in Deep Dark Galaxy",
            "Plunder the Purple Coins (Star 5) in Deep Dark Galaxy",
            "Boo in a Box (Star 6) in Deep Dark Galaxy",
            "Infiltrating the Dreadnought (Star 1) in Dreadnought Galaxy",
            "Dreadnought's Colossal Cannons (Star 2) in Dreadnought Galaxy",
            "Revenge of the Topman Tribe (Star 3) in Dreadnought Galaxy",
            "Topman Tribe Speed Run (Star 4) in Dreadnought Galaxy",
            "Dreadnought's Garbage Dump (Star 6) in Dreadnought Galaxy",
            "Watch Your Step in Matter Splatter Galaxy",
            "The Sinking Lava Spire (Star 1) in Melty Molten Galaxy",
            "Through the Meteor Storm (Star 2) in Melty Molten Galaxy",
            "Fiery Dino Piranha (Star 3) in Melty Molten Galaxy",
            "Red-Hot Purple Coins (Star 5) in Melty Molten Galaxy",
            "Burning Tide (Star 6) in Melty Molten Galaxy",
        ]
    
    @staticmethod
    def gateway_levels() -> List[str]:
        return [
            "Grand Star Rescue (Star 1) in Gateway Galaxy",
            "Gateway's Purple Coins (Star 2) in Gateway Galaxy",
        ]
    
    @staticmethod
    def planet_of_trials_levels() -> List[str]:
        return [
            "Gizmos, Gears, and Gadgets in Rolling Gizmo Galaxy",
            "The Electric Labyrinth in Bubble Blast Galaxy",
            "The Galaxy's Greatest Wave in Loopdeeswoop Galaxy",
        ]

# Archipelago Options
# ...
