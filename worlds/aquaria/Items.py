"""
Author: Louis M
Date: Fri, 15 Mar 2024 18:41:40 +0000
Description: Manage items in the Aquaria game multiworld randomizer
"""

from typing import Optional
from enum import Enum
from BaseClasses import Item, ItemClassification


class ItemType(Enum):
    """
    Used to indicate to the multi-world if an item is useful or not
    """
    NORMAL = 0
    PROGRESSION = 1
    JUNK = 2


class ItemGroup(Enum):
    """
    Used to group items
    """
    COLLECTIBLE = 0
    INGREDIENT = 1
    RECIPE = 2
    HEALTH = 3
    UTILITY = 4
    SONG = 5
    TURTLE = 6


class AquariaItem(Item):
    """
    A single item in the Aquaria game.
    """
    game: str = "Aquaria"
    """The name of the game"""

    def __init__(self, name: str, classification: ItemClassification,
                 code: Optional[int], player: int):
        """
        Initialisation of the Item
        :param name: The name of the item
        :param classification: If the item is useful or not
        :param code: The ID of the item (if None, it is an event)
        :param player: The ID of the player in the multiworld
        """
        super().__init__(name, classification, code, player)


class ItemData:
    """
    Data of an item.
    """
    id: int
    count: int
    type: ItemType
    group: ItemGroup

    def __init__(self, aId: int, count: int, aType: ItemType, group: ItemGroup):
        """
        Initialisation of the item data
        @param aId: The item ID
        @param count: the number of items in the pool
        @param aType: the importance type of the item
        @param group: the usage of the item in the game
        """
        self.id = aId
        self.count = count
        self.type = aType
        self.group = group

