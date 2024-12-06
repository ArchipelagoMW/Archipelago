from worlds.seaofthieves.Items.Items import Items
import typing
from ..Configurations import SotOptionsDerived
from BaseClasses import MultiWorld
import copy
from ..Items.ItemCollection import ItemCollection
from ..Items.Items import Items
from ..Items.ItemDetail import ItemDetail
from ..Regions.RegionDetails import Regions
from ..Regions.ConnectionDetails import ConnectionDetails
from ..Items.ItemReqEvalOr import ItemReqEvalOr
from ..Items.ItemReqEvalAnd import ItemReqEvalAnd
import collections
from itertools import combinations_with_replacement


class RegionDiver:

    def __init__(self):
        # IN form
        # map[reg_start][reg_end] = Item_logic
        self.region_map = {}
        self.visited = set()

        self.initDone = False
        self.items_player_has: typing.Set[str] = set()

    def __can_i_traverse(self, start: typing.Optional[str], end: str, current_items: typing.Set[str]) -> bool:
        if start is None:
            return True
        itm_logic: ItemReqEvalOr = self.region_map[start][end]
        return itm_logic.evaluate(current_items)

    def __dfs_util(self, to_node: str):
        self.visited.clear()
        self.__dfs(to_node, None)

    def __dfs(self, to_node: str, from_node: typing.Optional[str]):
        if (to_node not in self.visited) and self.__can_i_traverse(from_node, to_node, self.items_player_has):
            self.visited.add(to_node)
            # visit here

            # end ^
            if to_node in self.region_map.keys():
                for n in self.region_map[to_node]:
                    self.__dfs(n, to_node)

                    # walk out here

                    # end ^

    def update(self, items: typing.Set[str]):

        # if the items are the same, then the length should not change
        if len(items) == len(self.items_player_has) and self.initDone:
            return

        self.initDone = True
        node = "Menu"
        self.items_player_has = items
        self.__dfs_util(node)

    def get_regions_accessbile(self, items: typing.Set[str]) -> typing.Set[str]:
        self.update(items)
        return self.visited

    def create_from_rules(self, rules: typing.List[ConnectionDetails]):
        for connection_detail in rules:
            # here to there needs these items
            if connection_detail.start.name not in self.region_map.keys():
                self.region_map[connection_detail.start.name] = {}
            self.region_map[connection_detail.start.name][connection_detail.end.name] = connection_detail.itemLogic


def create_rules(options: SotOptionsDerived, world: MultiWorld):
    rules: typing.List[ConnectionDetails] = []

    rules.append(ConnectionDetails(Regions.R_MENU, Regions.R_PLAYER_SHIP, ItemReqEvalOr([])))

    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_OPEN_SEA,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))

    add_rules_sea_2_sea_logic(rules)    # Connects the Sea, Ashen Sea, and the Shared Sea together
    add_rules_sea_2_em(rules)           # Connect Sea to Em Sea
    add_rules_asea_2_aem(rules)
    add_rules_sea_2_islands(rules)      # Connect Sea to islands
    add_rules_asea_2_aislands(rules)
    add_rules_sea_2_fort(rules)         # Connect Sea to forts
    add_rules_asea_2_afort(rules)
    add_rules_sea_2_talltales(rules)    # Connect Sea to tall tales
    add_rules_asea_2_atalltales(rules)
    add_rules_seas_2_shops(rules)       # Connects the Shared sea to the Shops
    add_rules_sea_2_fod(rules, options, world)  # Connect sea to FOD
    add_rules_sea_2_othership(rules)  # Connects sea to other pirate ships
    add_rules_pship_2_onboard(rules)    # Connects player ship to ship contents

    return rules

def add_rules_sea_2_sea_logic(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail_inferno])])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_OPEN_SEA_SHARED, ItemReqEvalOr([])))

