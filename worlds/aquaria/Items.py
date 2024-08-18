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

    def __init__(self, id: int, count: int, type: ItemType, group: ItemGroup):
        """
        Initialisation of the item data
        @param id: The item ID
        @param count: the number of items in the pool
        @param type: the importance type of the item
        @param group: the usage of the item in the game
        """
        self.id = id
        self.count = count
        self.type = type
        self.group = group


"""Information data for every (not event) item."""
item_table = {
    #       name:           ID,    Nb,   Item Type,        Item Group
    "Anemone": ItemData(698000, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_anemone
    "Arnassi Statue": ItemData(698001, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_arnassi_statue
    "Big Seed": ItemData(698002, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_big_seed
    "Glowing Seed": ItemData(698003, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_bio_seed
    "Black Pearl": ItemData(698004, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_blackpearl
    "Baby Blaster": ItemData(698005, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_blaster
    "Crab Armor": ItemData(698006, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_crab_costume
    "Baby Dumbo": ItemData(698007, 1, ItemType.PROGRESSION, ItemGroup.UTILITY),  # collectible_dumbo
    "Tooth": ItemData(698008, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_boss
    "Energy Statue": ItemData(698009, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_statue
    "Krotite Armor": ItemData(698010, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_temple
    "Golden Starfish": ItemData(698011, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_gold_star
    "Golden Gear": ItemData(698012, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_golden_gear
    "Jelly Beacon": ItemData(698013, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_beacon
    "Jelly Costume": ItemData(698014, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_jelly_costume
    "Jelly Plant": ItemData(698015, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_plant
    "Mithalas Doll": ItemData(698016, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithala_doll
    "Mithalan Dress": ItemData(698017, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalan_costume
    "Mithalas Banner": ItemData(698018, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_banner
    "Mithalas Pot": ItemData(698019, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_pot
    "Mutant Costume": ItemData(698020, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mutant_costume
    "Baby Nautilus": ItemData(698021, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_nautilus
    "Baby Piranha": ItemData(698022, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_piranha
    "Arnassi Armor": ItemData(698023, 1, ItemType.PROGRESSION, ItemGroup.UTILITY),  # collectible_seahorse_costume
    "Seed Bag": ItemData(698024, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_seed_bag
    "King's Skull": ItemData(698025, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_skull
    "Song Plant Spore": ItemData(698026, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_spore_seed
    "Stone Head": ItemData(698027, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_stone_head
    "Sun Key": ItemData(698028, 1, ItemType.NORMAL, ItemGroup.COLLECTIBLE),  # collectible_sun_key
    "Girl Costume": ItemData(698029, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_teen_costume
    "Odd Container": ItemData(698030, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_treasure_chest
    "Trident": ItemData(698031, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_trident_head
    "Turtle Egg": ItemData(698032, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_turtle_egg
    "Jelly Egg": ItemData(698033, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_upsidedown_seed
    "Urchin Costume": ItemData(698034, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_urchin_costume
    "Baby Walker": ItemData(698035, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_walker
    "Vedha's Cure-All-All": ItemData(698036, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Vedha'sCure-All
    "Zuuna's perogi": ItemData(698037, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Zuuna'sperogi
    "Arcane poultice": ItemData(698038, 7, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_arcanepoultice
    "Berry ice cream": ItemData(698039, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_berryicecream
    "Buttery sea loaf": ItemData(698040, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_butterysealoaf
    "Cold borscht": ItemData(698041, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldborscht
    "Cold soup": ItemData(698042, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldsoup
    "Crab cake": ItemData(698043, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_crabcake
    "Divine soup": ItemData(698044, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_divinesoup
    "Dumbo ice cream": ItemData(698045, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_dumboicecream
    "Fish oil": ItemData(698046, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    "Glowing egg": ItemData(698047, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    "Hand roll": ItemData(698048, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_handroll
    "Healing poultice": ItemData(698049, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    "Hearty soup": ItemData(698050, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_heartysoup
    "Hot borscht": ItemData(698051, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_hotborscht
    "Hot soup": ItemData(698052, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    "Ice cream": ItemData(698053, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_icecream
    "Leadership roll": ItemData(698054, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    "Leaf poultice": ItemData(698055, 5, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_leafpoultice
    "Leeching poultice": ItemData(698056, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leechingpoultice
    "Legendary cake": ItemData(698057, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_legendarycake
    "Loaf of life": ItemData(698058, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_loafoflife
    "Long life soup": ItemData(698059, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_longlifesoup
    "Magic soup": ItemData(698060, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_magicsoup
    "Mushroom x 2": ItemData(698061, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_mushroom
    "Perogi": ItemData(698062, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_perogi
    "Plant leaf": ItemData(698063, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Plump perogi": ItemData(698064, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_plumpperogi
    "Poison loaf": ItemData(698065, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonloaf
    "Poison soup": ItemData(698066, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonsoup
    "Rainbow mushroom": ItemData(698067, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_rainbowmushroom
    "Rainbow soup": ItemData(698068, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_rainbowsoup
    "Red berry": ItemData(698069, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redberry
    "Red bulb x 2": ItemData(698070, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redbulb
    "Rotten cake": ItemData(698071, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottencake
    "Rotten loaf x 8": ItemData(698072, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottenloaf
    "Rotten meat": ItemData(698073, 5, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Royal soup": ItemData(698074, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_royalsoup
    "Sea cake": ItemData(698075, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_seacake
    "Sea loaf": ItemData(698076, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    "Shark fin soup": ItemData(698077, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sharkfinsoup
    "Sight poultice": ItemData(698078, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sightpoultice
    "Small bone x 2": ItemData(698079, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    "Small egg": ItemData(698080, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    "Small tentacle x 2": ItemData(698081, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smalltentacle
    "Special bulb": ItemData(698082, 5, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_specialbulb
    "Special cake": ItemData(698083, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_specialcake
    "Spicy meat x 2": ItemData(698084, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_spicymeat
    "Spicy roll": ItemData(698085, 11, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicyroll
    "Spicy soup": ItemData(698086, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicysoup
    "Spider roll": ItemData(698087, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spiderroll
    "Swamp cake": ItemData(698088, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_swampcake
    "Tasty cake": ItemData(698089, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastycake
    "Tasty roll": ItemData(698090, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastyroll
    "Tough cake": ItemData(698091, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_toughcake
    "Turtle soup": ItemData(698092, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_turtlesoup
    "Vedha sea crisp": ItemData(698093, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_vedhaseacrisp
    "Veggie cake": ItemData(698094, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiecake
    "Veggie ice cream": ItemData(698095, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggieicecream
    "Veggie soup": ItemData(698096, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiesoup
    "Volcano roll": ItemData(698097, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_volcanoroll
    "Health upgrade": ItemData(698098, 5, ItemType.NORMAL, ItemGroup.HEALTH),  # upgrade_health_?
    "Wok": ItemData(698099, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # upgrade_wok
    "Eel oil x 2": ItemData(698100, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_eeloil
    "Fish meat x 2": ItemData(698101, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishmeat
    "Fish oil x 3": ItemData(698102, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    "Glowing egg x 2": ItemData(698103, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    "Healing poultice x 2": ItemData(698104, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    "Hot soup x 2": ItemData(698105, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    "Leadership roll x 2": ItemData(698106, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    "Leaf poultice x 3": ItemData(698107, 2, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_leafpoultice
    "Plant leaf x 2": ItemData(698108, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Plant leaf x 3": ItemData(698109, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Rotten meat x 2": ItemData(698110, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Rotten meat x 8": ItemData(698111, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Sea loaf x 2": ItemData(698112, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    "Small bone x 3": ItemData(698113, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    "Small egg x 2": ItemData(698114, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    "Li and Li song": ItemData(698115, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_li
    "Shield song": ItemData(698116, 1, ItemType.NORMAL, ItemGroup.SONG),  # song_shield
    "Beast form": ItemData(698117, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_beast
    "Sun form": ItemData(698118, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_sun
    "Nature form": ItemData(698119, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_nature
    "Energy form": ItemData(698120, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_energy
    "Bind song": ItemData(698121, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_bind
    "Fish form": ItemData(698122, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_fish
    "Spirit form": ItemData(698123, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_spirit
    "Dual form": ItemData(698124, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_dual
    "Transturtle Veil top left": ItemData(698125, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil01
    "Transturtle Veil top right": ItemData(698126, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil02
    "Transturtle Open Water top right": ItemData(698127, 1, ItemType.PROGRESSION,
                                                 ItemGroup.TURTLE),  # transport_openwater03
    "Transturtle Forest bottom left": ItemData(698128, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_forest04
    "Transturtle Home Water": ItemData(698129, 1, ItemType.NORMAL, ItemGroup.TURTLE),  # transport_mainarea
    "Transturtle Abyss right": ItemData(698130, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_abyss03
    "Transturtle Final Boss": ItemData(698131, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_finalboss
    "Transturtle Simon Says": ItemData(698132, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_forest05
    "Transturtle Arnassi Ruins": ItemData(698133, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_seahorse
}
