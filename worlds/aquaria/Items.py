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
    LOGIC = 6

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


item_table = {
    """Information data for every (not event) item."""
    #       name:           ID,    Nb,   Item Type,        Item Group
    "collectible_anemone": (0, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_arnassi_statue": (1, 1, ItemType.JUNK,
                                   ItemGroup.COLLECTIBLE),
    "collectible_big_seed": (2, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_bio_seed": (3, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_blackpearl": (4, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_blaster": (5, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_crab_costume": (6, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_dumbo": (7, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_energy_boss": (8, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_energy_statue": (9, 1, ItemType.JUNK,
                                  ItemGroup.COLLECTIBLE),
    "collectible_energy_temple": (10, 1, ItemType.JUNK,
                                  ItemGroup.COLLECTIBLE),
    "collectible_gold_star": (11, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_golden_gear": (12, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_jelly_beacon": (13, 1, ItemType.JUNK,
                                 ItemGroup.COLLECTIBLE),
    "collectible_jelly_costume": (14, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_jelly_plant": (15, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_mithala_doll": (16, 1, ItemType.JUNK,
                                 ItemGroup.COLLECTIBLE),
    "collectible_mithalan_costume": (17, 1, ItemType.JUNK,
                                     ItemGroup.COLLECTIBLE),
    "collectible_mithalas_banner": (18, 1, ItemType.JUNK,
                                    ItemGroup.COLLECTIBLE),
    "collectible_mithalas_pot": (19, 1, ItemType.JUNK,
                                 ItemGroup.COLLECTIBLE),
    "collectible_mutant_costume": (20, 1, ItemType.JUNK,
                                   ItemGroup.COLLECTIBLE),
    "collectible_nautilus": (21, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_piranha": (22, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "collectible_seahorse_costume": (23, 1, ItemType.NORMAL,
                                     ItemGroup.UTILITY),
    "collectible_seed_bag": (24, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_skull": (25, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_spore_seed": (26, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_stone_head": (27, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_sun_key": (28, 1, ItemType.NORMAL, ItemGroup.COLLECTIBLE),
    "collectible_teen_costume": (29, 1, ItemType.JUNK,
                                 ItemGroup.COLLECTIBLE),
    "collectible_treasure_chest": (30, 1, ItemType.JUNK,
                                   ItemGroup.COLLECTIBLE),
    "collectible_trident_head": (31, 1, ItemType.JUNK,
                                 ItemGroup.COLLECTIBLE),
    "collectible_turtle_egg": (32, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "collectible_upsidedown_seed": (33, 1, ItemType.JUNK,
                                    ItemGroup.COLLECTIBLE),
    "collectible_urchin_costume": (34, 1, ItemType.JUNK,
                                   ItemGroup.COLLECTIBLE),
    "collectible_walker": (35, 1, ItemType.JUNK, ItemGroup.COLLECTIBLE),
    "ingredient_Vedha'sCure-All": (36, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_Zuuna'sperogi": (37, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_arcanepoultice": (38, 7, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_berryicecream": (39, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_butterysealoaf": (40, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_coldborscht": (41, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_coldsoup": (42, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_crabcake": (43, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_divinesoup": (44, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_dumboicecream": (45, 3, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_eeloil": (46, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_fishmeat": (47, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_fishoil": (48, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_glowingegg": (49, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_handroll": (50, 5, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_healingpoultice": (51, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_heartysoup": (52, 5, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_hotborscht": (53, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_hotsoup": (54, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "ingredient_icecream": (55, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_leadershiproll": (56, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_leafpoultice": (57, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "ingredient_leechingpoultice": (58, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_legendarycake": (59, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_loafoflife": (60, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_longlifesoup": (61, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_magicsoup": (62, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_mushroom_2": (63, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_perogi": (64, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_plantleaf": (65, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_plumpperogi": (66, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_poisonloaf": (67, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "ingredient_poisonsoup": (68, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "ingredient_rainbowmushroom": (69, 4, ItemType.NORMAL,
                                   ItemGroup.INGREDIENT),
    "ingredient_rainbowsoup": (70, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_redberry": (71, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_redbulb_2": (72, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_rottencake": (73, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "ingredient_rottenloaf_8": (74, 1, ItemType.JUNK, ItemGroup.RECIPE),
    "ingredient_rottenmeat": (75, 5, ItemType.JUNK, ItemGroup.INGREDIENT),
    "ingredient_royalsoup": (76, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_seacake": (77, 4, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_sealoaf": (78, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_sharkfinsoup": (79, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_sightpoultice": (80, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_smallbone_2": (81, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_smallegg": (82, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_smalltentacle_2": (83, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_specialbulb": (84, 5, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_specialcake": (85, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_spicymeat_2": (86, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_spicyroll": (87, 11, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_spicysoup": (88, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_spiderroll": (89, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_swampcake": (90, 3, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_tastycake": (91, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_tastyroll": (92, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_toughcake": (93, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_turtlesoup": (94, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_vedhaseacrisp": (95, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_veggiecake": (96, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_veggieicecream": (97, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_veggiesoup": (98, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_volcanoroll": (99, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "upgrade_health_1": (100, 1, ItemType.NORMAL, ItemGroup.HEALTH),
    "upgrade_health_2": (101, 1, ItemType.NORMAL, ItemGroup.HEALTH),
    "upgrade_health_3": (102, 1, ItemType.NORMAL, ItemGroup.HEALTH),
    "upgrade_health_4": (103, 1, ItemType.NORMAL, ItemGroup.HEALTH),
    "upgrade_health_5": (104, 1, ItemType.NORMAL, ItemGroup.HEALTH),
    "upgrade_wok": (105, 1, ItemType.NORMAL, ItemGroup.UTILITY),
    "ingredient_eeloil_2": (106, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_fishmeat_2": (107, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_fishoil_3": (108, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_glowingegg_2": (109, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_healingpoultice_2": (110, 2, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_hotsoup_2": (111, 3, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "ingredient_leadershiproll_2": (112, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_leafpoultice_3": (113, 1, ItemType.PROGRESSION, ItemGroup.RECIPE),
    "ingredient_plantleaf_2": (114, 2, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_plantleaf_3": (115, 4, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_rottenmeat_2": (116, 1, ItemType.JUNK, ItemGroup.INGREDIENT),
    "ingredient_rottenmeat_8": (117, 1, ItemType.JUNK, ItemGroup.INGREDIENT),
    "ingredient_sealoaf_2": (118, 1, ItemType.NORMAL, ItemGroup.RECIPE),
    "ingredient_smallbone_3": (119, 3, ItemType.NORMAL, ItemGroup.INGREDIENT),
    "ingredient_smallegg_2": (120, 1, ItemType.NORMAL, ItemGroup.INGREDIENT),
}
