from Options import PlandoConnection
from .connections import REVERSED_RANDOMIZED_CONNECTIONS
from .portals import find_spot
from .transitions import TRANSITIONS


def reverse_portal_exists_into_portal_plando(portal_exists: list[int]) -> list[PlandoConnection]:
    return [
        PlandoConnection("Autumn Hills", find_spot(portal_exists[0]), "both"),
        PlandoConnection("Riviere Turquoise", find_spot(portal_exists[1]), "both"),
        PlandoConnection("Howling Grotto", find_spot(portal_exists[2]), "both"),
        PlandoConnection("Sunken Shrine", find_spot(portal_exists[3]), "both"),
        PlandoConnection("Searing Crags", find_spot(portal_exists[4]), "both"),
        PlandoConnection("Glacial Peak", find_spot(portal_exists[5]), "both"),
    ]


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
