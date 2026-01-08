from __future__ import annotations

from typing import List

from dataclasses import dataclass

from ..game import Game
from ..game_objective_template import GameObjectiveTemplate

from ..enums import KeymastersKeepGamePlatforms


@dataclass
class DescendersArchipelagoOptions:
    pass


class DescendersGame(Game):
    name = "Descenders"
    platform = KeymastersKeepGamePlatforms.PC

    platforms_other = [
        KeymastersKeepGamePlatforms.PS4,
        KeymastersKeepGamePlatforms.SW,
        KeymastersKeepGamePlatforms.XONE,
    ]

    is_adult_only_or_unrated = False

    options_cls = DescendersArchipelagoOptions

    def optional_game_constraint_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Bike: BIKE.  Can only select COLOR Crew Members",
                data={
                    "BIKE": (self.bikes, 1),
                    "COLOR": (self.team_colors, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Bike: BIKE.  Cannot select the following Crew Members: MEMBERS",
                data={
                    "BIKE": (self.bikes, 1),
                    "MEMBERS": (self.crew_members, 4),
                },
            ),
            GameObjectiveTemplate(
                label="Bike: BIKE.  Must select every NODE Node",
                data={
                    "BIKE": (self.bikes, 1),
                    "NODE": (self.special_nodes, 1),
                },
            ),
            GameObjectiveTemplate(
                label="Bike: BIKE.  Cannot select Medic Camp Nodes",
                data={
                    "BIKE": (self.bikes, 1),
                },
            ),
        ]

    def game_objective_templates(self) -> List[GameObjectiveTemplate]:
        return [
            GameObjectiveTemplate(
                label="Reach REGION in Career mode",
                data={
                    "REGION": (self.regions_career_reach, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach REGION in Career-Plus mode",
                data={
                    "REGION": (self.regions_career_plus_reach, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=3,
            ),
            GameObjectiveTemplate(
                label="Reach the following Secret Region: REGION",
                data={
                    "REGION": (self.regions_secret, 1)
                },
                is_time_consuming=True,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear the following Bonus World: WORLD",
                data={
                    "WORLD": (self.bonus_worlds, 1)
                },
                is_time_consuming=False,
                is_difficult=True,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Clear a NODE node in REGION",
                data={
                    "NODE": (self.special_nodes, 1),
                    "REGION": (self.regions_all, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear SPONSOR Team node in REGION",
                data={
                    "SPONSOR": (self.sponsors, 1),
                    "REGION": (self.regions_career, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Achieve COUNT Bonus Objectives in REGION",
                data={
                    "COUNT": (self.bonus_objective_count_range, 1),
                    "REGION": (self.regions_all, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear a node with a PROPERTY level of at least COUNT in REGION",
                data={
                    "COUNT": (self.node_property_range, 1),
                    "PROPERTY": (self.node_properties, 1),
                    "REGION": (self.regions_all, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Clear COUNT consecutive nodes without bailing in REGION",
                data={
                    "COUNT": (self.node_consecutive_range, 1),
                    "REGION": (self.regions_all, 1)
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Land the following Mini-Boss Stunt: STUNT",
                data={
                    "STUNT": (self.mini_boss_stunts, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
            GameObjectiveTemplate(
                label="Collect at least COUNT Crew Members in a run",
                data={
                    "COUNT": (self.crew_member_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Finish a run with at least COUNT REP",
                data={
                    "COUNT": (self.rep_count_range, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Receive an item of the following Rarity at the end of a run: RARITY",
                data={
                    "RARITY": (self.item_rarities, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=1,
            ),
            GameObjectiveTemplate(
                label="Cross the finish line in the following Bike Park: PARK",
                data={
                    "PARK": (self.bike_parks, 1),
                },
                is_time_consuming=False,
                is_difficult=False,
                weight=2,
            ),
        ]

    @staticmethod
    def bikes() -> List[str]:
        return [
            "LX20 EndTrail (Enduro)",
            "Rosend DJ7 (Hardtail)",
            "TJ DH12 (Downhill)",
        ]

    @staticmethod
    def regions_career() -> List[str]:
        return [
            "Highlands",
            "Forest",
            "Canyon",
            "Peaks",
        ]

    @staticmethod
    def regions_career_reach() -> List[str]:
        return [
            "Forest",
            "Canyon",
            "Peaks",
        ]

    @staticmethod
    def regions_career_plus() -> List[str]:
        return [
            "Desert",
            "Jungle",
            "Favela",
            "Glaciers",
        ]

    @staticmethod
    def regions_career_plus_reach() -> List[str]:
        return [
            "Jungle",
            "Favela",
            "Glaciers",
        ]

    @staticmethod
    def regions_all() -> List[str]:
        return [
            "Highlands",
            "Forest",
            "Canyon",
            "Peaks",
            "Desert",
            "Jungle",
            "Favela",
            "Glaciers",
        ]

    @staticmethod
    def regions_secret() -> List[str]:
        return [
            "Volcano (Career)",
            "Ridges (Career-Plus)",
        ]

    @staticmethod
    def bonus_worlds() -> List[str]:
        return [
            "Construction Site (Highlands)",
            "Mega Ramp (Forest)",
            "Ranch (Canyon)",
            "Moon (Peaks)",
            "Kids Room (Volcano)",
        ]

    @staticmethod
    def sponsors() -> List[str]:
        return [
            "an Arboreal",
            "a Kinetic",
            "an Enemy",
        ]

    @staticmethod
    def team_colors() -> List[str]:
        return [
            "Blue",
            "Green",
            "Yellow",
        ]

    @staticmethod
    def crew_members() -> List[str]:
        return [
            "Bunny Hop (Green)",
            "Extra Steepness (Yellow)",
            "Extra Stunts (Yellow)",
            "Fakie Balance (Green)",
            "Fewer Obstacles (Yellow)",
            "Heavy Bail Threshold (Green)",
            "In Air Correction (Green)",
            "Landing Impact (Green)",
            "Less Curves (Yellow)",
            "More Checkpoints (Yellow)",
            "More Team Nodes (Blue)",
            "Off-Road Friction (Green)",
            "Prevent Modifiers (Blue)",
            "Pump Strength (Green)",
            "Scout Nodes (Blue)",
            "Show Compass (Blue)",
            "Smoother Curves (Yellow)",
            "Speed Wobbles (Green)",
            "Spin Speed (Green)",
            "Tweak Speed (Green)",
            "Wheelie Balance (Green)",
            "Wider Path (Yellow)",
        ]

    @staticmethod
    def special_nodes() -> List[str]:
        return [
            "Danger Zone",
            "Helmet Cam",
            "Fire",
        ]

    @staticmethod
    def node_properties() -> List[str]:
        return [
            "Curves",
            "Steepness",
            "Stunts",
        ]

    @staticmethod
    def node_property_range() -> range:
        return range(4, 9)

    @staticmethod
    def bike_parks() -> List[str]:
        return [
            "Alodalakes Bike Resort",
            "BC Bike Park",
            "BikeOut 2",
            "BikeOut 3",
            "BikeOut 4",
            "BikeOut",
            "Cambria",
            "Descenders Island",
            "Drylands National Park",
            "Dutchman's Rock",
            "Dyfi Valley",
            "Ido Bike Park",
            "Island Cakewalk",
            "Jump City",
            "Kushmuck 4X Park",
            "Llangynog Freeride",
            "Lost Cause Caves",
            "Megapark",
            "Mt Slope",
            "Mt. Rosie",
            "New Lexico",
            "Ragesquid Riot",
            "Red Raven Canyon",
            "Rival Falls",
            "Rose Ridge",
            "STMP Line",
            "Snowmans Ball",
            "Stoker Bike Park",
            "The Sanctuary",
            "Vuurberg",
        ]

    @staticmethod
    def bonus_objective_count_range() -> range:
        return range(2, 6)

    @staticmethod
    def node_consecutive_range() -> range:
        return range(3, 8)

    @staticmethod
    def mini_boss_stunts() -> List[str]:
        return [
            "Apres Ski Party (Peaks)",
            "Burn (Peaks)",
            "Firewatched (Forest)",
            "Gone With The Wind (Canyon)",
            "Holy Staircase (Peaks)",
            "In N Out (Favela)",
            "Is It A Bird (Peaks)",
            "It's Cold Up Here (Peaks)",
            "King of the Castle (Highlands)",
            "Loop de Loop (Forest)",
            "Narrow (Favela)",
            "On the Rocks (Highlands)",
            "Over The Trees (Jungle)",
            "Pump It Up (Canyon)",
            "Rooftap (Favela)",
            "Rooftopped (Favela)",
            "Spinebreaker (Peaks)",
            "Stonehenged (Highlands)",
            "Sweet Spot (Peaks)",
            "Switchback (Forest)",
            "Tabletopped (Canyon)",
            "Through The Trees (Jungle)",
            "To the Wall (Highlands)",
            "To the Window (Highlands)",
            "Treetopped (Jungle)",
            "Windy Up Here (Canyon)",
        ]

    @staticmethod
    def crew_member_count_range() -> range:
        return range(4, 10)

    @staticmethod
    def rep_count_range() -> range:
        return range(10000, 150001, 5000)

    @staticmethod
    def item_rarities() -> List[str]:
        return [
            "Uncommon",
            "Rare",
            "Extraordinary",
        ]

# Archipelago Options
# ...
