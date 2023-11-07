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

    def can_cut(state: CollectionState):
        return state.has("HM02 Fly", world.player) and state.has("Storm Badge", world.player)

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

    # def defeated_n_gym_leaders(state: CollectionState, n: int) -> bool:
    #     return sum([state.has(event, world.player) for event in [
    #         "EVENT_BEAT_FALKNER",
    #         "EVENT_BEAT_BUGSY",
    #         "EVENT_BEAT_WHITNEY",
    #         "EVENT_BEAT_MORTY",
    #         "EVENT_BEAT_JASMINE",
    #         "EVENT_BEAT_CHUCK",
    #         "EVENT_BEAT_PRYCE",
    #         "EVENT_BEAT_CLAIR",

    #         "EVENT_BEAT_BROCK",
    #         "EVENT_BEAT_MISTY",
    #         "EVENT_BEAT_LTSURGE",
    #         "EVENT_BEAT_ERIKA",
    #         "EVENT_BEAT_JANINE",
    #         "EVENT_BEAT_SABRINA",
    #         "EVENT_BEAT_BLAINE",
    #         "EVENT_BEAT_BLUE"
    #     ]]) >= n

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
    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "EVENT_BEAT_ELITE_FOUR", world.player)

    # New Bark Town
    set_rule(
        get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_29"),
        lambda state: state.has("EVENT_GOT_A_POKEMON_FROM_ELM", world.player)
    )

    set_rule(
        get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27"),
        can_surf
    )

    set_rule(
        get_location("Elm's Lab - Everstone from Elm"),
        lambda state: state.has(
            "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player)
    )

    set_rule(
        get_location("Elm's Lab - Master Ball from Elm"),
        lambda state: has_n_badges(state, 8)
    )

    set_rule(
        get_location("Elm's Lab - S.S. Ticket from Elm"),
        lambda state: state.has(
            "EVENT_BEAT_ELITE_FOUR", world.player)
    )

    # Route 29
    set_rule(
        get_location("Route 29 - Pink Bow from Tuscany"),
        lambda state: state.has(
            "Zephyr Badge", world.player)
    )

    set_rule(
        get_entrance("REGION_ROUTE_29_ROUTE_46_GATE -> REGION_ROUTE_46"),
        lambda state: False
    )

    # Route 30
    set_rule(
        get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_31"),
        lambda state: state.has(
            "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player)
    )

    # Cherrygrove
    set_rule(get_location(
        "Cherrygrove City - Mystic Water from Island Man"), can_surf)

    set_rule(
        get_entrance("REGION_ROUTE_31 -> REGION_DARK_CAVE_VIOLET_ENTRANCE"),
        can_flash
    )

    set_rule(
        get_location("Route 31 - TM50 for Delivering Kenya"),
        lambda state: state.has("EVENT_GOT_KENYA", world.player)
    )

    # Dark Cave Violet
    set_rule(get_location("Dark Cave Violet Entrance - Item 1"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Item 2"), can_rocksmash)
    set_rule(get_location("Dark Cave Violet Entrance - Item 3"), can_rocksmash)
    if hidden():
        set_rule(get_location(
            "Dark Cave Violet Entrance - Hidden Item in North"), can_rocksmash)

    # Violet City
    if hidden():
        set_rule(get_location("Violet City - Hidden Item Behind Cut Tree"), can_cut)
    set_rule(get_location("Violet City - Item 1"), can_surf)
    set_rule(get_location("Violet City - Item 2"), can_surf)
    set_rule(get_location("EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE"), lambda state: state.has(
        "EVENT_BEAT_FALKNER", world.player))

    set_rule(
        get_entrance("REGION_VIOLET_CITY -> REGION_ROUTE_32"),
        lambda state: state.has(
            "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player)
    )
    set_rule(
        get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_36_RUINS_OF_ALPH_GATE"),
        lambda state: state.has(
            "EVENT_GOT_TOGEPI_EGG_FROM_ELMS_AIDE", world.player)
    )

    # Route 32
    set_rule(get_location("Route 32 - Miracle Seed from Old Man"), lambda state: state.has(
        "Zephyr Badge", world.player))

    set_rule(get_location("Route 32 - TM05 from Roar Guy"), can_cut)

    # Union Cave

    # Azalea Town
    set_rule(get_location("Slowpoke Well B2F - Kings Rock from Man"),
             lambda state: can_strength(state) and can_surf(state))
    set_rule(get_location("Slowpoke Well B2F - Item 1"),
             lambda state: can_strength(state) and can_surf(state))

    set_rule(
        get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"),
        lambda state: state.has(
            "EVENT_CLEARED_SLOWPOKE_WELL", world.player)
    )

    set_rule(
        get_location("Azalea Town - Lure Ball from Kurt"),
        lambda state: state.has(
            "EVENT_CLEARED_SLOWPOKE_WELL", world.player)
    )

    set_rule(
        get_entrance("REGION_AZALEA_TOWN -> REGION_ILEX_FOREST_AZALEA_GATE"),
        lambda state: state.has(
            "EVENT_BEAT_BUGSY", world.player)
    )

    # Route 34
    set_rule(get_location("Route 34 - Soft Sand from Kate"), can_surf)
    if hidden():
        set_rule(get_location("Route 34 - Hidden Item Across Water"), can_surf)
    set_rule(get_location("Route 34 - Item Across Water"), can_surf)

    # Goldenrod City
    set_rule(get_location("Goldenrod City - Squirtbottle from Flower Shop"), lambda state: state.has(
        "Plain Badge", world.player))

    set_rule(
        get_entrance(
            "REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
        lambda state: state.has(
            "Pass", world.player)
    )

    # Route 35
    set_rule(get_location("Route 35 - HP Up After Delivering Kenya"), lambda state: state.has(
        "EVENT_GAVE_KENYA", world.player))

    # Sudowoodo
    set_rule(
        get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_37"),
        lambda state: state.has(
            "Squirtbottle", world.player)
    )

    set_rule(
        get_entrance("REGION_ROUTE_36 -> REGION_ROUTE_36_NATIONAL_PARK_GATE"),
        lambda state: state.has(
            "Squirtbottle", world.player)
    )

    set_rule(get_location("Route 36 - TM08 from Rock Smash Guy"), lambda state: state.has(
        "Squirtbottle", world.player))

    # Ecruteak City
    set_rule(
        get_entrance("REGION_ECRUTEAK_CITY -> REGION_ECRUTEAK_GYM"),
        lambda state: state.has("EVENT_BURNED_TOWER_MORTY", world.player)
    )

    set_rule(get_location("Burned Tower 1F - Item"), can_rocksmash)
    set_rule(get_location("Burned Tower B1F - Item"), can_strength)

    # Olivine City
    set_rule(
        get_location(
            "EVENT_JASMINE_RETURNED_TO_GYM"),
        lambda state: state.has(
            "Secretpotion", world.player)
    )

    set_rule(
        get_entrance("REGION_OLIVINE_PORT -> REGION_FAST_SHIP_1F"),
        lambda state: state.has(
            "S.S. Ticket", world.player)
    )

    if hidden():
        set_rule(
            get_location(
                "Olivine Port - Hidden Item in Southeast Buoy"),
            lambda state: state.has(
                "S.S. Ticket", world.player) and can_surf(state)
        )

    set_rule(
        get_entrance("REGION_OLIVINE_CITY -> REGION_OLIVINE_GYM"),
        lambda state: state.has(
            "EVENT_JASMINE_RETURNED_TO_GYM", world.player)
    )

    # Route 40

    set_rule(
        get_entrance("REGION_ROUTE_40 -> REGION_ROUTE_41"),
        can_surf
    )

    if hidden():
        set_rule(
            get_location(
                "Route 40 - Hidden Item in Rock"),
            can_rocksmash
        )

    # Route 41

    if hidden():
        set_rule(
            get_location(
                "Route 41 - Hidden Item on Southwest Island"),
            can_whirlpool
        )

    set_rule(
        get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NW"),
        can_whirlpool
    )
    set_rule(
        get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_NE"),
        can_whirlpool
    )
    set_rule(
        get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SW"),
        can_whirlpool
    )
    set_rule(
        get_entrance("REGION_ROUTE_41 -> REGION_WHIRL_ISLAND_SE"),
        can_whirlpool
    )

    # Cianwood

    if hidden():
        set_rule(
            get_location(
                "Cianwood City - Hidden Item in West Rock"),
            can_rocksmash
        )

        set_rule(
            get_location(
                "Cianwood City - Hidden Item in North Rock"),
            can_rocksmash
        )

    set_rule(
        get_location(
            "Cianwood City - HM02 from Chuck's Wife"),
        lambda state: state.has(
            "EVENT_BEAT_CHUCK", world.player)
    )

    set_rule(
        get_location(
            "Cianwood Pharmacy - Secretpotion"),
        lambda state: state.has(
            "EVENT_JASMINE_EXPLAINED_AMPHYS_SICKNESS", world.player)
    )

    # Route 42

    set_rule(
        get_entrance("REGION_ECRUTEAK_CITY -> REGION_ROUTE_42"),
        can_surf
    )

    if hidden():
        set_rule(
            get_location("Route 42 - Hidden Item in Pond Rock"),
            can_surf
        )

    set_rule(
        get_location("Route 42 - Item 1"),
        can_surf
    )

    # Mahogany Town

    set_rule(
        get_entrance(
            "REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_MART_1F"),
        lambda state: state.has(
            "EVENT_DECIDED_TO_HELP_LANCE", world.player)
    )

    set_rule(
        get_entrance("REGION_MAHOGANY_TOWN -> REGION_ROUTE_44"),
        lambda state: has_n_badges(state, 7)
    )

    # Lake of Rage

    set_rule(
        get_location("Lake of Rage - Blackbelt from Wesley"),
        can_cut
    )

    set_rule(
        get_location("Lake of Rage - TM10 from Hidden Power House"),
        can_cut
    )

    if hidden():
        set_rule(
            get_location("Lake of Rage - Hidden Item Behind Cut Tree"),
            can_cut
        )

    set_rule(
        get_location("Lake of Rage - Item 1"),
        can_cut
    )

    set_rule(
        get_location("Lake of Rage - Item 2"),
        can_cut
    )

    # Route 44

    # Ice Path
    set_rule(
        get_entrance("REGION_ROUTE_44 -> REGION_ICE_PATH_1F"),
        can_strength
    )

    set_rule(
        get_entrance(
            "REGION_INDIGO_PLATEAU_POKECENTER_1F -> REGION_WILLS_ROOM"),
        lambda state: has_n_badges(state, 8)
    )

    set_rule(
        get_entrance(
            "REGION_DARK_CAVE_VIOLET_ENTRANCE -> REGION_DARK_CAVE_BLACKTHORN_ENTRANCE"),
        lambda state: False
    )

    set_rule(
        get_entrance("REGION_DARK_CAVE_VIOLET_ENTRANCE -> REGION_ROUTE_46"),
        can_rocksmash
    )
