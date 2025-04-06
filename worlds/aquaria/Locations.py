"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage locations in the Aquaria game multiworld randomizer
"""

from BaseClasses import Location


class AquariaLocation(Location):
    """
    A location in the game.
    """
    game: str = "Aquaria"
    """The name of the game"""

    def __init__(self, player: int, name="", code=None, parent=None) -> None:
        """
        Initialisation of the object
        :param player: the ID of the player
        :param name: the name of the location
        :param code: the ID (or address) of the location (Event if None)
        :param parent: the Region that this location belongs to
        """
        super(AquariaLocation, self).__init__(player, name, code, parent)
        self.event = code is None


class AquariaLocationNames:
    """
    Constants used to represent every name of every locations.
    """

    VERSE_CAVE_RIGHT_AREA_BULB_IN_THE_SKELETON_ROOM = "Verse Cave right area, bulb in the skeleton room"
    VERSE_CAVE_RIGHT_AREA_BULB_IN_THE_PATH_RIGHT_OF_THE_SKELETON_ROOM = \
        "Verse Cave right area, bulb in the path right of the skeleton room"
    VERSE_CAVE_RIGHT_AREA_BIG_SEED = "Verse Cave right area, Big Seed"
    VERSE_CAVE_LEFT_AREA_THE_NAIJA_HINT_ABOUT_THE_SHIELD_ABILITY = \
        "Verse Cave left area, the Naija hint about the shield ability"
    VERSE_CAVE_LEFT_AREA_BULB_IN_THE_CENTER_PART = "Verse Cave left area, bulb in the center part"
    VERSE_CAVE_LEFT_AREA_BULB_IN_THE_RIGHT_PART = "Verse Cave left area, bulb in the right part"
    VERSE_CAVE_LEFT_AREA_BULB_UNDER_THE_ROCK_AT_THE_END_OF_THE_PATH = \
        "Verse Cave left area, bulb under the rock at the end of the path"
    HOME_WATERS_BULB_BELOW_THE_GROUPER_FISH = "Home Waters, bulb below the grouper fish"
    HOME_WATERS_BULB_IN_THE_LITTLE_ROOM_ABOVE_THE_GROUPER_FISH = \
        "Home Waters, bulb in the little room above the grouper fish"
    HOME_WATERS_BULB_IN_THE_END_OF_THE_PATH_CLOSE_TO_THE_VERSE_CAVE = \
        "Home Waters, bulb in the end of the path close to the Verse Cave"
    HOME_WATERS_BULB_IN_THE_TOP_LEFT_PATH = "Home Waters, bulb in the top left path"
    HOME_WATERS_BULB_CLOSE_TO_NAIJA_S_HOME = "Home Waters, bulb close to Naija's Home"
    HOME_WATERS_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH_FROM_THE_VERSE_CAVE = \
        "Home Waters, bulb under the rock in the left path from the Verse Cave"
    HOME_WATERS_BULB_IN_THE_PATH_BELOW_NAUTILUS_PRIME = "Home Waters, bulb in the path below Nautilus Prime"
    HOME_WATERS_BULB_IN_THE_BOTTOM_LEFT_ROOM = "Home Waters, bulb in the bottom left room"
    HOME_WATERS_NAUTILUS_EGG = "Home Waters, Nautilus Egg"
    HOME_WATERS_TRANSTURTLE = "Home Waters, Transturtle"
    NAIJA_S_HOME_BULB_AFTER_THE_ENERGY_DOOR = "Naija's Home, bulb after the energy door"
    NAIJA_S_HOME_BULB_UNDER_THE_ROCK_AT_THE_RIGHT_OF_THE_MAIN_PATH = \
        "Naija's Home, bulb under the rock at the right of the main path"
    SONG_CAVE_ERULIAN_SPIRIT = "Song Cave, Erulian spirit"
    SONG_CAVE_BULB_IN_THE_TOP_RIGHT_PART = "Song Cave, bulb in the top right part"
    SONG_CAVE_BULB_IN_THE_BIG_ANEMONE_ROOM = "Song Cave, bulb in the big anemone room"
    SONG_CAVE_BULB_IN_THE_PATH_TO_THE_SINGING_STATUES = "Song Cave, bulb in the path to the singing statues"
    SONG_CAVE_BULB_UNDER_THE_ROCK_IN_THE_PATH_TO_THE_SINGING_STATUES = \
        "Song Cave, bulb under the rock in the path to the singing statues"
    SONG_CAVE_BULB_UNDER_THE_ROCK_CLOSE_TO_THE_SONG_DOOR = "Song Cave, bulb under the rock close to the song door"
    SONG_CAVE_VERSE_EGG = "Song Cave, Verse Egg"
    SONG_CAVE_JELLY_BEACON = "Song Cave, Jelly Beacon"
    SONG_CAVE_ANEMONE_SEED = "Song Cave, Anemone Seed"
    ENERGY_TEMPLE_FIRST_AREA_BEATING_THE_ENERGY_STATUE = "Energy Temple first area, beating the Energy Statue"
    ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK =\
        "Energy Temple first area, bulb in the bottom room blocked by a rock"
    ENERGY_TEMPLE_ENERGY_IDOL = "Energy Temple, Energy Idol"
    ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK = "Energy Temple second area, bulb under the rock"
    ENERGY_TEMPLE_BOTTOM_ENTRANCE_KROTITE_ARMOR = "Energy Temple bottom entrance, Krotite Armor"
    ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH = "Energy Temple third area, bulb in the bottom path"
    ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH = "Energy Temple boss area, Fallen God Tooth"
    ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG = "Energy Temple blaster room, Blaster Egg"
    OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH = \
        "Open Waters top left area, bulb under the rock in the right path"
    OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH = \
        "Open Waters top left area, bulb under the rock in the left path"
    OPEN_WATERS_TOP_LEFT_AREA_BULB_TO_THE_RIGHT_OF_THE_SAVE_CRYSTAL = \
        "Open Waters top left area, bulb to the right of the save crystal"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_SMALL_PATH_BEFORE_MITHALAS = \
        "Open Waters top right area, bulb in the small path before Mithalas"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_PATH_FROM_THE_LEFT_ENTRANCE = \
        "Open Waters top right area, bulb in the path from the left entrance"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_CLEARING_CLOSE_TO_THE_BOTTOM_EXIT = \
        "Open Waters top right area, bulb in the clearing close to the bottom exit"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_CLOSE_TO_THE_SAVE_CRYSTAL = \
        "Open Waters top right area, bulb in the big clearing close to the save crystal"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_TO_THE_TOP_EXIT = \
        "Open Waters top right area, bulb in the big clearing to the top exit"
    OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_TURTLE_ROOM = "Open Waters top right area, bulb in the turtle room"
    OPEN_WATERS_TOP_RIGHT_AREA_TRANSTURTLE = "Open Waters top right area, Transturtle"
    OPEN_WATERS_TOP_RIGHT_AREA_FIRST_URN_IN_THE_MITHALAS_EXIT = \
        "Open Waters top right area, first urn in the Mithalas exit"
    OPEN_WATERS_TOP_RIGHT_AREA_SECOND_URN_IN_THE_MITHALAS_EXIT = \
        "Open Waters top right area, second urn in the Mithalas exit"
    OPEN_WATERS_TOP_RIGHT_AREA_THIRD_URN_IN_THE_MITHALAS_EXIT = \
        "Open Waters top right area, third urn in the Mithalas exit"
    OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_BEHIND_THE_CHOMPER_FISH = \
        "Open Waters bottom left area, bulb behind the chomper fish"
    OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS = \
        "Open Waters bottom left area, bulb inside the lowest fish pass"
    OPEN_WATERS_SKELETON_PATH_BULB_CLOSE_TO_THE_RIGHT_EXIT = "Open Waters skeleton path, bulb close to the right exit"
    OPEN_WATERS_SKELETON_PATH_BULB_BEHIND_THE_CHOMPER_FISH = "Open Waters skeleton path, bulb behind the chomper fish"
    OPEN_WATERS_SKELETON_PATH_KING_SKULL = "Open Waters skeleton path, King Skull"
    ARNASSI_RUINS_BULB_IN_THE_RIGHT_PART = "Arnassi Ruins, bulb in the right part"
    ARNASSI_RUINS_BULB_IN_THE_LEFT_PART = "Arnassi Ruins, bulb in the left part"
    ARNASSI_RUINS_BULB_IN_THE_CENTER_PART = "Arnassi Ruins, bulb in the center part"
    ARNASSI_RUINS_SONG_PLANT_SPORE = "Arnassi Ruins, Song Plant Spore"
    ARNASSI_RUINS_ARNASSI_ARMOR = "Arnassi Ruins, Arnassi Armor"
    ARNASSI_RUINS_ARNASSI_STATUE = "Arnassi Ruins, Arnassi Statue"
    ARNASSI_RUINS_TRANSTURTLE = "Arnassi Ruins, Transturtle"
    ARNASSI_RUINS_CRAB_ARMOR = "Arnassi Ruins, Crab Armor"
    SIMON_SAYS_AREA_BEATING_SIMON_SAYS = "Simon Says area, beating Simon Says"
    SIMON_SAYS_AREA_TRANSTURTLE = "Simon Says area, Transturtle"
    MITHALAS_CITY_FIRST_BULB_IN_THE_LEFT_CITY_PART = "Mithalas City, first bulb in the left city part"
    MITHALAS_CITY_SECOND_BULB_IN_THE_LEFT_CITY_PART = "Mithalas City, second bulb in the left city part"
    MITHALAS_CITY_BULB_IN_THE_RIGHT_PART = "Mithalas City, bulb in the right part"
    MITHALAS_CITY_BULB_AT_THE_TOP_OF_THE_CITY = "Mithalas City, bulb at the top of the city"
    MITHALAS_CITY_FIRST_BULB_IN_A_BROKEN_HOME = "Mithalas City, first bulb in a broken home"
    MITHALAS_CITY_SECOND_BULB_IN_A_BROKEN_HOME = "Mithalas City, second bulb in a broken home"
    MITHALAS_CITY_BULB_IN_THE_BOTTOM_LEFT_PART = "Mithalas City, bulb in the bottom left part"
    MITHALAS_CITY_FIRST_BULB_IN_ONE_OF_THE_HOMES = "Mithalas City, first bulb in one of the homes"
    MITHALAS_CITY_SECOND_BULB_IN_ONE_OF_THE_HOMES = "Mithalas City, second bulb in one of the homes"
    MITHALAS_CITY_FIRST_URN_IN_ONE_OF_THE_HOMES = "Mithalas City, first urn in one of the homes"
    MITHALAS_CITY_SECOND_URN_IN_ONE_OF_THE_HOMES = "Mithalas City, second urn in one of the homes"
    MITHALAS_CITY_FIRST_URN_IN_THE_CITY_RESERVE = "Mithalas City, first urn in the city reserve"
    MITHALAS_CITY_SECOND_URN_IN_THE_CITY_RESERVE = "Mithalas City, second urn in the city reserve"
    MITHALAS_CITY_THIRD_URN_IN_THE_CITY_RESERVE = "Mithalas City, third urn in the city reserve"
    MITHALAS_CITY_FIRST_BULB_AT_THE_END_OF_THE_TOP_PATH = "Mithalas City, first bulb at the end of the top path"
    MITHALAS_CITY_SECOND_BULB_AT_THE_END_OF_THE_TOP_PATH = "Mithalas City, second bulb at the end of the top path"
    MITHALAS_CITY_BULB_IN_THE_TOP_PATH = "Mithalas City, bulb in the top path"
    MITHALAS_CITY_MITHALAS_POT = "Mithalas City, Mithalas Pot"
    MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE = "Mithalas City, urn in the Castle flower tube entrance"
    MITHALAS_CITY_DOLL = "Mithalas City, Doll"
    MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS = "Mithalas City, urn inside a home fish pass"
    MITHALAS_CITY_CASTLE_BULB_IN_THE_FLESH_HOLE = "Mithalas City Castle, bulb in the flesh hole"
    MITHALAS_CITY_CASTLE_BLUE_BANNER = "Mithalas City Castle, Blue Banner"
    MITHALAS_CITY_CASTLE_URN_IN_THE_BEDROOM = "Mithalas City Castle, urn in the bedroom"
    MITHALAS_CITY_CASTLE_FIRST_URN_OF_THE_SINGLE_LAMP_PATH = "Mithalas City Castle, first urn of the single lamp path"
    MITHALAS_CITY_CASTLE_SECOND_URN_OF_THE_SINGLE_LAMP_PATH = "Mithalas City Castle, second urn of the single lamp path"
    MITHALAS_CITY_CASTLE_URN_IN_THE_BOTTOM_ROOM = "Mithalas City Castle, urn in the bottom room"
    MITHALAS_CITY_CASTLE_FIRST_URN_ON_THE_ENTRANCE_PATH = "Mithalas City Castle, first urn on the entrance path"
    MITHALAS_CITY_CASTLE_SECOND_URN_ON_THE_ENTRANCE_PATH = "Mithalas City Castle, second urn on the entrance path"
    MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS = "Mithalas City Castle, beating the Priests"
    MITHALAS_CITY_CASTLE_TRIDENT_HEAD = "Mithalas City Castle, Trident Head"
    MITHALAS_CATHEDRAL_BULB_IN_THE_FLESH_ROOM_WITH_FLEAS = "Mithalas Cathedral, bulb in the flesh room with fleas"
    MITHALAS_CATHEDRAL_MITHALAN_DRESS = "Mithalas Cathedral, Mithalan Dress"
    MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_TOP_RIGHT_ROOM = "Mithalas Cathedral, first urn in the top right room"
    MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_TOP_RIGHT_ROOM = "Mithalas Cathedral, second urn in the top right room"
    MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_TOP_RIGHT_ROOM = "Mithalas Cathedral, third urn in the top right room"
    MITHALAS_CATHEDRAL_URN_BEHIND_THE_FLESH_VEIN = "Mithalas Cathedral, urn behind the flesh vein"
    MITHALAS_CATHEDRAL_URN_IN_THE_TOP_LEFT_EYES_BOSS_ROOM = "Mithalas Cathedral, urn in the top left eyes boss room"
    MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN =\
        "Mithalas Cathedral, first urn in the path behind the flesh vein"
    MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN =\
        "Mithalas Cathedral, second urn in the path behind the flesh vein"
    MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN =\
        "Mithalas Cathedral, third urn in the path behind the flesh vein"
    MITHALAS_CATHEDRAL_FOURTH_URN_IN_THE_TOP_RIGHT_ROOM = "Mithalas Cathedral, fourth urn in the top right room"
    MITHALAS_CATHEDRAL_URN_BELOW_THE_LEFT_ENTRANCE = "Mithalas Cathedral, urn below the left entrance"
    MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_BOTTOM_RIGHT_PATH = "Mithalas Cathedral, first urn in the bottom right path"
    MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_BOTTOM_RIGHT_PATH = "Mithalas Cathedral, second urn in the bottom right path"
    CATHEDRAL_UNDERGROUND_BULB_IN_THE_CENTER_PART = "Cathedral Underground, bulb in the center part"
    CATHEDRAL_UNDERGROUND_FIRST_BULB_IN_THE_TOP_LEFT_PART = "Cathedral Underground, first bulb in the top left part"
    CATHEDRAL_UNDERGROUND_SECOND_BULB_IN_THE_TOP_LEFT_PART = "Cathedral Underground, second bulb in the top left part"
    CATHEDRAL_UNDERGROUND_THIRD_BULB_IN_THE_TOP_LEFT_PART = "Cathedral Underground, third bulb in the top left part"
    CATHEDRAL_UNDERGROUND_BULB_CLOSE_TO_THE_SAVE_CRYSTAL = "Cathedral Underground, bulb close to the save crystal"
    CATHEDRAL_UNDERGROUND_BULB_IN_THE_BOTTOM_RIGHT_PATH = "Cathedral Underground, bulb in the bottom right path"
    MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD = "Mithalas boss area, beating Mithalan God"
    KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_BOTTOM_LEFT_CLEARING =\
        "Kelp Forest top left area, bulb in the bottom left clearing"
    KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_PATH_DOWN_FROM_THE_TOP_LEFT_CLEARING =\
        "Kelp Forest top left area, bulb in the path down from the top left clearing"
    KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_TOP_LEFT_CLEARING = "Kelp Forest top left area, bulb in the top left clearing"
    KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG = "Kelp Forest top left area, Jelly Egg"
    KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG = "Kelp Forest top left area, bulb close to the Verse Egg"
    KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG = "Kelp Forest top left area, Verse Egg"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH =\
        "Kelp Forest top right area, bulb under the rock in the right path"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_LEFT_OF_THE_CENTER_CLEARING =\
        "Kelp Forest top right area, bulb at the left of the center clearing"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_BIG_ROOM =\
        "Kelp Forest top right area, bulb in the left path's big room"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_SMALL_ROOM =\
        "Kelp Forest top right area, bulb in the left path's small room"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_CENTER_CLEARING =\
        "Kelp Forest top right area, bulb at the top of the center clearing"
    KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL = "Kelp Forest top right area, Black Pearl"
    KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS = "Kelp Forest top right area, bulb in the top fish pass"
    KELP_FOREST_BOTTOM_LEFT_AREA_TRANSTURTLE = "Kelp Forest bottom left area, Transturtle"
    KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS =\
        "Kelp Forest bottom left area, bulb close to the spirit crystals"
    KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY = "Kelp Forest bottom left area, Walker Baby"
    KELP_FOREST_BOTTOM_LEFT_AREA_FISH_CAVE_PUZZLE = "Kelp Forest bottom left area, Fish Cave puzzle"
    KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER = "Kelp Forest bottom right area, Odd Container"
    KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD = "Kelp Forest boss area, beating Drunian God"
    KELP_FOREST_BOSS_ROOM_BULB_AT_THE_BOTTOM_OF_THE_AREA = "Kelp Forest boss room, bulb at the bottom of the area"
    KELP_FOREST_SPRITE_CAVE_BULB_INSIDE_THE_FISH_PASS = "Kelp Forest sprite cave, bulb inside the fish pass"
    KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM = "Kelp Forest sprite cave, bulb in the second room"
    KELP_FOREST_SPRITE_CAVE_SEED_BAG = "Kelp Forest sprite cave, Seed Bag"
    MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE = "Mermog cave, bulb in the left part of the cave"
    MERMOG_CAVE_PIRANHA_EGG = "Mermog cave, Piranha Egg"
    THE_VEIL_TOP_LEFT_AREA_IN_LI_S_CAVE = "The Veil top left area, In Li's cave"
    THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH =\
        "The Veil top left area, bulb under the rock in the top right path"
    THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK =\
        "The Veil top left area, bulb hidden behind the blocking rock"
    THE_VEIL_TOP_LEFT_AREA_TRANSTURTLE = "The Veil top left area, Transturtle"
    THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS = "The Veil top left area, bulb inside the fish pass"
    TURTLE_CAVE_TURTLE_EGG = "Turtle cave, Turtle Egg"
    TURTLE_CAVE_BULB_IN_BUBBLE_CLIFF = "Turtle cave, bulb in Bubble Cliff"
    TURTLE_CAVE_URCHIN_COSTUME = "Turtle cave, Urchin Costume"
    THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF = \
        "The Veil top right area, bulb in the middle of the wall jump cliff"
    THE_VEIL_TOP_RIGHT_AREA_GOLDEN_STARFISH = "The Veil top right area, Golden Starfish"
    THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL = \
        "The Veil top right area, bulb at the top of the waterfall"
    THE_VEIL_TOP_RIGHT_AREA_TRANSTURTLE = "The Veil top right area, Transturtle"
    THE_VEIL_BOTTOM_AREA_BULB_IN_THE_LEFT_PATH = "The Veil bottom area, bulb in the left path"
    THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH = "The Veil bottom area, bulb in the spirit path"
    THE_VEIL_BOTTOM_AREA_VERSE_EGG = "The Veil bottom area, Verse Egg"
    THE_VEIL_BOTTOM_AREA_STONE_HEAD = "The Veil bottom area, Stone Head"
    OCTOPUS_CAVE_DUMBO_EGG = "Octopus Cave, Dumbo Egg"
    OCTOPUS_CAVE_BULB_IN_THE_PATH_BELOW_THE_OCTOPUS_CAVE_PATH =\
        "Octopus Cave, bulb in the path below the Octopus Cave path"
    SUN_TEMPLE_BULB_IN_THE_TOP_LEFT_PART = "Sun Temple, bulb in the top left part"
    SUN_TEMPLE_BULB_IN_THE_TOP_RIGHT_PART = "Sun Temple, bulb in the top right part"
    SUN_TEMPLE_BULB_AT_THE_TOP_OF_THE_HIGH_DARK_ROOM = "Sun Temple, bulb at the top of the high dark room"
    SUN_TEMPLE_GOLDEN_GEAR = "Sun Temple, Golden Gear"
    SUN_TEMPLE_FIRST_BULB_OF_THE_TEMPLE = "Sun Temple, first bulb of the temple"
    SUN_TEMPLE_BULB_ON_THE_RIGHT_PART = "Sun Temple, bulb on the right part"
    SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART = "Sun Temple, bulb in the hidden room of the right part"
    SUN_TEMPLE_SUN_KEY = "Sun Temple, Sun Key"
    SUN_TEMPLE_BOSS_PATH_FIRST_PATH_BULB = "Sun Temple boss path, first path bulb"
    SUN_TEMPLE_BOSS_PATH_SECOND_PATH_BULB = "Sun Temple boss path, second path bulb"
    SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB = "Sun Temple boss path, first cliff bulb"
    SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB = "Sun Temple boss path, second cliff bulb"
    SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD = "Sun Temple boss area, beating Lumerean God"
    ABYSS_LEFT_AREA_BULB_IN_HIDDEN_PATH_ROOM = "Abyss left area, bulb in hidden path room"
    ABYSS_LEFT_AREA_BULB_IN_THE_RIGHT_PART = "Abyss left area, bulb in the right part"
    ABYSS_LEFT_AREA_GLOWING_SEED = "Abyss left area, Glowing Seed"
    ABYSS_LEFT_AREA_GLOWING_PLANT = "Abyss left area, Glowing Plant"
    ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS = "Abyss left area, bulb in the bottom fish pass"
    ABYSS_RIGHT_AREA_BULB_IN_THE_MIDDLE_PATH = "Abyss right area, bulb in the middle path"
    ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_MIDDLE_PATH =\
        "Abyss right area, bulb behind the rock in the middle path"
    ABYSS_RIGHT_AREA_BULB_IN_THE_LEFT_GREEN_ROOM = "Abyss right area, bulb in the left green room"
    ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM = "Abyss right area, bulb behind the rock in the whale room"
    ABYSS_RIGHT_AREA_TRANSTURTLE = "Abyss right area, Transturtle"
    ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT = "Ice Cavern, bulb in the room to the right"
    ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM = "Ice Cavern, first bulb in the top exit room"
    ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM = "Ice Cavern, second bulb in the top exit room"
    ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM = "Ice Cavern, third bulb in the top exit room"
    ICE_CAVERN_BULB_IN_THE_LEFT_ROOM = "Ice Cavern, bulb in the left room"
    BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL = "Bubble Cave, bulb in the left cave wall"
    BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL =\
        "Bubble Cave, bulb in the right cave wall (behind the ice crystal)"
    BUBBLE_CAVE_VERSE_EGG = "Bubble Cave, Verse Egg"
    KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY =\
        "King Jellyfish Cave, bulb in the right path from King Jelly"
    KING_JELLYFISH_CAVE_JELLYFISH_COSTUME = "King Jellyfish Cave, Jellyfish Costume"
    THE_WHALE_VERSE_EGG = "The Whale, Verse Egg"
    SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL = "Sunken City right area, crate close to the save crystal"
    SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM = "Sunken City right area, crate in the left bottom room"
    SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM = "Sunken City left area, crate in the little pipe room"
    SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL = "Sunken City left area, crate close to the save crystal"
    SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM = "Sunken City left area, crate before the bedroom"
    SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME = "Sunken City left area, Girl Costume"
    SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA = "Sunken City, bulb on top of the boss area"
    THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE = "The Body center area, breaking Li's cage"
    THE_BODY_CENTER_AREA_BULB_ON_THE_MAIN_PATH_BLOCKING_TUBE = \
        "The Body center area, bulb on the main path blocking tube"
    THE_BODY_LEFT_AREA_FIRST_BULB_IN_THE_TOP_FACE_ROOM = "The Body left area, first bulb in the top face room"
    THE_BODY_LEFT_AREA_SECOND_BULB_IN_THE_TOP_FACE_ROOM = "The Body left area, second bulb in the top face room"
    THE_BODY_LEFT_AREA_BULB_BELOW_THE_WATER_STREAM = "The Body left area, bulb below the water stream"
    THE_BODY_LEFT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_TOP_FACE_ROOM = \
        "The Body left area, bulb in the top path to the top face room"
    THE_BODY_LEFT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM = "The Body left area, bulb in the bottom face room"
    THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_FACE_ROOM = "The Body right area, bulb in the top face room"
    THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_BOTTOM_FACE_ROOM = \
        "The Body right area, bulb in the top path to the bottom face room"
    THE_BODY_RIGHT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM = "The Body right area, bulb in the bottom face room"
    THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM = "The Body bottom area, bulb in the Jelly Zap room"
    THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM = "The Body bottom area, bulb in the nautilus room"
    THE_BODY_BOTTOM_AREA_MUTANT_COSTUME = "The Body bottom area, Mutant Costume"
    FINAL_BOSS_AREA_FIRST_BULB_IN_THE_TURTLE_ROOM = "Final Boss area, first bulb in the turtle room"
    FINAL_BOSS_AREA_SECOND_BULB_IN_THE_TURTLE_ROOM = "Final Boss area, second bulb in the turtle room"
    FINAL_BOSS_AREA_THIRD_BULB_IN_THE_TURTLE_ROOM = "Final Boss area, third bulb in the turtle room"
    FINAL_BOSS_AREA_TRANSTURTLE = "Final Boss area, Transturtle"
    FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM = "Final Boss area, bulb in the boss third form room"
    BEATING_FALLEN_GOD = "Beating Fallen God"
    BEATING_MITHALAN_GOD = "Beating Mithalan God"
    BEATING_DRUNIAN_GOD = "Beating Drunian God"
    BEATING_LUMEREAN_GOD = "Beating Lumerean God"
    BEATING_THE_GOLEM = "Beating the Golem"
    BEATING_NAUTILUS_PRIME = "Beating Nautilus Prime"
    BEATING_BLASTER_PEG_PRIME = "Beating Blaster Peg Prime"
    BEATING_MERGOG = "Beating Mergog"
    BEATING_MITHALAN_PRIESTS = "Beating Mithalan priests"
    BEATING_OCTOPUS_PRIME = "Beating Octopus Prime"
    BEATING_CRABBIUS_MAXIMUS = "Beating Crabbius Maximus"
    BEATING_MANTIS_SHRIMP_PRIME = "Beating Mantis Shrimp Prime"
    BEATING_KING_JELLYFISH_GOD_PRIME = "Beating King Jellyfish God Prime"
    FIRST_SECRET = "First Secret"
    SECOND_SECRET = "Second Secret"
    THIRD_SECRET = "Third Secret"
    SUNKEN_CITY_CLEARED = "Sunken City cleared"
    SUN_CRYSTAL = "Sun Crystal"
    OBJECTIVE_COMPLETE = "Objective complete"


class AquariaLocations:
    locations_verse_cave_r = {
        AquariaLocationNames.VERSE_CAVE_RIGHT_AREA_BULB_IN_THE_SKELETON_ROOM: 698107,
        AquariaLocationNames.VERSE_CAVE_RIGHT_AREA_BULB_IN_THE_PATH_RIGHT_OF_THE_SKELETON_ROOM: 698108,
        AquariaLocationNames.VERSE_CAVE_RIGHT_AREA_BIG_SEED: 698175,
    }

    locations_verse_cave_l = {
        AquariaLocationNames.VERSE_CAVE_LEFT_AREA_THE_NAIJA_HINT_ABOUT_THE_SHIELD_ABILITY: 698200,
        AquariaLocationNames.VERSE_CAVE_LEFT_AREA_BULB_IN_THE_CENTER_PART: 698021,
        AquariaLocationNames.VERSE_CAVE_LEFT_AREA_BULB_IN_THE_RIGHT_PART: 698022,
        AquariaLocationNames.VERSE_CAVE_LEFT_AREA_BULB_UNDER_THE_ROCK_AT_THE_END_OF_THE_PATH: 698023,
    }

    locations_home_water = {
        AquariaLocationNames.HOME_WATERS_BULB_BELOW_THE_GROUPER_FISH: 698058,
        AquariaLocationNames.HOME_WATERS_BULB_IN_THE_LITTLE_ROOM_ABOVE_THE_GROUPER_FISH: 698060,
        AquariaLocationNames.HOME_WATERS_BULB_IN_THE_END_OF_THE_PATH_CLOSE_TO_THE_VERSE_CAVE: 698061,
        AquariaLocationNames.HOME_WATERS_BULB_IN_THE_TOP_LEFT_PATH: 698062,
        AquariaLocationNames.HOME_WATERS_BULB_CLOSE_TO_NAIJA_S_HOME: 698064,
        AquariaLocationNames.HOME_WATERS_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH_FROM_THE_VERSE_CAVE: 698065,
    }

    locations_home_water_behind_rocks = {
        AquariaLocationNames.HOME_WATERS_BULB_IN_THE_PATH_BELOW_NAUTILUS_PRIME: 698059,
        AquariaLocationNames.HOME_WATERS_BULB_IN_THE_BOTTOM_LEFT_ROOM: 698063,
    }

    locations_home_water_nautilus = {
        AquariaLocationNames.HOME_WATERS_NAUTILUS_EGG: 698194,
    }

    locations_home_water_transturtle = {
        AquariaLocationNames.HOME_WATERS_TRANSTURTLE: 698213,
    }

    locations_naija_home = {
        AquariaLocationNames.NAIJA_S_HOME_BULB_AFTER_THE_ENERGY_DOOR: 698119,
        AquariaLocationNames.NAIJA_S_HOME_BULB_UNDER_THE_ROCK_AT_THE_RIGHT_OF_THE_MAIN_PATH: 698120,
    }

    locations_song_cave = {
        AquariaLocationNames.SONG_CAVE_ERULIAN_SPIRIT: 698206,
        AquariaLocationNames.SONG_CAVE_BULB_IN_THE_TOP_RIGHT_PART: 698071,
        AquariaLocationNames.SONG_CAVE_BULB_IN_THE_BIG_ANEMONE_ROOM: 698072,
        AquariaLocationNames.SONG_CAVE_BULB_IN_THE_PATH_TO_THE_SINGING_STATUES: 698073,
        AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_IN_THE_PATH_TO_THE_SINGING_STATUES: 698074,
        AquariaLocationNames.SONG_CAVE_BULB_UNDER_THE_ROCK_CLOSE_TO_THE_SONG_DOOR: 698075,
        AquariaLocationNames.SONG_CAVE_VERSE_EGG: 698160,
        AquariaLocationNames.SONG_CAVE_JELLY_BEACON: 698178,
        AquariaLocationNames.SONG_CAVE_ANEMONE_SEED: 698162,
    }

    locations_energy_temple_1 = {
        AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BEATING_THE_ENERGY_STATUE: 698205,
        AquariaLocationNames.ENERGY_TEMPLE_FIRST_AREA_BULB_IN_THE_BOTTOM_ROOM_BLOCKED_BY_A_ROCK: 698027,
    }

    locations_energy_temple_idol = {
        AquariaLocationNames.ENERGY_TEMPLE_ENERGY_IDOL: 698170,
    }

    locations_energy_temple_2 = {
        AquariaLocationNames.ENERGY_TEMPLE_SECOND_AREA_BULB_UNDER_THE_ROCK: 698028,
        # This can be accessible via locations_energy_temple_altar too
    }

    locations_energy_temple_altar = {
        AquariaLocationNames.ENERGY_TEMPLE_BOTTOM_ENTRANCE_KROTITE_ARMOR: 698163,
    }

    locations_energy_temple_3 = {
        AquariaLocationNames.ENERGY_TEMPLE_THIRD_AREA_BULB_IN_THE_BOTTOM_PATH: 698029,
    }

    locations_energy_temple_boss = {
        AquariaLocationNames.ENERGY_TEMPLE_BOSS_AREA_FALLEN_GOD_TOOTH: 698169,
    }

    locations_energy_temple_blaster_room = {
        AquariaLocationNames.ENERGY_TEMPLE_BLASTER_ROOM_BLASTER_EGG: 698195,
    }

    locations_openwater_tl = {
        AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH: 698001,
        AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_LEFT_PATH: 698002,
        AquariaLocationNames.OPEN_WATERS_TOP_LEFT_AREA_BULB_TO_THE_RIGHT_OF_THE_SAVE_CRYSTAL: 698003,
    }

    locations_openwater_tr = {
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_SMALL_PATH_BEFORE_MITHALAS: 698004,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_PATH_FROM_THE_LEFT_ENTRANCE: 698005,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_CLEARING_CLOSE_TO_THE_BOTTOM_EXIT: 698006,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_CLOSE_TO_THE_SAVE_CRYSTAL: 698007,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_BIG_CLEARING_TO_THE_TOP_EXIT: 698008,
    }

    locations_openwater_tr_turtle = {
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_BULB_IN_THE_TURTLE_ROOM: 698009,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_TRANSTURTLE: 698211,
    }

    locations_openwater_tr_urns = {
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_FIRST_URN_IN_THE_MITHALAS_EXIT: 698148,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_SECOND_URN_IN_THE_MITHALAS_EXIT: 698149,
        AquariaLocationNames.OPEN_WATERS_TOP_RIGHT_AREA_THIRD_URN_IN_THE_MITHALAS_EXIT: 698150,
    }

    locations_openwater_bl = {
        AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_BEHIND_THE_CHOMPER_FISH: 698011,
        AquariaLocationNames.OPEN_WATERS_BOTTOM_LEFT_AREA_BULB_INSIDE_THE_LOWEST_FISH_PASS: 698010,
    }

    locations_skeleton_path = {
        AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_BULB_CLOSE_TO_THE_RIGHT_EXIT: 698012,
        AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_BULB_BEHIND_THE_CHOMPER_FISH: 698013,
    }

    locations_skeleton_path_sc = {
        AquariaLocationNames.OPEN_WATERS_SKELETON_PATH_KING_SKULL: 698177,
    }

    locations_arnassi = {
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_RIGHT_PART: 698014,
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_LEFT_PART: 698015,
        AquariaLocationNames.ARNASSI_RUINS_BULB_IN_THE_CENTER_PART: 698016,
        AquariaLocationNames.ARNASSI_RUINS_SONG_PLANT_SPORE: 698179,
        AquariaLocationNames.ARNASSI_RUINS_ARNASSI_ARMOR: 698191,
    }

    locations_arnassi_cave = {
        AquariaLocationNames.ARNASSI_RUINS_ARNASSI_STATUE: 698164,
    }

    locations_arnassi_cave_transturtle = {
        AquariaLocationNames.ARNASSI_RUINS_TRANSTURTLE: 698217,
    }

    locations_arnassi_crab_boss = {
        AquariaLocationNames.ARNASSI_RUINS_CRAB_ARMOR: 698187,
    }

    locations_simon = {
        AquariaLocationNames.SIMON_SAYS_AREA_BEATING_SIMON_SAYS: 698156,
        AquariaLocationNames.SIMON_SAYS_AREA_TRANSTURTLE: 698216,
    }

    locations_mithalas_city = {
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_THE_LEFT_CITY_PART: 698030,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_THE_LEFT_CITY_PART: 698035,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_RIGHT_PART: 698031,
        AquariaLocationNames.MITHALAS_CITY_BULB_AT_THE_TOP_OF_THE_CITY: 698033,
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_A_BROKEN_HOME: 698034,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_A_BROKEN_HOME: 698041,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_BOTTOM_LEFT_PART: 698037,
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_IN_ONE_OF_THE_HOMES: 698038,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_IN_ONE_OF_THE_HOMES: 698039,
    }

    locations_mithalas_city_urns = {
        AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_ONE_OF_THE_HOMES: 698123,
        AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_ONE_OF_THE_HOMES: 698124,
        AquariaLocationNames.MITHALAS_CITY_FIRST_URN_IN_THE_CITY_RESERVE: 698125,
        AquariaLocationNames.MITHALAS_CITY_SECOND_URN_IN_THE_CITY_RESERVE: 698126,
        AquariaLocationNames.MITHALAS_CITY_THIRD_URN_IN_THE_CITY_RESERVE: 698127,
    }

    locations_mithalas_city_top_path = {
        AquariaLocationNames.MITHALAS_CITY_FIRST_BULB_AT_THE_END_OF_THE_TOP_PATH: 698032,
        AquariaLocationNames.MITHALAS_CITY_SECOND_BULB_AT_THE_END_OF_THE_TOP_PATH: 698040,
        AquariaLocationNames.MITHALAS_CITY_BULB_IN_THE_TOP_PATH: 698036,
        AquariaLocationNames.MITHALAS_CITY_MITHALAS_POT: 698174,
        AquariaLocationNames.MITHALAS_CITY_URN_IN_THE_CASTLE_FLOWER_TUBE_ENTRANCE: 698128,
    }

    locations_mithalas_city_fishpass = {
        AquariaLocationNames.MITHALAS_CITY_DOLL: 698173,
        AquariaLocationNames.MITHALAS_CITY_URN_INSIDE_A_HOME_FISH_PASS: 698129,
    }

    locations_mithalas_castle = {
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BULB_IN_THE_FLESH_HOLE: 698042,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BLUE_BANNER: 698165,
    }

    locations_mithalas_castle_urns = {
        AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BEDROOM: 698130,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_OF_THE_SINGLE_LAMP_PATH: 698131,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_OF_THE_SINGLE_LAMP_PATH: 698132,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_URN_IN_THE_BOTTOM_ROOM: 698133,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_FIRST_URN_ON_THE_ENTRANCE_PATH: 698134,
        AquariaLocationNames.MITHALAS_CITY_CASTLE_SECOND_URN_ON_THE_ENTRANCE_PATH: 698135,
    }

    locations_mithalas_castle_tube = {
        AquariaLocationNames.MITHALAS_CITY_CASTLE_BEATING_THE_PRIESTS: 698208,
    }

    locations_mithalas_castle_sc = {
        AquariaLocationNames.MITHALAS_CITY_CASTLE_TRIDENT_HEAD: 698183,
    }

    locations_cathedral_top_start = {
        AquariaLocationNames.MITHALAS_CATHEDRAL_BULB_IN_THE_FLESH_ROOM_WITH_FLEAS: 698139,
        AquariaLocationNames.MITHALAS_CATHEDRAL_MITHALAN_DRESS: 698189,
    }

    locations_cathedral_top_start_urns = {
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_TOP_RIGHT_ROOM: 698136,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_TOP_RIGHT_ROOM: 698137,
        AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_TOP_RIGHT_ROOM: 698138,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BEHIND_THE_FLESH_VEIN: 698142,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_IN_THE_TOP_LEFT_EYES_BOSS_ROOM: 698143,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN: 698144,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN: 698145,
        AquariaLocationNames.MITHALAS_CATHEDRAL_THIRD_URN_IN_THE_PATH_BEHIND_THE_FLESH_VEIN: 698146,
        AquariaLocationNames.MITHALAS_CATHEDRAL_FOURTH_URN_IN_THE_TOP_RIGHT_ROOM: 698147,
        AquariaLocationNames.MITHALAS_CATHEDRAL_URN_BELOW_THE_LEFT_ENTRANCE: 698198,
    }

    locations_cathedral_top_end = {
        AquariaLocationNames.MITHALAS_CATHEDRAL_FIRST_URN_IN_THE_BOTTOM_RIGHT_PATH: 698140,
        AquariaLocationNames.MITHALAS_CATHEDRAL_SECOND_URN_IN_THE_BOTTOM_RIGHT_PATH: 698141,
    }

    locations_cathedral_underground = {
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_CENTER_PART: 698113,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_FIRST_BULB_IN_THE_TOP_LEFT_PART: 698114,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_SECOND_BULB_IN_THE_TOP_LEFT_PART: 698115,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_THIRD_BULB_IN_THE_TOP_LEFT_PART: 698116,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_CLOSE_TO_THE_SAVE_CRYSTAL: 698117,
        AquariaLocationNames.CATHEDRAL_UNDERGROUND_BULB_IN_THE_BOTTOM_RIGHT_PATH: 698118,
    }

    locations_cathedral_boss = {
        AquariaLocationNames.MITHALAS_BOSS_AREA_BEATING_MITHALAN_GOD: 698202,
    }

    locations_forest_tl = {
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_BOTTOM_LEFT_CLEARING: 698044,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_PATH_DOWN_FROM_THE_TOP_LEFT_CLEARING: 698045,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_IN_THE_TOP_LEFT_CLEARING: 698046,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_JELLY_EGG: 698185,
    }

    locations_forest_tl_verse_egg_room = {
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_BULB_CLOSE_TO_THE_VERSE_EGG: 698047,
        AquariaLocationNames.KELP_FOREST_TOP_LEFT_AREA_VERSE_EGG: 698158,
    }

    locations_forest_tr = {
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_UNDER_THE_ROCK_IN_THE_RIGHT_PATH: 698048,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_LEFT_OF_THE_CENTER_CLEARING: 698049,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_BIG_ROOM: 698051,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_LEFT_PATH_S_SMALL_ROOM: 698052,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_CENTER_CLEARING: 698053,
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BLACK_PEARL: 698167,
    }

    locations_forest_tr_fp = {
        AquariaLocationNames.KELP_FOREST_TOP_RIGHT_AREA_BULB_IN_THE_TOP_FISH_PASS: 698050,
    }

    locations_forest_bl = {
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_TRANSTURTLE: 698212,
    }

    locations_forest_bl_sc = {
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_BULB_CLOSE_TO_THE_SPIRIT_CRYSTALS: 698054,
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_WALKER_BABY: 698186,
    }

    locations_forest_fish_cave = {
        AquariaLocationNames.KELP_FOREST_BOTTOM_LEFT_AREA_FISH_CAVE_PUZZLE: 698207,
    }

    locations_forest_br = {
        AquariaLocationNames.KELP_FOREST_BOTTOM_RIGHT_AREA_ODD_CONTAINER: 698168,
    }

    locations_forest_boss = {
        AquariaLocationNames.KELP_FOREST_BOSS_AREA_BEATING_DRUNIAN_GOD: 698204,
    }

    locations_forest_boss_entrance = {
        AquariaLocationNames.KELP_FOREST_BOSS_ROOM_BULB_AT_THE_BOTTOM_OF_THE_AREA: 698055,
    }

    locations_sprite_cave = {
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_INSIDE_THE_FISH_PASS: 698056,
    }

    locations_sprite_cave_tube = {
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_BULB_IN_THE_SECOND_ROOM: 698057,
        AquariaLocationNames.KELP_FOREST_SPRITE_CAVE_SEED_BAG: 698176,
    }

    locations_mermog_cave = {
        AquariaLocationNames.MERMOG_CAVE_BULB_IN_THE_LEFT_PART_OF_THE_CAVE: 698121,
    }

    locations_mermog_boss = {
        AquariaLocationNames.MERMOG_CAVE_PIRANHA_EGG: 698197,
    }

    locations_veil_tl = {
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_IN_LI_S_CAVE: 698199,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_UNDER_THE_ROCK_IN_THE_TOP_RIGHT_PATH: 698078,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_HIDDEN_BEHIND_THE_BLOCKING_ROCK: 698076,
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_TRANSTURTLE: 698209,
    }

    locations_veil_tl_fp = {
        AquariaLocationNames.THE_VEIL_TOP_LEFT_AREA_BULB_INSIDE_THE_FISH_PASS: 698077,
    }

    locations_turtle_cave = {
        AquariaLocationNames.TURTLE_CAVE_TURTLE_EGG: 698184,
    }

    locations_turtle_cave_bubble = {
        AquariaLocationNames.TURTLE_CAVE_BULB_IN_BUBBLE_CLIFF: 698000,
        AquariaLocationNames.TURTLE_CAVE_URCHIN_COSTUME: 698193,
    }

    locations_veil_tr_r = {
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_IN_THE_MIDDLE_OF_THE_WALL_JUMP_CLIFF: 698079,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_GOLDEN_STARFISH: 698180,
    }

    locations_veil_tr_l = {
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_BULB_AT_THE_TOP_OF_THE_WATERFALL: 698080,
        AquariaLocationNames.THE_VEIL_TOP_RIGHT_AREA_TRANSTURTLE: 698210,
    }

    locations_veil_b = {
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_LEFT_PATH: 698082,
    }

    locations_veil_b_sc = {
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_BULB_IN_THE_SPIRIT_PATH: 698081,
    }

    locations_veil_b_fp = {
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_VERSE_EGG: 698157,
    }

    locations_veil_br = {
        AquariaLocationNames.THE_VEIL_BOTTOM_AREA_STONE_HEAD: 698181,
    }

    locations_octo_cave_t = {
        AquariaLocationNames.OCTOPUS_CAVE_DUMBO_EGG: 698196,
    }

    locations_octo_cave_b = {
        AquariaLocationNames.OCTOPUS_CAVE_BULB_IN_THE_PATH_BELOW_THE_OCTOPUS_CAVE_PATH: 698122,
    }

    locations_sun_temple_l = {
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_LEFT_PART: 698094,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_TOP_RIGHT_PART: 698095,
        AquariaLocationNames.SUN_TEMPLE_BULB_AT_THE_TOP_OF_THE_HIGH_DARK_ROOM: 698096,
        AquariaLocationNames.SUN_TEMPLE_GOLDEN_GEAR: 698171,
    }

    locations_sun_temple_r = {
        AquariaLocationNames.SUN_TEMPLE_FIRST_BULB_OF_THE_TEMPLE: 698091,
        AquariaLocationNames.SUN_TEMPLE_BULB_ON_THE_RIGHT_PART: 698092,
        AquariaLocationNames.SUN_TEMPLE_BULB_IN_THE_HIDDEN_ROOM_OF_THE_RIGHT_PART: 698093,
        AquariaLocationNames.SUN_TEMPLE_SUN_KEY: 698182,
    }

    locations_sun_temple_boss_path = {
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_PATH_BULB: 698017,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_PATH_BULB: 698018,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_FIRST_CLIFF_BULB: 698019,
        AquariaLocationNames.SUN_TEMPLE_BOSS_PATH_SECOND_CLIFF_BULB: 698020,
    }

    locations_sun_temple_boss = {
        AquariaLocationNames.SUN_TEMPLE_BOSS_AREA_BEATING_LUMEREAN_GOD: 698203,
    }

    locations_abyss_l = {
        AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_HIDDEN_PATH_ROOM: 698024,
        AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_RIGHT_PART: 698025,
        AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_SEED: 698166,
        AquariaLocationNames.ABYSS_LEFT_AREA_GLOWING_PLANT: 698172,
    }

    locations_abyss_lb = {
        AquariaLocationNames.ABYSS_LEFT_AREA_BULB_IN_THE_BOTTOM_FISH_PASS: 698026,
    }

    locations_abyss_r = {
        AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_MIDDLE_PATH: 698110,
        AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_MIDDLE_PATH: 698111,
        AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_IN_THE_LEFT_GREEN_ROOM: 698112,
    }

    locations_abyss_r_whale = {
        AquariaLocationNames.ABYSS_RIGHT_AREA_BULB_BEHIND_THE_ROCK_IN_THE_WHALE_ROOM: 698109,
    }

    locations_abyss_r_transturtle = {
        AquariaLocationNames.ABYSS_RIGHT_AREA_TRANSTURTLE: 698214,
    }

    locations_ice_cave = {
        AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_ROOM_TO_THE_RIGHT: 698083,
        AquariaLocationNames.ICE_CAVERN_FIRST_BULB_IN_THE_TOP_EXIT_ROOM: 698084,
        AquariaLocationNames.ICE_CAVERN_SECOND_BULB_IN_THE_TOP_EXIT_ROOM: 698085,
        AquariaLocationNames.ICE_CAVERN_THIRD_BULB_IN_THE_TOP_EXIT_ROOM: 698086,
        AquariaLocationNames.ICE_CAVERN_BULB_IN_THE_LEFT_ROOM: 698087,
    }

    locations_bubble_cave = {
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_LEFT_CAVE_WALL: 698089,
        AquariaLocationNames.BUBBLE_CAVE_BULB_IN_THE_RIGHT_CAVE_WALL_BEHIND_THE_ICE_CRYSTAL: 698090,
    }

    locations_bubble_cave_boss = {
        AquariaLocationNames.BUBBLE_CAVE_VERSE_EGG: 698161,
    }

    locations_king_jellyfish_cave = {
        AquariaLocationNames.KING_JELLYFISH_CAVE_BULB_IN_THE_RIGHT_PATH_FROM_KING_JELLY: 698088,
        AquariaLocationNames.KING_JELLYFISH_CAVE_JELLYFISH_COSTUME: 698188,
    }

    locations_whale = {
        AquariaLocationNames.THE_WHALE_VERSE_EGG: 698159,
    }

    locations_sunken_city_r = {
        AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL: 698154,
        AquariaLocationNames.SUNKEN_CITY_RIGHT_AREA_CRATE_IN_THE_LEFT_BOTTOM_ROOM: 698155,
    }

    locations_sunken_city_l = {
        AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_IN_THE_LITTLE_PIPE_ROOM: 698151,
        AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_CLOSE_TO_THE_SAVE_CRYSTAL: 698152,
        AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_CRATE_BEFORE_THE_BEDROOM: 698153,
    }

    locations_sunken_city_l_bedroom = {
        AquariaLocationNames.SUNKEN_CITY_LEFT_AREA_GIRL_COSTUME: 698192,
    }

    locations_sunken_city_boss = {
        AquariaLocationNames.SUNKEN_CITY_BULB_ON_TOP_OF_THE_BOSS_AREA: 698043,
    }

    locations_body_c = {
        AquariaLocationNames.THE_BODY_CENTER_AREA_BREAKING_LI_S_CAGE: 698201,
        AquariaLocationNames.THE_BODY_CENTER_AREA_BULB_ON_THE_MAIN_PATH_BLOCKING_TUBE: 698097,
    }

    locations_body_l = {
        AquariaLocationNames.THE_BODY_LEFT_AREA_FIRST_BULB_IN_THE_TOP_FACE_ROOM: 698066,
        AquariaLocationNames.THE_BODY_LEFT_AREA_SECOND_BULB_IN_THE_TOP_FACE_ROOM: 698069,
        AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_BELOW_THE_WATER_STREAM: 698067,
        AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_TOP_FACE_ROOM: 698068,
        AquariaLocationNames.THE_BODY_LEFT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM: 698070,
    }

    locations_body_rt = {
        AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_FACE_ROOM: 698100,
    }

    locations_body_rb = {
        AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_TOP_PATH_TO_THE_BOTTOM_FACE_ROOM: 698098,
        AquariaLocationNames.THE_BODY_RIGHT_AREA_BULB_IN_THE_BOTTOM_FACE_ROOM: 698099,
    }

    locations_body_b = {
        AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_JELLY_ZAP_ROOM: 698101,
        AquariaLocationNames.THE_BODY_BOTTOM_AREA_BULB_IN_THE_NAUTILUS_ROOM: 698102,
        AquariaLocationNames.THE_BODY_BOTTOM_AREA_MUTANT_COSTUME: 698190,
    }

    locations_final_boss_tube = {
        AquariaLocationNames.FINAL_BOSS_AREA_FIRST_BULB_IN_THE_TURTLE_ROOM: 698103,
        AquariaLocationNames.FINAL_BOSS_AREA_SECOND_BULB_IN_THE_TURTLE_ROOM: 698104,
        AquariaLocationNames.FINAL_BOSS_AREA_THIRD_BULB_IN_THE_TURTLE_ROOM: 698105,
        AquariaLocationNames.FINAL_BOSS_AREA_TRANSTURTLE: 698215,
    }

    locations_final_boss = {
        AquariaLocationNames.FINAL_BOSS_AREA_BULB_IN_THE_BOSS_THIRD_FORM_ROOM: 698106,
    }


location_table = {
    **AquariaLocations.locations_openwater_tl,
    **AquariaLocations.locations_openwater_tr,
    **AquariaLocations.locations_openwater_tr_turtle,
    **AquariaLocations.locations_openwater_tr_urns,
    **AquariaLocations.locations_openwater_bl,
    **AquariaLocations.locations_skeleton_path,
    **AquariaLocations.locations_skeleton_path_sc,
    **AquariaLocations.locations_arnassi,
    **AquariaLocations.locations_arnassi_cave,
    **AquariaLocations.locations_arnassi_cave_transturtle,
    **AquariaLocations.locations_arnassi_crab_boss,
    **AquariaLocations.locations_sun_temple_l,
    **AquariaLocations.locations_sun_temple_r,
    **AquariaLocations.locations_sun_temple_boss_path,
    **AquariaLocations.locations_sun_temple_boss,
    **AquariaLocations.locations_verse_cave_r,
    **AquariaLocations.locations_verse_cave_l,
    **AquariaLocations.locations_abyss_l,
    **AquariaLocations.locations_abyss_lb,
    **AquariaLocations.locations_abyss_r,
    **AquariaLocations.locations_abyss_r_whale,
    **AquariaLocations.locations_abyss_r_transturtle,
    **AquariaLocations.locations_energy_temple_1,
    **AquariaLocations.locations_energy_temple_2,
    **AquariaLocations.locations_energy_temple_3,
    **AquariaLocations.locations_energy_temple_boss,
    **AquariaLocations.locations_energy_temple_blaster_room,
    **AquariaLocations.locations_energy_temple_altar,
    **AquariaLocations.locations_energy_temple_idol,
    **AquariaLocations.locations_mithalas_city,
    **AquariaLocations.locations_mithalas_city_urns,
    **AquariaLocations.locations_mithalas_city_top_path,
    **AquariaLocations.locations_mithalas_city_fishpass,
    **AquariaLocations.locations_mithalas_castle,
    **AquariaLocations.locations_mithalas_castle_urns,
    **AquariaLocations.locations_mithalas_castle_tube,
    **AquariaLocations.locations_mithalas_castle_sc,
    **AquariaLocations.locations_cathedral_top_start,
    **AquariaLocations.locations_cathedral_top_start_urns,
    **AquariaLocations.locations_cathedral_top_end,
    **AquariaLocations.locations_cathedral_underground,
    **AquariaLocations.locations_cathedral_boss,
    **AquariaLocations.locations_forest_tl,
    **AquariaLocations.locations_forest_tl_verse_egg_room,
    **AquariaLocations.locations_forest_tr,
    **AquariaLocations.locations_forest_tr_fp,
    **AquariaLocations.locations_forest_bl,
    **AquariaLocations.locations_forest_bl_sc,
    **AquariaLocations.locations_forest_br,
    **AquariaLocations.locations_forest_boss,
    **AquariaLocations.locations_forest_boss_entrance,
    **AquariaLocations.locations_sprite_cave,
    **AquariaLocations.locations_sprite_cave_tube,
    **AquariaLocations.locations_forest_fish_cave,
    **AquariaLocations.locations_home_water,
    **AquariaLocations.locations_home_water_behind_rocks,
    **AquariaLocations.locations_home_water_transturtle,
    **AquariaLocations.locations_home_water_nautilus,
    **AquariaLocations.locations_body_l,
    **AquariaLocations.locations_body_rt,
    **AquariaLocations.locations_body_rb,
    **AquariaLocations.locations_body_c,
    **AquariaLocations.locations_body_b,
    **AquariaLocations.locations_final_boss_tube,
    **AquariaLocations.locations_final_boss,
    **AquariaLocations.locations_song_cave,
    **AquariaLocations.locations_veil_tl,
    **AquariaLocations.locations_veil_tl_fp,
    **AquariaLocations.locations_turtle_cave,
    **AquariaLocations.locations_turtle_cave_bubble,
    **AquariaLocations.locations_veil_tr_r,
    **AquariaLocations.locations_veil_tr_l,
    **AquariaLocations.locations_veil_b,
    **AquariaLocations.locations_veil_b_sc,
    **AquariaLocations.locations_veil_b_fp,
    **AquariaLocations.locations_veil_br,
    **AquariaLocations.locations_ice_cave,
    **AquariaLocations.locations_king_jellyfish_cave,
    **AquariaLocations.locations_bubble_cave,
    **AquariaLocations.locations_bubble_cave_boss,
    **AquariaLocations.locations_naija_home,
    **AquariaLocations.locations_mermog_cave,
    **AquariaLocations.locations_mermog_boss,
    **AquariaLocations.locations_octo_cave_t,
    **AquariaLocations.locations_octo_cave_b,
    **AquariaLocations.locations_sunken_city_l,
    **AquariaLocations.locations_sunken_city_r,
    **AquariaLocations.locations_sunken_city_boss,
    **AquariaLocations.locations_sunken_city_l_bedroom,
    **AquariaLocations.locations_simon,
    **AquariaLocations.locations_whale,
}
