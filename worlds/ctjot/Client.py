import json
import logging

from NetUtils import ClientStatus, NetworkItem

from worlds.AutoSNIClient import SNIClient

snes_logger = logging.getLogger("SNES")

# FXPAK Pro protocol memory mapping used by SNI
ROM_START = 0x000000
WRAM_START = 0xF50000
WRAM_SIZE = 0x20000
SRAM_START = 0xE00000

# CTJoT addresses/constants
# TODO: Unify the address scheme.  These use the SNES addresses,
#       but SNI maps things a little differently.
#       For now I'm just converting on the fly when they are used.
EVENT_BLOCK_SIZE = 0x200
EVENT_BASE_ADDR = 0x7F0000
TREASURE_BASE_ADDR = 0x7F0001
RECEIVE_ITEM_ADDR = 0x7E287A
RECEIVED_ITEM_COUNT_ADDR = 0x7E287C
VICTORY_ADDRESS = 0x7F0020
LOCATION_ADDRESS = 0xF50100  # already in SNI addressing

# These are already in SNI addressing
# NOTE: SNI with RetroArch can't read past 4MB in the ROM
#       Validation data must be before 4MB or the client can't validate/connect to the game
VALIDATION_ADDR = ROM_START + 0x3F8C03
VALIDATION_SIZE = 32

# Item and location ID offsets
LOCATION_ID_START = 5100000
ITEM_ID_START = 5100000
MAX_IN_GAME_ITEM_ID = 255

# Don't track on the Load Screen(0x00) or Title Screen(0x1B1)
INVALID_TRACKING_LOCATIONS = [0x00, 0x1B1]
MAX_MAP_ID = 0x1FF


# These are the event flag locations for the baseline (non chronosanity) checks
_locations_baseline_key_items = {
    # ##########
    # Prehistory
    # ##########
    "Reptite Lair Key": (0x7F0105, 0x20),

    # ##########
    # Dark Ages
    # ##########
    "Mt Woe Key": (0x7F0100, 0x20),

    # ##########
    # 600 AD
    # ##########
    # NOTE: Giant's Claw Key is triggered on warping out of the cave,
    #       not immediately on picking up the key item from the shell.
    "Giants Claw Key": (0x7F00A9, 0x80),
    "Zenan Bridge Key": (0x7F0101, 0x02),
    "Denadoro Mts Key": (0x7F0102, 0x02),
    "Frogs Burrow Left": (0x7F0106, 0x04),

    # This only applies in vanilla rando mode
    "Cyrus Grave Key": (0x7F01A3, 0x40),

    # ##########
    # 1000 AD
    # ##########
    "Fiona Key": (0x7F007C, 0x80),
    "Kings Trial Key": (0x7F00A2, 0x80),
    "Snail Stop Key": (0x7F01D0, 0x10),
    "Lazy Carpenter": (0x7F019E, 0x80),
    "Taban Key": (0x7F007A, 0x01),
    "Melchior Key": (0x7F001F, 0x80),

    # This only applies in vanilla rando mode
    "Bekkler Key": (0x7F007C, 0x01),

    # ##########
    # 2300 AD
    # ##########
    "Arris Dome Key": (0x7F00A4, 0x01),
    "Sun Palace Key": (0x7F013A, 0x02),
    "Geno Dome Key": (0x7F013B, 0x10)
}

