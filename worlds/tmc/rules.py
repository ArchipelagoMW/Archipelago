from collections.abc import Callable
from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from worlds.generic.Rules import CollectionRule, add_rule

from .constants import TMCEvent, TMCItem, TMCLocation, TMCRegion, TMCTricks
from .options import Biggoron, DHCAccess, DungeonItem, DungeonWarp, Goal, MinishCapOptions

if TYPE_CHECKING:
    from . import MinishCapWorld


class MinishCapRules:
    player: int
    world: "MinishCapWorld"
    options: MinishCapOptions
    connection_rules: dict[tuple[str, str], CollectionRule]
    region_rules: dict[str, CollectionRule]
    location_rules: dict[str, CollectionRule]

    def __init__(self, world: "MinishCapWorld") -> None:
        self.player = world.player
        self.world = world
        self.options = world.options

        self.connection_rules = {
            # region Connections
            ("Menu", TMCRegion.SOUTH_FIELD): None,
            (TMCRegion.SOUTH_FIELD, TMCRegion.HYRULE_TOWN): None,
            (TMCRegion.SOUTH_FIELD, TMCRegion.EASTERN_HILLS): self.smith_crest(),
            (TMCRegion.SOUTH_FIELD, TMCRegion.SOUTH_PUDDLE):
                self.logic_or([self.can_pass_trees(), self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS])]),
            (TMCRegion.SOUTH_FIELD, TMCRegion.LAKE_HYLIA_NORTH): self.has(TMCItem.OCARINA),
            (TMCRegion.SOUTH_FIELD, TMCRegion.BELARI): self.minish_crest(),
            (TMCRegion.SOUTH_FIELD, TMCRegion.CASTOR_WILDS): self.swamp_crest(),
            (TMCRegion.SOUTH_FIELD, TMCRegion.WIND_TRIBE): self.clouds_crest(),
            (TMCRegion.SOUTH_FIELD, TMCRegion.UPPER_FALLS): self.falls_crest(),
            (TMCRegion.SOUTH_FIELD, TMCRegion.MELARI): self.crenel_crest(),

            (TMCRegion.SOUTH_PUDDLE, TMCRegion.SOUTH_FIELD):
                self.logic_or([self.can_pass_trees(), self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS])]),

            (TMCRegion.HYRULE_TOWN, TMCRegion.NORTH_FIELD): None,
            (TMCRegion.HYRULE_TOWN, TMCRegion.SOUTH_FIELD): None,  # redundant
            (TMCRegion.HYRULE_TOWN, TMCRegion.LONLON): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.HYRULE_TOWN, TMCRegion.TRILBY_HIGHLANDS):
                self.logic_option(TMCTricks.BOOTS_GUARDS in self.world.options.tricks,
                                  self.logic_or([self.can_spin(), self.has(TMCItem.PEGASUS_BOOTS)]),
                                  self.can_spin()),

            (TMCRegion.NORTH_FIELD, TMCRegion.CASTLE_EXTERIOR): None,
            (TMCRegion.NORTH_FIELD, TMCRegion.HYRULE_TOWN): None,  # redundant
            (TMCRegion.NORTH_FIELD, TMCRegion.LONLON): self.can_pass_trees(),
            (TMCRegion.NORTH_FIELD, TMCRegion.TRILBY_HIGHLANDS): self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
            (TMCRegion.NORTH_FIELD, TMCRegion.FALLS_ENTRANCE): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.NORTH_FIELD, TMCRegion.ROYAL_VALLEY):
                self.logic_and([self.split_rule(3, True), self.logic_or([self.cape_extend(), self.has(TMCItem.BOMB_BAG)])]),

            (TMCRegion.CASTLE_EXTERIOR, TMCRegion.NORTH_FIELD): None,  # redundant
            (TMCRegion.CASTLE_EXTERIOR, TMCRegion.SANCTUARY): None,

            (TMCRegion.SANCTUARY, TMCRegion.CASTLE_EXTERIOR): None,  # redundant
            (TMCRegion.SANCTUARY, TMCRegion.STAINED_GLASS): self.pedestal_requirements(),

            (TMCRegion.LONLON, TMCRegion.HYRULE_TOWN): self.has(TMCItem.BOMB_BAG),  # redundant
            (TMCRegion.LONLON, TMCRegion.NORTH_FIELD): self.can_pass_trees(),  # redundant
            (TMCRegion.LONLON, TMCRegion.EASTERN_HILLS): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.LONLON, TMCRegion.MINISH_WOODS): None,  # Doesn't directly connect, but nothing is in between
            (TMCRegion.LONLON, TMCRegion.LOWER_FALLS): self.has(TMCItem.CANE_OF_PACCI),
            (TMCRegion.LONLON, TMCRegion.LAKE_HYLIA_NORTH): self.has(TMCItem.LONLON_KEY),

            (TMCRegion.EASTERN_HILLS, TMCRegion.LONLON): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.EASTERN_HILLS, TMCRegion.BELARI): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.EASTERN_HILLS, TMCRegion.SOUTH_FIELD): self.can_pass_trees(),

            (TMCRegion.LAKE_HYLIA_NORTH, TMCRegion.LONLON): None,
            # allows Ocarina warp access to lonlon and minish woods
            (TMCRegion.LAKE_HYLIA_NORTH, TMCRegion.LAKE_HYLIA_SOUTH): self.cape_extend(),
            (TMCRegion.LAKE_HYLIA_NORTH, TMCRegion.DUNGEON_TOD_ENTRANCE): self.cape_extend(),
            # (TMCRegion.LAKE_HYLIA_SOUTH, TMCRegion.MINISH_WOODS): # Already connected

            (TMCRegion.MINISH_WOODS, TMCRegion.LONLON): None,
            (TMCRegion.MINISH_WOODS, TMCRegion.LAKE_HYLIA_SOUTH):
                self.logic_and([self.access_minish_woods_top_left(), self.has(TMCItem.MOLE_MITTS)]),
            (TMCRegion.MINISH_WOODS, TMCRegion.LAKE_HYLIA_NORTH): self.has(TMCItem.ROCS_CAPE),
            (TMCRegion.MINISH_WOODS, TMCRegion.DUNGEON_DWS_ENTRANCE):
                self.has_any([TMCItem.FLIPPERS, TMCItem.JABBER_NUT]),
            (TMCRegion.MINISH_WOODS, TMCRegion.BELARI): self.has_any([TMCItem.BOMB_BAG, TMCEvent.CLEAR_DWS]),
            (TMCRegion.BELARI, TMCRegion.MINISH_WOODS): None,
            (TMCRegion.BELARI, TMCRegion.EASTERN_HILLS): self.has(TMCItem.BOMB_BAG),

            (TMCRegion.WESTERN_WOODS, TMCRegion.SOUTH_PUDDLE): None,
            (TMCRegion.WESTERN_WOODS, TMCRegion.CASTOR_WILDS): self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]),
            (TMCRegion.WESTERN_WOODS, TMCRegion.TRILBY_HIGHLANDS): None,

            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.HYRULE_TOWN): None,  # redundant
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.NORTH_FIELD):  # redundant
                self.logic_or([self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]),
                               self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.has_sword()])]),
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.WESTERN_WOODS): self.split_rule(2, True),
            (TMCRegion.TRILBY_HIGHLANDS, TMCRegion.CRENEL_BASE): self.has_bottle(),

            (TMCRegion.CRENEL_BASE, TMCRegion.TRILBY_HIGHLANDS): None,
            (TMCRegion.CRENEL_BASE, TMCRegion.CRENEL):
                self.logic_or([self.has(TMCItem.GRIP_RING),
                               self.logic_and([self.has(TMCItem.BOMB_BAG), self.blow_dust(), self.has_bottle()])]),
            (TMCRegion.CRENEL, TMCRegion.CRENEL_BASE): self.has(TMCItem.GRIP_RING),
            (TMCRegion.CRENEL, TMCRegion.MELARI):
                self.logic_or([
                    self.logic_and([self.mushroom(), self.has(TMCItem.CANE_OF_PACCI)]),
                    self.logic_and([
                        self.has(TMCItem.GRIP_RING),
                        self.logic_or([self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE]), self.arrow_break()]),
                        self.logic_or([self.has_bow(), self.has_boomerang(), self.has(TMCItem.BOMB_BAG),
                                       self.logic_option(TMCTricks.BEAM_CRENEL_SWITCH in self.world.options.tricks,
                                                         self.logic_or([self.can_beam(), self.has(TMCItem.ROCS_CAPE)]),
                                                         self.has(TMCItem.ROCS_CAPE))])
                    ])
                ]),
            (TMCRegion.MELARI, TMCRegion.CRENEL): None,
            (TMCRegion.MELARI, TMCRegion.DUNGEON_COF_ENTRANCE): None,

            (TMCRegion.CASTOR_WILDS, TMCRegion.WESTERN_WOODS):
                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
            (TMCRegion.CASTOR_WILDS, TMCRegion.WIND_RUINS):
                self.logic_and([self.has(TMCItem.KINSTONE_GOLD_SWAMP, 3),
                                self.logic_or([self.has(TMCItem.ROCS_CAPE),
                                               self.logic_and([self.has(TMCItem.PEGASUS_BOOTS),
                                                               self.logic_or([self.swamp_crest(), self.has_bow(),
                                                                              self.has(TMCItem.FLIPPERS)])])])]),
            (TMCRegion.WIND_RUINS, TMCRegion.DUNGEON_FOW_ENTRANCE):
                self.logic_and([self.has_sword(), self.has_weapon()]),  # redundancy for later logic improvements

            (TMCRegion.ROYAL_VALLEY, TMCRegion.NORTH_FIELD): None,  # redundant
            (TMCRegion.ROYAL_VALLEY, TMCRegion.TRILBY_HIGHLANDS): None,  # redundant
            (TMCRegion.ROYAL_VALLEY, TMCRegion.GRAVEYARD):
                self.logic_and([self.has_all([TMCItem.GRAVEYARD_KEY, TMCItem.PEGASUS_BOOTS]), self.dark_room()]),
            (TMCRegion.GRAVEYARD, TMCRegion.DUNGEON_RC): self.split_rule(3),
            (TMCRegion.DUNGEON_RC, TMCRegion.DUNGEON_RC_CLEAR):
                self.logic_and([self.has_weapon(), self.has(TMCItem.SMALL_KEY_RC, 3), self.has(TMCItem.LANTERN)]),

            (TMCRegion.FALLS_ENTRANCE, TMCRegion.MIDDLE_FALLS):
                self.logic_and([self.has(TMCItem.KINSTONE_GOLD_FALLS), self.dark_room()]),
            (TMCRegion.MIDDLE_FALLS, TMCRegion.FALLS_ENTRANCE): self.has(TMCItem.FLIPPERS),
            (TMCRegion.MIDDLE_FALLS, TMCRegion.UPPER_FALLS): self.has(TMCItem.GRIP_RING),
            (TMCRegion.UPPER_FALLS, TMCRegion.MIDDLE_FALLS): self.has(TMCItem.GRIP_RING),
            (TMCRegion.UPPER_FALLS, TMCRegion.CLOUDS): self.has(TMCItem.GRIP_RING),
            (TMCRegion.CLOUDS, TMCRegion.UPPER_FALLS): self.has(TMCItem.GRIP_RING),
            (TMCRegion.CLOUDS, TMCRegion.WIND_TRIBE):
                self.logic_and([self.has(TMCItem.KINSTONE_GOLD_CLOUD, 5),
                                self.has_any([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE])]),
            (TMCRegion.WIND_TRIBE, TMCRegion.CLOUDS): None,
            (TMCRegion.WIND_TRIBE, TMCRegion.DUNGEON_POW_ENTRANCE): None,

            (TMCRegion.DUNGEON_DWS_ENTRANCE, TMCRegion.DUNGEON_DWS_BARREL): self.dws_1st_door(),
            (TMCRegion.DUNGEON_DWS_ENTRANCE, TMCRegion.DUNGEON_DWS_BLUE_WARP): self.dws_blue_warp(),
            (TMCRegion.DUNGEON_DWS_BLUE_WARP, TMCRegion.DUNGEON_DWS_BACK_HALF): None,
            (TMCRegion.DUNGEON_DWS_ENTRANCE, TMCRegion.DUNGEON_DWS_RED_WARP): self.dws_red_warp(),
            (TMCRegion.DUNGEON_DWS_BARREL, TMCRegion.DUNGEON_DWS_MULLDOZER): self.has(TMCItem.SMALL_KEY_DWS, 4),
            (TMCRegion.DUNGEON_DWS_BARREL, TMCRegion.DUNGEON_DWS_BACK_HALF): self.dws_2nd_half(),
            (TMCRegion.DUNGEON_DWS_BARREL, TMCRegion.DUNGEON_DWS_RED_WARP):
                self.logic_and([self.has(TMCItem.SMALL_KEY_DWS, 4), self.has(TMCItem.GUST_JAR)]),
            (TMCRegion.DUNGEON_DWS_BACK_HALF, TMCRegion.DUNGEON_DWS_BLUE_WARP): self.blow_dust(),
            (TMCRegion.DUNGEON_DWS_BACK_HALF, TMCRegion.DUNGEON_DWS_BARREL): None,
            (TMCRegion.DUNGEON_DWS_MULLDOZER, TMCRegion.DUNGEON_DWS_BACK_HALF): None,
            (TMCRegion.DUNGEON_DWS_ENTRANCE, TMCRegion.DUNGEON_DWS_CLEAR):
                self.logic_and([self.has_all([TMCItem.BIG_KEY_DWS, TMCItem.GUST_JAR]), self.has_weapon_boss()]),

            (TMCRegion.DUNGEON_COF_ENTRANCE, TMCRegion.DUNGEON_COF_MAIN):
                self.logic_and([
                    self.logic_option(TMCTricks.BOBOMB_WALLS in self.world.options.tricks,
                                      self.logic_or([self.has_sword(), self.has(TMCItem.GUST_JAR)]),
                                      self.has(TMCItem.BOMB_BAG)),
                    self.has_weapon(),  # Spike Beetle Fight
                    self.logic_option(TMCTricks.DOWNTHRUST_BEETLE in self.world.options.tricks,
                                      self.logic_or([self.can_shield(),
                                                     self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG]),
                                                     self.downthrust()]),  # Allow Downthrust when true
                                      self.logic_or([self.can_shield(),
                                                     self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.BOMB_BAG])]))
                ]),
            (TMCRegion.DUNGEON_COF_MAIN, TMCRegion.DUNGEON_COF_MINECART):
                self.logic_and([self.logic_option(self.world.options.dungeon_warp_cof.has_blue,
                                                  self.has(TMCItem.SMALL_KEY_COF, 2),
                                                  self.has(TMCItem.SMALL_KEY_COF, 1)),
                                self.has_sword()]),
            (TMCRegion.DUNGEON_COF_MINECART, TMCRegion.DUNGEON_COF_BLUE_WARP):
                self.logic_and([self.has_weapon(), self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE])]),
            (TMCRegion.DUNGEON_COF_ENTRANCE, TMCRegion.DUNGEON_COF_BLUE_WARP): self.cof_blue_warp(),
            (TMCRegion.DUNGEON_COF_BLUE_WARP, TMCRegion.DUNGEON_COF_MINECART): self.has(TMCItem.CANE_OF_PACCI),
            (TMCRegion.DUNGEON_COF_BLUE_WARP, TMCRegion.DUNGEON_COF_LAVA_BASEMENT):
                self.logic_and([self.has_sword(), self.has(TMCItem.SMALL_KEY_COF, 2), self.has(TMCItem.CANE_OF_PACCI)]),
            (TMCRegion.DUNGEON_COF_ENTRANCE, TMCRegion.DUNGEON_COF_LAVA_BASEMENT): self.cof_red_warp(),
            (TMCRegion.DUNGEON_COF_LAVA_BASEMENT, TMCRegion.DUNGEON_COF_CLEAR):
                self.logic_and([self.has_sword(), self.has_weapon_gleerok_mazaal(),
                                self.has_all([TMCItem.CANE_OF_PACCI, TMCItem.BIG_KEY_COF])]),

            (TMCRegion.DUNGEON_FOW_ENTRANCE, TMCRegion.DUNGEON_FOW_EYEGORE): self.has_bow(),
            (TMCRegion.DUNGEON_FOW_ENTRANCE, TMCRegion.DUNGEON_FOW_BLUE_WARP): self.fow_blue_warp(),
            (TMCRegion.DUNGEON_FOW_EYEGORE, TMCRegion.DUNGEON_FOW_BLUE_WARP): self.has(TMCItem.SMALL_KEY_FOW, 4),
            (TMCRegion.DUNGEON_FOW_BLUE_WARP, TMCRegion.DUNGEON_FOW_EYEGORE): None,
            (TMCRegion.DUNGEON_FOW_ENTRANCE, TMCRegion.DUNGEON_FOW_CLEAR):
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.has_bow(),
                                self.has(TMCItem.BIG_KEY_FOW), self.has_weapon_gleerok_mazaal()]),

            (TMCRegion.DUNGEON_TOD_ENTRANCE, TMCRegion.DUNGEON_TOD_LEFT_BASEMENT): self.tod_blue_warp(),
            (TMCRegion.DUNGEON_TOD_ENTRANCE, TMCRegion.DUNGEON_TOD_WEST_SWITCH_LEDGE): self.tod_red_warp(),
            (TMCRegion.DUNGEON_TOD_ENTRANCE, TMCRegion.DUNGEON_TOD_MAIN): self.has(TMCItem.BIG_KEY_TOD),
            (TMCRegion.DUNGEON_TOD_WEST_SWITCH_LEDGE, TMCRegion.DUNGEON_TOD_MAIN): None,
            (TMCRegion.DUNGEON_TOD_LEFT_BASEMENT, TMCRegion.DUNGEON_TOD_MAIN): None,
            (TMCRegion.DUNGEON_TOD_MAIN, TMCRegion.DUNGEON_TOD_LEFT_BASEMENT):
                self.logic_and([self.has_tod_4_keys(), self.has_all([TMCItem.FLIPPERS, TMCItem.GUST_JAR])]),
            (TMCRegion.DUNGEON_TOD_MAIN, TMCRegion.DUNGEON_TOD_DARK_MAZE_END):
                self.logic_and([self.has(TMCItem.LANTERN), self.has_weapon_scissor(), self.has_tod_4_keys()]),
            (TMCRegion.DUNGEON_TOD_LEFT_BASEMENT, TMCRegion.DUNGEON_TOD_DARK_MAZE_END): self.has(TMCItem.ROCS_CAPE),
            (TMCRegion.DUNGEON_TOD_DARK_MAZE_END, TMCRegion.DUNGEON_TOD_LEFT_BASEMENT): self.has(TMCItem.ROCS_CAPE),
            (TMCRegion.DUNGEON_TOD_DARK_MAZE_END, TMCRegion.DUNGEON_TOD_WEST_SWITCH_LEDGE):
                self.logic_and(
                    [self.split_rule(2), self.has_all([TMCItem.LANTERN, TMCItem.BOMB_BAG]), self.cape_extend()]
            ),
            (TMCRegion.DUNGEON_TOD_LEFT_BASEMENT, TMCRegion.DUNGEON_TOD_EAST_SWITCH): self.split_rule(2),
            (TMCRegion.DUNGEON_TOD_WEST_SWITCH_LEDGE, TMCRegion.DUNGEON_TOD_WEST_SWITCH): self.split_rule(2),
            (TMCRegion.DUNGEON_TOD_MAIN, TMCRegion.DUNGEON_TOD_CLEAR):
                self.logic_and([self.logic_or([self.can_shield(), self.has_sword()]),
                                self.has_all(
                                    [TMCEvent.DROPLETS_WEST_SWITCH, TMCEvent.DROPLETS_EAST_SWITCH, TMCItem.LANTERN])]),

            (TMCRegion.DUNGEON_POW_ENTRANCE, TMCRegion.DUNGEON_POW_BLUE_WARP): self.pow_blue_warp(),
            (TMCRegion.DUNGEON_POW_ENTRANCE, TMCRegion.DUNGEON_POW_RED_WARP): self.pow_red_warp(),
            (TMCRegion.DUNGEON_POW_ENTRANCE, TMCRegion.DUNGEON_POW_OUT_1F):
                self.logic_and([self.split_rule(3),
                                self.logic_or([self.can_hit_distance(),
                                               self.has_any([TMCItem.ROCS_CAPE, TMCItem.GUST_JAR])])]),
            (TMCRegion.DUNGEON_POW_OUT_1F, TMCRegion.DUNGEON_POW_OUT_2F): self.pow_jump(),
            (TMCRegion.DUNGEON_POW_OUT_2F, TMCRegion.DUNGEON_POW_OUT_3F):
                self.logic_and([self.split_rule(3), self.has(TMCItem.ROCS_CAPE)]),
            (TMCRegion.DUNGEON_POW_OUT_3F, TMCRegion.DUNGEON_POW_OUT_4F):
                self.logic_and([self.pow_1st_door(), self.has(TMCItem.ROCS_CAPE)]),
            (TMCRegion.DUNGEON_POW_OUT_4F, TMCRegion.DUNGEON_POW_OUT_5F): self.has(TMCItem.ROCS_CAPE),
            (TMCRegion.DUNGEON_POW_OUT_5F, TMCRegion.DUNGEON_POW_BLUE_WARP):
                self.logic_and([self.has(TMCItem.BIG_KEY_POW), self.has_weapon_boss()]),
            (TMCRegion.DUNGEON_POW_BLUE_WARP, TMCRegion.DUNGEON_POW_IN_1F): self.dark_room(),
            (TMCRegion.DUNGEON_POW_IN_1F, TMCRegion.DUNGEON_POW_IN_2F): None,
            (TMCRegion.DUNGEON_POW_IN_2F, TMCRegion.DUNGEON_POW_IN_1F): self.dark_room(),
            (TMCRegion.DUNGEON_POW_IN_2F, TMCRegion.DUNGEON_POW_IN_3F):
                self.logic_and([self.pow_2nd_door(), self.has(TMCItem.ROCS_CAPE)]),
            (TMCRegion.DUNGEON_POW_IN_3F, TMCRegion.DUNGEON_POW_IN_2F): None,
            (TMCRegion.DUNGEON_POW_IN_3F, TMCRegion.DUNGEON_POW_IN_3F_SWITCH):
                self.logic_and([self.has_sword(), self.has_boomerang(), self.has_bow(),
                                self.has_any([TMCItem.GUST_JAR, TMCItem.BOMB_BAG])]),
            (TMCRegion.DUNGEON_POW_IN_3F, TMCRegion.DUNGEON_POW_IN_4F): self.has_weapon(),
            (TMCRegion.DUNGEON_POW_IN_4F, TMCRegion.DUNGEON_POW_IN_3F): None,
            (TMCRegion.DUNGEON_POW_IN_4F, TMCRegion.DUNGEON_POW_RED_WARP):
                self.logic_and([self.has(TMCItem.ROCS_CAPE), self.can_hit_distance()]),
            (TMCRegion.DUNGEON_POW_RED_WARP, TMCRegion.DUNGEON_POW_IN_3F): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.DUNGEON_POW_RED_WARP, TMCRegion.DUNGEON_POW_IN_4F):
                self.has_all([TMCItem.BOMB_BAG, TMCItem.ROCS_CAPE]),
            (TMCRegion.DUNGEON_POW_RED_WARP, TMCRegion.DUNGEON_POW_IN_5F):
                self.logic_and([self.pow_red_warp_door(), self.has(TMCItem.BOMB_BAG)]),
            (TMCRegion.DUNGEON_POW_IN_5F, TMCRegion.DUNGEON_POW_IN_3F): None,
            (TMCRegion.DUNGEON_POW_IN_5F, TMCRegion.DUNGEON_POW_IN_4F_END): self.pow_last_door(),
            (TMCRegion.DUNGEON_POW_IN_4F_END, TMCRegion.DUNGEON_POW_IN_5F_END): self.has(TMCItem.ROCS_CAPE),
            (TMCRegion.DUNGEON_POW_IN_4F_END, TMCRegion.DUNGEON_POW_CLEAR):
                self.logic_and([self.has(TMCItem.ROCS_CAPE), self.has(TMCItem.BIG_KEY_POW), self.split_rule(3)]),

            (TMCRegion.STAINED_GLASS, TMCRegion.VAATI_FIGHT):
                self.logic_option(self.world.options.dhc_access.value == DHCAccess.option_closed and
                                  self.world.options.goal.value == Goal.option_vaati,
                                  self.logic_and([
                                      self.has_all([TMCItem.GUST_JAR, TMCItem.CANE_OF_PACCI]),
                                      self.dark_room(),  # Don't make people do the final boss in the dark
                                      self.has_bow(),
                                      self.split_rule(4),
                                  ]),
                                  self.no_access()),
            (TMCRegion.STAINED_GLASS, TMCRegion.DUNGEON_DHC_B1_WEST):
                self.logic_option(self.world.options.dhc_access.value != DHCAccess.option_closed,
                                  None,
                                  self.no_access()),
            (TMCRegion.CASTLE_EXTERIOR, TMCRegion.DUNGEON_DHC_ENTRANCE):
                self.logic_option(self.world.options.dhc_access.value == DHCAccess.option_open,
                                  None,
                                  self.no_access()),

            (TMCRegion.DUNGEON_DHC_B1_WEST, TMCRegion.SANCTUARY): None,  # Ped items
            (TMCRegion.DUNGEON_DHC_B1_WEST, TMCRegion.DUNGEON_DHC_B2): self.has(TMCItem.BOMB_BAG),
            (TMCRegion.DUNGEON_DHC_B1_WEST, TMCRegion.DUNGEON_DHC_ENTRANCE): None,
            (TMCRegion.DUNGEON_DHC_B2, TMCRegion.DUNGEON_DHC_B1_WEST): None,  # redundant
            (TMCRegion.DUNGEON_DHC_ENTRANCE, TMCRegion.DUNGEON_DHC_B1_WEST): None,  # Ped items
            (TMCRegion.DUNGEON_DHC_ENTRANCE, TMCRegion.CASTLE_EXTERIOR): None,  # redundant
            (TMCRegion.DUNGEON_DHC_ENTRANCE, TMCRegion.DUNGEON_DHC_BLUE_WARP): self.dhc_blue_warp(),
            (TMCRegion.DUNGEON_DHC_ENTRANCE, TMCRegion.DUNGEON_DHC_RED_WARP): self.dhc_red_warp(),
            (TMCRegion.DUNGEON_DHC_ENTRANCE, TMCRegion.DUNGEON_DHC_B1_EAST):
                self.logic_and([self.dhc_door(), self.dhc_cannons(), self.has(TMCItem.BOMB_BAG)]),
            (TMCRegion.DUNGEON_DHC_B1_EAST, TMCRegion.DUNGEON_DHC_1F): self.has_weapon_boss(),
            (TMCRegion.DUNGEON_DHC_1F, TMCRegion.DUNGEON_DHC_OUTSIDE): None,
            (TMCRegion.DUNGEON_DHC_OUTSIDE, TMCRegion.DUNGEON_DHC_RED_WARP):
                self.logic_and([self.split_rule(4), self.dhc_switch_gap(), self.has_weapon()]),
            (TMCRegion.DUNGEON_DHC_RED_WARP, TMCRegion.DUNGEON_DHC_BLUE_WARP):
                self.logic_and([self.has(TMCItem.ROCS_CAPE), self.dhc_switch_gap(),
                                self.has_any([TMCItem.BOMB_BAG, TMCItem.GUST_JAR]), self.has_weapon_boss()]),
            (TMCRegion.DUNGEON_DHC_RED_WARP, TMCRegion.VAATI_FIGHT):
                self.logic_and([
                    self.has_all([TMCItem.BIG_KEY_DHC, TMCItem.GUST_JAR, TMCItem.CANE_OF_PACCI]),
                    self.has_weapon_boss(),  # Darknut
                    self.split_rule(4),
                    self.has_bow(),
                    self.dark_room(),  # Don't make people do the final boss in the dark
                ]),
            # endregion
        }

        self.location_rules = {
            # region South Field
            TMCLocation.SMITH_HOUSE_CHEST: None,
            TMCLocation.SMITH_HOUSE_SWORD: None,
            TMCLocation.SMITH_HOUSE_SHIELD: None,
            TMCLocation.SOUTH_FIELD_MINISH_SIZE_WATER_HOLE_HP:
                self.logic_and([self.can_pass_trees(), self.has_all([TMCItem.PEGASUS_BOOTS, TMCItem.FLIPPERS])]),
            # All the following require Fusion 58
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM1: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM2: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM3: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM4: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM5: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM6: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM7: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM8: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM9: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM10: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM11: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM12: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM13: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM14: None,
            TMCLocation.SOUTH_FIELD_PUDDLE_FUSION_ITEM15: None,
            TMCLocation.SOUTH_FIELD_FUSION_CHEST: None,  # Fusion 53
            TMCLocation.SOUTH_FIELD_TREE_FUSION_HP: None,  # Fusion 32
            TMCLocation.SOUTH_FIELD_TINGLE_NPC: self.has_all([TMCItem.CANE_OF_PACCI, TMCItem.TINGLE_TROPHY]),
            # endregion

            # region Hyrule Town
            TMCLocation.TOWN_CAFE_LADY_NPC: None,
            TMCLocation.TOWN_SHOP_80_ITEM: self.cost(80),
            TMCLocation.TOWN_SHOP_300_ITEM: self.cost(300),
            TMCLocation.TOWN_SHOP_600_ITEM: self.cost(600),
            TMCLocation.TOWN_SHOP_EXTRA_600_ITEM: self.cost(600),
            TMCLocation.TOWN_SHOP_BEHIND_COUNTER_ITEM: self.access_town_left(),
            TMCLocation.TOWN_SHOP_ATTIC_CHEST: self.access_town_left(),
            TMCLocation.TOWN_BAKERY_ATTIC_CHEST: self.access_town_left(),
            TMCLocation.TOWN_INN_BACKDOOR_HP: self.access_town_left(),
            TMCLocation.TOWN_INN_LEDGE_CHEST: self.has(TMCItem.LANTERN),
            TMCLocation.TOWN_INN_POT: None,
            TMCLocation.TOWN_WELL_RIGHT_CHEST: None,

            # Fusion 33
            TMCLocation.TOWN_GORON_MERCHANT_1_LEFT: self.cost(300 if self.options.goron_jp_prices.value else 200),
            TMCLocation.TOWN_GORON_MERCHANT_1_MIDDLE: self.cost(200 if self.options.goron_jp_prices.value else 100),
            TMCLocation.TOWN_GORON_MERCHANT_1_RIGHT: self.cost(50),
            # Fusion 33
            TMCLocation.TOWN_GORON_MERCHANT_2_LEFT: self.cost(300),
            TMCLocation.TOWN_GORON_MERCHANT_2_MIDDLE: self.cost(300 if self.options.goron_jp_prices.value else 200),
            TMCLocation.TOWN_GORON_MERCHANT_2_RIGHT: self.cost(300 if self.options.goron_jp_prices.value else 200),
            # Fusion 33
            TMCLocation.TOWN_GORON_MERCHANT_3_LEFT: self.cost(300 if self.options.goron_jp_prices.value else 400),
            TMCLocation.TOWN_GORON_MERCHANT_3_MIDDLE: self.cost(300),
            TMCLocation.TOWN_GORON_MERCHANT_3_RIGHT: self.cost(300),
            # Fusion 33
            TMCLocation.TOWN_GORON_MERCHANT_4_LEFT: self.cost(300 if self.options.goron_jp_prices.value else 500),
            TMCLocation.TOWN_GORON_MERCHANT_4_MIDDLE: self.cost(300 if self.options.goron_jp_prices.value else 400),
            TMCLocation.TOWN_GORON_MERCHANT_4_RIGHT: self.cost(300 if self.options.goron_jp_prices.value else 400),
            # Fusion 33
            TMCLocation.TOWN_GORON_MERCHANT_5_LEFT: self.cost(300 if self.options.goron_jp_prices.value else 600),
            TMCLocation.TOWN_GORON_MERCHANT_5_MIDDLE: self.cost(300 if self.options.goron_jp_prices.value else 500),
            TMCLocation.TOWN_GORON_MERCHANT_5_RIGHT: self.cost(300 if self.options.goron_jp_prices.value else 500),
            TMCLocation.TOWN_DOJO_NPC_1: self.has_sword(),
            TMCLocation.TOWN_DOJO_NPC_2:
                self.logic_or([self.has(TMCItem.WHITE_SWORD_GREEN), self.has(TMCItem.PROGRESSIVE_SWORD, 2)]),
            TMCLocation.TOWN_DOJO_NPC_3: self.logic_and([self.has_sword(), self.has(TMCItem.PEGASUS_BOOTS)]),
            TMCLocation.TOWN_DOJO_NPC_4: self.logic_and([self.has_sword(), self.has(TMCItem.ROCS_CAPE)]),
            TMCLocation.TOWN_WELL_TOP_CHEST: self.has(TMCItem.BOMB_BAG),
            TMCLocation.TOWN_SCHOOL_ROOF_CHEST: self.has(TMCItem.CANE_OF_PACCI),
            TMCLocation.TOWN_SCHOOL_PATH_FUSION_CHEST: self.has(TMCItem.CANE_OF_PACCI),  # Fusion 36
            TMCLocation.TOWN_SCHOOL_PATH_LEFT_CHEST:
                self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.split_rule(4)]),
            TMCLocation.TOWN_SCHOOL_PATH_MIDDLE_CHEST:
                self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.split_rule(4)]),
            TMCLocation.TOWN_SCHOOL_PATH_RIGHT_CHEST:
                self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.split_rule(4)]),
            TMCLocation.TOWN_SCHOOL_PATH_HP:
                self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.split_rule(4)]),
            TMCLocation.TOWN_DIGGING_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TOWN_DIGGING_TOP_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TOWN_DIGGING_RIGHT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TOWN_WELL_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TOWN_BELL_HP: self.has(TMCItem.ROCS_CAPE),
            TMCLocation.TOWN_WATERFALL_FUSION_CHEST: self.has(TMCItem.FLIPPERS),  # Fusion 42
            TMCLocation.TOWN_CARLOV_NPC: self.access_town_left(),
            TMCLocation.TOWN_WELL_BOTTOM_CHEST: self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]),
            TMCLocation.TOWN_CUCCOS_LV_1_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_2_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_3_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_4_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_5_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_6_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_7_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_8_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_9_NPC: None,
            TMCLocation.TOWN_CUCCOS_LV_10_NPC: self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]),
            TMCLocation.TOWN_JULLIETA_ITEM: self.logic_and([self.access_town_left(), self.has_bottle()]),
            TMCLocation.TOWN_SIMULATION_CHEST: self.logic_and([self.has_sword(), self.cost(10)]),
            TMCLocation.TOWN_SHOE_SHOP_NPC: self.has(TMCItem.WAKEUP_MUSHROOM),
            TMCLocation.TOWN_MUSIC_HOUSE_LEFT_CHEST: self.has(TMCItem.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_MIDDLE_CHEST: self.has(TMCItem.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_RIGHT_CHEST: self.has(TMCItem.CARLOV_MEDAL),
            TMCLocation.TOWN_MUSIC_HOUSE_HP: self.has(TMCItem.CARLOV_MEDAL),
            TMCLocation.TOWN_WELL_PILLAR_CHEST:
                self.logic_and([
                    self.has(TMCItem.MOLE_MITTS),
                    self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]),
                    self.split_rule(3, True),
                ]),
            TMCLocation.TOWN_DR_LEFT_ATTIC_ITEM:
                self.logic_and([
                    self.access_town_left(),
                    self.has_all([TMCItem.POWER_BRACELETS, TMCItem.GUST_JAR]),
                    self.split_rule(2),
                ]),
            TMCLocation.TOWN_FOUNTAIN_BIG_CHEST:
                self.logic_and([self.has_weapon(), self.access_town_fountain(), self.has(TMCItem.CANE_OF_PACCI)]),
            TMCLocation.TOWN_FOUNTAIN_SMALL_CHEST:
                self.logic_and([self.access_town_fountain(), self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE])]),
            TMCLocation.TOWN_FOUNTAIN_HP: self.logic_and([self.access_town_fountain(), self.has(TMCItem.ROCS_CAPE)]),
            TMCLocation.TOWN_LIBRARY_YELLOW_MINISH_NPC: self.complete_book_quest(),
            TMCLocation.TOWN_UNDER_LIBRARY_FROZEN_CHEST:
                self.has_all([TMCItem.OCARINA, TMCItem.CANE_OF_PACCI, TMCItem.FLIPPERS, TMCItem.LANTERN]),
            TMCLocation.TOWN_UNDER_LIBRARY_BIG_CHEST:
                self.logic_and([
                    self.logic_or([self.logic_and([self.complete_book_quest(), self.has(TMCItem.GRIP_RING),
                                                   self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
                                   self.has_all([TMCItem.OCARINA, TMCItem.CANE_OF_PACCI, TMCItem.FLIPPERS])]),
                    self.has_weapon_scissor(),
                ]),
            TMCLocation.TOWN_UNDER_LIBRARY_UNDERWATER:
                self.has_all([TMCItem.OCARINA, TMCItem.CANE_OF_PACCI, TMCItem.FLIPPERS]),
            # endregion

            # region North Field
            TMCLocation.NORTH_FIELD_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.NORTH_FIELD_HP: self.logic_or([self.has(TMCItem.BOMB_BAG), self.cape_extend()]),
            TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_LEFT_CHEST: None,  # Fusion 59
            TMCLocation.NORTH_FIELD_TREE_FUSION_TOP_RIGHT_CHEST: None,  # Fusion 40
            TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_LEFT_CHEST: None,  # Fusion 4D
            TMCLocation.NORTH_FIELD_TREE_FUSION_BOTTOM_RIGHT_CHEST: None,  # Fusion 5A
            TMCLocation.NORTH_FIELD_TREE_FUSION_CENTER_BIG_CHEST: None,  # All of the above
            TMCLocation.NORTH_FIELD_WATERFALL_FUSION_DOJO_NPC:  # Fusion 15
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_sword()]),
            # endregion

            # region Castle Gardens
            TMCLocation.CASTLE_MOAT_LEFT_CHEST: self.has(TMCItem.FLIPPERS),
            TMCLocation.CASTLE_MOAT_RIGHT_CHEST: self.has(TMCItem.FLIPPERS),
            TMCLocation.CASTLE_GOLDEN_ROPE: self.has_sword(),  # Fusion 3C
            TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_HP: None,  # Fusion 18
            TMCLocation.CASTLE_DOJO_HP: None,
            TMCLocation.CASTLE_DOJO_NPC: self.logic_and([self.has(TMCItem.LANTERN), self.has_sword()]),
            TMCLocation.CASTLE_RIGHT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: self.has(TMCItem.PEGASUS_BOOTS),  # Fusion 18
            TMCLocation.CASTLE_LEFT_FOUNTAIN_FUSION_MINISH_HOLE_CHEST: self.has(TMCItem.PEGASUS_BOOTS),  # Fusion 35
            # endregion

            # region Eastern Hills
            # Can Pass Trees
            TMCLocation.HILLS_GOLDEN_ROPE: self.has_sword(),  # Fusion 55
            TMCLocation.HILLS_FUSION_CHEST: None,  # Fusion 16
            TMCLocation.HILLS_BEANSTALK_FUSION_LEFT_CHEST: None,  # Fusion 2E
            TMCLocation.HILLS_BEANSTALK_FUSION_HP: None,  # Fusion 2E
            TMCLocation.HILLS_BEANSTALK_FUSION_RIGHT_CHEST: None,  # Fusion 2E
            TMCLocation.HILLS_BOMB_CAVE_CHEST: self.has(TMCItem.BOMB_BAG),
            TMCLocation.MINISH_GREAT_FAIRY_NPC: self.has(TMCItem.CANE_OF_PACCI),
            TMCLocation.HILLS_FARM_DIG_CAVE_ITEM: self.has(TMCItem.MOLE_MITTS),
            # endregion

            # region LonLon
            # Can Pass Trees
            TMCLocation.LON_LON_RANCH_POT: None,
            TMCLocation.LON_LON_PUDDLE_FUSION_BIG_CHEST: self.access_lonlon_right(),  # Fusion 1E
            TMCLocation.LON_LON_CAVE_CHEST: self.logic_and([self.access_lonlon_right(), self.split_rule(2, True)]),
            TMCLocation.LON_LON_CAVE_SECRET_CHEST:
                self.logic_and([self.access_lonlon_right(), self.split_rule(2, True),
                                self.has_all([TMCItem.BOMB_BAG, TMCItem.LANTERN])]),
            TMCLocation.LON_LON_PATH_FUSION_CHEST:  # Fusion 50
                self.logic_and([self.access_lonlon_right(), self.has(TMCItem.PEGASUS_BOOTS)]),
            TMCLocation.LON_LON_PATH_HP: self.logic_and([self.access_lonlon_right(), self.has(TMCItem.PEGASUS_BOOTS)]),
            TMCLocation.LON_LON_DIG_SPOT:
                self.logic_and([self.access_lonlon_right(), self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
                                self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.LON_LON_NORTH_MINISH_CRACK_CHEST:
                self.logic_and([self.access_lonlon_right(), self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE])]),
            TMCLocation.LON_LON_GORON_CAVE_FUSION_SMALL_CHEST: self.access_minish_woods_top_left(),
            # 4 of Fusion 25, 26, 29, 2A, 2B, 2F
            TMCLocation.LON_LON_GORON_CAVE_FUSION_BIG_CHEST: self.access_minish_woods_top_left(),
            # 6 of Fusion 25, 26, 29, 2A, 2B, 2F
            # endregion

            # region Lower Falls
            TMCLocation.FALLS_LOWER_LON_LON_FUSION_CHEST: None,  # Fusion 60
            TMCLocation.FALLS_LOWER_HP: None,
            TMCLocation.FALLS_LOWER_WATERFALL_FUSION_DOJO_NPC:  # Fusion 1D
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_sword()]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM1: self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM2: self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_ROCK_ITEM3: self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
            TMCLocation.FALLS_LOWER_DIG_CAVE_LEFT_CHEST:
                self.logic_and([self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.FALLS_LOWER_DIG_CAVE_RIGHT_CHEST:
                self.logic_and([
                    self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
                    self.has(TMCItem.MOLE_MITTS),
                ]),
            # endregion

            # region Lake Hylia
            TMCLocation.HYLIA_SUNKEN_HP: self.has(TMCItem.FLIPPERS),
            TMCLocation.HYLIA_DOG_NPC: self.has(TMCItem.DOG_FOOD),
            TMCLocation.HYLIA_SMALL_ISLAND_HP: self.has(TMCItem.ROCS_CAPE),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_RIGHT: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_LEFT: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_LEFT: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_TOP_MIDDLE: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_RIGHT: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_RIGHT: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_BOTTOM_MIDDLE: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_CAPE_CAVE_LON_LON_HP: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_BEANSTALK_FUSION_LEFT_CHEST:  # Fusion 23
                self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_BEANSTALK_FUSION_HP: self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),  # Fusion 23
            TMCLocation.HYLIA_BEANSTALK_FUSION_RIGHT_CHEST:  # Fusion 23
                self.has_all([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.HYLIA_MIDDLE_ISLAND_FUSION_DIG_CAVE_CHEST:  # Fusion 34
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.cape_extend()]),
            TMCLocation.HYLIA_BOTTOM_HP: self.cape_extend(),
            TMCLocation.HYLIA_DOJO_HP: self.cape_extend(),
            TMCLocation.HYLIA_DOJO_NPC:
                self.logic_and([self.cape_extend(), self.has_max_health(10), self.has_sword()]),
            TMCLocation.HYLIA_CRACK_FUSION_LIBRARI_NPC:  # fusion 12
                self.logic_and([self.has(TMCItem.OCARINA), self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE])]),
            TMCLocation.HYLIA_NORTH_MINISH_HOLE_CHEST: self.logic_and([self.lake_minish(), self.has(TMCItem.FLIPPERS)]),
            TMCLocation.HYLIA_SOUTH_MINISH_HOLE_CHEST: self.logic_and([self.lake_minish(), self.has(TMCItem.FLIPPERS)]),
            TMCLocation.HYLIA_CABIN_PATH_FUSION_CHEST:  # Fusion 51
                self.logic_and([self.lake_minish(), self.cabin_swim()]),
            TMCLocation.HYLIA_MAYOR_CABIN_ITEM:
                self.logic_and([self.lake_minish(), self.cabin_swim(), self.has(TMCItem.POWER_BRACELETS)]),
            # endregion

            # region Minish Woods
            # Can Pass Trees
            TMCLocation.MINISH_WOODS_GOLDEN_OCTO:  # Fusion 56
                self.logic_and([self.access_minish_woods_top_left(), self.has_sword()]),
            TMCLocation.MINISH_WOODS_WITCH_HUT_ITEM:
                self.logic_and([self.access_minish_woods_top_left(), self.cost(60)]),
            TMCLocation.WITCH_DIGGING_CAVE_CHEST:
                self.logic_and([self.access_minish_woods_top_left(), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.MINISH_WOODS_NORTH_FUSION_CHEST: self.access_minish_woods_top_left(),  # fusion 44
            TMCLocation.MINISH_WOODS_TOP_HP: self.access_minish_woods_top_left(),
            TMCLocation.MINISH_WOODS_WEST_FUSION_CHEST: None,  # fusion 47
            TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_LEFT_CHEST:
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.likelike()]),
            TMCLocation.MINISH_WOODS_LIKE_LIKE_DIGGING_CAVE_RIGHT_CHEST:
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.likelike()]),
            TMCLocation.MINISH_WOODS_EAST_FUSION_CHEST: None,  # fusion 46
            TMCLocation.MINISH_WOODS_SOUTH_FUSION_CHEST: None,  # fusion 39
            TMCLocation.MINISH_WOODS_BOTTOM_HP: None,
            TMCLocation.MINISH_WOODS_CRACK_FUSION_CHEST: None,  # fusion 4E
            TMCLocation.MINISH_WOODS_MINISH_PATH_FUSION_CHEST: None,  # fusion 37
            TMCLocation.MINISH_VILLAGE_BARREL_HOUSE_ITEM: None,
            TMCLocation.MINISH_VILLAGE_HP: None,
            TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_1: None,
            TMCLocation.MINISH_WOODS_BOMB_MINISH_NPC_2: None,  # fusion 1C
            TMCLocation.MINISH_WOODS_POST_VILLAGE_FUSION_CHEST: None,  # Fusion 38
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_MIDDLE_CHEST: self.has(TMCItem.FLIPPERS),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_RIGHT_CHEST: self.has(TMCItem.FLIPPERS),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_LEFT_CHEST: self.has(TMCItem.FLIPPERS),
            TMCLocation.MINISH_WOODS_FLIPPER_HOLE_HP: self.has(TMCItem.FLIPPERS),
            # endregion

            # region Trilby Highlands
            # Can Spin / Flippers / Roc's Cape
            TMCLocation.TRILBY_MIDDLE_FUSION_CHEST: None,  # fusion 5E
            TMCLocation.TRILBY_TOP_FUSION_CHEST: None,  # fusion 52
            TMCLocation.TRILBY_DIG_CAVE_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TRILBY_DIG_CAVE_RIGHT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.TRILBY_DIG_CAVE_WATER_FUSION_CHEST:  # fusion 22
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS])]),
            TMCLocation.TRILBY_SCRUB_NPC:
                self.logic_and([self.can_shield(), self.has(TMCItem.BOMB_BAG), self.cost(20)]),
            # endregion

            # region Western Woods
            TMCLocation.TRILBY_BOMB_CAVE_CHEST: self.has(TMCItem.BOMB_BAG),
            # Everything below require Fusion 3F
            # They also are part of the western wood region
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM1: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM2: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM3: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM4: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM5: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM6: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM7: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM8: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM9: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM10: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM11: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM12: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM13: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM14: None,
            TMCLocation.TRILBY_PUDDLE_FUSION_ITEM15: None,

            TMCLocation.WESTERN_WOODS_FUSION_CHEST: None,  # fusion 3A
            TMCLocation.WESTERN_WOODS_TREE_FUSION_HP: None,  # fusion 11
            TMCLocation.WESTERN_WOODS_TOP_DIG1: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG2: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG3: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG4: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG5: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_TOP_DIG6: self.has(TMCItem.MOLE_MITTS),  # fusion 48
            TMCLocation.WESTERN_WOODS_PERCY_FUSION_MOBLIN: self.has(TMCItem.LANTERN),  # fusion 21
            TMCLocation.WESTERN_WOODS_PERCY_FUSION_PERCY: self.has(TMCItem.LANTERN),  # fusion 21
            TMCLocation.WESTERN_WOODS_BOTTOM_DIG1: self.has(TMCItem.MOLE_MITTS),  # fusion 4C
            TMCLocation.WESTERN_WOODS_BOTTOM_DIG2: self.has(TMCItem.MOLE_MITTS),  # fusion 4C
            TMCLocation.WESTERN_WOODS_GOLDEN_OCTO: self.has_sword(),  # fusion 3D
            # All the following require Fusion 24
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_CHEST: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM1: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM2: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM3: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM4: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM5: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM6: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM7: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM8: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM9: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM10: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM11: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM12: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM13: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM14: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM15: None,
            TMCLocation.WESTERN_WOODS_BEANSTALK_FUSION_ITEM16: None,
            # endregion

            # region Crenel
            # Crenel Base = bottle
            TMCLocation.CRENEL_BASE_ENTRANCE_VINE: None,  # Assigned to Trilby so it doesn't require bottle
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM1: self.has(TMCItem.BOMB_BAG),
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM2: self.has(TMCItem.BOMB_BAG),
            TMCLocation.CRENEL_BASE_FAIRY_CAVE_ITEM3: self.has(TMCItem.BOMB_BAG),
            TMCLocation.CRENEL_BASE_GREEN_WATER_FUSION_CHEST: self.has(TMCItem.BOMB_BAG),  # Fusion 4F
            TMCLocation.CRENEL_BASE_WEST_FUSION_CHEST: self.has_any([TMCItem.BOMB_BAG, TMCItem.ROCS_CAPE]),  # Fusion 63
            TMCLocation.CRENEL_BASE_WATER_CAVE_LEFT_CHEST: self.has(TMCItem.BOMB_BAG),
            # can alternatively require cape if the bomb wall is broken
            TMCLocation.CRENEL_BASE_WATER_CAVE_RIGHT_CHEST: self.has(TMCItem.BOMB_BAG),
            # can alternatively require cape if the bomb wall is broken
            TMCLocation.CRENEL_BASE_WATER_CAVE_HP: self.has(TMCItem.BOMB_BAG),
            # can alternatively require cape/flippers if the bomb wall is broken
            TMCLocation.CRENEL_BASE_MINISH_VINE_HOLE_CHEST:
                self.logic_and([self.has_any([TMCItem.BOMB_BAG, TMCItem.ROCS_CAPE]), self.blow_dust()]),
            TMCLocation.CRENEL_BASE_MINISH_CRACK_CHEST:
                self.logic_and([self.has_any([TMCItem.BOMB_BAG, TMCItem.ROCS_CAPE]), self.blow_dust()]),
            TMCLocation.CRENEL_VINE_TOP_GOLDEN_TEKTITE: self.has_sword(),  # Fusion 3B
            TMCLocation.CRENEL_BRIDGE_CAVE_CHEST: self.has(TMCItem.BOMB_BAG),
            TMCLocation.CRENEL_FAIRY_CAVE_HP: self.has(TMCItem.BOMB_BAG),
            TMCLocation.CRENEL_BELOW_COF_GOLDEN_TEKTITE:  # Fusion 0D
                self.logic_and([self.has_sword(), self.mushroom()]),
            TMCLocation.CRENEL_SCRUB_NPC:
                self.logic_and([self.has(TMCItem.BOMB_BAG), self.can_shield(), self.cost(40), self.mushroom()]),
            TMCLocation.CRENEL_DOJO_LEFT_CHEST:
                self.logic_and([self.has(TMCItem.GRIP_RING), self.split_rule(2, True)]),
            TMCLocation.CRENEL_DOJO_RIGHT_CHEST:
                self.logic_and([self.has(TMCItem.GRIP_RING), self.split_rule(2, True)]),
            TMCLocation.CRENEL_DOJO_HP:
                self.logic_and([self.has(TMCItem.GRIP_RING), self.split_rule(2, True)]),
            TMCLocation.CRENEL_DOJO_NPC:
                self.logic_and([self.has(TMCItem.GRIP_RING), self.split_rule(2, True)]),
            TMCLocation.CRENEL_GREAT_FAIRY_NPC: self.has_all([TMCItem.GRIP_RING, TMCItem.BOMB_BAG]),
            TMCLocation.CRENEL_CLIMB_FUSION_CHEST:  # Fusion 62
                self.has_all([TMCItem.GRIP_RING, TMCItem.BOMB_BAG]),
            TMCLocation.CRENEL_DIG_CAVE_HP: self.has_all([TMCItem.GRIP_RING, TMCItem.MOLE_MITTS]),
            TMCLocation.CRENEL_BEANSTALK_FUSION_HP: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM1: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM2: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM3: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM4: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM5: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM6: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM7: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_BEANSTALK_FUSION_ITEM8: self.has(TMCItem.GRIP_RING),  # Fusion 1A
            TMCLocation.CRENEL_RAIN_PATH_FUSION_CHEST: self.has(TMCItem.GRIP_RING),  # Fusion 43
            # endregion

            # region Melari
            TMCLocation.CRENEL_UPPER_BLOCK_CHEST: None,
            TMCLocation.CRENEL_MINES_PATH_FUSION_CHEST: None,  # Fusion 45
            TMCLocation.CRENEL_MELARI_LEFT_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_MIDDLE_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_LEFT_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_TOP_RIGHT_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_RIGHT_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_MIDDLE_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_BOTTOM_LEFT_DIG: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CRENEL_MELARI_CENTER_DIG: self.has(TMCItem.MOLE_MITTS),
            # endregion

            # region Castor Wilds
            TMCLocation.SWAMP_BUTTERFLY_FUSION_ITEM: None,  # Fusion 10
            TMCLocation.SWAMP_CENTER_CAVE_DARKNUT_CHEST: self.has_weapon_boss(),
            TMCLocation.SWAMP_CENTER_CHEST: self.has_bow(),
            TMCLocation.SWAMP_GOLDEN_ROPE: self.has_sword(),  # Fusion 49
            TMCLocation.SWAMP_NEAR_WATERFALL_CAVE_HP:
                self.logic_and([self.has_bow(), self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS])]),
            TMCLocation.SWAMP_WATERFALL_FUSION_DOJO_NPC:  # Fusion 0C
                self.logic_and([self.has_bow(), self.has(TMCItem.FLIPPERS)]),
            TMCLocation.SWAMP_NORTH_CAVE_CHEST: self.has_bow(),
            TMCLocation.SWAMP_DIGGING_CAVE_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.SWAMP_DIGGING_CAVE_RIGHT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.SWAMP_UNDERWATER_TOP: self.has(TMCItem.FLIPPERS),
            TMCLocation.SWAMP_UNDERWATER_MIDDLE: self.has(TMCItem.FLIPPERS),
            TMCLocation.SWAMP_UNDERWATER_BOTTOM: self.has(TMCItem.FLIPPERS),
            TMCLocation.SWAMP_SOUTH_CAVE_CHEST:
                self.logic_or([self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]), self.has_bow()]),
            TMCLocation.SWAMP_DOJO_HP:
                self.logic_or([self.has(TMCItem.ROCS_CAPE), self.has_bow(),
                               self.has_all([TMCItem.PEGASUS_BOOTS, TMCItem.FLIPPERS]),
                               self.logic_and([self.swamp_crest(), self.has(TMCItem.PEGASUS_BOOTS)])]),
            TMCLocation.SWAMP_DOJO_NPC:
                self.logic_and([self.logic_or([self.has(TMCItem.ROCS_CAPE), self.has_bow(),
                                               self.has_all([TMCItem.PEGASUS_BOOTS, TMCItem.FLIPPERS]),
                                               self.logic_and([self.swamp_crest(), self.has(TMCItem.PEGASUS_BOOTS)])]),
                                self.has_sword(),
                                self.has_group("Scrolls", 7)]),
            TMCLocation.SWAMP_MINISH_FUSION_NORTH_CRACK_CHEST:  # Fusion 4B
                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
            TMCLocation.SWAMP_MINISH_MULLDOZER_BIG_CHEST:
                self.logic_and([
                    self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
                    self.has_any([TMCItem.FLIPPERS, TMCItem.GUST_JAR]),
                    self.has_weapon(),
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_NORTH_WEST_CRACK_CHEST:  # Fusion 5B
                self.logic_and([
                    self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
                    self.has_any([TMCItem.FLIPPERS, TMCItem.GUST_JAR])
                ]),
            TMCLocation.SWAMP_MINISH_FUSION_WEST_CRACK_CHEST:  # Fusion 57
                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
            TMCLocation.SWAMP_MINISH_FUSION_VINE_CRACK_CHEST:  # Fusion 57 & 3E
                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]), self.has_bow()]),
            TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_CHEST:  # Fusion 57
                self.logic_and([self.has(TMCItem.FLIPPERS),
                                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]),
                                               self.has_bow()])]),
            TMCLocation.SWAMP_MINISH_FUSION_WATER_HOLE_HP:  # Fusion 57
                self.logic_and([self.has(TMCItem.FLIPPERS),
                                self.logic_or([self.has_any([TMCItem.PEGASUS_BOOTS, TMCItem.ROCS_CAPE]),
                                               self.has_bow()])]),
            # endregion

            # region Wind Ruins
            # Fusion 06 07 08
            TMCLocation.RUINS_BUTTERFLY_FUSION_ITEM: None,  # Fusion 20
            TMCLocation.RUINS_BOMB_CAVE_CHEST: self.has(TMCItem.BOMB_BAG),
            TMCLocation.RUINS_MINISH_HOME_CHEST: None,
            # Everything beyond here requires at least 1 sword to pass the first armos
            TMCLocation.RUINS_PILLARS_FUSION_CHEST: self.has_sword(),  # Fusion 64
            TMCLocation.RUINS_BEAN_STALK_FUSION_BIG_CHEST:  # Fusion 17
                self.logic_and([self.has_sword(), self.has_weapon()]),
            TMCLocation.RUINS_CRACK_FUSION_CHEST: self.logic_and([self.has_sword(), self.has_weapon()]),  # Fusion 41
            TMCLocation.RUINS_MINISH_CAVE_HP: self.logic_and([self.has_sword(), self.has_weapon()]),
            TMCLocation.RUINS_ARMOS_KILL_LEFT_CHEST: self.logic_and([self.has_sword(), self.has_weapon()]),
            TMCLocation.RUINS_ARMOS_KILL_RIGHT_CHEST: self.logic_and([self.has_sword(), self.has_weapon()]),
            TMCLocation.RUINS_GOLDEN_OCTO: self.logic_and([self.has_sword(), self.has_weapon()]),  # Fusion 54
            TMCLocation.RUINS_NEAR_FOW_FUSION_CHEST: self.logic_and([self.has_sword(), self.has_weapon()]),  # Fusion 0A
            # endregion

            # region Royal Valley
            TMCLocation.VALLEY_PRE_VALLEY_FUSION_CHEST: None,  # Fusion 5F
            TMCLocation.VALLEY_GREAT_FAIRY_NPC: self.has(TMCItem.BOMB_BAG),
            TMCLocation.VALLEY_LOST_WOODS_CHEST: self.dark_room(),
            TMCLocation.VALLEY_DAMPE_NPC: self.dark_room(),
            # Graveyard locations, require graveyard key and pegasus boots
            TMCLocation.VALLEY_GRAVEYARD_BUTTERFLY_FUSION_ITEM: None,  # Fusion 19
            TMCLocation.VALLEY_GRAVEYARD_LEFT_FUSION_CHEST: None,  # Fusion 5C
            TMCLocation.VALLEY_GRAVEYARD_LEFT_GRAVE_HP: self.split_rule(3, True),
            TMCLocation.VALLEY_GRAVEYARD_RIGHT_FUSION_CHEST: None,  # Fusion 5D
            TMCLocation.VALLEY_GRAVEYARD_RIGHT_GRAVE_FUSION_CHEST: None,  # Fusion 30
            # endregion

            # region Dungeon RC
            TMCLocation.CRYPT_GIBDO_LEFT_ITEM: self.logic_or([self.has(TMCItem.LANTERN), self.has_weapon()]),
            TMCLocation.CRYPT_GIBDO_RIGHT_ITEM: self.logic_or([self.has(TMCItem.LANTERN), self.has_weapon()]),
            TMCLocation.CRYPT_LEFT_ITEM: self.logic_and([self.split_rule(3), self.has(TMCItem.SMALL_KEY_RC, 1)]),
            TMCLocation.CRYPT_RIGHT_ITEM: self.logic_and([self.split_rule(3), self.has(TMCItem.SMALL_KEY_RC, 1)]),
            # endregion

            # region Upper Falls
            # The first 3 are part of North Field logic, doesn't require falls fusion stone or lantern
            TMCLocation.FALLS_ENTRANCE_HP: self.cape_extend(),
            TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_HP:  # Fusion 1F
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.cape_extend()]),
            TMCLocation.FALLS_WATER_DIG_CAVE_FUSION_CHEST:  # Fusion 1F
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.cape_extend()]),
            # Fusion 09
            # TMCLocation.FALLS_1ST_CAVE_CHEST: None,
            TMCLocation.FALLS_CLIFF_CHEST: self.split_rule(3, True),
            TMCLocation.FALLS_SOUTH_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FALLS_GOLDEN_TEKTITE: self.has_sword(),  # Fusion 4A
            TMCLocation.FALLS_NORTH_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            # TMCLocation.FALLS_ROCK_FUSION_CHEST: None,  # Fusion 61
            TMCLocation.FALLS_WATERFALL_FUSION_HP: self.has(TMCItem.FLIPPERS),  # Fusion 13
            # TMCLocation.FALLS_RUPEE_CAVE_TOP_TOP: None,
            # TMCLocation.FALLS_RUPEE_CAVE_TOP_LEFT: None,
            # TMCLocation.FALLS_RUPEE_CAVE_TOP_MIDDLE: None,
            # TMCLocation.FALLS_RUPEE_CAVE_TOP_RIGHT: None,
            # TMCLocation.FALLS_RUPEE_CAVE_TOP_BOTTOM: None,
            # TMCLocation.FALLS_RUPEE_CAVE_SIDE_TOP: None,
            # TMCLocation.FALLS_RUPEE_CAVE_SIDE_LEFT: None,
            # TMCLocation.FALLS_RUPEE_CAVE_SIDE_RIGHT: None,
            # TMCLocation.FALLS_RUPEE_CAVE_SIDE_BOTTOM: None,
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_LEFT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_TOP_RIGHT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_LEFT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_MIDDLE_RIGHT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_LEFT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_RUPEE_CAVE_UNDERWATER_BOTTOM_RIGHT: self.has(TMCItem.FLIPPERS),
            TMCLocation.FALLS_TOP_CAVE_BOMB_WALL_CHEST: self.has(TMCItem.BOMB_BAG),
            # TMCLocation.FALLS_TOP_CAVE_CHEST: None,
            # endregion

            # region Cloud Tops
            TMCLocation.FALLS_BIGGORON: self.can_shield(self.options.shuffle_biggoron.value == Biggoron.option_mirror_shield),
            TMCLocation.CLOUDS_FREE_CHEST: None,
            TMCLocation.CLOUDS_NORTH_EAST_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_KILL:
                self.logic_and([self.has_any([TMCItem.ROCS_CAPE, TMCItem.MOLE_MITTS]), self.shark_kill()]),
            TMCLocation.CLOUDS_NORTH_WEST_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_RIGHT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_NORTH_WEST_BOTTOM_CHEST: self.has_any([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_MIDDLE_CHEST: self.has_any([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_MIDDLE_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_KILL:
                self.logic_and([self.has_any([TMCItem.ROCS_CAPE, TMCItem.MOLE_MITTS]), self.shark_kill()]),
            TMCLocation.CLOUDS_SOUTH_RIGHT_CHEST: self.has_any([TMCItem.MOLE_MITTS, TMCItem.ROCS_CAPE]),
            TMCLocation.CLOUDS_SOUTH_RIGHT_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_EAST_BOTTOM_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.CLOUDS_SOUTH_EAST_TOP_DIG_SPOT: self.has(TMCItem.MOLE_MITTS),
            # endregion

            # region Wind Tribe
            # Doesn't require many special access rules *yet*
            # 1F-2F is accessible due to open fusions
            # Fusion 0F
            TMCLocation.WIND_TRIBE_1F_LEFT_CHEST: None,
            TMCLocation.WIND_TRIBE_1F_RIGHT_CHEST: None,
            TMCLocation.WIND_TRIBE_2F_CHEST: None,
            TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_1: self.has(TMCItem.GUST_JAR),
            # Here starts the rules that require access to Cloudtops/Wind Tribe
            # Fusion 01 02 03 04 05
            TMCLocation.WIND_TRIBE_2F_GREGAL_NPC_2: self.has(TMCItem.GUST_JAR),
            TMCLocation.WIND_TRIBE_3F_LEFT_CHEST: None,
            TMCLocation.WIND_TRIBE_3F_CENTER_CHEST: None,
            TMCLocation.WIND_TRIBE_3F_RIGHT_CHEST: None,
            TMCLocation.WIND_TRIBE_4F_LEFT_CHEST: None,
            TMCLocation.WIND_TRIBE_4F_RIGHT_CHEST: None,
            # endregion

            # region Dungeon DWS Entrance
            TMCLocation.DEEPWOOD_2F_CHEST: self.has_any([TMCItem.LANTERN, TMCItem.GUST_JAR]),
            TMCLocation.DEEPWOOD_1F_SLUG_TORCHES_CHEST: None,
            # endregion

            # region Dungeon DWS Barrel
            TMCLocation.DEEPWOOD_1F_BARREL_ROOM_CHEST: self.blow_dust(),
            TMCLocation.DEEPWOOD_1F_WEST_BIG_CHEST: None,
            TMCLocation.DEEPWOOD_1F_WEST_STATUE_PUZZLE_CHEST: None,
            # endregion

            # region Dungeon DWS East
            TMCLocation.DEEPWOOD_1F_EAST_MULLDOZER_FIGHT_ITEM: self.has_weapon(),
            # endregion

            # region Dungeon DWS Backside
            TMCLocation.DEEPWOOD_1F_NORTH_EAST_CHEST: self.blow_dust(),
            TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_BIG_CHEST: None,
            TMCLocation.DEEPWOOD_B1_SWITCH_ROOM_CHEST: self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE]),
            TMCLocation.DEEPWOOD_1F_BLUE_WARP_LEFT_CHEST: self.blow_dust(),
            TMCLocation.DEEPWOOD_1F_BLUE_WARP_RIGHT_CHEST: self.blow_dust(),
            TMCLocation.DEEPWOOD_1F_MADDERPILLAR_BIG_CHEST:
                self.logic_and([self.has_weapon_boss(),
                                self.logic_or([self.has(TMCItem.SMALL_KEY_DWS, 4), self.has(TMCItem.LANTERN)])]),
            TMCLocation.DEEPWOOD_1F_MADDERPILLAR_HP:
                self.logic_or([self.logic_and([self.has(TMCItem.SMALL_KEY_DWS, 4), self.has(TMCItem.GUST_JAR)]),
                               self.has(TMCItem.LANTERN)]),
            # endregion

            # region Dungeon DWS Blue Warp
            TMCLocation.DEEPWOOD_1F_BLUE_WARP_HP: None,
            # endregion

            # region Dungeon DWS Red Warp
            TMCLocation.DEEPWOOD_B1_WEST_BIG_CHEST: None,
            # endregion

            # region Dungeon DWS Boss
            TMCLocation.DEEPWOOD_BOSS_ITEM: None,
            TMCLocation.DEEPWOOD_PRIZE: None,
            # endregion

            # region Dungeon COF Main
            TMCLocation.COF_1F_SPIKE_BEETLE_BIG_CHEST: None,
            TMCLocation.COF_1F_ITEM1: None,
            TMCLocation.COF_1F_ITEM2: None,
            TMCLocation.COF_1F_ITEM3: None,
            TMCLocation.COF_1F_ITEM4: None,
            TMCLocation.COF_1F_ITEM5: None,  # FUTURE: grabbed through wall
            TMCLocation.COF_B1_HAZY_ROOM_BIG_CHEST: self.has_weapon_helm_ghini(),
            TMCLocation.COF_B1_HAZY_ROOM_SMALL_CHEST: self.has_weapon_helm_ghini(),
            TMCLocation.COF_B1_ROLLOBITE_CHEST: self.has_weapon_helm_ghini(),
            TMCLocation.COF_B1_ROLLOBITE_PILLAR_CHEST: self.has_weapon_helm_ghini(),
            # endregion

            # region Dungeon COF Minecart Ride
            TMCLocation.COF_B1_SPIKEY_CHUS_PILLAR_CHEST: self.has(TMCItem.CANE_OF_PACCI),
            TMCLocation.COF_B1_HP: self.has(TMCItem.BOMB_BAG),
            TMCLocation.COF_B1_SPIKEY_CHUS_BIG_CHEST: self.has_weapon(),
            # endregion

            # region Dungeon COF Lava Basement
            TMCLocation.COF_B2_PRE_LAVA_NORTH_CHEST: self.has(TMCItem.CANE_OF_PACCI),
            TMCLocation.COF_B2_PRE_LAVA_SOUTH_CHEST: self.has(TMCItem.CANE_OF_PACCI),
            TMCLocation.COF_B2_LAVA_ROOM_BLADE_CHEST: self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
            TMCLocation.COF_B2_LAVA_ROOM_RIGHT_CHEST: self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
            TMCLocation.COF_B2_LAVA_ROOM_LEFT_CHEST: self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
            TMCLocation.COF_B2_LAVA_ROOM_BIG_CHEST: self.has_any([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
            # endregion

            # region Dungeon COF Boss
            TMCLocation.COF_BOSS_ITEM: None,
            TMCLocation.COF_PRIZE: None,
            # FUTURE: Dungeon Entrance Rando
            TMCLocation.CRENEL_MELARI_NPC: self.can_reach([TMCLocation.CRENEL_UPPER_BLOCK_CHEST]),
            # endregion

            # region Dungeon FOW Entrance
            TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FORTRESS_ENTRANCE_1F_LEFT_WIZZROBE_CHEST:
                self.logic_and([self.has(TMCItem.MOLE_MITTS), self.has_weapon_wizzrobe()]),
            TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_ITEM: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FORTRESS_LEFT_2F_DIG_CHEST:
                self.logic_and([self.has_bow(), self.has_weapon(), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM1: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM2: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM3: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM4: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM5: self.logic_and([self.has_bow(), self.has_weapon()]),
            # FUTURE: Item 5 can get grabbed through the wall
            TMCLocation.FORTRESS_LEFT_2F_ITEM6: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_2F_ITEM7: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_3F_SWITCH_CHEST:
                self.logic_and([self.has_bow(), self.has_weapon(), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.FORTRESS_LEFT_3F_EYEGORE_BIG_CHEST: self.logic_and([self.has_bow(), self.has_weapon()]),
            TMCLocation.FORTRESS_LEFT_3F_ITEM_DROP:
                self.logic_and([self.has_bow(), self.has_weapon(),
                                self.logic_or([self.has(TMCItem.ROCS_CAPE), self.split_rule(2)])]),
            TMCLocation.FORTRESS_MIDDLE_2F_STATUE_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FORTRESS_RIGHT_2F_LEFT_CHEST: None,
            TMCLocation.FORTRESS_RIGHT_2F_RIGHT_CHEST: None,
            TMCLocation.FORTRESS_RIGHT_2F_DIG_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FORTRESS_RIGHT_3F_DIG_CHEST: self.has(TMCItem.MOLE_MITTS),
            TMCLocation.FORTRESS_RIGHT_3F_ITEM_DROP: self.split_rule(2),
            TMCLocation.FORTRESS_ENTRANCE_1F_RIGHT_HP: self.split_rule(2),
            TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_BOTTOM_POT:
                self.logic_or([self.fow_pot(),
                               self.logic_and([self.has(TMCItem.SMALL_KEY_FOW, 3), self.has(TMCItem.MOLE_MITTS),
                                               self.logic_or([self.has_bow(), self.fow_blue_warp()])])]),
            # endregion

            # region Dungeon FOW Past Blue Warp
            TMCLocation.FORTRESS_BACK_LEFT_BIG_CHEST: self.has(TMCItem.BOMB_BAG),
            TMCLocation.FORTRESS_BACK_LEFT_SMALL_CHEST: self.has_all([TMCItem.BOMB_BAG, TMCItem.MOLE_MITTS]),
            # endregion

            # region Dungeon FOW Past Eyegores
            TMCLocation.FORTRESS_MIDDLE_2F_BIG_CHEST: None,
            TMCLocation.FORTRESS_BACK_RIGHT_STATUE_ITEM_DROP:
                self.logic_and([self.has(TMCItem.SMALL_KEY_FOW, 2), self.split_rule(2)]),
            TMCLocation.FORTRESS_BACK_RIGHT_MINISH_ITEM_DROP:
                self.logic_and([self.has(TMCItem.SMALL_KEY_FOW, 3), self.has_weapon(), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.FORTRESS_BACK_RIGHT_DIG_ROOM_TOP_POT:
                self.logic_and([self.has(TMCItem.SMALL_KEY_FOW, 3), self.has(TMCItem.MOLE_MITTS)]),
            TMCLocation.FORTRESS_BACK_RIGHT_BIG_CHEST:
                self.logic_and([self.has(TMCItem.SMALL_KEY_FOW, 4), self.has(TMCItem.MOLE_MITTS)]),
            # endregion

            # region Dungeon FOW Boss
            TMCLocation.FORTRESS_BOSS_ITEM: None,
            TMCLocation.FORTRESS_PRIZE: None,
            # endregion

            # region Dungeon TOD Entrance
            TMCLocation.DROPLETS_ENTRANCE_B2_EAST_ICEBLOCK: None,
            TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK: self.tod_west_iceblock_rule(),
            # endregion

            # region Dungeon TOD After Big Key
            TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM1: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM2: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM3: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM4: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_UNDERPASS_ITEM5: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_BIG_CHEST: None,
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER1: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER2: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER3: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER4: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER5: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B1_WATERFALL_UNDERWATER6: self.has(TMCItem.FLIPPERS),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER1:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER2:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER3:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER4:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER5:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_WATERFALL_UNDERWATER6:
                self.logic_and([self.has(TMCItem.FLIPPERS), self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_UNDERWATER_POT:
                self.logic_and([self.has(TMCItem.FLIPPERS),
                                self.logic_or([self.tod_blue_warp(),
                                               self.has_any([TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])])]),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_1ST_CHEST: self.tod_right_ice(),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_2ND_CHEST: self.tod_right_ice(),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_POT: self.tod_right_ice(),
            TMCLocation.DROPLETS_RIGHT_PATH_B3_FROZEN_CHEST: self.tod_right_ice(),
            TMCLocation.DROPLETS_RIGHT_PATH_B1_BLU_CHU_BIG_CHEST:
                self.logic_and([self.tod_right_ice(), self.has(TMCItem.SMALL_KEY_TOD, 4), self.has(TMCItem.GUST_JAR),
                                self.has_weapon_boss()]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_FROZEN_CHEST: self.has(TMCItem.LANTERN),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_BOTTOM_CHEST:
                self.logic_and([self.has_weapon_scissor(), self.has(TMCItem.LANTERN)]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_MULLDOZERS_ITEM_DROP:
                self.logic_and([self.has_weapon_scissor(), self.has_weapon(),  # redundancy for future settings
                                self.has_all([TMCItem.LANTERN, TMCItem.BOMB_BAG])]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_RIGHT_CHEST:
                self.logic_and([self.has_weapon_scissor(), self.has(TMCItem.LANTERN)]),
            TMCLocation.DROPLETS_RIGHT_PATH_B2_DARK_MAZE_TOP_LEFT_CHEST:
                self.logic_and([self.has_weapon_scissor(), self.has(TMCItem.LANTERN)]),
            # endregion

            # region Dungeon TOD Lilypad Basement
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_MADDERPILLAR_BIG_CHEST:
                self.logic_and([self.has_weapon_boss(), self.has(TMCItem.GUST_JAR)]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_FROZEN_CHEST:
                self.logic_and([self.has(TMCItem.LANTERN),
                                self.has_any([TMCItem.FLIPPERS, TMCItem.GUST_JAR, TMCItem.ROCS_CAPE])]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_ICE_PLAIN_CHEST:
                self.has_any([TMCItem.FLIPPERS, TMCItem.GUST_JAR, TMCItem.ROCS_CAPE]),
            TMCLocation.DROPLETS_LEFT_PATH_B2_LILYPAD_CORNER_FROZEN_CHEST:
                self.has_all([TMCItem.GUST_JAR, TMCItem.LANTERN]),
            # end region

            # region Dungeon TOD Dark Maze End
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM1: None,
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM2: None,
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM3: None,
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM4: None,
            TMCLocation.DROPLETS_RIGHT_PATH_B2_UNDERPASS_ITEM5: None,
            # endregion

            # region Dungeon TOD Boss
            TMCLocation.DROPLETS_BOSS_ITEM: None,
            TMCLocation.DROPLETS_PRIZE: None,
            # endregion

            # region Dungeon POW 1st Half 1F
            TMCLocation.PALACE_1ST_HALF_1F_GRATE_CHEST: self.has(TMCItem.ROCS_CAPE),
            TMCLocation.PALACE_1ST_HALF_1F_WIZZROBE_BIG_CHEST:
                self.logic_and([self.has_weapon_wizzrobe(),
                                self.logic_or([self.has_boomerang(),
                                               self.has_any([TMCItem.ROCS_CAPE, TMCItem.BOMB_BAG])])]),
            # endregion

            # region Dungeon POW 1st Half 2F
            TMCLocation.PALACE_1ST_HALF_2F_ITEM1: None,
            TMCLocation.PALACE_1ST_HALF_2F_ITEM2: None,
            TMCLocation.PALACE_1ST_HALF_2F_ITEM3: None,
            TMCLocation.PALACE_1ST_HALF_2F_ITEM4: None,
            TMCLocation.PALACE_1ST_HALF_2F_ITEM5: None,
            # endregion

            # region Dungeon POW 1st Half 3F
            TMCLocation.PALACE_1ST_HALF_3F_POT_PUZZLE_ITEM_DROP:
                self.logic_and([self.has(TMCItem.CANE_OF_PACCI), self.pow_pot()]),
            # endregion

            # region Dungeon POW 1st Half 4F
            TMCLocation.PALACE_1ST_HALF_4F_BOW_MOBLINS_CHEST: None,
            # endregion

            # region Dungeon POW 1st Half 5F
            TMCLocation.PALACE_1ST_HALF_5F_BALL_AND_CHAIN_SOLDIERS_ITEM_DROP: self.has_weapon(),
            TMCLocation.PALACE_1ST_HALF_5F_FAN_LOOP_CHEST:
                self.logic_and([self.has(TMCItem.ROCS_CAPE), self.has(TMCItem.SMALL_KEY_POW, 5), self.has_weapon()]),
            TMCLocation.PALACE_1ST_HALF_5F_BIG_CHEST: self.has(TMCItem.SMALL_KEY_POW, 6),
            # endregion

            # region Dungeon POW 2nd Half 1F
            TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_BIG_CHEST: None,
            # endregion

            # region Dungeon POW 2nd Half 2F
            TMCLocation.PALACE_2ND_HALF_1F_DARK_ROOM_SMALL_CHEST: None,
            TMCLocation.PALACE_2ND_HALF_2F_MANY_ROLLERS_CHEST:
                self.logic_and([self.split_rule(3), self.has(TMCItem.ROCS_CAPE)]),  # FUTURE: Bomb Trick
            # endregion

            # region Dungeon POW 2nd Half 3F
            TMCLocation.PALACE_2ND_HALF_2F_TWIN_WIZZROBES_CHEST: self.has_weapon_wizzrobe(),
            TMCLocation.PALACE_2ND_HALF_3F_FIRE_WIZZROBES_BIG_CHEST: self.has_weapon_wizzrobe(),
            # endregion

            # region Dungeon POW 2nd Half 4F
            TMCLocation.PALACE_2ND_HALF_4F_HP: self.has(TMCItem.ROCS_CAPE),
            TMCLocation.PALACE_2ND_HALF_4F_SWITCH_HIT_CHEST: self.pow_red_chest(),
            # endregion

            # region Dungeon POW End
            TMCLocation.PALACE_2ND_HALF_5F_BOMBAROSSA_CHEST: None,
            TMCLocation.PALACE_2ND_HALF_4F_BLOCK_MAZE_CHEST: None,
            TMCLocation.PALACE_2ND_HALF_5F_RIGHT_SIDE_CHEST: None,
            # endregion

            # region Dungeon POW Boss
            TMCLocation.PALACE_BOSS_ITEM: None,
            TMCLocation.PALACE_PRIZE: None,
            # endregion

            # region Sanctuary
            TMCLocation.PEDESTAL_REQUIREMENT_REWARD: self.pedestal_requirements(),
            TMCLocation.SANCTUARY_PEDESTAL_ITEM1: self.has_group("Elements", 2),
            TMCLocation.SANCTUARY_PEDESTAL_ITEM2: self.has_group("Elements", 3),
            TMCLocation.SANCTUARY_PEDESTAL_ITEM3: self.has_group("Elements", 4),
            # endregion

            # region Dungeon DHC B2
            TMCLocation.DHC_B2_KING: self.split_rule(4),
            # endregion

            # region Dungeon DHC B1
            TMCLocation.DHC_B1_BIG_CHEST: None,
            # endregion

            # region Dungeon DHC Entrance
            TMCLocation.DHC_1F_BLADE_CHEST: self.logic_and([self.dhc_cannons(), self.dhc_pads()]),
            # endregion

            # region Dungeon DHC 1F
            TMCLocation.DHC_1F_THRONE_BIG_CHEST: None,
            # endregion

            # region Dungeon DHC Blue Warp
            TMCLocation.DHC_3F_NORTH_WEST_CHEST: self.logic_and([self.has_weapon_boss(), self.has_bow()]),
            TMCLocation.DHC_3F_NORTH_EAST_CHEST: self.logic_and([self.has_weapon_boss(), self.has(TMCItem.LANTERN)]),
            TMCLocation.DHC_3F_SOUTH_WEST_CHEST: self.logic_and([self.has_weapon_boss(), self.dhc_south_towers()]),
            TMCLocation.DHC_3F_SOUTH_EAST_CHEST:
                self.logic_and([self.has_weapon_boss(), self.dhc_south_towers(), self.dhc_spin()]),
            TMCLocation.DHC_2F_BLUE_WARP_BIG_CHEST:
                self.logic_and([self.has(TMCItem.SMALL_KEY_DHC, 5), self.split_rule(4)]),
            # endregion
        }

    @staticmethod
    def no_access() -> CollectionRule:
        # return self.has(TMCItem.INACCESSIBLE)
        return lambda state: False

    @staticmethod
    def logic_or(rules: list[CollectionRule | None]) -> CollectionRule | None:
        for entry in rules:
            if entry is None:
                return None

        return lambda state: any(rule(state) for rule in rules)

    @staticmethod
    def logic_and(rules: list[CollectionRule | None]) -> CollectionRule:
        return lambda state: all(rule(state) for rule in rules if rule is not None)

    @staticmethod
    def logic_option(option: bool, rule_true: CollectionRule | None = None,
                     rule_false: CollectionRule | None = None) -> CollectionRule | None:
        return rule_true if option else rule_false

    def dws_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dws.has_blue,
                                 None,
                                 self.no_access())

    def dws_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dws.has_red,
                                 None,
                                 self.no_access())

    def cof_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_cof.has_blue,
                                 None,
                                 self.no_access())

    def cof_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_cof.has_red,
                                 None,
                                 self.no_access())

    def fow_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_fow.has_blue,
                                 self.has_weapon_boss(),
                                 self.no_access())

    def fow_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_fow.has_red,
                                 None,
                                 self.no_access())

    def tod_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_tod.has_blue,
                                 self.has_weapon_scissor(),
                                 self.no_access())

    def tod_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_tod.has_red,
                                 self.logic_and([self.has_all([TMCItem.BOMB_BAG, TMCItem.LANTERN]),
                                                 self.has_weapon_boss()]),
                                 self.no_access())

    def pow_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_pow.has_blue,
                                 self.has_weapon_boss(),
                                 self.no_access())

    def pow_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_pow.has_red,
                                 None,
                                 self.no_access())

    def dhc_blue_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dhc.has_blue,
                                 self.has_weapon_boss(),
                                 self.no_access())

    def dhc_red_warp(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dhc.has_red,
                                 self.has_weapon(),
                                 self.no_access())

    def dws_1st_door(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dws.has_blue,
                                 self.has(TMCItem.SMALL_KEY_DWS, 4),
                                 self.has(TMCItem.SMALL_KEY_DWS, 1))

    def dws_2nd_half(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dws.has_blue,
                                 self.no_access(),
                                 self.logic_or([self.has(TMCItem.SMALL_KEY_DWS, 2),
                                                self.has(TMCItem.GUST_JAR)]))

    def tod_right_ice(self) -> CollectionRule:
        return self.has_any([TMCEvent.DROPLETS_EAST_SWITCH, TMCItem.LANTERN])

    def has_tod_4_keys(self) -> CollectionRule:
        return self.logic_option(DungeonItem.option_anywhere == self.world.options.dungeon_small_keys.value,
                                 self.has(TMCItem.SMALL_KEY_TOD, 4),
                                 self.logic_and([self.has(TMCItem.SMALL_KEY_TOD, 3),
                                                 self.has_all([TMCItem.FLIPPERS, TMCItem.GUST_JAR, TMCItem.BOMB_BAG,
                                                               TMCItem.LANTERN, TMCItem.ROCS_CAPE]),
                                                 self.has_weapon_scissor()]))

    def pow_1st_door(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_pow.has_blue or
                                 self.world.options.dungeon_warp_pow.has_red,
                                 self.has(TMCItem.SMALL_KEY_POW, 4),
                                 self.has(TMCItem.SMALL_KEY_POW, 1))

    def pow_fan_door(self) -> CollectionRule:
        return self.has(TMCItem.SMALL_KEY_POW, 5)  # FUTURE: Key settings

    def pow_big_chest_door(self) -> CollectionRule:
        return self.has(TMCItem.SMALL_KEY_POW, 6)  # FUTURE: Key settings

    def pow_2nd_door(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_pow.has_red,
                                 self.has(TMCItem.SMALL_KEY_POW, 6),
                                 self.has(TMCItem.SMALL_KEY_POW, 4))

    def pow_red_chest(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_pow.has_red,
                                 self.can_hit_distance(),
                                 self.logic_and([self.has(TMCItem.ROCS_CAPE), self.can_hit_distance()]))

    def pow_red_warp_door(self) -> CollectionRule:
        return self.has(TMCItem.SMALL_KEY_POW, 5)

    def pow_last_door(self) -> CollectionRule:
        return self.has(TMCItem.SMALL_KEY_POW, 6)

    def dhc_door(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dhc.has_blue or
                                 self.world.options.dungeon_warp_dhc.has_red,
                                 self.has(TMCItem.SMALL_KEY_DHC, 5),
                                 self.has(TMCItem.SMALL_KEY_DHC, 1))

    def dhc_switch_gap(self) -> CollectionRule:
        return self.logic_or([self.has_bow(), self.has_boomerang(), self.can_beam()])

    def dhc_south_towers(self) -> CollectionRule:
        return self.logic_option(self.world.options.dungeon_warp_dhc.has_blue and
                                 self.world.options.dungeon_warp_dhc.has_red,
                                 None,
                                 self.has_any([TMCItem.BOMB_BAG, TMCItem.ROCS_CAPE]))

    def crenel_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_crenel.value,
                                 self.has(TMCItem.OCARINA),
                                 self.no_access())

    def falls_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_falls.value,
                                 self.has(TMCItem.OCARINA),
                                 self.no_access())

    def clouds_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_clouds.value,
                                 self.has(TMCItem.OCARINA),
                                 self.no_access())

    def swamp_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_castor.value,
                                 self.has(TMCItem.OCARINA),
                                 self.no_access())

    def smith_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_south_field.value,
                                 self.logic_or([self.can_pass_trees(), self.has(TMCItem.OCARINA)]),
                                 self.can_pass_trees())

    def minish_crest(self) -> CollectionRule:
        return self.logic_option(self.world.options.wind_crest_minish_woods.value,
                                 self.has(TMCItem.OCARINA),
                                 self.no_access())

    def has_4_elements(self) -> CollectionRule:
        return self.has_all([TMCItem.EARTH_ELEMENT, TMCItem.WATER_ELEMENT, TMCItem.FIRE_ELEMENT, TMCItem.WIND_ELEMENT])

    def has_group(self, item_group_name: str, count: int = 1) -> CollectionRule:
        return lambda state: state.has_group(item_group_name, self.player, count)

    def has_max_health(self, hearts=3) -> Callable[[CollectionState], bool]:
        def heart_count(state: CollectionState) -> bool:
            starting_hearts = self.options.starting_hearts.value
            heart_containers = state.count(TMCItem.HEART_CONTAINER, self.player)
            heart_pieces = state.count(TMCItem.HEART_PIECE, self.player)

            max_health = starting_hearts + heart_containers + (heart_pieces // 4)
            return max_health >= hearts

        return heart_count

    def can_spin(self) -> CollectionRule:
        return self.logic_and([self.has_sword(),
                               self.has_any([TMCItem.PROGRESSIVE_SCROLL, TMCItem.SPIN_ATTACK]),
                               ])

    def split_rule(self, link_count: int, allow_max: bool = False) -> CollectionRule:
        ordered_swords = [
            TMCItem.SMITHS_SWORD,
            TMCItem.WHITE_SWORD_GREEN,
            TMCItem.WHITE_SWORD_RED,
            TMCItem.WHITE_SWORD_BLUE,
            TMCItem.FOUR_SWORD,
        ]
        swords = ordered_swords[link_count:] if allow_max else [ordered_swords[link_count]]
        return self.logic_and([
            self.can_spin(),
            self.logic_or([
                self.has(TMCItem.PROGRESSIVE_SWORD, link_count + 1),
                self.has_any(swords)
            ])
        ])

    def can_beam(self) -> CollectionRule:
        return self.logic_and([
            self.has_sword(),
            self.has_any([TMCItem.SWORD_BEAM, TMCItem.PERIL_BEAM]),
            self.has_bottle(),
        ])

    def can_hit_distance(self) -> CollectionRule:
        return self.logic_or([
            self.has_boomerang(),
            self.has(TMCItem.BOMB_BAG),
            self.has_bow(),
            self.can_beam(),
        ])

    def downthrust(self) -> CollectionRule:
        return self.logic_and([
            self.has_sword(),
            self.has_all([TMCItem.ROCS_CAPE, TMCItem.DOWNTHRUST]),
        ])

    def can_shield(self, mirror: bool = False) -> CollectionRule:
        return self.logic_or([
            self.has(TMCItem.PROGRESSIVE_SHIELD, 2 if mirror else 1),
            self.has(TMCItem.MIRROR_SHIELD if mirror else TMCItem.SHIELD)
        ])

    def pedestal_requirements(self) -> CollectionRule:
        return self.logic_and([
            self.has_group("Elements", self.world.options.ped_elements.value),
            self.logic_or([
                self.has_prog_sword(self.world.options.ped_swords.value),
                self.has_sword_level(self.world.options.ped_swords.value),
            ]),
            self.has_from_list([
                TMCEvent.CLEAR_DWS,
                TMCEvent.CLEAR_COF,
                TMCEvent.CLEAR_FOW,
                TMCEvent.CLEAR_TOD,
                TMCEvent.CLEAR_RC,
                TMCEvent.CLEAR_POW,
            ], self.world.options.ped_dungeons.value),
            self.has(TMCItem.FIGURINE, self.world.options.ped_figurines.value)
        ])

    def has_sword(self) -> CollectionRule:
        return self.has_any([
            TMCItem.SMITHS_SWORD,
            TMCItem.WHITE_SWORD_GREEN,
            TMCItem.WHITE_SWORD_RED,
            TMCItem.WHITE_SWORD_BLUE,
            TMCItem.FOUR_SWORD,
            TMCItem.PROGRESSIVE_SWORD,
        ])

    def has_prog_sword(self, count: int = 1):
        return self.has(TMCItem.PROGRESSIVE_SWORD, count)

    def has_sword_level(self, level: int = 1):
        if level == 0:
            return lambda state: True
        swords = [TMCItem.SMITHS_SWORD,
            TMCItem.WHITE_SWORD_GREEN,
            TMCItem.WHITE_SWORD_RED,
            TMCItem.WHITE_SWORD_BLUE,
            TMCItem.FOUR_SWORD]
        return self.has(swords[level - 1])

    def has_bow(self) -> CollectionRule:
        return self.has_any([TMCItem.BOW, TMCItem.LIGHT_ARROW, TMCItem.PROGRESSIVE_BOW])

    def has_lightarrows(self) -> CollectionRule:
        return self.logic_or([
            self.has(TMCItem.LIGHT_ARROW),
            self.has(TMCItem.PROGRESSIVE_BOW, 2),
        ])

    def has_boomerang(self) -> CollectionRule:
        return self.has_any([TMCItem.BOOMERANG, TMCItem.MAGIC_BOOMERANG, TMCItem.PROGRESSIVE_BOOMERANG])

    def has_magic_boomerang(self) -> CollectionRule:
        return self.logic_or([
            self.has(TMCItem.MAGIC_BOOMERANG),
            self.has(TMCItem.PROGRESSIVE_BOOMERANG, 2),
        ])

    def has_weapon(self) -> CollectionRule:
        return self.logic_or([
            self.logic_option(self.world.options.weapon_bomb.value in {1, 2},
                              self.logic_or([self.has(TMCItem.BOMB_BAG), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(self.world.options.weapon_bow.value == 1,
                              self.logic_or([self.has_bow(), self.has_sword()]),
                              self.has_sword()),
        ])

    def has_weapon_boss(self) -> CollectionRule:
        return self.logic_option(self.world.options.weapon_bomb.value == 2,
                                 self.logic_or([self.has(TMCItem.BOMB_BAG), self.has_sword()]),
                                 self.has_sword())

    def has_weapon_helm_ghini(self) -> CollectionRule:
        return self.logic_or([
            self.logic_option(self.world.options.weapon_bomb.value in {1, 2},
                              self.logic_or([self.has(TMCItem.BOMB_BAG), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(self.world.options.weapon_bow.value == 1,
                              self.logic_or([self.has_bow(), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(self.world.options.weapon_gust.value == 1,
                              self.logic_or([self.has(TMCItem.GUST_JAR), self.has_sword()]),
                              self.has_sword()),
        ])

    def has_weapon_gleerok_mazaal(self) -> CollectionRule:
        return self.logic_or([
            self.logic_option(self.world.options.weapon_bomb.value == 2,
                              self.logic_or([self.has(TMCItem.BOMB_BAG, 2), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(self.world.options.weapon_bow.value == 1,
                              self.logic_or([self.has_bow(), self.has_sword()]),
                              self.has_sword()),
        ])

    def has_weapon_wizzrobe(self) -> CollectionRule:
        return self.logic_or([
            self.logic_option(self.world.options.weapon_bomb.value in {1, 2},
                              self.logic_or([self.has(TMCItem.BOMB_BAG), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(self.world.options.weapon_bow.value == 1,
                              self.logic_or([self.has_bow(), self.has_sword()]),
                              self.has_sword()),
            self.logic_option(
                self.world.options.weapon_lantern.value == 1,
                self.logic_or([self.has(TMCItem.LANTERN), self.has_sword()]),
                self.has_sword()),
        ])

    def has_weapon_scissor(self) -> CollectionRule:
        return self.logic_option(self.world.options.weapon_bomb.value == 2,
                                 self.logic_or([self.has(TMCItem.BOMB_BAG, 2), self.has_sword()]),
                                 self.has_sword())

    def cost(self, price: int) -> CollectionRule:
        wallet_count = [(100, 0), (300, 1), (500, 2), (999, 3)]
        needed_wallets = None
        for size, count in wallet_count:
            if price <= size:
                needed_wallets = count
                break
        if needed_wallets is None:
            return self.no_access()
        return self.has(TMCItem.BIG_WALLET, needed_wallets)

    def blow_dust(self) -> CollectionRule:
        return self.logic_option(TMCTricks.BOMB_DUST in self.world.options.tricks,
                                 self.has_any([TMCItem.GUST_JAR, TMCItem.BOMB_BAG]),
                                 self.has(TMCItem.GUST_JAR))

    def mushroom(self) -> CollectionRule:
        return self.logic_option(TMCTricks.MUSHROOM in self.world.options.tricks,
                                 self.has_any([TMCItem.GUST_JAR, TMCItem.BOMB_BAG, TMCItem.GRIP_RING]),
                                 self.has_any([TMCItem.BOMB_BAG, TMCItem.GRIP_RING]))

    def arrow_break(self) -> CollectionRule:
        return self.logic_option(TMCTricks.ARROWS_BREAK in self.world.options.tricks,
                                 self.has_lightarrows(),
                                 self.no_access())

    def likelike(self) -> CollectionRule:
        return self.logic_option(TMCTricks.LIKELIKE_SWORDLESS in self.world.options.tricks,
                                 self.has(TMCItem.MOLE_MITTS),
                                 self.logic_and([self.has_weapon(), self.has(TMCItem.MOLE_MITTS)]))

    def dark_room(self) -> CollectionRule:
        return self.logic_option(TMCTricks.DARK_ROOMS in self.world.options.tricks,
                                 None,
                                 self.has(TMCItem.LANTERN))

    def cape_extend(self) -> CollectionRule:
        return self.logic_option(TMCTricks.CAPE_EXTENSIONS in self.world.options.tricks,
                                 self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS]),
                                 self.has(TMCItem.FLIPPERS))

    def lake_minish(self) -> CollectionRule:
        return self.logic_option(TMCTricks.LAKE_MINISH in self.world.options.tricks,
                                 self.logic_or([self.has_all([TMCItem.OCARINA, TMCItem.FLIPPERS]),
                                                self.has(TMCItem.PEGASUS_BOOTS)]),
                                 self.has(TMCItem.PEGASUS_BOOTS))

    def cabin_swim(self) -> CollectionRule:
        return self.logic_option(TMCTricks.CABIN_SWIM in self.world.options.tricks,
                                 self.has_any([TMCItem.FLIPPERS, TMCItem.GUST_JAR]),
                                 self.has(TMCItem.GUST_JAR))

    def shark_kill(self) -> CollectionRule:
        return self.logic_option(TMCTricks.SHARKS_SWORDLESS in self.world.options.tricks,
                                 None,
                                 self.has_weapon())

    def fow_pot(self) -> CollectionRule:
        return self.logic_option(TMCTricks.FOW_POT in self.world.options.tricks,
                                 self.has(TMCItem.GUST_JAR),
                                 self.no_access())

    def pow_jump(self) -> CollectionRule:
        return self.logic_option(TMCTricks.POW_NOCANE in self.world.options.tricks,
                                 self.has(TMCItem.ROCS_CAPE),
                                 self.logic_and([self.has_all([TMCItem.CANE_OF_PACCI, TMCItem.ROCS_CAPE]),
                                                 self.split_rule(3)]))

    def pow_pot(self) -> CollectionRule:
        return self.logic_option(TMCTricks.POT_PUZZLE in self.world.options.tricks,
                                 self.logic_or([self.has_all([TMCItem.ROCS_CAPE, TMCEvent.POW_1ST_HALF_3F_ITEM_DROP]),
                                                self.logic_and([self.split_rule(3), self.has(TMCItem.POWER_BRACELETS),
                                                                self.can_hit_distance()])]),
                                 self.logic_and([self.split_rule(3), self.has(TMCItem.POWER_BRACELETS),
                                                 self.can_hit_distance()]))  # FUTURE: Boomerang/Bomb Trick

    def dhc_cannons(self) -> CollectionRule:
        return self.logic_option(TMCTricks.DHC_CANNONS in self.world.options.tricks,
                                 self.logic_and([self.has_sword(), self.has(TMCItem.BOMB_BAG)]),
                                 self.split_rule(4))

    def dhc_pads(self) -> CollectionRule:
        return self.logic_option(TMCTricks.DHC_CLONES in self.world.options.tricks,
                                 self.split_rule(2),
                                 self.split_rule(4))

    def dhc_spin(self) -> CollectionRule:
        return self.logic_option(TMCTricks.DHC_SPIN in self.world.options.tricks,
                                 self.can_spin(),
                                 self.split_rule(4))

    def can_pass_trees(self) -> CollectionRule:
        return self.logic_or([self.has_any([TMCItem.BOMB_BAG, TMCItem.LANTERN]), self.has_sword(), self.arrow_break()])

    def access_town_left(self) -> CollectionRule:
        return self.has_any([TMCItem.ROCS_CAPE, TMCItem.FLIPPERS, TMCItem.CANE_OF_PACCI])

    def has_bottle(self) -> CollectionRule:
        return self.has_group("Bottle")

    def access_town_fountain(self) -> CollectionRule:
        return self.logic_and([self.access_town_left(), self.has_bottle()])

    def access_minish_woods_top_left(self) -> CollectionRule:
        return self.logic_or([self.has_any([TMCItem.FLIPPERS, TMCItem.ROCS_CAPE]),
                              self.logic_and([self.access_lonlon_right(), self.has(TMCItem.CANE_OF_PACCI)])])

    def complete_book_quest(self) -> CollectionRule:
        return self.has_all(
            [TMCItem.OCARINA, TMCItem.CANE_OF_PACCI, TMCItem.RED_BOOK, TMCItem.BLUE_BOOK, TMCItem.GREEN_BOOK])

    def access_lonlon_right(self) -> CollectionRule:
        """ Assumes can_pass_trees is already used somewhere in the chain """
        return self.logic_or([self.has_any([TMCItem.LONLON_KEY, TMCItem.ROCS_CAPE, TMCItem.OCARINA]),
                              self.has_all([TMCItem.FLIPPERS, TMCItem.MOLE_MITTS])])

    def tod_west_iceblock_rule(self) -> CollectionRule | None:
        """
        ToD is stupid, getting to the west ice block needs special access rules based off what got placed at it.
        Item placement for this location only occurs in create_items stage.
        """
        west_item = self.world.get_location(TMCLocation.DROPLETS_ENTRANCE_B2_WEST_ICEBLOCK).item
        if west_item is None or west_item.name is not TMCItem.BIG_KEY_TOD or self.options.dungeon_warp_tod.value != DungeonWarp.option_none:
            return self.has(TMCItem.SMALL_KEY_TOD, 4)
        if (west_item.name is TMCItem.BIG_KEY_TOD and
                self.world.options.dungeon_small_keys.value is DungeonItem.option_own_dungeon):
            return self.has(TMCItem.SMALL_KEY_TOD, 1)
        return None

    def has(self, item: str, count: int = 1) -> CollectionRule:
        return lambda state: state.has(item, self.player, count)

    def has_all(self, items: list[str]) -> CollectionRule:
        return lambda state: state.has_all(items, self.player)

    def has_any(self, items: list[str]) -> CollectionRule:
        return lambda state: state.has_any(items, self.player)

    def has_from_list(self, items: list[str], count: int = 1) -> CollectionRule:
        return lambda state: state.has_from_list(items, self.player, count)

    def can_reach(self, locations: list[str]) -> CollectionRule:
        return lambda state: all(state.can_reach(loc, "Location", self.player) for loc in locations)

    def set_rules(self, disabled_locations: set[str], location_name_to_id: dict[str, int]) -> None:
        multiworld = self.world.multiworld

        for region_pair, rule in self.connection_rules.items():
            if region_pair[0] is None or region_pair[1] is None:
                continue
            region_one = multiworld.get_region(region_pair[0], self.player)
            region_two = multiworld.get_region(region_pair[1], self.player)
            region_one.connect(region_two, rule=rule)

        for loc in multiworld.get_locations(self.player):
            if loc.name not in location_name_to_id or loc.name in disabled_locations:
                continue

            if loc.name in self.location_rules and self.location_rules[loc.name] is not None:
                add_rule(loc, self.location_rules[loc.name])

        multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)
