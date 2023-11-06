from typing import TYPE_CHECKING
from worlds.generic.Rules import add_rule, set_rule
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

    def defeated_n_gym_leaders(state: CollectionState, n: int) -> bool:
        return sum([state.has(event, world.player) for event in [
            "EVENT_BEAT_FALKNER",
            "EVENT_BEAT_BUGSY",
            "EVENT_BEAT_WHITNEY",
            "EVENT_BEAT_MORTY",
            "EVENT_BEAT_JASMINE",
            "EVENT_BEAT_CHUCK",
            "EVENT_BEAT_PRYCE",
            "EVENT_BEAT_CLAIR"

            # "EVENT_BEAT_BROCK",
            # "EVENT_BEAT_MISTY",
            # "EVENT_BEAT_LTSURGE",
            # "EVENT_BEAT_ERIKA",
            # "EVENT_BEAT_JANINE",
            # "EVENT_BEAT_SABRINA",
            # "EVENT_BEAT_BLAINE",
            # "EVENT_BEAT_BLUE"
        ]]) >= n

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

    # def get_location(location: str):
    #     if location in data.locations:
    #         location = data.locations[location].label

    world.multiworld.completion_condition[world.player] = lambda state: state.has(
        "EVENT_BEAT_ELITE_FOUR", world.player)

    # NEW BARK TOWN
    set_rule(
        get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_29"),
        lambda state: state.has("EVENT_GOT_A_POKEMON_FROM_ELM", world.player)
    )

    set_rule(
        get_entrance("REGION_NEW_BARK_TOWN -> REGION_ROUTE_27"),
        can_surf
    )

    set_rule(
        get_entrance("REGION_ROUTE_29_ROUTE_46_GATE -> REGION_ROUTE_46"),
        lambda state: False
    )

    set_rule(
        get_entrance("REGION_ROUTE_30 -> REGION_ROUTE_31"),
        lambda state: state.has(
            "EVENT_GOT_MYSTERY_EGG_FROM_MR_POKEMON", world.player)
    )

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

    set_rule(
        get_entrance("REGION_AZALEA_TOWN -> REGION_AZALEA_GYM"),
        lambda state: state.has(
            "EVENT_CLEARED_SLOWPOKE_WELL", world.player)
    )

    set_rule(
        get_entrance("REGION_AZALEA_TOWN -> REGION_ILEX_FOREST_AZALEA_GATE"),
        lambda state: state.has(
            "EVENT_BEAT_BUGSY", world.player)
    )

    set_rule(
        get_entrance("REGION_OLIVINE_CITY -> REGION_ROUTE_40"),
        can_surf
    )

    set_rule(
        get_entrance("REGION_ECRUTEAK_CITY -> REGION_ROUTE_42"),
        can_surf
    )

    set_rule(
        get_entrance(
            "REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_MART_1F"),
        lambda state: state.has(
            "EVENT_DECIDED_TO_HELP_LANCE", world.player)
    )

    set_rule(
        get_entrance("REGION_MAHOGANY_TOWN -> REGION_ROUTE_44"),
        lambda state: state.has(
            "EVENT_CLEARED_ROCKET_HIDEOUT", world.player)
    )

    set_rule(
        get_entrance("REGION_ROUTE_44 -> REGION_ICE_PATH_1F"),
        can_strength
    )

    set_rule(
        get_entrance(
            "REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION"),
        lambda state: state.has(
            "Pass", world.player)
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
        lambda state: state.has(
            "TM08 Rock Smash", world.player)
    )

    set_rule(
        get_entrance("REGION_OLIVINE_CITY -> REGION_OLIVINE_GYM"),
        lambda state: state.has(
            "EVENT_JASMINE_RETURNED_TO_GYM", world.player)
    )

    # set_rule(
    #     get_location(
    #         "EVENT_JASMINE_RETURNED_TO_GYM"),
    #     lambda state: state.has(
    #         "Secretpotion", world.player)
    # )