def add_rules_sea_2_fod(rules, options: SotOptionsDerived.SotOptionsDerived, world: MultiWorld):
    game_seals: typing.List[ItemDetail] = [
        Items.seal_gh,
        Items.seal_ma,
        Items.seal_af,
        Items.seal_rb,
        Items.seal_oos
    ]

    # generates all valid seal combinations and allows them in logic
    allowable_seal_combinations: typing.List = list(combinations_with_replacement(game_seals, options.menuSettings.fodSealRequirement))
    orable_list: typing.List[ItemReqEvalAnd] = []
    for i in allowable_seal_combinations:
        orable_list.append(ItemReqEvalAnd(i))

    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORT_OF_THE_DAMNED,
                                   ItemReqEvalOr(orable_list)))
def add_rules_sea_2_em(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_DOMAIN_EM,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([Items.emissary_ma]),
                                       ItemReqEvalAnd([Items.emissary_gh]),
                                       ItemReqEvalAnd([Items.emissary_oos]),
                                       ItemReqEvalAnd([Items.emissary_af]),
                                       ItemReqEvalAnd([Items.emissary_rb])]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_AF,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_af, Items.emissary_af]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_RB,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_rb, Items.emissary_rb]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_MA,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_ma, Items.emissary_ma]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GH,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_gh, Items.emissary_gh]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_OOS,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_oos, Items.emissary_oos]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_SV,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.ship_weapons,
                                           Items.personal_weapons, Items.emissary_rb]
                                       )],
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM, Regions.R_DOMAIN_GF,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.ship_weapons,
                                           Items.personal_weapons, Items.emissary_af]
                                       )],
                                   )))
def add_rules_asea_2_aem(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_DOMAIN_EM_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([Items.emissary_ma]),
                                       ItemReqEvalAnd([Items.emissary_gh]),
                                       ItemReqEvalAnd([Items.emissary_oos]),
                                       ItemReqEvalAnd([Items.emissary_af]),
                                       ItemReqEvalAnd([Items.emissary_rb])]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_AF_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_af, Items.emissary_af]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_RB_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_rb, Items.emissary_rb]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_MA_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_ma, Items.emissary_ma]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_GH_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_gh, Items.emissary_gh]
                                       )]
                                   )))
    rules.append(ConnectionDetails(Regions.R_DOMAIN_EM_ASHEN, Regions.R_DOMAIN_OOS_ASHEN,
                                   ItemReqEvalOr([
                                       ItemReqEvalAnd([
                                           Items.sail, Items.voyages_oos, Items.emissary_oos]
                                       )]
                                   )))
def add_rules_asea_2_aislands(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))

def add_rules_asea_2_afort(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))


def add_rules_sea_2_islands(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_ISLANDS,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))

def add_rules_sea_2_fort(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_FORTRESSES,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))
def add_rules_seas_2_shops(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_SHARED, Regions.R_SHOP_ALL, ItemReqEvalOr([ItemReqEvalAnd([])])))

    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_ANCIENT_SPIRE,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_as])])))
    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_DAGGER_TOOTH,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_dt])])))
    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_GALLEONS_GRAVE,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_gg])])))
    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_MORROWS_PEAK,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_mp])])))
    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_PLUNDER_OUTPOST,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_p])])))
    rules.append(ConnectionDetails(Regions.R_SHOP_ALL, Regions.R_SHOP_SANCTUARY_OUTPOST,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.cat_s])])))
def add_rules_sea_2_talltales(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA, Regions.R_DOMAIN_TT,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_tt])])))

def add_rules_asea_2_atalltales(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_ASHEN, Regions.R_DOMAIN_TT_ASHEN,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.voyages_tt])])))
def add_rules_pship_2_onboard(rules):
    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_SHIP_CANNONS,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.ship_weapons, Items.barrel_cannon])])))
    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_SHIP_COOKER,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.stove, Items.barrel_food])])))

def add_rules_pship_2_onboard(rules):
    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_SHIP_CANNONS,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.ship_weapons, Items.barrel_cannon])])))
    rules.append(ConnectionDetails(Regions.R_PLAYER_SHIP, Regions.R_SHIP_COOKER,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.stove, Items.barrel_food])])))
def add_rules_sea_2_othership(rules):
    rules.append(ConnectionDetails(Regions.R_OPEN_SEA_SHARED, Regions.R_OTHER_SHIP,
                                   ItemReqEvalOr([ItemReqEvalAnd([Items.sail])])))