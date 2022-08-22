"""
Defines constants for different types of locations in the game
"""

from .Options import is_option_enabled, get_option_value
from .player_logic import StaticWitnessLogic, WitnessPlayerLogic


class StaticWitnessLocations:
    """
    Witness Location Constants that stay consistent across worlds
    """
    ID_START = 158000

    TYPE_OFFSETS = {
        "General": 0,
        "Discard": 600,
        "Vault": 650,
        "Laser": 700,
    }

    EXTRA_LOCATIONS = {
        "Tutorial Front Left",
        "Tutorial Back Left",
        "Tutorial Back Right",
    }

    GENERAL_LOCATIONS = {
        "Tutorial Gate Open",

        "Outside Tutorial Vault Box",
        "Outside Tutorial Discard",
        "Outside Tutorial Dots Introduction 5",
        "Outside Tutorial Squares Introduction 9",

        "Glass Factory Discard",
        "Glass Factory Vertical Symmetry 5",
        "Glass Factory Rotational Symmetry 3",
        "Glass Factory Melting 3",

        "Symmetry Island Black Dots 5",
        "Symmetry Island Colored Dots 6",
        "Symmetry Island Fading Lines 7",
        "Symmetry Island Scenery Outlines 5",
        "Symmetry Island Laser Panel",

        "Orchard Apple Tree 5",

        "Desert Vault Box",
        "Desert Discard",
        "Desert Sun Reflection 8",
        "Desert Artificial Light Reflection 3",
        "Desert Pond Reflection 5",
        "Desert Flood Reflection 6",
        "Desert Laser Panel",

        "Quarry Mill Eraser and Dots 6",
        "Quarry Mill Eraser and Squares 8",
        "Quarry Mill Small Squares & Dots & Eraser",
        "Quarry Boathouse Intro Shapers",
        "Quarry Boathouse Intro Stars",
        "Quarry Boathouse Eraser and Shapers 5",
        "Quarry Boathouse Stars & Eraser & Shapers 2",
        "Quarry Boathouse Stars & Eraser & Shapers 5",
        "Quarry Discard",
        "Quarry Laser Panel",

        "Shadows Lower Avoid 8",
        "Shadows Environmental Avoid 8",
        "Shadows Follow 5",
        "Shadows Laser Panel",

        "Keep Hedge Maze 4",
        "Keep Pressure Plates 4",
        "Keep Discard",
        "Keep Laser Panel Hedges",
        "Keep Laser Panel Pressure Plates",

        "Shipwreck Vault Box",
        "Shipwreck Discard",

        "Monastery Rhombic Avoid 3",
        "Monastery Branch Follow 2",
        "Monastery Laser Panel",

        "Town Cargo Box Discard",
        "Town Hexagonal Reflection",
        "Town Church Lattice",
        "Town Rooftop Discard",
        "Town Symmetry Squares 5 + Dots",
        "Town Full Dot Grid Shapers 5",
        "Town Shapers & Dots & Eraser",
        "Town Laser Panel",

        "Theater Discard",

        "Jungle Discard",
        "Jungle Waves 3",
        "Jungle Waves 7",
        "Jungle Popup Wall 6",
        "Jungle Laser Panel",

        "River Vault Box",

        "Bunker Drawn Squares 5",
        "Bunker Drawn Squares 9",
        "Bunker Drawn Squares through Tinted Glass 3",
        "Bunker Drop-Down Door Squares 2",
        "Bunker Laser Panel",

        "Swamp Seperatable Shapers 6",
        "Swamp Combinable Shapers 8",
        "Swamp Broken Shapers 4",
        "Swamp Cyan Underwater Negative Shapers 5",
        "Swamp Platform Shapers 4",
        "Swamp Rotated Shapers 4",
        "Swamp Red Underwater Negative Shapers 4",
        "Swamp More Rotated Shapers 4",
        "Swamp Blue Underwater Negative Shapers 5",
        "Swamp Laser Panel",

        "Treehouse Yellow Bridge 9",
        "Treehouse First Purple Bridge 5",
        "Treehouse Second Purple Bridge 7",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Treehouse Left Orange Bridge 15",
        "Treehouse Burnt House Discard",
        "Treehouse Right Orange Bridge 12",
        "Treehouse Laser Panel",

        "Mountaintop Discard",
        "Mountaintop Vault Box",
    }

    UNCOMMON_LOCATIONS = {
        "Mountaintop River Shape",
        "Tutorial Patio Floor",
        "Quarry Mill Big Squares & Dots & Eraser",
        "Theater Tutorial Video",
        "Theater Desert Video",
        "Theater Jungle Video",
        "Theater Shipwreck Video",
        "Theater Mountain Video",
        "Town RGB Squares",
        "Town RGB Stars",
        "Swamp Underwater Back Optional",
    }

    CAVES_LOCATIONS = {
        "Inside Mountain Caves Dot Grid Triangles 4",
        "Inside Mountain Caves Symmetry Triangles",
        "Inside Mountain Caves Stars & Squares and Triangles 2",
        "Inside Mountain Caves Shapers and Triangles 2",
        "Inside Mountain Caves Symmetry Shapers",
        "Inside Mountain Caves Broken and Negative Shapers",
        "Inside Mountain Caves Broken Shapers",

        "Inside Mountain Caves Rainbow Squares",
        "Inside Mountain Caves Squares & Stars and Colored Eraser",
        "Inside Mountain Caves Rotated Broken Shapers",
        "Inside Mountain Caves Stars and Squares",
        "Inside Mountain Caves Lone Pillar",
        "Inside Mountain Caves Wooden Beam Shapers",
        "Inside Mountain Caves Wooden Beam Squares and Shapers",
        "Inside Mountain Caves Wooden Beam Stars and Squares",
        "Inside Mountain Caves Wooden Beam Shapers and Stars",
        "Inside Mountain Caves Upstairs Invisible Dots 8",
        "Inside Mountain Caves Upstairs Invisible Dot Symmetry 3",
        "Inside Mountain Caves Upstairs Dot Grid Negative Shapers",
        "Inside Mountain Caves Upstairs Dot Grid Rotated Shapers",

        "Theater Walkway Vault Box",
        "Inside Mountain Bottom Layer Discard",
        "Theater Challenge Video",
    }

    MOUNTAIN_UNREACHABLE_FROM_BEHIND = {
        "Mountaintop Trap Door Triple Exit",

        "Inside Mountain Obscured Vision 5",
        "Inside Mountain Moving Background 7",
        "Inside Mountain Physically Obstructed 3",
        "Inside Mountain Angled Inside Trash 2",
        "Inside Mountain Color Cycle 5",
        "Inside Mountain Same Solution 6",
    }

    MOUNTAIN_REACHABLE_FROM_BEHIND = {
        "Inside Mountain Elevator Discard",
        "Inside Mountain Giant Puzzle",

        "Inside Mountain Final Room Left Pillar 4",
        "Inside Mountain Final Room Right Pillar 4",
    }

    ALL_LOCATIONS_TO_ID = dict()

    @staticmethod
    def get_id(chex):
        """
        Calculates the location ID for any given location
        """

        return StaticWitnessLogic.CHECKS_BY_HEX[chex]["id"]

    @staticmethod
    def get_event_name(panel_hex):
        """
        Returns the event name of any given panel.
        Currently this is always "Panelname Solved"
        """

        return StaticWitnessLogic.CHECKS_BY_HEX[panel_hex]["checkName"] + " Solved"

    def __init__(self):
        all_loc_to_id = {
            panel_obj["checkName"]: self.get_id(chex)
            for chex, panel_obj in StaticWitnessLogic.CHECKS_BY_HEX.items()
            if panel_obj["id"]
        }

        all_loc_to_id = dict(
            sorted(all_loc_to_id.items(), key=lambda loc: loc[1])
        )

        for key, item in all_loc_to_id.items():
            self.ALL_LOCATIONS_TO_ID[key] = item


