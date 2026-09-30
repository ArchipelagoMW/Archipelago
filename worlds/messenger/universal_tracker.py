from Options import PlandoConnection
from .connections import RANDOMIZED_CONNECTIONS
from .portals import REGION_ORDER, SHOP_POINTS, CHECKPOINTS
from .shop import FIGURINES, SHOP_ITEMS
from .transitions import TRANSITIONS

REVERSED_RANDOMIZED_CONNECTIONS = {v: k for k, v in RANDOMIZED_CONNECTIONS.items()}
REVERSED_SHOP_ITEMS = {v.internal_name: k for k, v in (SHOP_ITEMS | FIGURINES).items()}


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