class ItemNames:
    """
    Constants used to represent the mane of every items.
    """
    # Normal items
    ANEMONE = "Anemone"
    ARNASSI_STATUE = "Arnassi Statue"
    BIG_SEED = "Big Seed"
    GLOWING_SEED = "Glowing Seed"
    BLACK_PEARL = "Black Pearl"
    BABY_BLASTER = "Baby Blaster"
    CRAB_ARMOR = "Crab Armor"
    BABY_DUMBO = "Baby Dumbo"
    TOOTH = "Tooth"
    ENERGY_STATUE = "Energy Statue"
    KROTITE_ARMOR = "Krotite Armor"
    GOLDEN_STARFISH = "Golden Starfish"
    GOLDEN_GEAR = "Golden Gear"
    JELLY_BEACON = "Jelly Beacon"
    JELLY_COSTUME = "Jelly Costume"
    JELLY_PLANT = "Jelly Plant"
    MITHALAS_DOLL = "Mithalas Doll"
    MITHALAN_DRESS = "Mithalan Dress"
    MITHALAS_BANNER = "Mithalas Banner"
    MITHALAS_POT = "Mithalas Pot"
    MUTANT_COSTUME = "Mutant Costume"
    BABY_NAUTILUS = "Baby Nautilus"
    BABY_PIRANHA = "Baby Piranha"
    ARNASSI_ARMOR = "Arnassi Armor"
    SEED_BAG = "Seed Bag"
    KING_S_SKULL = "King's Skull"
    SONG_PLANT_SPORE = "Song Plant Spore"
    STONE_HEAD = "Stone Head"
    SUN_KEY = "Sun Key"
    GIRL_COSTUME = "Girl Costume"
    ODD_CONTAINER = "Odd Container"
    TRIDENT = "Trident"
    TURTLE_EGG = "Turtle Egg"
    JELLY_EGG = "Jelly Egg"
    URCHIN_COSTUME = "Urchin Costume"
    BABY_WALKER = "Baby Walker"
    VEDHA_S_CURE_ALL = "Vedha's Cure-All"
    ZUUNA_S_PEROGI = "Zuuna's Perogi"
    ARCANE_POULTICE = "Arcane Poultice"
    BERRY_ICE_CREAM = "Berry Ice Cream"
    BUTTERY_SEA_LOAF = "Buttery Sea Loaf"
    COLD_BORSCHT = "Cold Borscht"
    COLD_SOUP = "Cold Soup"
    CRAB_CAKE = "Crab Cake"
    DIVINE_SOUP = "Divine Soup"
    DUMBO_ICE_CREAM = "Dumbo Ice Cream"
    FISH_OIL = "Fish Oil"
    GLOWING_EGG = "Glowing Egg"
    HAND_ROLL = "Hand Roll"
    HEALING_POULTICE = "Healing Poultice"
    HEARTY_SOUP = "Hearty Soup"
    HOT_BORSCHT = "Hot Borscht"
    HOT_SOUP = "Hot Soup"
    ICE_CREAM = "Ice Cream"
    LEADERSHIP_ROLL = "Leadership Roll"
    LEAF_POULTICE = "Leaf Poultice"
    LEECHING_POULTICE = "Leeching Poultice"
    LEGENDARY_CAKE = "Legendary Cake"
    LOAF_OF_LIFE = "Loaf of Life"
    LONG_LIFE_SOUP = "Long Life Soup"
    MAGIC_SOUP = "Magic Soup"
    MUSHROOM_X_2 = "Mushroom x 2"
    PEROGI = "Perogi"
    PLANT_LEAF = "Plant Leaf"
    PLUMP_PEROGI = "Plump Perogi"
    POISON_LOAF = "Poison Loaf"
    POISON_SOUP = "Poison Soup"
    RAINBOW_MUSHROOM = "Rainbow Mushroom"
    RAINBOW_SOUP = "Rainbow Soup"
    RED_BERRY = "Red Berry"
    RED_BULB_X_2 = "Red Bulb x 2"
    ROTTEN_CAKE = "Rotten Cake"
    ROTTEN_LOAF_X_8 = "Rotten Loaf x 8"
    ROTTEN_MEAT = "Rotten Meat"
    ROYAL_SOUP = "Royal Soup"
    SEA_CAKE = "Sea Cake"
    SEA_LOAF = "Sea Loaf"
    SHARK_FIN_SOUP = "Shark Fin Soup"
    SIGHT_POULTICE = "Sight Poultice"
    SMALL_BONE_X_2 = "Small Bone x 2"
    SMALL_EGG = "Small Egg"
    SMALL_TENTACLE_X_2 = "Small Tentacle x 2"
    SPECIAL_BULB = "Special Bulb"
    SPECIAL_CAKE = "Special Cake"
    SPICY_MEAT_X_2 = "Spicy Meat x 2"
    SPICY_ROLL = "Spicy Roll"
    SPICY_SOUP = "Spicy Soup"
    SPIDER_ROLL = "Spider Roll"
    SWAMP_CAKE = "Swamp Cake"
    TASTY_CAKE = "Tasty Cake"
    TASTY_ROLL = "Tasty Roll"
    TOUGH_CAKE = "Tough Cake"
    TURTLE_SOUP = "Turtle Soup"
    VEDHA_SEA_CRISP = "Vedha Sea Crisp"
    VEGGIE_CAKE = "Veggie Cake"
    VEGGIE_ICE_CREAM = "Veggie Ice Cream"
    VEGGIE_SOUP = "Veggie Soup"
    VOLCANO_ROLL = "Volcano Roll"
    HEALTH_UPGRADE = "Health Upgrade"
    WOK = "Wok"
    EEL_OIL_X_2 = "Eel Oil x 2"
    FISH_MEAT_X_2 = "Fish Meat x 2"
    FISH_OIL_X_3 = "Fish Oil x 3"
    GLOWING_EGG_X_2 = "Glowing Egg x 2"
    HEALING_POULTICE_X_2 = "Healing Poultice x 2"
    HOT_SOUP_X_2 = "Hot Soup x 2"
    LEADERSHIP_ROLL_X_2 = "Leadership Roll x 2"
    LEAF_POULTICE_X_3 = "Leaf Poultice x 3"
    PLANT_LEAF_X_2 = "Plant Leaf x 2"
    PLANT_LEAF_X_3 = "Plant Leaf x 3"
    ROTTEN_MEAT_X_2 = "Rotten Meat x 2"
    ROTTEN_MEAT_X_8 = "Rotten Meat x 8"
    SEA_LOAF_X_2 = "Sea Loaf x 2"
    SMALL_BONE_X_3 = "Small Bone x 3"
    SMALL_EGG_X_2 = "Small Egg x 2"
    LI_AND_LI_SONG = "Li and Li Song"
    SHIELD_SONG = "Shield Song"
    BEAST_FORM = "Beast Form"
    SUN_FORM = "Sun Form"
    NATURE_FORM = "Nature Form"
    ENERGY_FORM = "Energy Form"
    BIND_SONG = "Bind Song"
    FISH_FORM = "Fish Form"
    SPIRIT_FORM = "Spirit Form"
    DUAL_FORM = "Dual Form"
    TRANSTURTLE_VEIL_TOP_LEFT = "Transturtle Veil top left"
    TRANSTURTLE_VEIL_TOP_RIGHT = "Transturtle Veil top right"
    TRANSTURTLE_OPEN_WATERS = "Transturtle Open Waters top right"
    TRANSTURTLE_KELP_FOREST = "Transturtle Kelp Forest bottom left"
    TRANSTURTLE_HOME_WATERS = "Transturtle Home Waters"
    TRANSTURTLE_ABYSS = "Transturtle Abyss right"
    TRANSTURTLE_BODY = "Transturtle Final Boss"
    TRANSTURTLE_SIMON_SAYS = "Transturtle Simon Says"
    TRANSTURTLE_ARNASSI_RUINS = "Transturtle Arnassi Ruins"
    # Events name
    BODY_TONGUE_CLEARED = "Body Tongue cleared"
    HAS_SUN_CRYSTAL = "Has Sun Crystal"
    FALLEN_GOD_BEATED = "Fallen God beated"
    MITHALAN_GOD_BEATED = "Mithalan God beated"
    DRUNIAN_GOD_BEATED = "Drunian God beated"
    LUMEREAN_GOD_BEATED = "Lumerean God beated"
    THE_GOLEM_BEATED = "The Golem beated"
    NAUTILUS_PRIME_BEATED = "Nautilus Prime beated"
    BLASTER_PEG_PRIME_BEATED = "Blaster Peg Prime beated"
    MERGOG_BEATED = "Mergog beated"
    MITHALAN_PRIESTS_BEATED = "Mithalan priests beated"
    OCTOPUS_PRIME_BEATED = "Octopus Prime beated"
    CRABBIUS_MAXIMUS_BEATED = "Crabbius Maximus beated"
    MANTIS_SHRIMP_PRIME_BEATED = "Mantis Shrimp Prime beated"
    KING_JELLYFISH_GOD_PRIME_BEATED = "King Jellyfish God Prime beated"
    VICTORY = "Victory"
    FIRST_SECRET_OBTAINED = "First Secret obtained"
    SECOND_SECRET_OBTAINED = "Second Secret obtained"
    THIRD_SECRET_OBTAINED = "Third Secret obtained"

