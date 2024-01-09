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


# keep in sync with BASE_ID in the game code
BASE_ID = 300000

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
