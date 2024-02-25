from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule, CollectionRule
from BaseClasses import CollectionState
from .data import data

if TYPE_CHECKING:
    from . import PokemonCrystalWorld
else:
    PokemonCrystalWorld = object


def set_rules(world: PokemonCrystalWorld) -> None:
    def can_cut(state: CollectionState):
        return state.has("HM01 Cut", world.player) and state.has("Hive Badge", world.player)

    # def can_fly(state: CollectionState):
    #     return state.has("HM02 Fly", world.player) and state.has("Storm Badge", world.player)

    def can_surf(state: CollectionState):
        return state.has("HM03 Surf", world.player) and state.has("Fog Badge", world.player)

    def can_strength(state: CollectionState):
        return state.has("HM04 Strength", world.player) and state.has("Plain Badge", world.player)

    def can_flash(state: CollectionState):
        return state.has("HM05 Flash", world.player) and state.has("Zephyr Badge", world.player)

    def can_whirlpool(state: CollectionState):
        return state.has("HM06 Whirlpool", world.player) and state.has("Glacier Badge", world.player)

    def can_waterfall(state: CollectionState):
        return state.has("HM07 Waterfall", world.player) and state.has("Rising Badge", world.player)

    def can_rocksmash(state: CollectionState):
        return state.has("TM08 Rock Smash", world.player)

    def has_n_badges(state: CollectionState, n: int) -> bool:
        return sum([state.has(event, world.player) for event in [
            "Zephyr Badge",
            "Hive Badge",
            "Plain Badge",
            "Fog Badge",
            "Mineral Badge",
            "Storm Badge",
            "Glacier Badge",
            "Rising Badge",

            "Boulder Badge",
            "Cascade Badge",
            "Thunder Badge",
            "Rainbow Badge",
            "Soul Badge",
            "Marsh Badge",
            "Volcano Badge",
            "Earth Badge"
        ]]) >= n

    def get_entrance(entrance: str):
        return world.multiworld.get_entrance(entrance, world.player)

    def get_location(location: str):
        if location in data.locations:
            location = data.locations[location].label

        return world.multiworld.get_location(location, world.player)

    def hidden():
        return world.options.randomize_hidden_items

    # Goal
    if world.options.goal == 1:
        world.multiworld.completion_condition[world.player] = lambda state: state.has("EVENT_BEAT_RED", world.player)
    else:
        world.multiworld.completion_condition[world.player] = lambda state: state.has(
            "EVENT_BEAT_ELITE_FOUR", world.player)

    # New Bark Town
    set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_29"),
             lambda state: state.has("EVENT_GOT_A_POKEMON_FROM_ELM", world.player))

    set_rule(get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27:WEST"), can_surf)

    # set_rule(get_location("Elm's Lab - Everstone from Elm"),
    #          lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))

    set_rule(get_location("Elm's Lab - Gift from Aide After Returning Mystery Egg"),
             lambda state: state.has("Mystery Egg", world.player))

    set_rule(get_location("Elm's Lab - Master Ball from Elm"), lambda state: state.has("Rising Badge", world.player))

    set_rule(get_location("Elm's Lab - S.S. Ticket from Elm"),
             lambda state: state.has("EVENT_BEAT_ELITE_FOUR", world.player))

    # Route 29
    set_rule(get_location("Route 29 - Pink Bow from Tuscany"), lambda state: state.has("Zephyr Badge", world.player))
    # Route 30
    set_rule(get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_31"),
             lambda state: state.has("EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player))

    set_rule(get_location("Route 30 - Exp Share from Mr Pokemon"), lambda state: state.has("Red Scale", world.player))

    # Cherrygrove
    set_rule(get_location("Cherrygrove City - Mystic Water from Island Man"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_31 -> REGION_DARK_CAVE_VIOLET_ENTRANCE"), can_flash)

    set_rule(get_location("Route 31 - TM50 for Delivering Kenya"),
             lambda state: state.has("EVENT_GOT_KENYA", world.player))

    # Dark Cave Violet
    set_rule(get_location("Dark Cave Violet Entrance - Item 1"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Item 2"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Item 3"), can_rocksmash)
    if hidden():
        set_rule(get_location("Dark Cave Violet Entrance - Hidden Item in North"), can_rocksmash)

    set_rule(get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE -> REGION_ROUTE_46"), can_rocksmash)

    set_rule(get_entrance("REGION_ROUTE_46 -> REGION_DARK_CAVE_VIOLET_ENTRANCE"),
             lambda state: can_rocksmash(state) and can_flash(state))

    set_rule(get_entrance("REGION_ROUTE_45 -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE"),
             lambda state: can_surf(state) and can_flash(state))

    # Violet City
    if hidden():
        set_rule(get_location("Violet City - Hidden Item Behind Cut Tree"), can_cut)
    set_rule(get_location("Violet City - Item 1"), can_surf)
    set_rule(get_location("Violet City - Item 2"), can_surf)
    set_rule(get_location("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"),
             lambda state: state.has("EVENT_BEAT_FALKNER", world.player))

    set_rule(get_entrance("REGION_VIOLET_CITY -> REGION_ROUTE_32"),
             lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))
    set_rule(get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_36_RUINS_OF_ALPH_GATE"),
             lambda state: state.has("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player))

    # Route 32
    set_rule(get_location("Route 32 - Miracle Seed from Man in North"),
             lambda state: state.has("Zephyr Badge", world.player))

    set_rule(get_location("Route 32 - TM05 from Roar Guy"), can_cut)

    # Union Cave

    set_rule(get_entrance("REGION_UNION_CAVE_B1F -> REGION_UNION_CAVE_B2F"), can_surf)

    # Azalea Town
    set_rule(get_location("Slowpoke Well B2F - Kings Rock from Man"),
             lambda state: can_strength(state) and can_surf(state))
    set_rule(get_location("Slowpoke Well B2F - Item 1"), lambda state: can_strength(state) and can_surf(state))

    set_rule(get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    set_rule(get_location("Azalea Town - Lure Ball from Kurt"),
             lambda state: state.has("EVENT_CLEARED_SLOWPOKE_WELL", world.player))

    # Route 34
    set_rule(get_location("Route 34 - Soft Sand from Kate"), can_surf)
    if hidden():
        set_rule(get_location("Route 34 - Hidden Item Across Water"), can_surf)
    set_rule(get_location("Route 34 - Item Across Water"), can_surf)

    # Goldenrod City
    set_rule(get_location("Goldenrod City - Squirtbottle from Flower Shop"),
             lambda state: state.has("Plain Badge", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
             lambda state: state.has("Pass", world.player))

    # Underground

    set_rule(get_entrance("REGION_GOLDENROD_UNDERGROUND -> REGION_GOLDENROD_UNDERGROUND_SWITCH_ROOM_ENTRANCES"),
             lambda state: state.has("Basement Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F -> REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_entrance("REGION_GOLDENROD_DEPT_STORE_B1F:WAREHOUSE -> REGION_GOLDENROD_DEPT_STORE_B1F"),
             lambda state: state.has("Card Key", world.player))

    # Radio Tower

    set_rule(get_entrance("REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_3F"), lambda state: has_n_badges(state, 7))

    set_rule(get_entrance("REGION_RADIO_TOWER_3F -> REGION_RADIO_TOWER_4F:CARDKEY"),
             lambda state: state.has("Card Key", world.player))

    set_rule(get_location("Radio Tower 3F - TM11 from Woman"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_location("Radio Tower 4F - Pink Bow from Mary"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    # Route 35
    set_rule(get_location("Route 35 - HP Up After Delivering Kenya"),
             lambda state: state.has("EVENT_GAVE_KENYA", world.player))

    # Sudowoodo
    set_rule(get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_37"), lambda state: state.has("Squirtbottle", world.player))

    set_rule(get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_36_NATIONAL_PARK_GATE"),
             lambda state: state.has("Squirtbottle", world.player))

    set_rule(get_location("Route 36 - TM08 from Rock Smash Guy"), lambda state: state.has("Squirtbottle", world.player))

    # Ecruteak City
    set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM"),
             lambda state: state.has("EVENT_BURNED_TOWER_MORTY", world.player))

    set_rule(get_location("Burned Tower 1F - Item"), can_rocksmash)
    set_rule(get_location("Burned Tower B1F - Item"), can_strength)

    set_rule(get_entrance("REGION_ECRUTEAK_CITY -> REGION_TIN_TOWER_1F"),
             lambda state: state.has("Clear Bell", world.player) and
                           state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    # Olivine City
    set_rule(get_location("EVENT_JASMINE_RETURNED_TO_GYM"), lambda state: state.has("Secretpotion", world.player))

    set_rule(get_entrance("REGION_OLIVINE_PORT -> REGION_FAST_SHIP_1F"),
             lambda state: state.has("S.S. Ticket", world.player))

    if hidden():
        set_rule(get_location("Olivine Port - Hidden Item in Southeast Buoy"),
                 lambda state: state.has("S.S. Ticket", world.player) and can_surf(state))

    set_rule(get_entrance("REGION_OLIVINE_CITY -> REGION_OLIVINE_GYM"),
             lambda state: state.has("EVENT_JASMINE_RETURNED_TO_GYM", world.player))

    # Route 40

    set_rule(get_entrance("REGION_ROUTE_40 -> REGION_ROUTE_41"), can_surf)

    if hidden():
        set_rule(get_location("Route 40 - Hidden Item in Rock"), can_rocksmash)

    # Route 41

    if hidden():
        set_rule(get_location("Route 41 - Hidden Item on Southwest Island"), can_whirlpool)

    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NW"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NE"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SW"),
             lambda state: can_whirlpool(state) and can_flash(state))
    set_rule(get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SE"),
             lambda state: can_whirlpool(state) and can_flash(state))

    # Cianwood

    if hidden():
        set_rule(get_location("Cianwood City - Hidden Item in West Rock"), can_rocksmash)

        set_rule(get_location("Cianwood City - Hidden Item in North Rock"), can_rocksmash)

    set_rule(get_location("Cianwood City - HM02 from Chuck's Wife"),
             lambda state: state.has("EVENT_BEAT_CHUCK", world.player))

    set_rule(get_entrance("REGION_CIANWOOD_CITY -> REGION_CIANWOOD_GYM"), can_strength)

    set_rule(get_location("Cianwood Pharmacy - Secretpotion"),
             lambda state: state.has("EVENT_JASMINE_EXPLAINED_AMPHYS_SICKNESS", world.player))

    # Route 42

    set_rule(get_entrance("REGION_ROUTE_42:WEST -> REGION_ROUTE_42:CENTER"), can_surf)
    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:WEST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_42:EAST -> REGION_ROUTE_42:CENTER"), can_surf)
    set_rule(get_entrance("REGION_ROUTE_42:CENTER -> REGION_ROUTE_42:EAST"), can_surf)

    if hidden():
        set_rule(get_location("Route 42 - Hidden Item in Pond Rock"), can_surf)

    # Mt Mortar
    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_2F_OUTSIDE"),
             lambda state: can_surf(state) and can_waterfall(state))

    # 1F Inside Front
    set_rule(get_location("Mount Mortar 1F Inside - Item 1"), can_strength)
    set_rule(get_location("Mount Mortar 1F Inside - Item 2"), can_strength)
    set_rule(get_location("Mount Mortar 1F Inside - Item 6"), can_strength)
    set_rule(get_location("Mount Mortar 1F Inside - Item 7"), can_strength)

    # 1F C -> B1F Everything needs surf so im being lazy

    set_rule(get_entrance("REGION_MOUNT_MORTAR_1F_OUTSIDE:CENTER -> REGION_MOUNT_MORTAR_B1F"), can_surf)

    # Behind boulder, need to come down from 2F for this

    set_rule(get_entrance("REGION_MOUNT_MORTAR_B1F:BACK -> REGION_MOUNT_MORTAR_B1F"),
             lambda state: can_strength(state) and can_surf(state) and can_waterfall(state))

    # Mahogany Town

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_MART_1F"),
             lambda state: state.has("EVENT_DECIDED_TO_HELP_LANCE", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_GYM"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    set_rule(get_entrance("REGION_MAHOGANY_TOWN -> REGION_ROUTE_44"), lambda state: has_n_badges(state, 7))

    # Route 43

    set_rule(get_location("Route 43 - Sludge Bomb from Guard in Gate"),
             lambda state: state.has("EVENT_CLEARED_ROCKET_HIDEOUT", world.player))

    # Lake of Rage

    set_rule(get_location("EVENT_DECIDED_TO_HELP_LANCE"), can_surf)

    set_rule(get_location("Lake of Rage - Red Scale from Gyarados"), can_surf)

    set_rule(get_location("Lake of Rage - Blackbelt from Wesley"), can_cut)

    set_rule(get_location("Lake of Rage - TM10 from Hidden Power House"), can_cut)

    if hidden():
        set_rule(get_location("Lake of Rage - Hidden Item Behind Cut Tree"), can_cut)

    set_rule(get_location("Lake of Rage - Item 1"), can_cut)

    set_rule(get_location("Lake of Rage - Item 2"), can_cut)

    # Route 44

    if hidden():
        set_rule(get_location("Route 44 - Hidden Item Across Water"), can_surf)

    set_rule(get_location("Route 44 - Item 2"), can_surf)

    # Ice Path
    set_rule(get_entrance("REGION_ICE_PATH_B2F_MAHOGANY_SIDE -> REGION_ICE_PATH_B3F"), can_strength)

    set_rule(get_location("Ice Path B2F - Item 2"), can_strength)

    # Blackthorn

    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_BLACKTHORN_GYM_1F"),
             lambda state: state.has("EVENT_CLEARED_RADIO_TOWER", world.player))

    set_rule(get_location("EVENT_BEAT_CLAIR"), can_strength)

    set_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_DRAGONS_DEN_1F"),
             lambda state: state.has("EVENT_BEAT_CLAIR", world.player))

    add_rule(get_entrance("REGION_BLACKTHORN_CITY -> REGION_DRAGONS_DEN_1F"), can_surf)

    # Dragons Den
    set_rule(get_location("Dragon's Den B1F - Item 3"), can_whirlpool)

    if hidden():
        set_rule(get_location("Dragon's Den B1F - Hidden Item in Water 2"),
                 can_whirlpool)
        set_rule(get_location("Dragon's Den B1F - Hidden Item in SE Corner"),
                 can_whirlpool)

    # Route 45

    if hidden():
        set_rule(get_location("Route 45 - Hidden Item in Southeast Pond"), can_surf)

    # Route 27

    set_rule(get_entrance("REGION_ROUTE_27:WEST -> REGION_NEW_BARK_TOWN"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:CENTER -> REGION_ROUTE_27:EAST"), can_surf)

    set_rule(get_entrance("REGION_ROUTE_27:EAST -> REGION_ROUTE_27:CENTER"), can_surf)

    set_rule(get_location("Route 27 - Item 1"), can_surf)

    set_rule(get_location("Route 27 - Item 2"), lambda state: can_surf(state) and can_whirlpool(state))

    set_rule(get_location("Tohjo Falls - Item"), can_surf)

    set_rule(get_entrance("REGION_TOHJO_FALLS:WEST -> REGION_TOHJO_FALLS:EAST"),
             lambda state: can_surf(state) and can_waterfall(state))
    set_rule(get_entrance("REGION_TOHJO_FALLS:EAST -> REGION_TOHJO_FALLS:WEST"),
             lambda state: can_surf(state) and can_waterfall(state))

    # Victory Road

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_VICTORY_ROAD"), lambda state: has_n_badges(state, 8))

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_26"), lambda state: has_n_badges(state, 8))

    set_rule(get_entrance("REGION_ROUTE_28 -> REGION_VICTORY_ROAD_GATE"),
             lambda state: state.has("EVENT_OPENED_MT_SILVER", world.player))

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_28"),
             lambda state: state.has("EVENT_OPENED_MT_SILVER", world.player))

    set_rule(get_entrance("REGION_ROUTE_22 -> REGION_VICTORY_ROAD_GATE"),
             lambda state: state.has("EVENT_FOUGHT_SNORLAX", world.player))

    set_rule(get_entrance("REGION_VICTORY_ROAD_GATE -> REGION_ROUTE_22"),
             lambda state: state.has("EVENT_FOUGHT_SNORLAX", world.player))

    # Route 28
    set_rule(get_location("Route 28 - Steel Wing from Celebrity in House"), can_cut)
    if hidden():
        set_rule(get_location("Route 28 - Hidden Item Behind Cut Tree"), can_cut)

    # Silver Cave
    set_rule(get_entrance("REGION_SILVER_CAVE_OUTSIDE -> REGION_SILVER_CAVE_ROOM_1"), can_flash)

    if hidden():
        set_rule(get_location("Outside Silver Cave - Hidden Item Across Water"), can_surf)

    set_rule(get_location("Silver Cave 2F - Item 1"), lambda state: can_surf(state) and can_waterfall(state))

    set_rule(get_location("Silver Cave 2F - Item 2"), lambda state: can_surf(state) and can_waterfall(state))

    set_rule(get_entrance("REGION_SILVER_CAVE_ROOM_2 -> REGION_SILVER_CAVE_ITEM_ROOMS"),
             lambda state: can_surf(state) and can_waterfall(state))

    # Viridian
    set_rule(get_location("Viridian City - TM42 from Sleepy Guy"), lambda state: can_surf(state) or can_cut(state))

    set_rule(get_entrance("REGION_VIRIDIAN_CITY -> REGION_VIRIDIAN_GYM"),
             lambda state: state.has("EVENT_VIRIDIAN_GYM_BLUE", world.player))

    # Route 2
    set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:NORTHEAST"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_2:WEST -> REGION_ROUTE_2:SOUTHEAST"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:WEST"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_2:SOUTHEAST -> REGION_ROUTE_2:NORTHEAST"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_2:NORTHEAST -> REGION_ROUTE_2:SOUTHEAST"), can_cut)

    # Cerulean
    if hidden():
        set_rule(get_location("Cerulean City - Hidden Item in Water"), can_surf)

    set_rule(get_entrance("REGION_CERULEAN_CITY -> REGION_ROUTE_9"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_9 -> REGION_CERULEAN_CITY"), can_cut)

    set_rule(get_entrance("REGION_ROUTE_10_NORTH -> REGION_POWER_PLANT"), can_surf)

    # Route 25
    set_rule(get_location("Route 25 - Item Behind Cut Tree"), can_cut)

    # Power Plant
    set_rule(get_location("EVENT_RESTORED_POWER_TO_KANTO"), lambda state: state.has("Machine Part", world.player))

    set_rule(get_location("Power Plant - TM07 from Manager"),
             lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Rock Tunnel
    set_rule(get_entrance("REGION_ROUTE_9 -> REGION_ROCK_TUNNEL_1F"), can_flash)

    set_rule(get_entrance("REGION_ROUTE_10_SOUTH -> REGION_ROCK_TUNNEL_1F"), can_flash)

    # Lavendar
    set_rule(get_location("EVENT_GOT_EXPN_CARD"), lambda state: state.has(
        "EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Route 12

    set_rule(get_location("Route 12 - Item 1"), can_cut)

    set_rule(get_location("Route 12 - Item 2"), lambda state: can_cut(state) and can_surf(state))

    if hidden():
        set_rule(get_location("Route 12 - Hidden Item on Island"), can_surf)

    # Vermilion
    set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_VERMILION_GYM"),
             lambda state: can_cut(state) or can_surf(state))

    set_rule(get_location("Vermilion City - HP Up from Man by PokeCenter"), lambda state: has_n_badges(state, 16))

    set_rule(get_location("Vermilion City - Lost Item from Guy in Fan Club"),
             lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player) and state.has(
                 "EVENT_MET_COPYCAT_FOUND_OUT_ABOUT_LOST_ITEM", world.player))

    if hidden():
        set_rule(get_location("Vermilion Port - Hidden Item in Buoy"), can_surf)

    set_rule(get_location("EVENT_FOUGHT_SNORLAX"), lambda state: state.has("EVENT_GOT_EXPN_CARD", world.player))

    set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_ROUTE_11"),
             lambda state: state.has("EVENT_GOT_EXPN_CARD", world.player))

    set_rule(get_entrance("REGION_ROUTE_11 -> REGION_VERMILION_CITY"),
             lambda state: state.has("EVENT_GOT_EXPN_CARD", world.player))

    set_rule(get_entrance("REGION_VERMILION_CITY -> REGION_DIGLETTS_CAVE"),
             lambda state: state.has("EVENT_GOT_EXPN_CARD", world.player))

    set_rule(get_entrance("REGION_DIGLETTS_CAVE -> REGION_VERMILION_CITY"),
             lambda state: state.has("EVENT_GOT_EXPN_CARD", world.player))

    set_rule(get_entrance("REGION_VERMILION_PORT_PASSAGE -> REGION_VERMILION_PORT"),
             lambda state: state.has("S.S. Ticket", world.player))

    # Saffron
    set_rule(get_location("Copycat's House - Pass from Copycat"), lambda state: state.has("Lost Item", world.player))

    set_rule(get_entrance("REGION_SAFFRON_MAGNET_TRAIN_STATION -> REGION_GOLDENROD_MAGNET_TRAIN_STATION"),
             lambda state: state.has("Pass", world.player))

    # Underground Path
    set_rule(get_entrance("REGION_ROUTE_5 -> REGION_ROUTE_5_UNDERGROUND_PATH_ENTRANCE"),
             lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    set_rule(get_entrance("REGION_ROUTE_6 -> REGION_ROUTE_6_UNDERGROUND_PATH_ENTRANCE"),
             lambda state: state.has("EVENT_RESTORED_POWER_TO_KANTO", world.player))

    # Celadon

    set_rule(get_entrance("REGION_CELADON_CITY -> REGION_CELADON_GYM"), can_cut)

    # Cycling Road
    set_rule(get_entrance("REGION_ROUTE_16 -> REGION_ROUTE_17"), lambda state: state.has("Bicycle", world.player))

    set_rule(get_entrance("REGION_ROUTE_17_ROUTE_18_GATE -> REGION_ROUTE_17"),
             lambda state: state.has("Bicycle", world.player))

    # Route 15
    set_rule(get_location("Route 15 - Item"), can_cut)

    # Route 20
    set_rule(get_entrance("REGION_ROUTE_19 -> REGION_ROUTE_20"),
             lambda state: state.has("EVENT_CINNABAR_ROCKS_CLEARED", world.player) and can_surf(state))

    set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_20"), can_surf)

    set_rule(get_entrance("REGION_CINNABAR_ISLAND -> REGION_ROUTE_21"), can_surf)

    set_rule(get_entrance("REGION_PALLET_TOWN -> REGION_ROUTE_21"), can_surf)

    # Pallet

    set_rule(get_location("EVENT_OPENED_MT_SILVER"), lambda state: has_n_badges(state, 16))

    if world.options.require_itemfinder:
        for location in world.multiworld.get_locations(world.player):
            if "Hidden" in location.tags:
                add_rule(location, lambda state: state.has("Itemfinder", world.player))
