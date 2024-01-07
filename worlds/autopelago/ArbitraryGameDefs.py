from collections import ChainMap
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

    @classmethod
    def singles():
        return (r.name for r in AutopelagoRegion if len(r.name) == 1)

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
num_locations_in = dict(ChainMap([
    { r: 1 for r in AutopelagoRegion.singles() },
    {
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
    },
]))

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
_nxt_id: int
_nxt_id = BASE_ID

class AutopelagoLocationIds:

    @staticmethod
    def _next_one():
        global _nxt_id
        res = _nxt_id
        _nxt_id = _nxt_id + 1
        return res

    @staticmethod
    def _next_list(region: AutopelagoRegion):
        global _nxt_id
        res = [x for x in range(_nxt_id, _nxt_id + num_locations_in[region])]
        _nxt_id = res[-1] + 1
        return res

    goal = _next_one()
    a = _next_one()
    b = _next_one()
    c = _next_one()
    d = _next_one()
    e = _next_one()
    f = _next_one()
    before_8_rats = _next_list(AutopelagoRegion.Before8Rats)
    after_8_rats_before_a = _next_list(AutopelagoRegion.After8RatsBeforeA)
    after_8_rats_before_b = _next_list(AutopelagoRegion.After8RatsBeforeB)
    after_a_before_c = _next_list(AutopelagoRegion.AfterABeforeC)
    after_b_before_d = _next_list(AutopelagoRegion.AfterBBeforeD)
    after_c_before_20_rats = _next_list(AutopelagoRegion.AfterCBefore20Rats)
    after_d_before_20_rats = _next_list(AutopelagoRegion.AfterDBefore20Rats)
    after_20_rats_before_e = _next_list(AutopelagoRegion.After20RatsBeforeE)
    after_20_rats_before_f = _next_list(AutopelagoRegion.After20RatsBeforeF)

    @staticmethod
    def of(region: AutopelagoRegion):
        x = AutopelagoLocationIds
        match region:
            case AutopelagoRegion.TryingForGoal:
                return [x.goal]
            case AutopelagoRegion.A:
                return [x.a]
            case AutopelagoRegion.B:
                return [x.b]
            case AutopelagoRegion.C:
                return [x.c]
            case AutopelagoRegion.D:
                return [x.d]
            case AutopelagoRegion.E:
                return [x.e]
            case AutopelagoRegion.F:
                return [x.f]
            case AutopelagoRegion.Before8Rats:
                return x.before_8_rats
            case AutopelagoRegion.After8RatsBeforeA:
                return x.after_8_rats_before_a
            case AutopelagoRegion.After8RatsBeforeB:
                return x.after_8_rats_before_b
            case AutopelagoRegion.AfterABeforeC:
                return x.after_a_before_c
            case AutopelagoRegion.AfterBBeforeD:
                return x.after_b_before_d
            case AutopelagoRegion.AfterCBefore20Rats:
                return x.after_c_before_20_rats
            case AutopelagoRegion.AfterDBefore20Rats:
                return x.after_d_before_20_rats
            case AutopelagoRegion.After20RatsBeforeE:
                return x.after_20_rats_before_e
            case AutopelagoRegion.After20RatsBeforeF:
                return x.after_20_rats_before_f
            case _:
                raise KeyError