# These are things like sealed chests and the chests
# at the Northern Ruins that aren't treated like normal
# treasure chests.  These are handled in event code.
_locations_event_treasures = {
    "Northern Ruins Antechamber Left 600": (0x7F01AC, 0x08),
    "Northern Ruins Antechamber Sealed 600": (0x7F01A9, 0x20),
    "Northern Ruins Antechamber Left 1000": (0x7F01AC, 0x04),
    "Northern Ruins Antechamber Sealed 1000": (0x7F01A6, 0x01),
    "Northern Ruins Back Left Sealed 600": (0x7F01A9, 0x40),
    "Northern Ruins Back Right Sealed 600": (0x7F01A9, 0x80),
    "Northern Ruins Back Left Sealed 1000": (0x7F01A6, 0x02),
    "Northern Ruins Back Right Sealed 1000": (0x7F01A6, 0x04),
    "Northern Ruins Basement 600": (0x7F01AC, 0x02),
    "Northern Ruins Basement 1000": (0x7F01AC, 0x01),
    "Truce Inn Sealed 600": (0x7F014A, 0x80),
    "Porre Elder Sealed 1": (0x7F01D3, 0x10),
    "Porre Elder Sealed 2": (0x7F01D3, 0x20),
    "Guardia Castle Sealed 600": (0x7F00D9, 0x02),
    "Guardia Forest Sealed 600": (0x7F01D2, 0x80),
    "Truce Inn Sealed 1000": (0x7F014A, 0x20),
    "Porre Mayor Sealed 1": (0x7F01D1, 0x40),
    "Porre Mayor Sealed 2": (0x7F01D1, 0x80),
    "Guardia Forest Sealed 1000": (0x7F01D1, 0x20),
    "Guardia Castle Sealed 1000": (0x7F00D9, 0x04),
    "Heckran Sealed 1": (0x7F01A0, 0x04),
    "Heckran Sealed 2": (0x7F01A0, 0x04),
    "Magic Cave Sealed": (0x7F0079, 0x01),

    # The pyramid chests share a flag.  Opening one will cause the other to vanish.
    # In the normal randomizer the player could only get one of these, but in multiworld
    # we will send items for both chests when the flag is cleared.
    "Pyramid Left": (0x7F01A0, 0x01),
    "Pyramid Right": (0x7F01A0, 0x01),

}

# Not currently used for item randomization
_locations_tab_events = {
    "Guardia Forest Power Tab 600": 192,
    "Guardia Forest Power Tab 1000": 193,
    "Manoria Confinement Power Tab": 194,
    "Porre Market 600 Power Tab": 195,
    "Denadoro Mts Speed Tab": 196,
    "Tomas Grave Speed Tab": 197,
    "Giants Claw Caverns Power Tab": 198,
    "Giants Claw Entrance Power Tab": 199,
    "Giants Claw Traps Power Tab": 200,
    "Sun Keep 600 Power Tab": 201,
    "Medina Elder Speed Tab": 202,
    "Medina Elder Magic Tab": 203,
    "Magus Castle Flea Magic Tab": 204,
    "Magus Castle Dungeons Magic Tab": 205,
    "Trann Dome Sealed Magic Tab": 206,
    "Arris Dome Sealed Power Tab": 207,
    "Death Peak Power Tab": 208,
}

# Location IDs for miscellaneous events.
_locations_misc_events = {
    "Taban Gift Weapon": 300,
    "Taban Gift Helm": 301,
    "Trading Post Ranged Weapon": 302,
    "Trading Post Accessory": 303,
    "Trading Post Tab": 304,
    "Trading Post Melee Weapon": 305,
    "Trading Post Armor": 306,
    "Trading Post Helm": 307,
    "Jerky Gift": 308,
    "Giants Claw Rock": (0x0B, 0x40),  # Treasure chest
    "Black Omen Terra Rock": 283,
    "Denadoro Rock": 309,
    "Kajar Rock": 310,
    "Laruba Rock": 311,
}

