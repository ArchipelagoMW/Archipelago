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
    Used to indicate to the multi-world if an item is usefull or not
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
        :param classification: If the item is usefull or not
        :param code: The ID of the item (if None, it is an event)
        :param player: The ID of the player in the multiworld
        """
        super().__init__(name, classification, code, player)

"""Information data for every (not event) item."""
item_table = {
    #       name:           ID,    Nb,   Item Type,        Item Group
    "Anemone": (698000, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_anemone
    "Arnassi statue": (698001, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_arnassi_statue
    "Big seed": (698002, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_big_seed
    "Glowing seed": (698003, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_bio_seed
    "Black pearl": (698004, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_blackpearl
    "Baby blaster": (698005, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_blaster
    "Crab armor": (698006, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_crab_costume
    "Baby dumbo": (698007, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_dumbo
    "Tooth": (698008, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_boss
    "Energy statue": (698009, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_statue
    "Krotite armor": (698010, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_energy_temple
    "Golden starfish": (698011, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_gold_star
    "Golden gear": (698012, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_golden_gear
    "Jelly beacon": (698013, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_beacon
    "Jelly costume": (698014, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_jelly_costume
    "Jelly plant": (698015, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_jelly_plant
    "Mithalas doll": (698016, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithala_doll
    "Mithalan dress": (698017, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalan_costume
    "Mithalas banner": (698018, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_banner
    "Mithalas pot": (698019, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mithalas_pot
    "Mutant costume": (698020, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_mutant_costume
    "Baby nautilus": (698021, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_nautilus
    "Baby piranha": (698022, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_piranha
    "Arnassi Armor": (698023, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # collectible_seahorse_costume
    "Seed bag": (698024, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_seed_bag
    "King's Skull": (698025, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_skull
    "Song plant spore": (698026, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_spore_seed
    "Stone head": (698027, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_stone_head
    "Sun key": (698028, 1, ItemType.NORMAL, ItemGroup.COLLECTIBLE),  # collectible_sun_key
    "Girl costume": (698029, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_teen_costume
    "Odd container": (698030, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_treasure_chest
    "Trident": (698031, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_trident_head
    "Turtle egg": (698032, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_turtle_egg
    "Jelly egg": (698033, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_upsidedown_seed
    "Urchin costume": (698034, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_urchin_costume
    "Baby walker": (698035, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),  # collectible_walker
    "Vedha's Cure-All-All": (698036, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Vedha'sCure-All
    "Zuuna's perogi": (698037, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_Zuuna'sperogi
    "Arcane poultice": (698038, 7, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_arcanepoultice
    "Berry ice cream": (698039, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_berryicecream
    "Buttery sea loaf": (698040, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_butterysealoaf
    "Cold borscht": (698041, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldborscht
    "Cold soup": (698042, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_coldsoup
    "Crab cake": (698043, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_crabcake
    "Divine soup": (698044, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_divinesoup
    "Dumbo ice cream": (698045, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_dumboicecream
    "Fish oil": (698046, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    "Glowing egg": (698047, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    "Hand roll": (698048, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_handroll
    "Healing poultice": (698049, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    "Hearty soup": (698050, 5, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_heartysoup
    "Hot borscht": (698051, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_hotborscht
    "Hot soup": (698052, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    "Ice cream": (698053, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_icecream
    "Leadership roll": (698054, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    "Leaf poultice": (698055, 5, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_leafpoultice
    "Leeching poultice": (698056, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leechingpoultice
    "Legendary cake": (698057, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_legendarycake
    "Loaf of life": (698058, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_loafoflife
    "Long life soup": (698059, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_longlifesoup
    "Magic soup": (698060, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_magicsoup
    "Mushroom x 2": (698061, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_mushroom
    "Perogi": (698062, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_perogi
    "Plant leaf": (698063, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Plump perogi": (698064, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_plumpperogi
    "Poison loaf": (698065, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonloaf
    "Poison soup": (698066, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_poisonsoup
    "Rainbow mushroom": (698067, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_rainbowmushroom
    "Rainbow soup": (698068, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_rainbowsoup
    "Red berry": (698069, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redberry
    "Red bulb x 2": (698070, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_redbulb
    "Rotten cake": (698071, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottencake
    "Rotten loaf x 8": (698072, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_rottenloaf
    "Rotten meat": (698073, 5, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Royal soup": (698074, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_royalsoup
    "Sea cake": (698075, 4, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_seacake
    "Sea loaf": (698076, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    "Shark fin soup": (698077, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sharkfinsoup
    "Sight poultice": (698078, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_sightpoultice
    "Small bone x 2": (698079, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    "Small egg": (698080, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    "Small tentacle x 2": (698081, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smalltentacle
    "Special bulb": (698082, 5, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_specialbulb
    "Special cake": (698083, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_specialcake
    "Spicy meat x 2": (698084, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_spicymeat
    "Spicy roll": (698085, 11, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicyroll
    "Spicy soup": (698086, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spicysoup
    "Spider roll": (698087, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_spiderroll
    "Swamp cake": (698088, 3, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_swampcake
    "Tasty cake": (698089, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastycake
    "Tasty roll": (698090, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_tastyroll
    "Tough cake": (698091, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_toughcake
    "Turtle soup": (698092, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_turtlesoup
    "Vedha sea crisp": (698093, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_vedhaseacrisp
    "Veggie cake": (698094, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiecake
    "Veggie ice cream": (698095, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggieicecream
    "Veggie soup": (698096, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_veggiesoup
    "Volcano roll": (698097, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_volcanoroll
    "Health upgrade": (698098, 5, ItemType.NORMAL, ItemGroup.HEALTH),  # upgrade_health_1 .. upgrade_health_5
    "Wok": (698099, 1, ItemType.NORMAL, ItemGroup.UTILITY),  # upgrade_wok
    "Eel oil x 2": (698100, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_eeloil
    "Fish meat x 2": (698101, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishmeat
    "Fish oil x 3": (698102, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_fishoil
    "Glowing egg x 2": (698103, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_glowingegg
    "Healing poultice x 2": (698104, 2, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_healingpoultice
    "Hot soup x 2": (698105, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_hotsoup
    "Leadership roll x 2": (698106, 1, ItemType.NORMAL, ItemGroup.RECIPE),  # ingredient_leadershiproll
    "Leaf poultice x 3": (698107, 2, ItemType.PROGRESSION, ItemGroup.RECIPE),  # ingredient_leafpoultice
    "Plant leaf x 2": (698108, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Plant leaf x 3": (698109, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_plantleaf
    "Rotten meat x 2": (698110, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Rotten meat x 8": (698111, 1, ItemType.JUNK, ItemGroup.INGREDIENT),  # ingredient_rottenmeat
    "Sea loaf x 2": (698112, 1, ItemType.JUNK, ItemGroup.RECIPE),  # ingredient_sealoaf
    "Small bone x 3": (698113, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallbone
    "Small egg x 2": (698114, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),  # ingredient_smallegg
    "Li and Li song": (698115, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_li
    "Shield song": (698116, 1, ItemType.NORMAL, ItemGroup.SONG),  # song_shield
    "Beast form": (698117, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_beast
    "Sun form": (698118, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_sun
    "Nature form": (698119, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_nature
    "Energy form": (698120, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_energy
    "Bind song": (698121, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_bind
    "Fish form": (698122, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_fish
    "Spirit form": (698123, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_spirit
    "Dual form": (698124, 1, ItemType.PROGRESSION, ItemGroup.SONG),  # song_dual
    "Transturtle Veil top left": (698125, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil01
    "Transturtle Veil top right": (698126, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_veil02
    "Transturtle Open Water top right": (698127, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_openwater03
    "Transturtle Forest bottom left": (698128, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_forest04
    "Transturtle Home water": (698129, 1, ItemType.NORMAL, ItemGroup.TURTLE),  # transport_mainarea
    "Transturtle Abyss right": (698130, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_abyss03
    "Transturtle Final Boss": (698131, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_finalboss
    "Transturtle Simon says": (698132, 1, ItemType.NORMAL, ItemGroup.TURTLE),  # transport_forest05
    "Transturtle Arnassi ruins": (698133, 1, ItemType.PROGRESSION, ItemGroup.TURTLE),  # transport_seahorse
}

