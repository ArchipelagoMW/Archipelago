from BaseClasses import CollectionState, Callable
from typing import List

RABANASTRE = "Rabanastre Aeropass"
NALBINA = "Nalbina Aeropass"
BHUJERBA = "Bhujerba Aeropass"
ARCHADES = "Archades Aeropass"
BALFONHEIM = "Balfonheim Aeropass"

destination_reqs = {
    RABANASTRE: lambda state, player: True,
    NALBINA: lambda state, player: True,
    BHUJERBA: lambda state, player: False,
    ARCHADES: lambda state, player:
    state.has("Soul Ward Key", player) and
    (state.has("Defeat Bergan", player) or
     (state.has("Cactus Flower", player) and
      state.has("Defeat Vossler", player)) or
     (state.has("Wind Globe", player) and
      state.has("Windvane", player) and
      state.has("Defeat Vossler", player)) or
     state_has_aerodromes(state, "Balfonheim Aeropass", player, False))
    ,
    BALFONHEIM: lambda state, player:
    state.has("Defeat Bergan", player) or
    (state.has("Cactus Flower", player) and
     state.has("Defeat Vossler", player)) or
    (state.has("Wind Globe", player) and
     state.has("Windvane", player) and
     state.has("Defeat Vossler", player)) or
    (state.has("Soul Ward Key", player) and
     state_has_aerodromes(state, "Archades Aeropass", player, False))
}

destination_graph = {
    RABANASTRE: [NALBINA, BHUJERBA, ARCHADES],
    NALBINA: [RABANASTRE, ARCHADES, BALFONHEIM],
    BHUJERBA: [RABANASTRE, BALFONHEIM],
    ARCHADES: [RABANASTRE, NALBINA, BALFONHEIM],
    BALFONHEIM: [NALBINA, ARCHADES, BHUJERBA]
}

destination_strahl_needed = {
    RABANASTRE: 1,
    NALBINA: 1,
    BHUJERBA: 1,
    ARCHADES: 3,
    BALFONHEIM: 3
}

aeropass_stack = []


class AeropassValidator:
    def __init__(self, destination, allow_strahl=True):
        self.Destination = destination
        self.AllowStrahl = allow_strahl
        if destination not in destination_reqs:
            raise ValueError("Invalid destination: " + destination)

    def is_met_impl(self, state: CollectionState, player: int):

        for origin in destination_graph[self.Destination]:

            if (self.AllowStrahl and
                    state.has("Systems Access Key", player,
                              destination_strahl_needed[self.Destination]) and
                    state.has("Systems Access Key", player,
                              destination_strahl_needed[origin])):
                return True

            if (state.has(origin, player) and
                    self.is_origin_available(origin, state, player) and
                    state.has(self.Destination, player)):
                return True

        return False

    def is_met(self, state: CollectionState, player: int):
        if self in aeropass_stack:
            return False
        aeropass_stack.append(self)

        result = self.is_met_impl(state, player)

        aeropass_stack.remove(self)
        return result

    def is_origin_available(self, origin: str, state: CollectionState, player: int):
        return (destination_reqs[origin](state, player) or
                AeropassValidator(origin, self.AllowStrahl).is_met(state, player))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.Destination == other.Destination and self.AllowStrahl == other.AllowStrahl
        return False


def state_has_aerodromes(state: CollectionState, item: str, player: int, allow_strahl: bool) -> bool:
    return AeropassValidator(item, allow_strahl).is_met(state, player)


def state_has_at_least(possible: List[bool], count: int) -> bool:
    # Returns true if at least count of the possible are true
    return possible.count(True) >= count


def get_chara_count(state: CollectionState, player: int) -> int:
    count = 0
    if state.has("Vaan", player):
        count += 1
    if state.has("Balthier", player):
        count += 1
    if state.has("Fran", player):
        count += 1
    if state.has("Basch", player):
        count += 1
    if state.has("Ashe", player):
        count += 1
    if state.has("Penelo", player):
        count += 1
    if state.has("Guest", player):
        count += 1
    return count


def state_has_characters(state: CollectionState, difficulty: int, player: int) -> bool:
    chara_count = get_chara_count(state, player)
    if difficulty >= 7:
        return chara_count >= 6 and state.has("Second Board", player)
    if difficulty >= 5:
        return chara_count >= 5 and state.has("Second Board", player)
    if difficulty >= 4:
        return chara_count >= 4
    if difficulty >= 3:
        return chara_count >= 3
    return True
