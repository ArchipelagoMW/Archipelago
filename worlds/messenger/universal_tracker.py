from typing import TYPE_CHECKING

from BaseClasses import CollectionState
from Options import PlandoConnection

from .connections import RANDOMIZED_CONNECTIONS
from .portals import CHECKPOINTS, REGION_ORDER, SHOP_POINTS
from .rules import MessengerHardRules, MessengerRules
from .shop import FIGURINES, SHOP_ITEMS
from .transitions import TRANSITIONS

if TYPE_CHECKING:
    from . import MessengerWorld

REVERSED_RANDOMIZED_CONNECTIONS = {v: k for k, v in RANDOMIZED_CONNECTIONS.items()}
REVERSED_SHOP_ITEMS = {v.internal_name: k for k, v in (SHOP_ITEMS | FIGURINES).items()}
GLITCHED_ITEM = "Glitched Item"


def handle_auto_tabbing(data: str) -> int:
    match data:
        case "Level_01_NinjaVillage":
            return 1
        case "Level_02_AutumnHills":
            return 2
        case "Level_03_ForlornTemple":
            return 3
        case "Level_04_Catacombs":
            return 4
        case "Level_04_C_RiviereTurquoise":
            return 13
        case "Level_05_A_HowlingGrotto":
            return 6
        case "Level_05_B_SunkenShrine":
            return 14
        case "Level_06_A_BambooCreek":
            return 5
        case "Level_07_QuillshroomMarsh":
            return 7
        case "Level_08_SearingCrags":
            return 8
        case "Level_09_A_GlacialPeak":
            return 9
        case "Level_09_B_ElementalSkylands":
            return 15
        case "Level_10_A_TowerOfTime":
            return 10
        case "Level_11_A_CloudRuins":
            return 11
        case "Level_12_UnderWorld":
            return 12
        case _:
            return 0


TRACKER_PACK_CONFIG = {
    "external_pack_key": "ut_pack_path",
    "map_page_folder": "tracker",
    "map_page_maps": "maps/maps.json",
    "map_page_locations": [
        "locations/AutumnHills.json", "locations/BambooCreek.json", "locations/Catacombs.json", "locations/CloudRuins.json",
        "locations/CorruptedFuture.json", "locations/ElementalSkylands.json", "locations/ForlornTemple.json", "locations/GlacialPeak.json",
        "locations/HowlingGrotto.json", "locations/MusicBox.json", "locations/NinjaVillage.json", "locations/QuillshroomMarsh.json",
        "locations/RiviereTurquoise.json", "locations/SearingCrags.json", "locations/SunkenShrine.json", "locations/TheShop.json",
        "locations/TowerOfTime.json", "locations/Underworld.json"
    ],
    "map_page_setting_key": "Slot:{player}:CurrentRegion",
    "map_page_index": handle_auto_tabbing,
}


def find_spot(portal_key: int) -> str:
    """finds the spot associated with the portal key"""
    parent = REGION_ORDER[portal_key // 100]
    if portal_key % 100 == 0:
        return f"{parent} Portal"
    if portal_key % 100 // 10 == 1:
        return SHOP_POINTS[parent][portal_key % 10]
    return CHECKPOINTS[parent][portal_key % 10]


def reverse_portal_exits_into_portal_plando(portal_exits: list[int]) -> list[PlandoConnection]:
    return [
        PlandoConnection("Autumn Hills", find_spot(portal_exits[0]), "both"),
        PlandoConnection("Riviere Turquoise", find_spot(portal_exits[1]), "both"),
        PlandoConnection("Howling Grotto", find_spot(portal_exits[2]), "both"),
        PlandoConnection("Sunken Shrine", find_spot(portal_exits[3]), "both"),
        PlandoConnection("Searing Crags", find_spot(portal_exits[4]), "both"),
        PlandoConnection("Glacial Peak", find_spot(portal_exits[5]), "both"),
    ]

def reverse_shop_prices(
    shop_prices: dict[str, int], figures_prices: dict[str, int]
) -> tuple[dict[str, int], dict[str, int]]:
    return (
        {REVERSED_SHOP_ITEMS[item_internal_name]: price for item_internal_name, price in shop_prices.items()},
        {REVERSED_SHOP_ITEMS[item_internal_name]: price for item_internal_name, price in figures_prices.items()},
    )


def reverse_transitions_into_plando_connections(transitions: list[list[int]]) -> list[PlandoConnection]:
    plando_connections = []

    for connection in [
        PlandoConnection(REVERSED_RANDOMIZED_CONNECTIONS[TRANSITIONS[transition[0]]], TRANSITIONS[transition[1]], "both")
        for transition in transitions
    ]:
        if connection.exit in {con.entrance for con in plando_connections}:
            continue
        plando_connections.append(connection)

    return plando_connections


class MessengerGlitchedRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        super().__init__(world)

        hard_logic = MessengerHardRules(world)

        for connection in hard_logic.connection_rules.keys():
            hard_rule = hard_logic.connection_rules[connection]
            normal_rule = self.connection_rules[connection]
            if normal_rule != hard_rule:

                def glitch_aware_rule(
                    state: CollectionState, glitched_rule=normal_rule, previous_rule=hard_rule
                ) -> bool:
                    return (state.has(GLITCHED_ITEM, world.player) and glitched_rule(state)) or previous_rule(state)

                self.connection_rules[connection] = glitch_aware_rule

        for location in hard_logic.location_rules.keys():
            hard_rule = hard_logic.location_rules[location]
            normal_rule = self.location_rules[location]
            if normal_rule != hard_rule:

                def glitch_aware_rule(
                    state: CollectionState, glitched_rule=normal_rule, previous_rule=hard_rule
                ) -> bool:
                    return (state.has(GLITCHED_ITEM, world.player) and glitched_rule(state)) or previous_rule(state)

                self.location_rules[location] = glitch_aware_rule