# These are treasure chests that are not considered in logic for
# key items.  Some may still hold bucket fragments.
_locations_treasure_chests_not_in_logic = {
    "Guardia Jail Fritz Storage": (0x01, 0x02),
    "Guardia Jail Cell": (0x02, 0x01),
    "Guardia Jail Omnicrone 1": (0x02, 0x02),
    "Guardia Jail Omnicrone 2": (0x02, 0x04),
    "Guardia Jail Omnicrone 3": (0x02, 0x08),
    "Guardia Jail Hole 1": (0x02, 0x10),
    "Guardia Jail Hole 2": (0x02, 0x20),
    "Guardia Jail Outer Wall": (0x02, 0x40),
    "Guardia Jail Omnicrone 4": (0x02, 0x80),
    "Guardia Jail Fritz": (0x03, 0x01),
    "Sunken Desert B1 Nw": (0x08, 0x01),
    "Sunken Desert B1 Ne": (0x08, 0x02),
    "Sunken Desert B1 Se": (0x08, 0x04),
    "Sunken Desert B1 Sw": (0x08, 0x08),
    "Sunken Desert B2 Nw": (0x08, 0x10),
    "Sunken Desert B2 N": (0x08, 0x20),
    "Sunken Desert B2 W": (0x09, 0x02),
    "Sunken Desert B2 Sw": (0x09, 0x01),
    "Sunken Desert B2 Se": (0x08, 0x80),
    "Sunken Desert B2 E": (0x08, 0x40),
    "Sunken Desert B2 Center": (0x09, 0x04),
    "Magus Castle Right Hall": 219,
    "Magus Castle Guillotine 1": 231,
    "Magus Castle Guillotine 2": 232,
    "Magus Castle Slash Room 1": 233,
    "Magus Castle Slash Room 2": 234,
    "Magus Castle Statue Hall": 235,
    "Magus Castle Four Kids": 236,
    "Magus Castle Ozzie 1": 237,
    "Magus Castle Ozzie 2": 238,
    "Magus Castle Enemy Elevator": 239,
    "Reptite Lair Secret B2 Ne Right": 240,
    "Lab 32 Race Log": 241,
    "Death Peak South Face Krakker": 243,
    "Death Peak South Face Spawn Save": 244,
    "Death Peak South Face Summit": 245,
    "Death Peak Field": 246,
    "Death Peak Krakker Parade": 247,
    "Death Peak Caves Left": 248,
    "Death Peak Caves Center": 249,
    "Death Peak Caves Right": 250,
    "Reptite Lair Secret B1 Sw": 251,
    "Reptite Lair Secret B1 Ne": (0x15, 0x01),
    "Reptite Lair Secret B1 Se": 253,
    "Reptite Lair Secret B2 Se Right": 254,
    "Reptite Lair Secret B2 Ne Or Se Left": (0x15, 0x08),
    "Reptite Lair Secret B2 Sw": 256,
    "Giants Claw Throne 1": 257,
    "Giants Claw Throne 2": 258,
    "Tyrano Lair Trapdoor": 259,
    "Tyrano Lair Kino Cell": 260,
    "Tyrano Lair Maze 1": 261,
    "Tyrano Lair Maze 2": 262,
    "Tyrano Lair Maze 3": 263,
    "Tyrano Lair Maze 4": 264,
    "Black Omen Aux Command Mid": 265,
    "Black Omen Aux Command Ne": 266,
    "Black Omen Grand Hall": 267,
    "Black Omen Nu Hall Nw": 268,
    "Black Omen Nu Hall W": 269,
    "Black Omen Nu Hall Sw": 270,
    "Black Omen Nu Hall Ne": 271,
    "Black Omen Nu Hall E": 272,
    "Black Omen Nu Hall Se": 273,
    "Black Omen Royal Path": 274,
    "Black Omen Ruminator Parade": 275,
    "Black Omen Eyeball Hall": 276,
    "Black Omen Tubster Fly": 277,
    "Black Omen Martello": 278,
    "Black Omen Alien Sw": 279,
    "Black Omen Alien Ne": 280,
    "Black Omen Alien Nw": 281,
    "Black Omen Terra W": 282,
    "Black Omen Terra Ne": 284,
    "Ocean Palace Main S": 285,
    "Ocean Palace Main N": 286,
    "Ocean Palace E Room": 287,
    "Ocean Palace W Room": 288,
    "Ocean Palace Switch Nw": 289,
    "Ocean Palace Switch Sw": 290,
    "Ocean Palace Switch Ne": 291,
    "Ocean Palace Switch Secret": 292,
    "Ocean Palace Final": 293,
    "Magus Castle Left Hall": 294,
    "Magus Castle Unskippables": 295,
    "Magus Castle Pit E": 296,
    "Magus Castle Pit Ne": 297,
    "Magus Castle Pit Nw": 298,
    "Magus Castle Pit W": 299,
}

