"""
Defines constants for different types of locations in the game
"""

from .Options import is_option_enabled, get_option_value
from .player_logic import WitnessPlayerLogic
from .static_logic import StaticWitnessLogic


ID_START = 158000


class StaticWitnessLocations:
    """
    Witness Location Constants that stay consistent across worlds
    """

    GENERAL_LOCATIONS = {
        "Tutorial Front Left",
        "Tutorial Back Left",
        "Tutorial Back Right",
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
        "Desert Final Hexagonal",
        "Desert Final Bent 3",
        "Desert Laser Panel",

        "Quarry Stoneworks Lower Row 6",
        "Quarry Stoneworks Upper Row 8",
        "Quarry Stoneworks Control Room Right",
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

        "Keep Hedge Maze 1",
        "Keep Hedge Maze 2",
        "Keep Hedge Maze 3",
        "Keep Hedge Maze 4",
        "Keep Pressure Plates 1",
        "Keep Pressure Plates 2",
        "Keep Pressure Plates 3",
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
        "Quarry Stoneworks Control Room Left",
        "Theater Tutorial Video",
        "Theater Desert Video",
        "Theater Jungle Video",
        "Theater Shipwreck Video",
        "Theater Mountain Video",
        "Town RGB Room Left",
        "Town RGB Room Right",
        "Town Sound Room Right",
        "Swamp Purple Underwater",

        "First Hallway EP",
        "Tutorial Cloud EP",
        "Tutorial Patio Flowers EP",
        "Tutorial Gate EP",
        "Outside Tutorial Garden EP",
        "Outside Tutorial Town Sewer EP",
        "Outside Tutorial Path EP",
        "Outside Tutorial Tractor EP",
        "Main Island Thundercloud EP",
        "Glass Factory Vase EP",
        "Symmetry Island Glass Factory Black Line Reflection EP",
        "Symmetry Island Glass Factory Black Line EP",
        "Desert Sand Snake EP",
        "Desert Facade Right EP",
        "Desert Facade Left EP",
        "Desert Stairs Left EP",
        "Desert Stairs Right EP",
        "Desert Broken Wall Straight EP",
        "Desert Broken Wall Bend EP",
        "Desert Shore EP",
        "Desert Island EP",
        "Desert Pond Room Near Reflection EP",
        "Desert Pond Room Far Reflection EP",
        "Desert Flood Room EP",
        "Desert Elevator EP",
        "Quarry Shore EP",
        "Quarry Entrance Pipe EP",
        "Quarry Sand Pile EP",
        "Quarry Rock Line EP",
        "Quarry Rock Line Reflection EP",
        "Quarry Railroad EP",
        "Quarry Stoneworks Ramp EP",
        "Quarry Stoneworks Lift EP",
        "Quarry Boathouse Moving Ramp EP",
        "Quarry Boathouse Hook EP",
        "Shadows Quarry Stoneworks Rooftop Vent EP",
        "Treehouse Beach Rock Shadow EP",
        "Treehouse Beach Sand Shadow EP",
        "Treehouse Beach Both Orange Bridges EP",
        "Keep Red Flowers EP",
        "Keep Purple Flowers EP",
        "Shipwreck Circle Near EP",
        "Shipwreck Circle Left EP",
        "Shipwreck Circle Far EP",
        "Shipwreck Stern EP",
        "Shipwreck Rope Inner EP",
        "Shipwreck Rope Outer EP",
        "Shipwreck Couch EP",
        "Keep Pressure Plates 1 EP",
        "Keep Pressure Plates 2 EP",
        "Keep Pressure Plates 3 EP",
        "Keep Pressure Plates 4 Left Exit EP",
        "Keep Pressure Plates 4 Right Exit EP",
        "Keep Path EP",
        "Keep Hedges EP",
        "Monastery Facade Left Near EP",
        "Monastery Facade Left Far Short EP",
        "Monastery Facade Left Far Long EP",
        "Monastery Facade Right Near EP",
        "Monastery Facade Left Stairs EP",
        "Monastery Facade Right Stairs EP",
        "Monastery Grass Stairs EP",
        "Monastery Left Shutter EP",
        "Monastery Middle Shutter EP",
        "Monastery Right Shutter EP",
        "Town Windmill First Blade EP",
        "Town Windmill Second Blade EP",
        "Town Windmill Third Blade EP",
        "Town Tower Underside Third EP",
        "Town Tower Underside Fourth EP",
        "Town Tower Underside First EP",
        "Town Tower Underside Second EP",
        "Town RGB House Red EP",
        "Town RGB House Green EP",
        "Town Maze Bridge Underside EP",
        "Town Black Line Redirect EP",
        "Town Black Line Church EP",
        "Town Brown Bridge EP",
        "Town Black Line Tower EP",
        "Theater Eclipse EP",
        "Theater Window EP",
        "Theater Door EP",
        "Theater Church EP",
        "Jungle Long Arch Moss EP",
        "Jungle Straight Left Moss EP",
        "Jungle Pop-up Wall Moss EP",
        "Jungle Short Arch Moss EP",
        "Jungle Entrance EP",
        "Jungle Tree Halo EP",
        "Jungle Bamboo CCW EP",
        "Jungle Bamboo CW EP",
        "River Green Leaf Moss EP",
        "River Monastery Garden Left EP",
        "River Monastery Garden Right EP",
        "River Monastery Wall EP",
        "Bunker Tinted Door EP",
        "Bunker Green Room Flowers EP",
        "Swamp Purple Sand Middle EP",
        "Swamp Purple Sand Top EP",
        "Swamp Purple Sand Bottom EP",
        "Swamp Sliding Bridge Left EP",
        "Swamp Sliding Bridge Right EP",
        "Swamp Cyan Underwater Sliding Bridge EP",
        "Swamp Rotating Bridge CCW EP",
        "Swamp Rotating Bridge CW EP",
        "Swamp Boat EP",
        "Swamp Long Bridge Side EP",
        "Swamp Purple Underwater Right EP",
        "Swamp Purple Underwater Left EP",
        "Treehouse Buoy EP",
        "Treehouse Right Orange Bridge EP",
        "Treehouse Burned House Beach EP",
        "Mountainside Cloud Cycle EP",
        "Mountainside Bush EP",
        "Mountainside Apparent River EP",
        "Mountaintop River Shape EP",
        "Mountaintop Arch Black EP",
        "Mountaintop Arch White Right EP",
        "Mountaintop Arch White Left EP",
        "Mountain Bottom Floor Yellow Bridge EP",
        "Mountain Bottom Floor Blue Bridge EP",
        "Mountain Floor 2 Pink Bridge EP",
        "Caves Skylight EP",
        "Challenge Water EP",
        "Tunnels Theater Flowers EP",
        "Boat Desert EP",
        "Boat Shipwreck CCW Underside EP",
        "Boat Shipwreck Green EP",
        "Boat Shipwreck CW Underside EP",
        "Boat Bunker Yellow Line EP",
        "Boat Town Long Sewer EP",
        "Boat Tutorial EP",
        "Boat Tutorial Reflection EP",
        "Boat Tutorial Moss EP",
        "Boat Cargo Box EP",

        "Desert Obelisk Side 1",
        "Desert Obelisk Side 2",
        "Desert Obelisk Side 3",
        "Desert Obelisk Side 4",
        "Desert Obelisk Side 5",
        "Monastery Obelisk Side 1",
        "Monastery Obelisk Side 2",
        "Monastery Obelisk Side 3",
        "Monastery Obelisk Side 4",
        "Monastery Obelisk Side 5",
        "Monastery Obelisk Side 6",
        "Treehouse Obelisk Side 1",
        "Treehouse Obelisk Side 2",
        "Treehouse Obelisk Side 3",
        "Treehouse Obelisk Side 4",
        "Treehouse Obelisk Side 5",
        "Treehouse Obelisk Side 6",
        "River Obelisk Side 1",
        "River Obelisk Side 2",
        "River Obelisk Side 3",
        "River Obelisk Side 4",
        "River Obelisk Side 5",
        "River Obelisk Side 6",
        "Quarry Obelisk Side 1",
        "Quarry Obelisk Side 2",
        "Quarry Obelisk Side 3",
        "Quarry Obelisk Side 4",
        "Quarry Obelisk Side 5",
        "Town Obelisk Side 1",
        "Town Obelisk Side 2",
        "Town Obelisk Side 3",
        "Town Obelisk Side 4",
        "Town Obelisk Side 5",
        "Town Obelisk Side 6",
    }

    OBELISK_SIDES = {
        "Desert Obelisk Side 1",
        "Desert Obelisk Side 2",
        "Desert Obelisk Side 3",
        "Desert Obelisk Side 4",
        "Desert Obelisk Side 5",
        "Monastery Obelisk Side 1",
        "Monastery Obelisk Side 2",
        "Monastery Obelisk Side 3",
        "Monastery Obelisk Side 4",
        "Monastery Obelisk Side 5",
        "Monastery Obelisk Side 6",
        "Treehouse Obelisk Side 1",
        "Treehouse Obelisk Side 2",
        "Treehouse Obelisk Side 3",
        "Treehouse Obelisk Side 4",
        "Treehouse Obelisk Side 5",
        "Treehouse Obelisk Side 6",
        "River Obelisk Side 1",
        "River Obelisk Side 2",
        "River Obelisk Side 3",
        "River Obelisk Side 4",
        "River Obelisk Side 5",
        "River Obelisk Side 6",
        "Quarry Obelisk Side 1",
        "Quarry Obelisk Side 2",
        "Quarry Obelisk Side 3",
        "Quarry Obelisk Side 4",
        "Quarry Obelisk Side 5",
        "Town Obelisk Side 1",
        "Town Obelisk Side 2",
        "Town Obelisk Side 3",
        "Town Obelisk Side 4",
        "Town Obelisk Side 5",
        "Town Obelisk Side 6",
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
        "Theater Challenge Video",

        "Caves Skylight EP",
        "Challenge Water EP",
        "Tunnels Theater Flowers EP",
        "Tutorial Gate EP",
    }

    MOUNTAIN_UNREACHABLE_FROM_BEHIND = {
        "Mountaintop Trap Door Triple Exit",

        "Mountain Floor 1 Right Row 5",
        "Mountain Floor 1 Left Row 7",
        "Mountain Floor 1 Back Row 3",
        "Mountain Floor 1 Trash Pillar 2",
        "Mountain Floor 2 Near Row 5",
        "Mountain Floor 2 Far Row 6",

        "Mountain Floor 2 Light Bridge Controller Near",
        "Mountain Floor 2 Light Bridge Controller Far",

        "Mountain Bottom Floor Yellow Bridge EP",
        "Mountain Bottom Floor Blue Bridge EP",
        "Mountain Floor 2 Pink Bridge EP",
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
        """

        action = " Opened" if StaticWitnessLogic.CHECKS_BY_HEX[panel_hex]["panelType"] == "Door" else " Solved"

        return StaticWitnessLogic.CHECKS_BY_HEX[panel_hex]["checkName"] + action

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

        doors = get_option_value(world, player, "shuffle_doors") >= 2
        earlyutm = is_option_enabled(world, player, "early_secret_area")
        victory = get_option_value(world, player, "victory_condition")
        mount_lasers = get_option_value(world, player, "mountain_lasers")
        chal_lasers = get_option_value(world, player, "challenge_lasers")
        # laser_shuffle = get_option_value(world, player, "shuffle_lasers")

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

        if get_option_value(world, player, "shuffle_EPs") == 1:
            self.PANEL_TYPES_TO_SHUFFLE.add("EP")
        elif get_option_value(world, player, "shuffle_EPs") == 2:
            self.PANEL_TYPES_TO_SHUFFLE.add("Obelisk Side")

            for obelisk_loc in StaticWitnessLocations.OBELISK_SIDES:
                obelisk_loc_hex = StaticWitnessLogic.CHECKS_BY_NAME[obelisk_loc]["checkHex"]
                if player_logic.REQUIREMENTS_BY_HEX[obelisk_loc_hex] == frozenset({frozenset()}):
                    self.CHECK_LOCATIONS.discard(obelisk_loc)

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS | player_logic.ADDED_CHECKS

        if not is_option_enabled(world, player, "shuffle_postgame"):
            self.CHECK_LOCATIONS -= postgame

        self.CHECK_LOCATIONS -= {
            StaticWitnessLogic.CHECKS_BY_HEX[panel]["checkName"]
            for panel in player_logic.PRECOMPLETED_LOCATIONS
        }

        self.CHECK_LOCATIONS.discard(StaticWitnessLogic.CHECKS_BY_HEX[player_logic.VICTORY_LOCATION]["checkName"])

        self.CHECK_LOCATIONS = self.CHECK_LOCATIONS - {
            StaticWitnessLogic.CHECKS_BY_HEX[check_hex]["checkName"]
            for check_hex in player_logic.COMPLETELY_DISABLED_CHECKS
        }

        self.CHECK_PANELHEX_TO_ID = {
            StaticWitnessLogic.CHECKS_BY_NAME[ch]["checkHex"]: StaticWitnessLocations.ALL_LOCATIONS_TO_ID[ch]
            for ch in self.CHECK_LOCATIONS
            if StaticWitnessLogic.CHECKS_BY_NAME[ch]["panelType"] in self.PANEL_TYPES_TO_SHUFFLE
        }

        dog_hex = StaticWitnessLogic.CHECKS_BY_NAME["Town Pet the Dog"]["checkHex"]
        dog_id = StaticWitnessLocations.ALL_LOCATIONS_TO_ID["Town Pet the Dog"]
        self.CHECK_PANELHEX_TO_ID[dog_hex] = dog_id

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
            StaticWitnessLogic.CHECKS_BY_HEX[location]["checkName"]:
            StaticWitnessLocations.get_id(StaticWitnessLogic.CHECKS_BY_HEX[location]["checkHex"])
            for location in self.CHECK_PANELHEX_TO_ID
        }

        self.CHECK_LOCATION_TABLE = {**self.EVENT_LOCATION_TABLE, **check_dict}
