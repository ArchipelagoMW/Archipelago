from test.general import setup_solo_multiworld
from .bases import FF4FETestBase
from ...AutoWorld import call_all


class LogicTestBase(FF4FETestBase):
    boss_events = ["Boss 1 Defeated", "Boss 2 Defeated", "Boss 3 Defeated", "Boss 4 Defeated",
                   "Boss 5 Defeated", "Boss 6 Defeated", "Boss 7 Defeated", "Boss 8 Defeated", "Boss 9 Defeated"]
    supplementary_items = [*boss_events, "Candle", "Red Candle", "Raft", "Stepladder", "Recorder", "Bow", "Arrow",
                           "Silver Arrow"]

class DarkMatterHuntTest(FF4FETestBase):
    options = {
        "FindTheDarkMatter": "true"
    }