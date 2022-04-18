"""
Defines constants for different types of locations in the game
"""


from worlds.witness.Options import is_option_enabled
from worlds.witness.full_logic import ParsedWitnessLogic


class WitnessLocations():
    """Class that handles Witness Locations"""
    ID_START = 158000

    TYPE_OFFSETS = {
        "General": 0,
        "Discard": 600,
        "Vault": 650,
        "Laser": 700,
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
        "Symmetry Island Laser",

        "Orchard Apple Tree 5",

        "Desert Vault Box",
        "Desert Discard",
        "Desert Sun Reflection 8",
        "Desert Artificial Light Reflection 3",
        "Desert Pond Reflection 5",
        "Desert Flood Reflection 5",
        "Desert Laser",

        "Quarry Mill Eraser and Dots 6",
        "Quarry Mill Eraser and Squares 8",
        "Quarry Mill Small Squares & Dots & and Eraser",
        "Quarry Boathouse Intro Shapers",
        "Quarry Boathouse Eraser and Shapers 5",
        "Quarry Boathouse Stars & Eraser & and Shapers 2",
        "Quarry Boathouse Stars & Eraser & and Shapers 5",
        "Quarry Laser",

        "Shadows Lower Avoid 8",
        "Shadows Environmental Avoid 8",
        "Shadows Follow 5",
        "Shadows Laser",

        "Keep Hedge Maze 4",
        "Keep Pressure Plates 4",
        "Keep Discard",
        "Keep Laser Hedges",
        "Keep Laser Pressure Plates",

        "Shipwreck Vault Box",
        "Shipwreck Discard",

        "Monastery Rhombic Avoid 3",
        "Monastery Branch Follow 2",
        "Monastery Laser",

        "Town Cargo Box Discard",
        "Town Hexagonal Reflection",
        "Town Square Avoid",
        "Town Rooftop Discard",
        "Town Symmetry Squares 5 + Dots",
        "Town Full Dot Grid Shapers 5",
        "Town Shapers & Dots & and Eraser",
        "Town RGB Squares",
        "Town RGB Stars",
        "Town Laser",

        "Theater Discard",

        "Jungle Discard",
        "Jungle Waves 3",
        "Jungle Waves 7",
        "Jungle Popup Wall 6",
        "Jungle Laser",

        "River Rhombic Avoid Vault",

        "Bunker Drawn Squares 5",
        "Bunker Drawn Squares 9",
        "Bunker Drawn Squares through Tinted Glass 3",
        "Bunker Drop-Down Door Squares 2",
        "Bunker Laser",

        "Swamp Seperatable Shapers 6",
        "Swamp Combinable Shapers 8",
        "Swamp Broken Shapers 4",
        "Swamp Cyan Underwater Negative Shapers 5",
        "Swamp Platform Shapers 4",
        "Swamp Rotated Shapers 4",
        "Swamp Red Underwater Negative Shapers 4",
        "Swamp More Rotated Shapers 4",
        "Swamp Blue Underwater Negative Shapers 5",
        "Swamp Laser",

        "Treehouse Yellow Bridge 9",
        "Treehouse First Purple Bridge 5",
        "Treehouse Second Purple Bridge 7",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Treehouse Left Orange Bridge 15",
        "Treehouse Burned House Discard",
        "Treehouse Right Orange Bridge 12",
        "Treehouse Laser",

        "Mountaintop Trap Door Triple Exit",
        "Mountaintop Discard",
        "Mountaintop Vault Box",

        "Inside Mountain Obscured Vision 5",
        "Inside Mountain Moving Background 7",
        "Inside Mountain Physically Obstructed 3",
        "Inside Mountain Angled Inside Trash 2",
        "Inside Mountain Color Cycle 5",
        "Inside Mountain Same Solution 6",
        "Inside Mountain Elevator Discard",
        "Inside Mountain Giant Puzzle",



        "Inside Mountain Final Room Elevator Start"
    }

    UNCOMMON_LOCATIONS = {
        "Mountaintop River Shape",
        "Tutorial Patio Floor",
        "Theater Tutorial Video",
        "Theater Desert Video",
        "Theater Jungle Video",
        "Theater Challenge Video",
        "Theater Shipwreck Video",
        "Theater Mountain Video"
    }

    HARD_LOCATIONS = {
        "Tutorial Gate Close",
        "Quarry Mill Big Squares & Dots & and Eraser",
        "Swamp Underwater Back Optional",

        "Inside Mountain Secret Area Dot Grid Triangles 4",
        "Inside Mountain Secret Area Symmetry Triangles",
        "Inside Mountain Secret Area Stars & Squares and Triangles 2",
        "Inside Mountain Secret Area Shapers and Triangles 2",
        "Inside Mountain Secret Area Symmetry Shapers",
        "Inside Mountain Secret Area Broken and Negative Shapers",
        "Inside Mountain Secret Area Broken Shapers",

        "Inside Mountain Secret Area Rainbow Squares",
        "Inside Mountain Secret Area Squares & Stars and Colored Eraser",
        "Inside Mountain Secret Area Rotated Broken Shapers",
        "Inside Mountain Secret Area Stars and Squares",
        "Inside Mountain Secret Area Lone Pillar",
        "Inside Mountain Secret Area Wooden Beam Shapers",
        "Inside Mountain Secret Area Wooden Beam Squares and Shapers",
        "Inside Mountain Secret Area Wooden Beam Shapers and Squares",
        "Inside Mountain Secret Area Wooden Beam Shapers and Stars",
        "Inside Mountain Secret Area Upstairs Invisible Dots 8",
        "Inside Mountain Secret Area Upstairs Invisible Dot Symmetry 3",
        "Inside Mountain Secret Area Upstairs Dot Grid Shapers",
        "Inside Mountain Secret Area Upstairs Dot Grid Rotated Shapers",

        "Challenge Vault Box",
        "Theater Walkway Vault Box",
        "Inside Mountain Bottom Layer Discard"
    }

    def get_id(self, chex):
        """
        Calculates the location ID for any given location
        """

        panel_offset = self.logic.CHECKS_DEPENDENT_BY_HEX[chex]["idOffset"]
        type_offset = self.TYPE_OFFSETS[
             self.logic.CHECKS_DEPENDENT_BY_HEX[chex]["panelType"]
        ]

        return self.ID_START + panel_offset + type_offset

    def get_event_name(self, panel_hex):
        """
        Returns the event name of any given panel.
        Currently this is always "Panelname Solved"
        """

        return self.logic.CHECKS_BY_HEX[panel_hex]["checkName"] + " Solved"

    def __init__(self, early_logic: ParsedWitnessLogic):
        self.logic = early_logic
        self.CHECK_LOCATIONS = None
        self.ALL_LOCATIONS = None
        self.EVENT_LOCATION_TABLE = None
        self.CHECK_LOCATION_TABLE = None
        self.ALL_LOCATIONS_TO_ID = None
        self.CHECK_PANELHEX_TO_ID = None

        self.PANEL_TYPES_TO_SHUFFLE = {"General", "Laser"}

        self.ALL_LOCATIONS_TO_ID = {
            panel_obj["checkName"]: self.get_id(chex)

            for chex, panel_obj in self.logic.CHECKS_DEPENDENT_BY_HEX.items()
        }

        self.CHECK_LOCATIONS = (
            self.GENERAL_LOCATIONS
        )

    def define_locations(self, world, player):
        """Defines locations AFTER logic changes due to options"""

        if is_option_enabled(world, player, "shuffle_discarded_panels"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Discard")

        if is_option_enabled(world, player, "shuffle_vault_boxes"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Vault")

        if is_option_enabled(world, player, "shuffle_uncommon"):
            self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | self.UNCOMMON_LOCATIONS
            
        if is_option_enabled(world, player, "shuffle_hard"):
            self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | self.HARD_LOCATIONS


        self.ALL_LOCATIONS_TO_ID = dict(
            sorted(self.ALL_LOCATIONS_TO_ID.items(), key=lambda item: item[1])
        )

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS - {
            self.logic.CHECKS_BY_HEX[check_hex]["checkName"]
            for check_hex in self.logic.COMPLETELY_DISABLED_CHECKS
        }

        self.BYE_PANELS = {"Inside Mountain Final Room Elevator Start"}

        if is_option_enabled(world, player, "challenge_victory"):
            self.CHECK_LOCATIONS.add("Challenge Vault Box")
            self.CHECK_LOCATIONS.remove("Inside Mountain Final Room Elevator Start")
            self.BYE_PANELS.add("Challenge Vault Box")
            self.BYE_PANELS.remove("Inside Mountain Final Room Elevator Start")


        self.CHECK_PANELHEX_TO_ID = {
            self.logic.CHECKS_BY_NAME[ch]["checkHex"]:
            self.ALL_LOCATIONS_TO_ID[ch]
            for ch in self.CHECK_LOCATIONS
        }

        self.CHECK_PANELHEX_TO_ID = dict(
            sorted(self.CHECK_PANELHEX_TO_ID.items(), key=lambda item: item[1])
        )

        event_locations = {
            p for p in self.logic.NECESSARY_EVENT_PANELS
            if self.logic.CHECKS_BY_HEX[p]["checkName"]
            not in self.CHECK_LOCATIONS
            or p in self.logic.ALWAYS_EVENT_HEX_CODES
        }

        self.EVENT_LOCATION_TABLE = {
            self.get_event_name(panel_hex): None
            for panel_hex in event_locations
        }

        self.CHECK_LOCATION_TABLE = self.EVENT_LOCATION_TABLE | {
            location:
            self.get_id(self.logic.CHECKS_BY_NAME[location]["checkHex"])
            for location in self.CHECK_LOCATIONS

            if self.logic.CHECKS_BY_NAME[location]["panelType"]
            in self.PANEL_TYPES_TO_SHUFFLE
            or location in self.BYE_PANELS
        }