class WitnessPlayerLocations:
    """
    Class that defines locations for a single player
    """

    def __init__(self, world, player, player_logic: WitnessPlayerLogic):
        """Defines locations AFTER logic changes due to options"""

        self.PANEL_TYPES_TO_SHUFFLE = {"General", "Laser"}
        self.CHECK_LOCATIONS = (
            StaticWitnessLocations.GENERAL_LOCATIONS
        )

        doors = get_option_value(world, player, "shuffle_doors")
        earlyutm = is_option_enabled(world, player, "early_secret_area")
        victory = get_option_value(world, player, "victory_condition")
        lasers = get_option_value(world, player, "challenge_lasers")
        laser_shuffle = get_option_value(world, player, "shuffle_lasers")

        postgame = set()
        postgame = postgame | StaticWitnessLocations.CAVES_LOCATIONS
        postgame = postgame | StaticWitnessLocations.MOUNTAIN_REACHABLE_FROM_BEHIND
        postgame = postgame | StaticWitnessLocations.MOUNTAIN_UNREACHABLE_FROM_BEHIND

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | postgame

        if earlyutm or doors >= 2 or (victory == 1 and (lasers <= 11 or laser_shuffle)):
            postgame -= StaticWitnessLocations.CAVES_LOCATIONS

        if doors >= 2:
            postgame -= StaticWitnessLocations.MOUNTAIN_REACHABLE_FROM_BEHIND

        if victory != 2:
            postgame -= StaticWitnessLocations.MOUNTAIN_UNREACHABLE_FROM_BEHIND

        if is_option_enabled(world, player, "shuffle_discarded_panels"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Discard")

        if is_option_enabled(world, player, "shuffle_vault_boxes"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Vault")

        if is_option_enabled(world, player, "shuffle_uncommon"):
            self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | StaticWitnessLocations.UNCOMMON_LOCATIONS

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | player_logic.ADDED_CHECKS

        if not is_option_enabled(world, player, "shuffle_postgame"):
            self.CHECK_LOCATIONS -= postgame

        self.CHECK_LOCATIONS.discard(StaticWitnessLogic.CHECKS_BY_HEX[player_logic.VICTORY_LOCATION]["checkName"])

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS - {
            StaticWitnessLogic.CHECKS_BY_HEX[check_hex]["checkName"]
            for check_hex in player_logic.COMPLETELY_DISABLED_CHECKS
        }

        self.CHECK_PANELHEX_TO_ID = {
            StaticWitnessLogic.CHECKS_BY_NAME[ch]["checkHex"]: StaticWitnessLocations.ALL_LOCATIONS_TO_ID[ch]
            for ch in self.CHECK_LOCATIONS
        }

        self.CHECK_PANELHEX_TO_ID = dict(
            sorted(self.CHECK_PANELHEX_TO_ID.items(), key=lambda item: item[1])
        )

        event_locations = {
            p for p in player_logic.EVENT_PANELS
        }

        self.EVENT_LOCATION_TABLE = {
            StaticWitnessLocations.get_event_name(panel_hex): None
            for panel_hex in event_locations
        }

        check_dict = {
            location: StaticWitnessLocations.get_id(StaticWitnessLogic.CHECKS_BY_NAME[location]["checkHex"])
            for location in self.CHECK_LOCATIONS
            if StaticWitnessLogic.CHECKS_BY_NAME[location]["panelType"] in self.PANEL_TYPES_TO_SHUFFLE
        }

        self.CHECK_LOCATION_TABLE = {**self.EVENT_LOCATION_TABLE, **check_dict}
