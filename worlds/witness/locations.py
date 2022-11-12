"""
Defines constants for different types of locations in the game
"""

from .Options import is_option_enabled, get_option_value
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic


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
        "Outside Tutorial Shed Row 5",
        "Outside Tutorial Tree Row 9",

        "Glass Factory Discard",
        "Glass Factory Back Wall 5",
        "Glass Factory Front 3",
        "Glass Factory Melting 3",

        "Symmetry Island Right 5",
        "Symmetry Island Back 6",
        "Symmetry Island Left 7",
        "Symmetry Island Scenery Outlines 5",
        "Symmetry Island Laser Panel",

        "Orchard Apple Tree 5",

        "Desert Vault Box",
        "Desert Discard",
        "Desert Surface 8",
        "Desert Light Room 3",
        "Desert Pond Room 5",
        "Desert Flood Room 6",
        "Desert Laser Panel",

        "Quarry Mill Lower Row 6",
        "Quarry Mill Upper Row 8",
        "Quarry Mill Control Room Right",
        "Quarry Boathouse Intro Right",
        "Quarry Boathouse Intro Left",
        "Quarry Boathouse Front Row 5",
        "Quarry Boathouse Back First Row 9",
        "Quarry Boathouse Back Second Row 3",
        "Quarry Discard",
        "Quarry Laser Panel",

        "Shadows Intro 8",
        "Shadows Far 8",
        "Shadows Near 5",
        "Shadows Laser Panel",

        "Keep Hedge Maze 4",
        "Keep Pressure Plates 4",
        "Keep Discard",
        "Keep Laser Panel Hedges",
        "Keep Laser Panel Pressure Plates",

        "Shipwreck Vault Box",
        "Shipwreck Discard",

        "Monastery Outside 3",
        "Monastery Inside 4",
        "Monastery Laser Panel",

        "Town Cargo Box Discard",
        "Town Tall Hexagonal",
        "Town Church Lattice",
        "Town Rooftop Discard",
        "Town Red Rooftop 5",
        "Town Wooden Roof Lower Row 5",
        "Town Wooden Rooftop",
        "Town Laser Panel",

        "Theater Discard",

        "Jungle Discard",
        "Jungle First Row 3",
        "Jungle Second Row 4",
        "Jungle Popup Wall 6",
        "Jungle Laser Panel",

        "River Vault Box",

        "Bunker Intro Left 5",
        "Bunker Intro Back 4",
        "Bunker Glass Room 3",
        "Bunker UV Room 2",
        "Bunker Laser Panel",

        "Swamp Intro Front 6",
        "Swamp Intro Back 8",
        "Swamp Between Bridges Near Row 4",
        "Swamp Cyan Underwater 5",
        "Swamp Platform Row 4",
        "Swamp Between Bridges Far Row 4",
        "Swamp Red Underwater 4",
        "Swamp Beyond Rotating Bridge 4",
        "Swamp Blue Underwater 5",
        "Swamp Laser Panel",

        "Treehouse Yellow Bridge 9",
        "Treehouse First Purple Bridge 5",
        "Treehouse Second Purple Bridge 7",
        "Treehouse Green Bridge 7",
        "Treehouse Green Bridge Discard",
        "Treehouse Left Orange Bridge 15",
        "Treehouse Laser Discard",
        "Treehouse Right Orange Bridge 12",
        "Treehouse Laser Panel",

        "Mountainside Discard",
        "Mountainside Vault Box",

        "Mountaintop River Shape",
        "Tutorial Patio Floor",
        "Quarry Mill Control Room Left",
        "Theater Tutorial Video",
        "Theater Desert Video",
        "Theater Jungle Video",
        "Theater Shipwreck Video",
        "Theater Mountain Video",
        "Town RGB Room Left",
        "Town RGB Room Right",
        "Swamp Purple Underwater",
    }

    CAVES_LOCATIONS = {
        "Caves Blue Tunnel Right First 4",
        "Caves Blue Tunnel Left First 1",
        "Caves Blue Tunnel Left Second 5",
        "Caves Blue Tunnel Right Second 5",
        "Caves Blue Tunnel Right Third 1",
        "Caves Blue Tunnel Left Fourth 1",
        "Caves Blue Tunnel Left Third 1",

        "Caves First Floor Middle",
        "Caves First Floor Right",
        "Caves First Floor Left",
        "Caves First Floor Grounded",
        "Caves Lone Pillar",
        "Caves First Wooden Beam",
        "Caves Second Wooden Beam",
        "Caves Third Wooden Beam",
        "Caves Fourth Wooden Beam",
        "Caves Right Upstairs Left Row 8",
        "Caves Right Upstairs Right Row 3",
        "Caves Left Upstairs Single",
        "Caves Left Upstairs Left Row 5",

        "Tunnels Vault Box",
        "Mountain Bottom Floor Discard",
        "Theater Challenge Video",
    }

    MOUNTAIN_UNREACHABLE_FROM_BEHIND = {
        "Mountaintop Trap Door Triple Exit",

        "Mountain Floor 1 Right Row 5",
        "Mountain Floor 1 Left Row 7",
        "Mountain Floor 1 Back Row 3",
        "Mountain Floor 1 Trash Pillar 2",
        "Mountain Floor 2 Near Row 5",
        "Mountain Floor 2 Far Row 6",
    }

    MOUNTAIN_REACHABLE_FROM_BEHIND = {
        "Mountain Floor 2 Elevator Discard",
        "Mountain Bottom Floor Giant Puzzle",

        "Mountain Final Room Left Pillar 4",
        "Mountain Final Room Right Pillar 4",
    }

    MOUNTAIN_EXTRAS = {
        "Challenge Vault Box",
        "Theater Challenge Video",
        "Mountain Bottom Floor Discard"
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
        self.CHECK_LOCATIONS = StaticWitnessLocations.GENERAL_LOCATIONS.copy()

        if get_option_value(world, player, "puzzle_randomization") == 1:
            self.CHECK_LOCATIONS.remove("Keep Pressure Plates 4")
            self.CHECK_LOCATIONS.add("Keep Pressure Plates 2")

        doors = get_option_value(world, player, "shuffle_doors") >= 2
        earlyutm = is_option_enabled(world, player, "early_secret_area")
        victory = get_option_value(world, player, "victory_condition")
        mount_lasers = get_option_value(world, player, "mountain_lasers")
        chal_lasers = get_option_value(world, player, "challenge_lasers")
        laser_shuffle = get_option_value(world, player, "shuffle_lasers")

        postgame = set()
        postgame = postgame | StaticWitnessLocations.CAVES_LOCATIONS
        postgame = postgame | StaticWitnessLocations.MOUNTAIN_REACHABLE_FROM_BEHIND
        postgame = postgame | StaticWitnessLocations.MOUNTAIN_UNREACHABLE_FROM_BEHIND
        postgame = postgame | StaticWitnessLocations.MOUNTAIN_EXTRAS

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | postgame

        mountain_enterable_from_top = victory == 0 or victory == 1 or (victory == 3 and chal_lasers > mount_lasers)

        if earlyutm or doors:  # in non-doors, there is no way to get symbol-locked by the final pillars (currently)
            postgame -= StaticWitnessLocations.CAVES_LOCATIONS

        if (doors or earlyutm) and (victory == 0 or (victory == 2 and mount_lasers > chal_lasers)):
            postgame -= {"Challenge Vault Box", "Theater Challenge Video"}

        if doors or mountain_enterable_from_top:
            postgame -= StaticWitnessLocations.MOUNTAIN_REACHABLE_FROM_BEHIND

        if mountain_enterable_from_top:
            postgame -= StaticWitnessLocations.MOUNTAIN_UNREACHABLE_FROM_BEHIND

        if (victory == 0 and doors) or victory == 1 or (victory == 2 and mount_lasers > chal_lasers and doors):
            postgame -= {"Mountain Bottom Floor Discard"}

        if is_option_enabled(world, player, "shuffle_discarded_panels"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Discard")

        if is_option_enabled(world, player, "shuffle_vault_boxes"):
            self.PANEL_TYPES_TO_SHUFFLE.add("Vault")

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
