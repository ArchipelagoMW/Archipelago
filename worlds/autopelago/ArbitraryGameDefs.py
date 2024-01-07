from enum import Enum, auto


# keep in sync with Region in the game code
class AutopelagoRegion(Enum):
    # Traveling = auto() # only used by the game
    Before8Rats = auto()
    After8RatsBeforeA = auto()
    After8RatsBeforeB = auto()
    A = auto()
    B = auto()
    AfterABeforeC = auto()
    AfterBBeforeD = auto()
    C = auto()
    D = auto()
    AfterCBefore20Rats = auto()
    AfterDBefore20Rats = auto()
    After20RatsBeforeE = auto()
    After20RatsBeforeF = auto()
    E = auto()
    F = auto()
    TryingForGoal = auto()
    # CompletedGoal = auto() # only used by the game

    def is_connected(self, to: "AutopelagoRegion"):
        conn = connected_regions[self]
        return to in conn if conn else False

    def get_location_name(self, i: int):
        match self:
            case AutopelagoRegion.Before8Rats:
                return f"b8r_{i}"
            case AutopelagoRegion.After8RatsBeforeA:
                return f"a8rba_{i}"
            case AutopelagoRegion.After8RatsBeforeB:
                return f"a8rbb_{i}"
            case AutopelagoRegion.AfterABeforeC:
                return f"aabc_{i}"
            case AutopelagoRegion.AfterBBeforeD:
                return f"abbd_{i}"
            case AutopelagoRegion.AfterCBefore20Rats:
                return f"acb20r_{i}"
            case AutopelagoRegion.AfterDBefore20Rats:
                return f"adb20r_{i}"
            case AutopelagoRegion.After20RatsBeforeE:
                return f"a20rbe_{i}"
            case AutopelagoRegion.After20RatsBeforeF:
                return f"a20rbf_{i}"
            case AutopelagoRegion.TryingForGoal:
                return "goal"
            case _:
                return self.name.lower()


# keep in sync with s_numLocationsIn in the game code
num_locations_in = {
    AutopelagoRegion.A: 1,
    AutopelagoRegion.B: 1,
    AutopelagoRegion.C: 1,
    AutopelagoRegion.D: 1,
    AutopelagoRegion.E: 1,
    AutopelagoRegion.F: 1,
    AutopelagoRegion.Before8Rats: 40,
    AutopelagoRegion.After8RatsBeforeA: 10,
    AutopelagoRegion.After8RatsBeforeB: 10,
    AutopelagoRegion.AfterABeforeC: 10,
    AutopelagoRegion.AfterBBeforeD: 10,
    AutopelagoRegion.AfterCBefore20Rats: 10,
    AutopelagoRegion.AfterDBefore20Rats: 10,
    AutopelagoRegion.After20RatsBeforeE: 20,
    AutopelagoRegion.After20RatsBeforeF: 20,
    AutopelagoRegion.TryingForGoal: 1,
}

# keep in sync with s_regionDistances in the game code
# as over there, only list forward for the sake of brevity and DRY
connected_regions: dict[AutopelagoRegion, set[AutopelagoRegion]] = {
    AutopelagoRegion.Before8Rats: { AutopelagoRegion.After8RatsBeforeA, AutopelagoRegion.After8RatsBeforeB },
    AutopelagoRegion.After8RatsBeforeA: { AutopelagoRegion.A },
    AutopelagoRegion.After8RatsBeforeB: { AutopelagoRegion.B },
    AutopelagoRegion.A: { AutopelagoRegion.AfterABeforeC },
    AutopelagoRegion.B: { AutopelagoRegion.AfterBBeforeD },
    AutopelagoRegion.AfterABeforeC: { AutopelagoRegion.C },
    AutopelagoRegion.AfterBBeforeD: { AutopelagoRegion.D },
    AutopelagoRegion.C: { AutopelagoRegion.AfterCBefore20Rats },
    AutopelagoRegion.D: { AutopelagoRegion.AfterDBefore20Rats },
    AutopelagoRegion.AfterCBefore20Rats: { AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.After20RatsBeforeF },
    AutopelagoRegion.AfterDBefore20Rats: { AutopelagoRegion.After20RatsBeforeE, AutopelagoRegion.After20RatsBeforeF },
    AutopelagoRegion.After20RatsBeforeE: { AutopelagoRegion.E },
    AutopelagoRegion.After20RatsBeforeF: { AutopelagoRegion.F },
    AutopelagoRegion.E: { AutopelagoRegion.TryingForGoal },
    AutopelagoRegion.F: { AutopelagoRegion.TryingForGoal },
    AutopelagoRegion.TryingForGoal: set(),
}
# complete the connected regions by including reverse-direction connections
for s, ts in connected_regions.items():
    for t in ts:
        connected_regions[t].add(s)

def get_autopelago_entrance_name(r_from: AutopelagoRegion, r_to: AutopelagoRegion):
    return f"from {r_from.name} to {r_to.name}"

# keep remainder in sync with everything derived from BASE_ID in the game code
BASE_ID = 300000
__nxt_id: int
__nxt_id = BASE_ID

def __next(region: AutopelagoRegion):
    global __nxt_id
    res = __nxt_id
    __nxt_id += num_locations_in[region]
    return res

location_base_ids = {
    r: __next(r) for r in AutopelagoRegion
}