"""Information data for every (not event) item."""
item_table = {
    #       name:           ID,    Nb,   Item Type,        Item Group
    ItemNames.ANEMONE: ItemData(698000, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_anemone
    ItemNames.ARNASSI_STATUE: ItemData(698001, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_arnassi_statue
    ItemNames.BIG_SEED: ItemData(698002, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_big_seed
    ItemNames.GLOWING_SEED: ItemData(698003, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_bio_seed
    ItemNames.BLACK_PEARL: ItemData(698004, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_blackpearl
    ItemNames.BABY_BLASTER: ItemData(698005, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_blaster
    ItemNames.CRAB_ARMOR: ItemData(698006, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_crab_costume
    ItemNames.BABY_DUMBO: ItemData(698007, 1, ItemType.PROGRESSION, ItemGroup.UTILITY),  # collectible_dumbo
    ItemNames.TOOTH: ItemData(698008, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_boss
    ItemNames.ENERGY_STATUE: ItemData(698009, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_statue
    ItemNames.KROTITE_ARMOR: ItemData(698010, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_temple
    ItemNames.GOLDEN_STARFISH: ItemData(698011, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_gold_star
    ItemNames.GOLDEN_GEAR: ItemData(698012, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_golden_gear
    ItemNames.JELLY_BEACON: ItemData(698013, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_beacon
    ItemNames.JELLY_COSTUME: ItemData(698014, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_jelly_costume
    ItemNames.JELLY_PLANT: ItemData(698015, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_plant
    ItemNames.MITHALAS_DOLL: ItemData(698016, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithala_doll
    ItemNames.MITHALAN_DRESS: ItemData(698017, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalan_costume
    ItemNames.MITHALAS_BANNER: ItemData(698018, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_banner
    ItemNames.MITHALAS_POT: ItemData(698019, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_pot
    ItemNames.MUTANT_COSTUME: ItemData(698020, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mutant_costume
    ItemNames.BABY_NAUTILUS: ItemData(698021, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_nautilus
    ItemNames.BABY_PIRANHA: ItemData(698022, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_piranha
    ItemNames.ARNASSI_ARMOR: ItemData(698023, 1, ItemType.PROGRESSION, ItemGroup.UTILITY),  # collectible_seahorse_costume
    ItemNames.SEED_BAG: ItemData(698024, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_seed_bag
    ItemNames.KING_S_SKULL: ItemData(698025, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_skull
    ItemNames.SONG_PLANT_SPORE: ItemData(698026, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_spore_seed
    ItemNames.STONE_HEAD: ItemData(698027, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_stone_head
    ItemNames.SUN_KEY: ItemData(698028, 1, ItemType.NORMAL, ItemGroup.COLLECTIBLE),  # collectible_sun_key
    ItemNames.GIRL_COSTUME: ItemData(698029, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_teen_costume
    ItemNames.ODD_CONTAINER: ItemData(698030, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_treasure_chest
    ItemNames.TRIDENT: ItemData(698031, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_trident_head
    ItemNames.TURTLE_EGG: ItemData(698032, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_turtle_egg
    ItemNames.JELLY_EGG: ItemData(698033, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_upsidedown_seed
    ItemNames.URCHIN_COSTUME: ItemData(698034, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_urchin_costume
    ItemNames.BABY_WALKER: ItemData(698035, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_walker
    ItemNames.VEDHA_S_CURE_ALL: ItemData(698036, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Vedha'sCure-All
    ItemNames.ZUUNA_S_PEROGI: ItemData(698037, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Zuuna'sperogi
    ItemNames.ARCANE_POULTICE: ItemData(698038, 7, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_arcanepoultice
    ItemNames.BERRY_ICE_CREAM: ItemData(698039, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_berryicecream
    ItemNames.BUTTERY_SEA_LOAF: ItemData(698040, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_butterysealoaf
    ItemNames.COLD_BORSCHT: ItemData(698041, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldborscht
    ItemNames.COLD_SOUP: ItemData(698042, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldsoup
    ItemNames.CRAB_CAKE: ItemData(698043, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_crabcake
    ItemNames.DIVINE_SOUP: ItemData(698044, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_divinesoup
    ItemNames.DUMBO_ICE_CREAM: ItemData(698045, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_dumboicecream
    ItemNames.FISH_OIL: ItemData(698046, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    ItemNames.GLOWING_EGG: ItemData(698047, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    ItemNames.HAND_ROLL: ItemData(698048, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_handroll
    ItemNames.HEALING_POULTICE: ItemData(698049, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    ItemNames.HEARTY_SOUP: ItemData(698050, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_heartysoup
    ItemNames.HOT_BORSCHT: ItemData(698051, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_hotborscht
    ItemNames.HOT_SOUP: ItemData(698052, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    ItemNames.ICE_CREAM: ItemData(698053, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_icecream
    ItemNames.LEADERSHIP_ROLL: ItemData(698054, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    ItemNames.LEAF_POULTICE: ItemData(698055, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leafpoultice
    ItemNames.LEECHING_POULTICE: ItemData(698056, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leechingpoultice
    ItemNames.LEGENDARY_CAKE: ItemData(698057, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_legendarycake
    ItemNames.LOAF_OF_LIFE: ItemData(698058, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_loafoflife
    ItemNames.LONG_LIFE_SOUP: ItemData(698059, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_longlifesoup
    ItemNames.MAGIC_SOUP: ItemData(698060, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_magicsoup
    ItemNames.MUSHROOM_X_2: ItemData(698061, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_mushroom
    ItemNames.PEROGI: ItemData(698062, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_perogi
    ItemNames.PLANT_LEAF: ItemData(698063, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    ItemNames.PLUMP_PEROGI: ItemData(698064, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_plumpperogi
    ItemNames.POISON_LOAF: ItemData(698065, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonloaf
    ItemNames.POISON_SOUP: ItemData(698066, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonsoup
    ItemNames.RAINBOW_MUSHROOM: ItemData(698067, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_rainbowmushroom
    ItemNames.RAINBOW_SOUP: ItemData(698068, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_rainbowsoup
    ItemNames.RED_BERRY: ItemData(698069, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redberry
    ItemNames.RED_BULB_X_2: ItemData(698070, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redbulb
    ItemNames.ROTTEN_CAKE: ItemData(698071, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottencake
    ItemNames.ROTTEN_LOAF_X_8: ItemData(698072, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottenloaf
    ItemNames.ROTTEN_MEAT: ItemData(698073, 5, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    ItemNames.ROYAL_SOUP: ItemData(698074, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_royalsoup
    ItemNames.SEA_CAKE: ItemData(698075, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_seacake
    ItemNames.SEA_LOAF: ItemData(698076, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    ItemNames.SHARK_FIN_SOUP: ItemData(698077, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sharkfinsoup
    ItemNames.SIGHT_POULTICE: ItemData(698078, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sightpoultice
    ItemNames.SMALL_BONE_X_2: ItemData(698079, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    ItemNames.SMALL_EGG: ItemData(698080, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    ItemNames.SMALL_TENTACLE_X_2: ItemData(698081, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smalltentacle
    ItemNames.SPECIAL_BULB: ItemData(698082, 5, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_specialbulb
    ItemNames.SPECIAL_CAKE: ItemData(698083, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_specialcake
    ItemNames.SPICY_MEAT_X_2: ItemData(698084, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_spicymeat
    ItemNames.SPICY_ROLL: ItemData(698085, 11, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicyroll
    ItemNames.SPICY_SOUP: ItemData(698086, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicysoup
    ItemNames.SPIDER_ROLL: ItemData(698087, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spiderroll
    ItemNames.SWAMP_CAKE: ItemData(698088, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_swampcake
    ItemNames.TASTY_CAKE: ItemData(698089, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastycake
    ItemNames.TASTY_ROLL: ItemData(698090, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastyroll
    ItemNames.TOUGH_CAKE: ItemData(698091, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_toughcake
    ItemNames.TURTLE_SOUP: ItemData(698092, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_turtlesoup
    ItemNames.VEDHA_SEA_CRISP: ItemData(698093, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_vedhaseacrisp
    ItemNames.VEGGIE_CAKE: ItemData(698094, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiecake
    ItemNames.VEGGIE_ICE_CREAM: ItemData(698095, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggieicecream
    ItemNames.VEGGIE_SOUP: ItemData(698096, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiesoup
    ItemNames.VOLCANO_ROLL: ItemData(698097, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_volcanoroll
    ItemNames.HEALTH_UPGRADE: ItemData(698098, 5, ItemType.NORMAL, ItemGroup.HEALTH),  # upgrade_health_?
    ItemNames.WOK: ItemData(698099, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # upgrade_wok
    ItemNames.EEL_OIL_X_2: ItemData(698100, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_eeloil
    ItemNames.FISH_MEAT_X_2: ItemData(698101, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishmeat
    ItemNames.FISH_OIL_X_3: ItemData(698102, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    ItemNames.GLOWING_EGG_X_2: ItemData(698103, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    ItemNames.HEALING_POULTICE_X_2: ItemData(698104, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    ItemNames.HOT_SOUP_X_2: ItemData(698105, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    ItemNames.LEADERSHIP_ROLL_X_2: ItemData(698106, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    ItemNames.LEAF_POULTICE_X_3: ItemData(698107, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leafpoultice
    ItemNames.PLANT_LEAF_X_2: ItemData(698108, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    ItemNames.PLANT_LEAF_X_3: ItemData(698109, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    ItemNames.ROTTEN_MEAT_X_2: ItemData(698110, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    ItemNames.ROTTEN_MEAT_X_8: ItemData(698111, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    ItemNames.SEA_LOAF_X_2: ItemData(698112, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    ItemNames.SMALL_BONE_X_3: ItemData(698113, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    ItemNames.SMALL_EGG_X_2: ItemData(698114, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    ItemNames.LI_AND_LI_SONG: ItemData(698115, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_li
    ItemNames.SHIELD_SONG: ItemData(698116, 1, ItemType.NORMAL, ItemGroup.SONG),  # song_shield
    ItemNames.BEAST_FORM: ItemData(698117, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_beast
    ItemNames.SUN_FORM: ItemData(698118, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_sun
    ItemNames.NATURE_FORM: ItemData(698119, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_nature
    ItemNames.ENERGY_FORM: ItemData(698120, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_energy
    ItemNames.BIND_SONG: ItemData(698121, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_bind
    ItemNames.FISH_FORM: ItemData(698122, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_fish
    ItemNames.SPIRIT_FORM: ItemData(698123, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_spirit
    ItemNames.DUAL_FORM: ItemData(698124, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_dual
    ItemNames.TRANSTURTLE_VEIL_TOP_LEFT: ItemData(698125, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil01
    ItemNames.TRANSTURTLE_VEIL_TOP_RIGHT: ItemData(698126, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil02
    ItemNames.TRANSTURTLE_OPEN_WATERS: ItemData(698127, 1, ItemType.PROGRESSION,
                                                ItemGroup.TURTLE),  # transport_openwater03
    ItemNames.TRANSTURTLE_KELP_FOREST: ItemData(698128, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),
    # transport_forest04
    ItemNames.TRANSTURTLE_HOME_WATERS: ItemData(698129, 1, ItemType.NORMAL, ItemGroup.TURTLE),  # transport_mainarea
    ItemNames.TRANSTURTLE_ABYSS: ItemData(698130, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_abyss03
    ItemNames.TRANSTURTLE_BODY: ItemData(698131, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_finalboss
    ItemNames.TRANSTURTLE_SIMON_SAYS: ItemData(698132, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_forest05
    ItemNames.TRANSTURTLE_ARNASSI_RUINS: ItemData(698133, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_seahorse
}