# Treasure locations with offset from treasure base addr and a bit flag
_locations_treasure_chests = {
    "Mt Woe 1St Screen": (0x1B, 0x08),
    "Mt Woe 2Nd Screen 1": (0x1A, 0x02),
    "Mt Woe 2Nd Screen 2": (0x1A, 0x04),
    "Mt Woe 2Nd Screen 3": (0x1A, 0x08),
    "Mt Woe 2Nd Screen 4": (0x1A, 0x10),
    "Mt Woe 2Nd Screen 5": (0x1A, 0x20),
    "Mt Woe 3Rd Screen 1": (0x1A, 0x40),
    "Mt Woe 3Rd Screen 2": (0x1A, 0x80),
    "Mt Woe 3Rd Screen 3": (0x1B, 0x01),
    "Mt Woe 3Rd Screen 4": (0x1B, 0x02),
    "Mt Woe 3Rd Screen 5": (0x1B, 0x04),
    "Mt Woe Final 1": (0x1B, 0x10),
    "Mt Woe Final 2": (0x1B, 0x20),
    "Arris Dome Rats": (0x0E, 0x02),
    "Arris Dome Food Store": (0x1A, 0x01),
    "Sewers 1": (0x10, 0x10),
    "Sewers 2": (0x10, 0x20),
    "Sewers 3": (0x10, 0x40),
    "Lab 16 1": (0x0D, 0x20),
    "Lab 16 2": (0x0D, 0x40),
    "Lab 16 3": (0x0D, 0x80),
    "Lab 16 4": (0x0E, 0x01),
    "Lab 32 1": (0x0E, 0x80),
    "Prison Tower 1000": (0x1E, 0x40),
    "Geno Dome 1F 1": (0x11, 0x08),
    "Geno Dome 1F 2": (0x11, 0x10),
    "Geno Dome 1F 3": (0x11, 0x20),
    "Geno Dome 1F 4": (0x11, 0x40),
    "Geno Dome Room 1": (0x11, 0x80),
    "Geno Dome Room 2": (0x12, 0x01),
    "Geno Dome Proto4 1": (0x12, 0x02),
    "Geno Dome Proto4 2": (0x12, 0x04),
    "Geno Dome 2F 1": (0x13, 0x02),
    "Geno Dome 2F 2": (0x13, 0x04),
    "Geno Dome 2F 3": (0x13, 0x08),
    "Geno Dome 2F 4": (0x13, 0x10),
    "Factory Left Aux Console": (0x0F, 0x02),
    "Factory Left Security Right": (0x0F, 0x04),
    "Factory Left Security Left": (0x0F, 0x08),
    "Factory Right Data Core 1": (0x12, 0x08),
    "Factory Right Data Core 2": (0x12, 0x10),
    "Factory Right Floor Top": (0x0F, 0x10),
    "Factory Right Floor Left": (0x0F, 0x20),
    "Factory Right Floor Bottom": (0x0F, 0x40),
    "Factory Right Floor Secret": (0x0F, 0x80),
    "Factory Right Crane Lower": (0x10, 0x02),
    "Factory Right Crane Upper": (0x10, 0x01),
    "Factory Right Info Archive": (0x10, 0x04),
    "Giants Claw Kino Cell": (0x03, 0x02),
    "Giants Claw Traps": (0x03, 0x04),
    "Giants Claw Caves 1": (0x0B, 0x04),
    "Giants Claw Caves 2": (0x0B, 0x08),
    "Giants Claw Caves 3": (0x0B, 0x10),
    "Giants Claw Caves 4": (0x0B, 0x20),
    "Giants Claw Caves 5": (0x0B, 0x80),
    "Guardia Basement 1": (0x00, 0x40),
    "Guardia Basement 2": (0x00, 0x80),
    "Guardia Basement 3": (0x01, 0x01),
    "Guardia Treasury 1": (0x1D, 0x01),
    "Guardia Treasury 2": (0x1D, 0x02),
    "Guardia Treasury 3": (0x1D, 0x04),
    "Ozzies Fort Guillotines 1": (0x0A, 0x10),
    "Ozzies Fort Guillotines 2": (0x0A, 0x20),
    "Ozzies Fort Guillotines 3": (0x0A, 0x40),
    "Ozzies Fort Guillotines 4": (0x0A, 0x80),
    "Ozzies Fort Final 1": (0x0B, 0x01),
    "Ozzies Fort Final 2": (0x0B, 0x02),
    "Truce Mayor 1F": (0x00, 0x04),
    "Truce Mayor 2F": (0x00, 0x08),
    "Forest Ruins": (0x01, 0x04),
    "Porre Mayor 2F": (0x01, 0x80),
    "Truce Canyon 1": (0x03, 0x08),
    "Truce Canyon 2": (0x03, 0x10),
    "Fionas House 1": (0x07, 0x40),
    "Fionas House 2": (0x07, 0x80),
    "Cursed Woods 1": (0x05, 0x01),
    "Cursed Woods 2": (0x05, 0x02),
    "Frogs Burrow Right": (0x05, 0x04),
    "Heckran Cave Sidetrack": (0x01, 0x08),
    "Heckran Cave Entrance": (0x01, 0x10),
    "Heckran Cave 1": (0x01, 0x20),
    "Heckran Cave 2": (0x01, 0x40),
    "Kings Room 1000": (0x00, 0x10),
    "Queens Room 1000": (0x00, 0x20),
    "Kings Room 600": (0x03, 0x20),
    "Queens Room 600": (0x03, 0x40),
    "Royal Kitchen": (0x03, 0x80),
    "Queens Tower 600": (0x1D, 0x08),
    "Kings Tower 600": (0x1E, 0x04),
    "Kings Tower 1000": (0x1E, 0x08),
    "Queens Tower 1000": (0x1E, 0x10),
    "Guardia Court Tower": (0x1E, 0x20),
    "Manoria Cathedral 1": (0x04, 0x02),
    "Manoria Cathedral 2": (0x04, 0x04),
    "Manoria Cathedral 3": (0x04, 0x08),
    "Manoria Interior 1": (0x04, 0x10),
    "Manoria Interior 2": (0x04, 0x20),
    "Manoria Interior 3": (0x04, 0x40),
    "Manoria Interior 4": (0x04, 0x80),
    "Manoria Shrine Sideroom 1": (0x0C, 0x02),
    "Manoria Shrine Sideroom 2": (0x0C, 0x04),
    "Manoria Bromide 1": (0x0C, 0x08),
    "Manoria Bromide 2": (0x0C, 0x10),
    "Manoria Bromide 3": (0x0C, 0x20),
    "Manoria Shrine Magus 1": (0x0C, 0x40),
    "Manoria Shrine Magus 2": (0x0C, 0x80),
    "Yakras Room": (0x0C, 0x01),
    "Denadoro Mts Screen2 1": (0x05, 0x08),
    "Denadoro Mts Screen2 2": (0x05, 0x10),
    "Denadoro Mts Screen2 3": (0x05, 0x20),
    "Denadoro Mts Final 1": (0x05, 0x40),
    "Denadoro Mts Final 2": (0x05, 0x80),
    "Denadoro Mts Final 3": (0x06, 0x01),
    "Denadoro Mts Waterfall Top 1": (0x06, 0x02),
    "Denadoro Mts Waterfall Top 2": (0x06, 0x04),
    "Denadoro Mts Waterfall Top 3": (0x06, 0x08),
    "Denadoro Mts Waterfall Top 4": (0x06, 0x10),
    "Denadoro Mts Waterfall Top 5": (0x06, 0x20),
    "Denadoro Mts Entrance 1": (0x06, 0x40),
    "Denadoro Mts Entrance 2": (0x06, 0x80),
    "Denadoro Mts Screen3 1": (0x07, 0x01),
    "Denadoro Mts Screen3 2": (0x07, 0x02),
    "Denadoro Mts Screen3 3": (0x07, 0x04),
    "Denadoro Mts Screen3 4": (0x07, 0x08),
    "Denadoro Mts Ambush": (0x07, 0x10),
    "Denadoro Mts Save Pt": (0x07, 0x20),
    "Bangor Dome Seal 1": (0x0D, 0x01),
    "Bangor Dome Seal 2": (0x0D, 0x02),
    "Bangor Dome Seal 3": (0x0D, 0x04),
    "Trann Dome Seal 1": (0x0D, 0x08),
    "Trann Dome Seal 2": (0x0D, 0x10),
    "Arris Dome Seal 1": (0x0E, 0x04),
    "Arris Dome Seal 2": (0x0E, 0x08),
    "Arris Dome Seal 3": (0x0E, 0x10),
    "Arris Dome Seal 4": (0x0E, 0x20),
    "Mystic Mt Stream": (0x13, 0x20),
    "Forest Maze 1": (0x13, 0x40),
    "Forest Maze 2": (0x13, 0x80),
    "Forest Maze 3": (0x14, 0x01),
    "Forest Maze 4": (0x14, 0x10),
    "Forest Maze 5": (0x14, 0x04),
    "Forest Maze 6": (0x14, 0x08),
    "Forest Maze 7": (0x14, 0x02),
    "Forest Maze 8": (0x14, 0x20),
    "Forest Maze 9": (0x14, 0x40),  # TODO: Verify this with maze 3 (both rolled Full Tonic)
    "Reptite Lair Reptites 1": (0x15, 0x20),
    "Reptite Lair Reptites 2": (0x15, 0x40),
    "Dactyl Nest 1": (0x15, 0x80),
    "Dactyl Nest 2": (0x16, 0x01),
    "Dactyl Nest 3": (0x16, 0x02),
    "Factory Ruins Generator": (0x10, 0x08),
}

# Maps location names to IDs.  Populated by client init.
_location_name_to_id = {}


class CTJoTSNIClient(SNIClient):
    """
    Game client for Chrono Trigger Jets of Time.
    """

    game = "Chrono Trigger Jets of Time"

    def __init__(self):
        super().__init__()
        import pkgutil
        locations = json.loads(pkgutil.get_data(__name__, "data/location_data.json").decode())
        for key, value in locations.items():
            _location_name_to_id[key] = LOCATION_ID_START + value

    @staticmethod
    def _convert_to_sni_addressing(address: int):
        """
        Convert from SNES address mapping to the SNI address mapping.

        :param address: SNES address to convert to SNI mapping
        :return: SNI address corresponding to this SNES address
        """
        return (address - 0x7E0000) + WRAM_START

    @staticmethod
    def _check_event_location(address: int, flag: int, data: bytes) -> bool:
        """
        Check if an event location has been checked by the runner.

        :param address: Event memory address of this location flag
        :param flag: Bit flag for this specific location
        :param data: Event data block from SNES RAM
        :return: True if the check has been completed, false if not
        """
        offset = address - EVENT_BASE_ADDR
        return (data[offset] & flag) > 0

    @staticmethod
    def _check_treasure_location(offset: int, flag: int, data: bytes) -> bool:
        """
        Check if a treasure chest has been opened by the runner.

        :param offset: Offset into treasure memory
        :param flag: Bit flag for this specific treasure chest
        :param data: Event data block from SNES RAM
        :return: True if the chest has been opened, false if not
        """
        # Adjust offset.  It's based on 0x7F0001 (treasure data start)
        # but the data block starts at 0x7F0000 (event data start)
        return (data[offset + 1] & flag) > 0

    @staticmethod
    def _check_victory_condition(data: bytes) -> bool:
        """
        Check if the player has beaten the game.

        The multiworld code adds a new flag to the ending selector scene to reliably
        verify that the player has beaten the game.  This should work with all  the
        different game modes and endings.

        :param data: Event data to check for victory condition
        :return: True if the player has beaten the game, false if not
        """
        return (data[VICTORY_ADDRESS - EVENT_BASE_ADDR]) & 0x01 > 0

    @classmethod
    async def _deliver_next_item(cls, ctx, items: list[NetworkItem]):
        """
        Check if there are any items to deliver, and if there are, deliver the next one.

        :param ctx: SNIContext used to communicate with the SNES/Emulator
        :param items: List of items that have been found for this player
        """
        from SNIClient import snes_read, snes_buffered_write, snes_flush_writes

        # Check how many items have been delivered so far
        data = await snes_read(ctx, cls._convert_to_sni_addressing(RECEIVED_ITEM_COUNT_ADDR), 1)
        if data is None:
            # Something failed with the read
            return

        num_items_delivered = data[0]
        if len(items) > num_items_delivered:
            item = ctx.items_received[num_items_delivered]

            # Verify the receive slot is empty before sending a new item.
            # Items are awarded via in-game event code.  The event code will
            # zero out the RECEIVE_ITEM_ADDR memory once the item has been awarded.
            data = await snes_read(ctx, cls._convert_to_sni_addressing(RECEIVE_ITEM_ADDR), 1)
            if data is not None and data[0] == 0:

                # Certain event related AP items are not real in game items.  We want to skip those but still
                # update the received counter.  This is currently just a concern for the items representing
                # character pickups.
                in_game_id = item.item - ITEM_ID_START
                if in_game_id <= MAX_IN_GAME_ITEM_ID:
                    snes_buffered_write(
                        ctx,
                        cls._convert_to_sni_addressing(RECEIVE_ITEM_ADDR),
                        bytes([in_game_id]))

                # TODO: Writing this value back manually for now.  Event scripts can only write to a
                #       very limited range of memory, and this value is outside of that range.
                #       Maybe use a custom arbitrary ASM function? Find a different event command?
                snes_buffered_write(
                    ctx,
                    cls._convert_to_sni_addressing(RECEIVED_ITEM_COUNT_ADDR),
                    bytes([num_items_delivered + 1]))
                await snes_flush_writes(ctx)

    async def _track_locations(self, ctx) -> bool:
        """
        Track the locations checked by the player.

        :param ctx: SNIContext for this SNI connection
        """
        from SNIClient import snes_read

        if not ctx.allow_collect or ctx.server is None or ctx.slot is None:
            # We're not fully connected yet, to the server or emulator/hardware
            return False

        # Read the player's in-game location and then do one big read to get all event and treasure flags.
        # NOTE: There is a potential race condition here where the location read happens in a good location
        #       but the event data read occurs in an invalid location for tracking.
        location_data = await snes_read(ctx, LOCATION_ADDRESS, 2)
        event_data = await snes_read(ctx, self._convert_to_sni_addressing(EVENT_BASE_ADDR), EVENT_BLOCK_SIZE)
        if event_data is None:
            return False

        # NOTE: Travelling through a time gate puts the game into a mode 7 scene that overwrites
        # event memory. It always uses a predictable pattern starting at 7F0000, so we can use that
        # to detect when gate travel is occurring and skip item tracking for the duration.
        if event_data[0:4] == b"@ABC":
            return False

        # Check the player's current location and don't track if they are
        # on either the title screen or the load screen.
        # Current location is stored in two bytes starting at 0x7F0100
        map_id = int.from_bytes(location_data, "little")
        if map_id in INVALID_TRACKING_LOCATIONS:
            return False

        # Sanity check to make sure the map actually exists before tracking
        # This can catch an issue where the hardware/emulator fills RAM with invalid values before the game loads
        #
        # This check is a bit naive, since some maps under this value are also invalid, but it should
        # work to stop the but where the game auto-completes on connect
        if map_id >  MAX_MAP_ID:
            return False

        # Normal locations (standard randomizer checks)
        new_locations: list[int] = []
        for name, (address, flag) in _locations_baseline_key_items.items():
            loc_id = _location_name_to_id[name]
            if loc_id not in ctx.checked_locations and loc_id not in new_locations:
                if self._check_event_location(address, flag, event_data):
                    # This location has been checked
                    new_locations.append(loc_id)

        # Treasure chest locations
        for name, (offset, flag) in _locations_treasure_chests.items():
            loc_id = _location_name_to_id[name]
            if loc_id not in ctx.checked_locations and loc_id not in new_locations:
                if self._check_treasure_location(offset, flag, event_data):
                    # This location has been checked
                    new_locations.append(loc_id)

        # Sealed chests and event chest locations
        for name, (address, flag) in _locations_event_treasures.items():
            loc_id = _location_name_to_id[name]
            if loc_id not in ctx.checked_locations and loc_id not in new_locations:
                if self._check_event_location(address, flag, event_data):
                    # This location has been checked
                    new_locations.append(loc_id)

        # Send the list of newly checked locations to the server
        if len(new_locations) > 0:
            await ctx.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])

        # Check to see if the player has beaten the game
        if self._check_victory_condition(event_data):
            if not ctx.finished_game:
                await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                ctx.finished_game = True

        return True

    async def validate_rom(self, ctx) -> bool:
        # Format is: APxyzPlayer_name
        # Where:
        #   AP is a string literal
        #   xyz are a three byte version number
        #   Player_name can be up to 16 characters
        #
        # TODO: Do something with version info
        # TODO: This identifies the player, but not necessarily the AP seed.
        #       Need to expand on this a bit.
        from SNIClient import snes_read
        data = await snes_read(ctx, VALIDATION_ADDR, VALIDATION_SIZE)
        if data is None or data[0:2] != b"AP":
            return False

        name_end = min(data[5:22].find(b'\00'), 16) + 5
        name = data[5:name_end]
        ctx.game = self.game
        # We receive items from other worlds as well as our own world.
        ctx.items_handling = 0b011
        ctx.rom = name
        ctx.allow_collect = True
        return True

    async def game_watcher(self, ctx) -> None:
        # Send newly checked locations to the server.
        tracking_succeeded = await self._track_locations(ctx)

        # Deliver the next item to the player if there are items to give.
        # Don't try to deliver items if something went wrong with tracking.
        if tracking_succeeded:
            await self._deliver_next_item(ctx, ctx.items_received)

    async def deathlink_kill_player(self, ctx) -> None:
        """
        Not implemented for Jets of Time
        """
        pass
