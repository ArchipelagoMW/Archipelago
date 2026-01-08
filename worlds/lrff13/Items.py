from typing import Dict, NamedTuple, Optional
from BaseClasses import Item, ItemClassification


class LRFF13Item(Item):
    game: str = "Lightning Returns: Final Fantasy XIII"


class LRFF13ItemData(NamedTuple):
    code: Optional[int] = None
    str_id: str = ""
    classification: ItemClassification = ItemClassification.filler
    category: str = ""
    weight: int = 0
    amount: int = 1
    duplicate_amount: int = 1
    traits: list = []


item_data_table: Dict[str, LRFF13ItemData] = {
    "Attack Lv 1": LRFF13ItemData(
        code=1,
        str_id="at010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Attack Lv 2": LRFF13ItemData(
        code=2,
        str_id="at010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Attack Lv 3": LRFF13ItemData(
        code=3,
        str_id="at010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Attack Lv 4": LRFF13ItemData(
        code=4,
        str_id="at010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Attack Lv 5": LRFF13ItemData(
        code=5,
        str_id="at010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Flamestrike Lv 1": LRFF13ItemData(
        code=6,
        str_id="at010_10_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Flamestrike Lv 2": LRFF13ItemData(
        code=7,
        str_id="at010_10_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Flamestrike Lv 3": LRFF13ItemData(
        code=8,
        str_id="at010_10_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Flamestrike Lv 4": LRFF13ItemData(
        code=9,
        str_id="at010_10_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Flamestrike Lv 5": LRFF13ItemData(
        code=10,
        str_id="at010_10_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Froststrike Lv 1": LRFF13ItemData(
        code=11,
        str_id="at010_20_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Froststrike Lv 2": LRFF13ItemData(
        code=12,
        str_id="at010_20_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Froststrike Lv 3": LRFF13ItemData(
        code=13,
        str_id="at010_20_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Froststrike Lv 4": LRFF13ItemData(
        code=14,
        str_id="at010_20_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Froststrike Lv 5": LRFF13ItemData(
        code=15,
        str_id="at010_20_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Sparkstrike Lv 1": LRFF13ItemData(
        code=16,
        str_id="at010_30_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Sparkstrike Lv 2": LRFF13ItemData(
        code=17,
        str_id="at010_30_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Sparkstrike Lv 3": LRFF13ItemData(
        code=18,
        str_id="at010_30_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Sparkstrike Lv 4": LRFF13ItemData(
        code=19,
        str_id="at010_30_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Sparkstrike Lv 5": LRFF13ItemData(
        code=20,
        str_id="at010_30_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Galestrike Lv 1": LRFF13ItemData(
        code=21,
        str_id="at010_50_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Galestrike Lv 2": LRFF13ItemData(
        code=22,
        str_id="at010_50_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Galestrike Lv 3": LRFF13ItemData(
        code=23,
        str_id="at010_50_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Galestrike Lv 4": LRFF13ItemData(
        code=24,
        str_id="at010_50_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Galestrike Lv 5": LRFF13ItemData(
        code=25,
        str_id="at010_50_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Light Slash Lv 1": LRFF13ItemData(
        code=26,
        str_id="at060_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Light Slash Lv 2": LRFF13ItemData(
        code=27,
        str_id="at060_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Light Slash Lv 3": LRFF13ItemData(
        code=28,
        str_id="at060_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Light Slash Lv 4": LRFF13ItemData(
        code=29,
        str_id="at060_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Light Slash Lv 5": LRFF13ItemData(
        code=30,
        str_id="at060_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Beat Down Lv 1": LRFF13ItemData(
        code=31,
        str_id="at130_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Beat Down Lv 2": LRFF13ItemData(
        code=32,
        str_id="at130_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Beat Down Lv 3": LRFF13ItemData(
        code=33,
        str_id="at130_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Beat Down Lv 4": LRFF13ItemData(
        code=34,
        str_id="at130_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Beat Down Lv 5": LRFF13ItemData(
        code=35,
        str_id="at130_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Fatal Sweep Lv 1": LRFF13ItemData(
        code=36,
        str_id="at150_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Fatal Sweep Lv 2": LRFF13ItemData(
        code=37,
        str_id="at150_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Fatal Sweep Lv 3": LRFF13ItemData(
        code=38,
        str_id="at150_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Fatal Sweep Lv 4": LRFF13ItemData(
        code=39,
        str_id="at150_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Fatal Sweep Lv 5": LRFF13ItemData(
        code=40,
        str_id="at150_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Charged Strike Lv 1": LRFF13ItemData(
        code=41,
        str_id="at160_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Charged Strike Lv 2": LRFF13ItemData(
        code=42,
        str_id="at160_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Charged Strike Lv 3": LRFF13ItemData(
        code=43,
        str_id="at160_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Charged Strike Lv 4": LRFF13ItemData(
        code=44,
        str_id="at160_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Charged Strike Lv 5": LRFF13ItemData(
        code=45,
        str_id="at160_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Blitz Lv 1": LRFF13ItemData(
        code=46,
        str_id="at520_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Blitz Lv 2": LRFF13ItemData(
        code=47,
        str_id="at520_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Blitz Lv 3": LRFF13ItemData(
        code=48,
        str_id="at520_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Blitz Lv 4": LRFF13ItemData(
        code=49,
        str_id="at520_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Blitz Lv 5": LRFF13ItemData(
        code=50,
        str_id="at520_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Area Sweep Lv 1": LRFF13ItemData(
        code=51,
        str_id="at620_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Area Sweep Lv 2": LRFF13ItemData(
        code=52,
        str_id="at620_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Area Sweep Lv 3": LRFF13ItemData(
        code=53,
        str_id="at620_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Area Sweep Lv 4": LRFF13ItemData(
        code=54,
        str_id="at620_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Area Sweep Lv 5": LRFF13ItemData(
        code=55,
        str_id="at620_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Heat Blitz Lv 1": LRFF13ItemData(
        code=56,
        str_id="at620_10_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Heat Blitz Lv 2": LRFF13ItemData(
        code=57,
        str_id="at620_10_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Heat Blitz Lv 3": LRFF13ItemData(
        code=58,
        str_id="at620_10_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Heat Blitz Lv 4": LRFF13ItemData(
        code=59,
        str_id="at620_10_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Heat Blitz Lv 5": LRFF13ItemData(
        code=60,
        str_id="at620_10_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Ice Blitz Lv 1": LRFF13ItemData(
        code=61,
        str_id="at620_20_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Ice Blitz Lv 2": LRFF13ItemData(
        code=62,
        str_id="at620_20_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Ice Blitz Lv 3": LRFF13ItemData(
        code=63,
        str_id="at620_20_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Ice Blitz Lv 4": LRFF13ItemData(
        code=64,
        str_id="at620_20_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Ice Blitz Lv 5": LRFF13ItemData(
        code=65,
        str_id="at620_20_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Electric Blitz Lv 1": LRFF13ItemData(
        code=66,
        str_id="at620_30_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Electric Blitz Lv 2": LRFF13ItemData(
        code=67,
        str_id="at620_30_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Electric Blitz Lv 3": LRFF13ItemData(
        code=68,
        str_id="at620_30_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Electric Blitz Lv 4": LRFF13ItemData(
        code=69,
        str_id="at620_30_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Electric Blitz Lv 5": LRFF13ItemData(
        code=70,
        str_id="at620_30_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Aero Blitz Lv 1": LRFF13ItemData(
        code=71,
        str_id="at620_50_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Aero Blitz Lv 2": LRFF13ItemData(
        code=72,
        str_id="at620_50_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Aero Blitz Lv 3": LRFF13ItemData(
        code=73,
        str_id="at620_50_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Aero Blitz Lv 4": LRFF13ItemData(
        code=74,
        str_id="at620_50_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Aero Blitz Lv 5": LRFF13ItemData(
        code=75,
        str_id="at620_50_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Punt Lv 1": LRFF13ItemData(
        code=76,
        str_id="at700_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Punt Lv 2": LRFF13ItemData(
        code=77,
        str_id="at700_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Punt Lv 3": LRFF13ItemData(
        code=78,
        str_id="at700_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Punt Lv 4": LRFF13ItemData(
        code=79,
        str_id="at700_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Punt Lv 5": LRFF13ItemData(
        code=80,
        str_id="at700_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Heavy Slash Lv 1": LRFF13ItemData(
        code=81,
        str_id="at800_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Heavy Slash Lv 2": LRFF13ItemData(
        code=82,
        str_id="at800_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Heavy Slash Lv 3": LRFF13ItemData(
        code=83,
        str_id="at800_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Heavy Slash Lv 4": LRFF13ItemData(
        code=84,
        str_id="at800_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Heavy Slash Lv 5": LRFF13ItemData(
        code=85,
        str_id="at800_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Evade Lv 1": LRFF13ItemData(
        code=86,
        str_id="av010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Evade Lv 2": LRFF13ItemData(
        code=87,
        str_id="av010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Evade Lv 3": LRFF13ItemData(
        code=88,
        str_id="av010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Evade Lv 4": LRFF13ItemData(
        code=89,
        str_id="av010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Evade Lv 5": LRFF13ItemData(
        code=90,
        str_id="av010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "ATB Charge Lv 1": LRFF13ItemData(
        code=91,
        str_id="ac300_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "ATB Charge Lv 2": LRFF13ItemData(
        code=92,
        str_id="ac300_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "ATB Charge Lv 3": LRFF13ItemData(
        code=93,
        str_id="ac300_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "ATB Charge Lv 4": LRFF13ItemData(
        code=94,
        str_id="ac300_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "ATB Charge Lv 5": LRFF13ItemData(
        code=95,
        str_id="ac300_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Counterblow Lv 1": LRFF13ItemData(
        code=96,
        str_id="ga010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Counterblow Lv 2": LRFF13ItemData(
        code=97,
        str_id="ga010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Counterblow Lv 3": LRFF13ItemData(
        code=98,
        str_id="ga010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Counterblow Lv 4": LRFF13ItemData(
        code=99,
        str_id="ga010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Counterblow Lv 5": LRFF13ItemData(
        code=100,
        str_id="ga010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Counterspell Lv 1": LRFF13ItemData(
        code=101,
        str_id="ga110_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Counterspell Lv 2": LRFF13ItemData(
        code=102,
        str_id="ga110_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Counterspell Lv 3": LRFF13ItemData(
        code=103,
        str_id="ga110_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Counterspell Lv 4": LRFF13ItemData(
        code=104,
        str_id="ga110_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Counterspell Lv 5": LRFF13ItemData(
        code=105,
        str_id="ga110_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Steelguard Lv 1": LRFF13ItemData(
        code=106,
        str_id="gd010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Steelguard Lv 2": LRFF13ItemData(
        code=107,
        str_id="gd010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Steelguard Lv 3": LRFF13ItemData(
        code=108,
        str_id="gd010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Steelguard Lv 4": LRFF13ItemData(
        code=109,
        str_id="gd010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Steelguard Lv 5": LRFF13ItemData(
        code=110,
        str_id="gd010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Guard Lv 1": LRFF13ItemData(
        code=111,
        str_id="gd020_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Guard Lv 2": LRFF13ItemData(
        code=112,
        str_id="gd020_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Guard Lv 3": LRFF13ItemData(
        code=113,
        str_id="gd020_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Guard Lv 4": LRFF13ItemData(
        code=114,
        str_id="gd020_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Guard Lv 5": LRFF13ItemData(
        code=115,
        str_id="gd020_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Light Guard Lv 1": LRFF13ItemData(
        code=116,
        str_id="gd030_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Light Guard Lv 2": LRFF13ItemData(
        code=117,
        str_id="gd030_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Light Guard Lv 3": LRFF13ItemData(
        code=118,
        str_id="gd030_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Light Guard Lv 4": LRFF13ItemData(
        code=119,
        str_id="gd030_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Light Guard Lv 5": LRFF13ItemData(
        code=120,
        str_id="gd030_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Heavy Guard Lv 1": LRFF13ItemData(
        code=121,
        str_id="gd040_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Heavy Guard Lv 2": LRFF13ItemData(
        code=122,
        str_id="gd040_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Heavy Guard Lv 3": LRFF13ItemData(
        code=123,
        str_id="gd040_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Heavy Guard Lv 4": LRFF13ItemData(
        code=124,
        str_id="gd040_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Heavy Guard Lv 5": LRFF13ItemData(
        code=125,
        str_id="gd040_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Mediguard Lv 1": LRFF13ItemData(
        code=126,
        str_id="gd110_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Mediguard Lv 2": LRFF13ItemData(
        code=127,
        str_id="gd110_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Mediguard Lv 3": LRFF13ItemData(
        code=128,
        str_id="gd110_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Mediguard Lv 4": LRFF13ItemData(
        code=129,
        str_id="gd110_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Mediguard Lv 5": LRFF13ItemData(
        code=130,
        str_id="gd110_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "NulAll Guard Lv 1": LRFF13ItemData(
        code=131,
        str_id="gd510_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "NulAll Guard Lv 2": LRFF13ItemData(
        code=132,
        str_id="gd510_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "NulAll Guard Lv 3": LRFF13ItemData(
        code=133,
        str_id="gd510_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "NulAll Guard Lv 4": LRFF13ItemData(
        code=134,
        str_id="gd510_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "NulAll Guard Lv 5": LRFF13ItemData(
        code=135,
        str_id="gd510_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Heroic Guard Lv 1": LRFF13ItemData(
        code=136,
        str_id="gd810_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Heroic Guard Lv 2": LRFF13ItemData(
        code=137,
        str_id="gd810_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Heroic Guard Lv 3": LRFF13ItemData(
        code=138,
        str_id="gd810_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Heroic Guard Lv 4": LRFF13ItemData(
        code=139,
        str_id="gd810_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Heroic Guard Lv 5": LRFF13ItemData(
        code=140,
        str_id="gd810_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Ruin Lv 1": LRFF13ItemData(
        code=141,
        str_id="ma000_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Ruin Lv 2": LRFF13ItemData(
        code=142,
        str_id="ma000_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Ruin Lv 3": LRFF13ItemData(
        code=143,
        str_id="ma000_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Ruin Lv 4": LRFF13ItemData(
        code=144,
        str_id="ma000_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Ruin Lv 5": LRFF13ItemData(
        code=145,
        str_id="ma000_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Ruinga Lv 1": LRFF13ItemData(
        code=146,
        str_id="ma020_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Ruinga Lv 2": LRFF13ItemData(
        code=147,
        str_id="ma020_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Ruinga Lv 3": LRFF13ItemData(
        code=148,
        str_id="ma020_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Ruinga Lv 4": LRFF13ItemData(
        code=149,
        str_id="ma020_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Ruinga Lv 5": LRFF13ItemData(
        code=150,
        str_id="ma020_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Magnet Lv 1": LRFF13ItemData(
        code=151,
        str_id="ma100_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Magnet Lv 2": LRFF13ItemData(
        code=152,
        str_id="ma100_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Magnet Lv 3": LRFF13ItemData(
        code=153,
        str_id="ma100_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Magnet Lv 4": LRFF13ItemData(
        code=154,
        str_id="ma100_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Magnet Lv 5": LRFF13ItemData(
        code=155,
        str_id="ma100_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Fire Lv 1": LRFF13ItemData(
        code=156,
        str_id="mb000_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Fire Lv 2": LRFF13ItemData(
        code=157,
        str_id="mb000_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Fire Lv 3": LRFF13ItemData(
        code=158,
        str_id="mb000_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Fire Lv 4": LRFF13ItemData(
        code=159,
        str_id="mb000_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Fire Lv 5": LRFF13ItemData(
        code=160,
        str_id="mb000_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Fira Lv 1": LRFF13ItemData(
        code=161,
        str_id="mb010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Fira Lv 2": LRFF13ItemData(
        code=162,
        str_id="mb010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Fira Lv 3": LRFF13ItemData(
        code=163,
        str_id="mb010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Fira Lv 4": LRFF13ItemData(
        code=164,
        str_id="mb010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Fira Lv 5": LRFF13ItemData(
        code=165,
        str_id="mb010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Firaga Lv 1": LRFF13ItemData(
        code=166,
        str_id="mb020_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Firaga Lv 2": LRFF13ItemData(
        code=167,
        str_id="mb020_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Firaga Lv 3": LRFF13ItemData(
        code=168,
        str_id="mb020_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Firaga Lv 4": LRFF13ItemData(
        code=169,
        str_id="mb020_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Firaga Lv 5": LRFF13ItemData(
        code=170,
        str_id="mb020_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Flare Lv 1": LRFF13ItemData(
        code=171,
        str_id="mb030_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Flare Lv 2": LRFF13ItemData(
        code=172,
        str_id="mb030_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Flare Lv 3": LRFF13ItemData(
        code=173,
        str_id="mb030_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Flare Lv 4": LRFF13ItemData(
        code=174,
        str_id="mb030_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Flare Lv 5": LRFF13ItemData(
        code=175,
        str_id="mb030_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Blizzard Lv 1": LRFF13ItemData(
        code=176,
        str_id="mb100_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Blizzard Lv 2": LRFF13ItemData(
        code=177,
        str_id="mb100_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Blizzard Lv 3": LRFF13ItemData(
        code=178,
        str_id="mb100_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Blizzard Lv 4": LRFF13ItemData(
        code=179,
        str_id="mb100_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Blizzard Lv 5": LRFF13ItemData(
        code=180,
        str_id="mb100_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Blizzara Lv 1": LRFF13ItemData(
        code=181,
        str_id="mb110_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Blizzara Lv 2": LRFF13ItemData(
        code=182,
        str_id="mb110_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Blizzara Lv 3": LRFF13ItemData(
        code=183,
        str_id="mb110_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Blizzara Lv 4": LRFF13ItemData(
        code=184,
        str_id="mb110_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Blizzara Lv 5": LRFF13ItemData(
        code=185,
        str_id="mb110_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Blizzaga Lv 1": LRFF13ItemData(
        code=186,
        str_id="mb120_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Blizzaga Lv 2": LRFF13ItemData(
        code=187,
        str_id="mb120_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Blizzaga Lv 3": LRFF13ItemData(
        code=188,
        str_id="mb120_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Blizzaga Lv 4": LRFF13ItemData(
        code=189,
        str_id="mb120_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Blizzaga Lv 5": LRFF13ItemData(
        code=190,
        str_id="mb120_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Chill Lv 1": LRFF13ItemData(
        code=191,
        str_id="mb130_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Chill Lv 2": LRFF13ItemData(
        code=192,
        str_id="mb130_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Chill Lv 3": LRFF13ItemData(
        code=193,
        str_id="mb130_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Chill Lv 4": LRFF13ItemData(
        code=194,
        str_id="mb130_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Chill Lv 5": LRFF13ItemData(
        code=195,
        str_id="mb130_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Thunder Lv 1": LRFF13ItemData(
        code=196,
        str_id="mb200_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Thunder Lv 2": LRFF13ItemData(
        code=197,
        str_id="mb200_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Thunder Lv 3": LRFF13ItemData(
        code=198,
        str_id="mb200_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Thunder Lv 4": LRFF13ItemData(
        code=199,
        str_id="mb200_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Thunder Lv 5": LRFF13ItemData(
        code=200,
        str_id="mb200_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Thundara Lv 1": LRFF13ItemData(
        code=201,
        str_id="mb210_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Thundara Lv 2": LRFF13ItemData(
        code=202,
        str_id="mb210_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Thundara Lv 3": LRFF13ItemData(
        code=203,
        str_id="mb210_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Thundara Lv 4": LRFF13ItemData(
        code=204,
        str_id="mb210_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Thundara Lv 5": LRFF13ItemData(
        code=205,
        str_id="mb210_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Thundaga Lv 1": LRFF13ItemData(
        code=206,
        str_id="mb220_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Thundaga Lv 2": LRFF13ItemData(
        code=207,
        str_id="mb220_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Thundaga Lv 3": LRFF13ItemData(
        code=208,
        str_id="mb220_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Thundaga Lv 4": LRFF13ItemData(
        code=209,
        str_id="mb220_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Thundaga Lv 5": LRFF13ItemData(
        code=210,
        str_id="mb220_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Surge Lv 1": LRFF13ItemData(
        code=211,
        str_id="mb230_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Surge Lv 2": LRFF13ItemData(
        code=212,
        str_id="mb230_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Surge Lv 3": LRFF13ItemData(
        code=213,
        str_id="mb230_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Surge Lv 4": LRFF13ItemData(
        code=214,
        str_id="mb230_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Surge Lv 5": LRFF13ItemData(
        code=215,
        str_id="mb230_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Aero Lv 1": LRFF13ItemData(
        code=216,
        str_id="mb400_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Aero Lv 2": LRFF13ItemData(
        code=217,
        str_id="mb400_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Aero Lv 3": LRFF13ItemData(
        code=218,
        str_id="mb400_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Aero Lv 4": LRFF13ItemData(
        code=219,
        str_id="mb400_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Aero Lv 5": LRFF13ItemData(
        code=220,
        str_id="mb400_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Aerora Lv 1": LRFF13ItemData(
        code=221,
        str_id="mb410_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Aerora Lv 2": LRFF13ItemData(
        code=222,
        str_id="mb410_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Aerora Lv 3": LRFF13ItemData(
        code=223,
        str_id="mb410_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Aerora Lv 4": LRFF13ItemData(
        code=224,
        str_id="mb410_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Aerora Lv 5": LRFF13ItemData(
        code=225,
        str_id="mb410_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Aeroga Lv 1": LRFF13ItemData(
        code=226,
        str_id="mb420_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Aeroga Lv 2": LRFF13ItemData(
        code=227,
        str_id="mb420_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Aeroga Lv 3": LRFF13ItemData(
        code=228,
        str_id="mb420_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Aeroga Lv 4": LRFF13ItemData(
        code=229,
        str_id="mb420_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Aeroga Lv 5": LRFF13ItemData(
        code=230,
        str_id="mb420_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Tornado Lv 1": LRFF13ItemData(
        code=231,
        str_id="mb430_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Tornado Lv 2": LRFF13ItemData(
        code=232,
        str_id="mb430_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Tornado Lv 3": LRFF13ItemData(
        code=233,
        str_id="mb430_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Tornado Lv 4": LRFF13ItemData(
        code=234,
        str_id="mb430_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Tornado Lv 5": LRFF13ItemData(
        code=235,
        str_id="mb430_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Flamespark Lv 1": LRFF13ItemData(
        code=236,
        str_id="mc100_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Flamespark Lv 2": LRFF13ItemData(
        code=237,
        str_id="mc100_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Flamespark Lv 3": LRFF13ItemData(
        code=238,
        str_id="mc100_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Flamespark Lv 4": LRFF13ItemData(
        code=239,
        str_id="mc100_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Flamespark Lv 5": LRFF13ItemData(
        code=240,
        str_id="mc100_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Flamesparka Lv 1": LRFF13ItemData(
        code=241,
        str_id="mc110_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Flamesparka Lv 2": LRFF13ItemData(
        code=242,
        str_id="mc110_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Flamesparka Lv 3": LRFF13ItemData(
        code=243,
        str_id="mc110_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Flamesparka Lv 4": LRFF13ItemData(
        code=244,
        str_id="mc110_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Flamesparka Lv 5": LRFF13ItemData(
        code=245,
        str_id="mc110_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Firestorm Lv 1": LRFF13ItemData(
        code=246,
        str_id="mc200_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Firestorm Lv 2": LRFF13ItemData(
        code=247,
        str_id="mc200_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Firestorm Lv 3": LRFF13ItemData(
        code=248,
        str_id="mc200_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Firestorm Lv 4": LRFF13ItemData(
        code=249,
        str_id="mc200_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Firestorm Lv 5": LRFF13ItemData(
        code=250,
        str_id="mc200_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Firestorma Lv 1": LRFF13ItemData(
        code=251,
        str_id="mc210_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Firestorma Lv 2": LRFF13ItemData(
        code=252,
        str_id="mc210_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Firestorma Lv 3": LRFF13ItemData(
        code=253,
        str_id="mc210_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Firestorma Lv 4": LRFF13ItemData(
        code=254,
        str_id="mc210_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Firestorma Lv 5": LRFF13ItemData(
        code=255,
        str_id="mc210_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Icespark Lv 1": LRFF13ItemData(
        code=256,
        str_id="mc300_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Icespark Lv 2": LRFF13ItemData(
        code=257,
        str_id="mc300_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Icespark Lv 3": LRFF13ItemData(
        code=258,
        str_id="mc300_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Icespark Lv 4": LRFF13ItemData(
        code=259,
        str_id="mc300_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Icespark Lv 5": LRFF13ItemData(
        code=260,
        str_id="mc300_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Icesparka Lv 1": LRFF13ItemData(
        code=261,
        str_id="mc310_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Icesparka Lv 2": LRFF13ItemData(
        code=262,
        str_id="mc310_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Icesparka Lv 3": LRFF13ItemData(
        code=263,
        str_id="mc310_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Icesparka Lv 4": LRFF13ItemData(
        code=264,
        str_id="mc310_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Icesparka Lv 5": LRFF13ItemData(
        code=265,
        str_id="mc310_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Icestorm Lv 1": LRFF13ItemData(
        code=266,
        str_id="mc400_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Icestorm Lv 2": LRFF13ItemData(
        code=267,
        str_id="mc400_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Icestorm Lv 3": LRFF13ItemData(
        code=268,
        str_id="mc400_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Icestorm Lv 4": LRFF13ItemData(
        code=269,
        str_id="mc400_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Icestorm Lv 5": LRFF13ItemData(
        code=270,
        str_id="mc400_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Icestorma Lv 1": LRFF13ItemData(
        code=271,
        str_id="mc410_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Icestorma Lv 2": LRFF13ItemData(
        code=272,
        str_id="mc410_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Icestorma Lv 3": LRFF13ItemData(
        code=273,
        str_id="mc410_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Icestorma Lv 4": LRFF13ItemData(
        code=274,
        str_id="mc410_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Icestorma Lv 5": LRFF13ItemData(
        code=275,
        str_id="mc410_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Element Lv 1": LRFF13ItemData(
        code=276,
        str_id="mc900_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Element Lv 2": LRFF13ItemData(
        code=277,
        str_id="mc900_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Element Lv 3": LRFF13ItemData(
        code=278,
        str_id="mc900_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Element Lv 4": LRFF13ItemData(
        code=279,
        str_id="mc900_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Element Lv 5": LRFF13ItemData(
        code=280,
        str_id="mc900_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Elementa Lv 1": LRFF13ItemData(
        code=281,
        str_id="mc910_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Elementa Lv 2": LRFF13ItemData(
        code=282,
        str_id="mc910_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Elementa Lv 3": LRFF13ItemData(
        code=283,
        str_id="mc910_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Elementa Lv 4": LRFF13ItemData(
        code=284,
        str_id="mc910_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Elementa Lv 5": LRFF13ItemData(
        code=285,
        str_id="mc910_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Deprotect Lv 1": LRFF13ItemData(
        code=286,
        str_id="mg000_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Deprotect Lv 2": LRFF13ItemData(
        code=287,
        str_id="mg000_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Deprotect Lv 3": LRFF13ItemData(
        code=288,
        str_id="mg000_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Deprotect Lv 4": LRFF13ItemData(
        code=289,
        str_id="mg000_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Deprotect Lv 5": LRFF13ItemData(
        code=290,
        str_id="mg000_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Deshell Lv 1": LRFF13ItemData(
        code=291,
        str_id="mg010_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Deshell Lv 2": LRFF13ItemData(
        code=292,
        str_id="mg010_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Deshell Lv 3": LRFF13ItemData(
        code=293,
        str_id="mg010_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Deshell Lv 4": LRFF13ItemData(
        code=294,
        str_id="mg010_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Deshell Lv 5": LRFF13ItemData(
        code=295,
        str_id="mg010_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Poison Lv 1": LRFF13ItemData(
        code=296,
        str_id="mg020_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Poison Lv 2": LRFF13ItemData(
        code=297,
        str_id="mg020_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Poison Lv 3": LRFF13ItemData(
        code=298,
        str_id="mg020_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Poison Lv 4": LRFF13ItemData(
        code=299,
        str_id="mg020_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Poison Lv 5": LRFF13ItemData(
        code=300,
        str_id="mg020_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Imperil Lv 1": LRFF13ItemData(
        code=301,
        str_id="mg030_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Imperil Lv 2": LRFF13ItemData(
        code=302,
        str_id="mg030_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Imperil Lv 3": LRFF13ItemData(
        code=303,
        str_id="mg030_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Imperil Lv 4": LRFF13ItemData(
        code=304,
        str_id="mg030_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Imperil Lv 5": LRFF13ItemData(
        code=305,
        str_id="mg030_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Deprotega Lv 1": LRFF13ItemData(
        code=306,
        str_id="mg200_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Deprotega Lv 2": LRFF13ItemData(
        code=307,
        str_id="mg200_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Deprotega Lv 3": LRFF13ItemData(
        code=308,
        str_id="mg200_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Deprotega Lv 4": LRFF13ItemData(
        code=309,
        str_id="mg200_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Deprotega Lv 5": LRFF13ItemData(
        code=310,
        str_id="mg200_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Deshellga Lv 1": LRFF13ItemData(
        code=311,
        str_id="mg210_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Deshellga Lv 2": LRFF13ItemData(
        code=312,
        str_id="mg210_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Deshellga Lv 3": LRFF13ItemData(
        code=313,
        str_id="mg210_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Deshellga Lv 4": LRFF13ItemData(
        code=314,
        str_id="mg210_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Deshellga Lv 5": LRFF13ItemData(
        code=315,
        str_id="mg210_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Poisonga Lv 1": LRFF13ItemData(
        code=316,
        str_id="mg220_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Poisonga Lv 2": LRFF13ItemData(
        code=317,
        str_id="mg220_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Poisonga Lv 3": LRFF13ItemData(
        code=318,
        str_id="mg220_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Poisonga Lv 4": LRFF13ItemData(
        code=319,
        str_id="mg220_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Poisonga Lv 5": LRFF13ItemData(
        code=320,
        str_id="mg220_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Imperilga Lv 1": LRFF13ItemData(
        code=321,
        str_id="mg230_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Imperilga Lv 2": LRFF13ItemData(
        code=322,
        str_id="mg230_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Imperilga Lv 3": LRFF13ItemData(
        code=323,
        str_id="mg230_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Imperilga Lv 4": LRFF13ItemData(
        code=324,
        str_id="mg230_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Imperilga Lv 5": LRFF13ItemData(
        code=325,
        str_id="mg230_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Dispel Lv 1": LRFF13ItemData(
        code=326,
        str_id="mg240_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Dispel Lv 2": LRFF13ItemData(
        code=327,
        str_id="mg240_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Dispel Lv 3": LRFF13ItemData(
        code=328,
        str_id="mg240_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Dispel Lv 4": LRFF13ItemData(
        code=329,
        str_id="mg240_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Dispel Lv 5": LRFF13ItemData(
        code=330,
        str_id="mg240_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Dispelga Lv 1": LRFF13ItemData(
        code=331,
        str_id="mg250_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Dispelga Lv 2": LRFF13ItemData(
        code=332,
        str_id="mg250_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Dispelga Lv 3": LRFF13ItemData(
        code=333,
        str_id="mg250_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Dispelga Lv 4": LRFF13ItemData(
        code=334,
        str_id="mg250_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Dispelga Lv 5": LRFF13ItemData(
        code=335,
        str_id="mg250_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Slow Lv 1": LRFF13ItemData(
        code=336,
        str_id="mg500_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Slow Lv 2": LRFF13ItemData(
        code=337,
        str_id="mg500_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Slow Lv 3": LRFF13ItemData(
        code=338,
        str_id="mg500_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Slow Lv 4": LRFF13ItemData(
        code=339,
        str_id="mg500_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Slow Lv 5": LRFF13ItemData(
        code=340,
        str_id="mg500_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Curse Lv 1": LRFF13ItemData(
        code=341,
        str_id="mg530_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Curse Lv 2": LRFF13ItemData(
        code=342,
        str_id="mg530_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Curse Lv 3": LRFF13ItemData(
        code=343,
        str_id="mg530_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Curse Lv 4": LRFF13ItemData(
        code=344,
        str_id="mg530_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Curse Lv 5": LRFF13ItemData(
        code=345,
        str_id="mg530_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Debrave Lv 1": LRFF13ItemData(
        code=346,
        str_id="mg560_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Debrave Lv 2": LRFF13ItemData(
        code=347,
        str_id="mg560_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Debrave Lv 3": LRFF13ItemData(
        code=348,
        str_id="mg560_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Debrave Lv 4": LRFF13ItemData(
        code=349,
        str_id="mg560_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Debrave Lv 5": LRFF13ItemData(
        code=350,
        str_id="mg560_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Defaith Lv 1": LRFF13ItemData(
        code=351,
        str_id="mg570_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Defaith Lv 2": LRFF13ItemData(
        code=352,
        str_id="mg570_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Defaith Lv 3": LRFF13ItemData(
        code=353,
        str_id="mg570_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Defaith Lv 4": LRFF13ItemData(
        code=354,
        str_id="mg570_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Defaith Lv 5": LRFF13ItemData(
        code=355,
        str_id="mg570_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Slowga Lv 1": LRFF13ItemData(
        code=356,
        str_id="mg700_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Slowga Lv 2": LRFF13ItemData(
        code=357,
        str_id="mg700_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Slowga Lv 3": LRFF13ItemData(
        code=358,
        str_id="mg700_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Slowga Lv 4": LRFF13ItemData(
        code=359,
        str_id="mg700_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Slowga Lv 5": LRFF13ItemData(
        code=360,
        str_id="mg700_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Cursega Lv 1": LRFF13ItemData(
        code=361,
        str_id="mg730_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Cursega Lv 2": LRFF13ItemData(
        code=362,
        str_id="mg730_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Cursega Lv 3": LRFF13ItemData(
        code=363,
        str_id="mg730_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Cursega Lv 4": LRFF13ItemData(
        code=364,
        str_id="mg730_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Cursega Lv 5": LRFF13ItemData(
        code=365,
        str_id="mg730_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Debravega Lv 1": LRFF13ItemData(
        code=366,
        str_id="mg760_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Debravega Lv 2": LRFF13ItemData(
        code=367,
        str_id="mg760_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Debravega Lv 3": LRFF13ItemData(
        code=368,
        str_id="mg760_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Debravega Lv 4": LRFF13ItemData(
        code=369,
        str_id="mg760_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Debravega Lv 5": LRFF13ItemData(
        code=370,
        str_id="mg760_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Defaithga Lv 1": LRFF13ItemData(
        code=371,
        str_id="mg770_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Defaithga Lv 2": LRFF13ItemData(
        code=372,
        str_id="mg770_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Defaithga Lv 3": LRFF13ItemData(
        code=373,
        str_id="mg770_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Defaithga Lv 4": LRFF13ItemData(
        code=374,
        str_id="mg770_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Defaithga Lv 5": LRFF13ItemData(
        code=375,
        str_id="mg770_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Disaster Lv 1": LRFF13ItemData(
        code=376,
        str_id="mg900_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Disaster Lv 2": LRFF13ItemData(
        code=377,
        str_id="mg900_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Disaster Lv 3": LRFF13ItemData(
        code=378,
        str_id="mg900_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Disaster Lv 4": LRFF13ItemData(
        code=379,
        str_id="mg900_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Disaster Lv 5": LRFF13ItemData(
        code=380,
        str_id="mg900_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Ultima Lv 1": LRFF13ItemData(
        code=381,
        str_id="ms900_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Ultima Lv 2": LRFF13ItemData(
        code=382,
        str_id="ms900_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Ultima Lv 3": LRFF13ItemData(
        code=383,
        str_id="ms900_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Ultima Lv 4": LRFF13ItemData(
        code=384,
        str_id="ms900_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Ultima Lv 5": LRFF13ItemData(
        code=385,
        str_id="ms900_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Elementaga Lv 1": LRFF13ItemData(
        code=386,
        str_id="ms910_00_00",
        classification=ItemClassification.filler,
        category="Ability",
        weight=140
    ),
    "Elementaga Lv 2": LRFF13ItemData(
        code=387,
        str_id="ms910_00_10",
        classification=ItemClassification.filler,
        category="Ability",
        weight=98
    ),
    "Elementaga Lv 3": LRFF13ItemData(
        code=388,
        str_id="ms910_00_20",
        classification=ItemClassification.filler,
        category="Ability",
        weight=69
    ),
    "Elementaga Lv 4": LRFF13ItemData(
        code=389,
        str_id="ms910_00_30",
        classification=ItemClassification.filler,
        category="Ability",
        weight=49
    ),
    "Elementaga Lv 5": LRFF13ItemData(
        code=390,
        str_id="ms910_00_40",
        classification=ItemClassification.filler,
        category="Ability",
        weight=34
    ),
    "Fighter's Emblem": LRFF13ItemData(
        code=391,
        str_id="acc_a_0000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fighter's Emblem+": LRFF13ItemData(
        code=392,
        str_id="acc_a_0001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior's Emblem": LRFF13ItemData(
        code=393,
        str_id="acc_a_0002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Magician's Token": LRFF13ItemData(
        code=394,
        str_id="acc_a_0010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Magician's Token+": LRFF13ItemData(
        code=395,
        str_id="acc_a_0011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sorcerer's Token": LRFF13ItemData(
        code=396,
        str_id="acc_a_0012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Samurai's Comb": LRFF13ItemData(
        code=397,
        str_id="acc_a_0020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Samurai's Comb+": LRFF13ItemData(
        code=398,
        str_id="acc_a_0021",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tycoon's Comb": LRFF13ItemData(
        code=399,
        str_id="acc_a_0022",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Wolf's Emblem": LRFF13ItemData(
        code=400,
        str_id="acc_a_0030",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Wolf's Emblem+": LRFF13ItemData(
        code=401,
        str_id="acc_a_0031",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tiger's Emblem": LRFF13ItemData(
        code=402,
        str_id="acc_a_0032",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Imp's Crest": LRFF13ItemData(
        code=403,
        str_id="acc_a_0040",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Imp's Crest+": LRFF13ItemData(
        code=404,
        str_id="acc_a_0041",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Djinn's Crest+": LRFF13ItemData(
        code=405,
        str_id="acc_a_0042",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Soldier's Tie": LRFF13ItemData(
        code=406,
        str_id="acc_a_1000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Soldier's Tie+": LRFF13ItemData(
        code=407,
        str_id="acc_a_1001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "General's Tie": LRFF13ItemData(
        code=408,
        str_id="acc_a_1002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mage's Turban": LRFF13ItemData(
        code=409,
        str_id="acc_a_1010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mage's Turban+": LRFF13ItemData(
        code=410,
        str_id="acc_a_1011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Shaman's Turban": LRFF13ItemData(
        code=411,
        str_id="acc_a_1012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior's Plume": LRFF13ItemData(
        code=412,
        str_id="acc_a_1020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior's Plume+": LRFF13ItemData(
        code=413,
        str_id="acc_a_1021",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Commander's Plume": LRFF13ItemData(
        code=414,
        str_id="acc_a_1022",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Guard's Cravat": LRFF13ItemData(
        code=415,
        str_id="acc_a_1030",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Guard's Cravat+": LRFF13ItemData(
        code=416,
        str_id="acc_a_1031",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Imperial Guard's Cravat": LRFF13ItemData(
        code=417,
        str_id="acc_a_1032",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Spiritual Veil": LRFF13ItemData(
        code=418,
        str_id="acc_a_1040",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Spiritual Veil+": LRFF13ItemData(
        code=419,
        str_id="acc_a_1041",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mystic Veil": LRFF13ItemData(
        code=420,
        str_id="acc_a_1042",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Flamebane Choker": LRFF13ItemData(
        code=421,
        str_id="acc_a_1100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Flamebane Choker+": LRFF13ItemData(
        code=422,
        str_id="acc_a_1101",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Flameshield Choker": LRFF13ItemData(
        code=423,
        str_id="acc_a_1102",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostbane Choker": LRFF13ItemData(
        code=424,
        str_id="acc_a_1110",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostbane Choker+": LRFF13ItemData(
        code=425,
        str_id="acc_a_1111",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostshield Choker": LRFF13ItemData(
        code=426,
        str_id="acc_a_1112",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkbane Choker": LRFF13ItemData(
        code=427,
        str_id="acc_a_1120",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkbane Choker+": LRFF13ItemData(
        code=428,
        str_id="acc_a_1121",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkshield Choker": LRFF13ItemData(
        code=429,
        str_id="acc_a_1122",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormbane Choker": LRFF13ItemData(
        code=430,
        str_id="acc_a_1130",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormbane Choker+": LRFF13ItemData(
        code=431,
        str_id="acc_a_1131",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormshield Choker": LRFF13ItemData(
        code=432,
        str_id="acc_a_1132",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tri-Point Coronet": LRFF13ItemData(
        code=433,
        str_id="acc_a_1140",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tri-Point Coronet+": LRFF13ItemData(
        code=434,
        str_id="acc_a_1141",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tri-Point Crown": LRFF13ItemData(
        code=435,
        str_id="acc_a_1142",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Twist Headband": LRFF13ItemData(
        code=436,
        str_id="acc_a_3000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Twist Headband+": LRFF13ItemData(
        code=437,
        str_id="acc_a_3001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Guts Headband": LRFF13ItemData(
        code=438,
        str_id="acc_a_3002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Corsair Scarf": LRFF13ItemData(
        code=439,
        str_id="acc_a_3010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Corsair Scarf+": LRFF13ItemData(
        code=440,
        str_id="acc_a_3011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Pirate Scarf": LRFF13ItemData(
        code=441,
        str_id="acc_a_3012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Promised Necklace": LRFF13ItemData(
        code=442,
        str_id="acc_a_3020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Promised Necklace+": LRFF13ItemData(
        code=443,
        str_id="acc_a_3021",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Avowed Necklace": LRFF13ItemData(
        code=444,
        str_id="acc_a_3022",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Satin Scrunchie": LRFF13ItemData(
        code=445,
        str_id="acc_a_4100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Satin Scrunchie+": LRFF13ItemData(
        code=446,
        str_id="acc_a_4101",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Ribbon": LRFF13ItemData(
        code=447,
        str_id="acc_a_4102",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Zirconia Brooch": LRFF13ItemData(
        code=448,
        str_id="acc_a_5000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Zirconia Brooch+": LRFF13ItemData(
        code=449,
        str_id="acc_a_5001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mythril Brooch": LRFF13ItemData(
        code=450,
        str_id="acc_a_5002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Corundum Pin": LRFF13ItemData(
        code=451,
        str_id="acc_a_5010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Corundum Pin+": LRFF13ItemData(
        code=452,
        str_id="acc_a_5011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Vajra Pin": LRFF13ItemData(
        code=453,
        str_id="acc_a_5012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Silver Barrette": LRFF13ItemData(
        code=454,
        str_id="acc_a_5100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Silver Barrette+": LRFF13ItemData(
        code=455,
        str_id="acc_a_5101",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Platinum Barrette": LRFF13ItemData(
        code=456,
        str_id="acc_a_5102",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Silk Scarf": LRFF13ItemData(
        code=457,
        str_id="acc_a_5200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Silk Scarf+": LRFF13ItemData(
        code=458,
        str_id="acc_a_5201",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Dragoon Scarf": LRFF13ItemData(
        code=459,
        str_id="acc_a_5202",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Demon Earrings": LRFF13ItemData(
        code=460,
        str_id="acc_a_8000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Demon Earrings+": LRFF13ItemData(
        code=461,
        str_id="acc_a_8001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Devil Earrings": LRFF13ItemData(
        code=462,
        str_id="acc_a_8002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparrow Comb": LRFF13ItemData(
        code=463,
        str_id="acc_a_8010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparrow Comb+": LRFF13ItemData(
        code=464,
        str_id="acc_a_8011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Swallowtail": LRFF13ItemData(
        code=465,
        str_id="acc_a_8012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Angel's Headband": LRFF13ItemData(
        code=466,
        str_id="acc_a_8120",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Angel's Headband+": LRFF13ItemData(
        code=467,
        str_id="acc_a_8121",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Angel's Halo": LRFF13ItemData(
        code=468,
        str_id="acc_a_8122",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Cursed Band": LRFF13ItemData(
        code=469,
        str_id="acc_a_8130",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Cursed Band+": LRFF13ItemData(
        code=470,
        str_id="acc_a_8131",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Ill Will Band": LRFF13ItemData(
        code=471,
        str_id="acc_a_8132",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fencer's Earrings": LRFF13ItemData(
        code=472,
        str_id="acc_a_8200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fencer's Earrings+": LRFF13ItemData(
        code=473,
        str_id="acc_a_8201",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Duelist's Earrings": LRFF13ItemData(
        code=474,
        str_id="acc_a_8202",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Witch's Rosary": LRFF13ItemData(
        code=475,
        str_id="acc_a_8210",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Witch's Rosary+": LRFF13ItemData(
        code=476,
        str_id="acc_a_8211",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Devil's Rosary": LRFF13ItemData(
        code=477,
        str_id="acc_a_8212",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Soul of Thamasa": LRFF13ItemData(
        code=478,
        str_id="acc_a_8300",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Soul of Thamasa+": LRFF13ItemData(
        code=479,
        str_id="acc_a_8301",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Soul of Minwu": LRFF13ItemData(
        code=480,
        str_id="acc_a_8302",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Locket Pendant": LRFF13ItemData(
        code=481,
        str_id="acc_a_8310",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Locket Pendant+": LRFF13ItemData(
        code=482,
        str_id="acc_a_8311",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Locket Necklace": LRFF13ItemData(
        code=483,
        str_id="acc_a_8312",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Swift Ornament": LRFF13ItemData(
        code=484,
        str_id="acc_a_8400",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Swift Ornament+": LRFF13ItemData(
        code=485,
        str_id="acc_a_8401",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Falcon Ornament": LRFF13ItemData(
        code=486,
        str_id="acc_a_8402",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sight's Circlet": LRFF13ItemData(
        code=487,
        str_id="acc_a_8410",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sight's Circlet+": LRFF13ItemData(
        code=488,
        str_id="acc_a_8411",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Determined Tiara": LRFF13ItemData(
        code=489,
        str_id="acc_a_8412",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Early-blooming Corsage": LRFF13ItemData(
        code=490,
        str_id="acc_a_9000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Early-blooming Corsage+": LRFF13ItemData(
        code=491,
        str_id="acc_a_9001",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Charging Chaplet": LRFF13ItemData(
        code=492,
        str_id="acc_a_9002",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fireseal Jewel": LRFF13ItemData(
        code=493,
        str_id="acc_a_9010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fireseal Jewel+": LRFF13ItemData(
        code=494,
        str_id="acc_a_9011",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Firesup Malcreous": LRFF13ItemData(
        code=495,
        str_id="acc_a_9012",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostseal Jewel": LRFF13ItemData(
        code=496,
        str_id="acc_a_9020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostseal Jewel+": LRFF13ItemData(
        code=497,
        str_id="acc_a_9021",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostsup Malcreous": LRFF13ItemData(
        code=498,
        str_id="acc_a_9022",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkseal Jewel": LRFF13ItemData(
        code=499,
        str_id="acc_a_9030",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkseal Jewel+": LRFF13ItemData(
        code=500,
        str_id="acc_a_9031",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparksup Malcreous": LRFF13ItemData(
        code=501,
        str_id="acc_a_9032",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormseal Jewel": LRFF13ItemData(
        code=502,
        str_id="acc_a_9040",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormseal Jewel+": LRFF13ItemData(
        code=503,
        str_id="acc_a_9041",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormsup Malcreous": LRFF13ItemData(
        code=504,
        str_id="acc_a_9042",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Ghostly Hood": LRFF13ItemData(
        code=505,
        str_id="acc_a_9050",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Ghostly Hood+": LRFF13ItemData(
        code=506,
        str_id="acc_a_9051",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Ghostly Crown": LRFF13ItemData(
        code=507,
        str_id="acc_a_9052",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Preta Hood": LRFF13ItemData(
        code=508,
        str_id="acc_a_9060",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Preta Hood+": LRFF13ItemData(
        code=509,
        str_id="acc_a_9061",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Preta Crown": LRFF13ItemData(
        code=510,
        str_id="acc_a_9062",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Wild Crest": LRFF13ItemData(
        code=511,
        str_id="acc_a_9070",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Wild Crest+": LRFF13ItemData(
        code=512,
        str_id="acc_a_9071",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Beast Mane": LRFF13ItemData(
        code=513,
        str_id="acc_a_9072",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Devil Crest": LRFF13ItemData(
        code=514,
        str_id="acc_a_9080",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Devil Crest+": LRFF13ItemData(
        code=515,
        str_id="acc_a_9081",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Demon Mane": LRFF13ItemData(
        code=516,
        str_id="acc_a_9082",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Irondragon Scale": LRFF13ItemData(
        code=517,
        str_id="acc_a_9090",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Irondragon Scale+": LRFF13ItemData(
        code=518,
        str_id="acc_a_9091",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Armor Plate": LRFF13ItemData(
        code=519,
        str_id="acc_a_9092",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Dreamdragon's Scale": LRFF13ItemData(
        code=520,
        str_id="acc_a_9100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Dreamdragon's Scale+": LRFF13ItemData(
        code=521,
        str_id="acc_a_9101",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mythical Scale": LRFF13ItemData(
        code=522,
        str_id="acc_a_9102",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior Hunter's Mask": LRFF13ItemData(
        code=523,
        str_id="acc_a_9110",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior Hunter's Mask+": LRFF13ItemData(
        code=524,
        str_id="acc_a_9111",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Face of the Warrior's Nemesis": LRFF13ItemData(
        code=525,
        str_id="acc_a_9112",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mage Hunter's Mask": LRFF13ItemData(
        code=526,
        str_id="acc_a_9120",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mage Hunter's Mask+": LRFF13ItemData(
        code=527,
        str_id="acc_a_9121",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Face of the Mage's Nemesis": LRFF13ItemData(
        code=528,
        str_id="acc_a_9122",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sapping Hood": LRFF13ItemData(
        code=529,
        str_id="acc_a_9130",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sapping Hood+": LRFF13ItemData(
        code=530,
        str_id="acc_a_9131",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Destructive Headdress": LRFF13ItemData(
        code=531,
        str_id="acc_a_9132",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Crippling Hood": LRFF13ItemData(
        code=532,
        str_id="acc_a_9140",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Crippling Hood+": LRFF13ItemData(
        code=533,
        str_id="acc_a_9141",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Deranged Headdress": LRFF13ItemData(
        code=534,
        str_id="acc_a_9142",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Bandit Scarf": LRFF13ItemData(
        code=535,
        str_id="acc_a_9150",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Bandit Scarf+": LRFF13ItemData(
        code=536,
        str_id="acc_a_9151",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sky Pirate's Scarf": LRFF13ItemData(
        code=537,
        str_id="acc_a_9152",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Coldflame Droplet": LRFF13ItemData(
        code=538,
        str_id="acc_a_9160",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Coldflame Droplet+": LRFF13ItemData(
        code=539,
        str_id="acc_a_9161",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Icy Inferno": LRFF13ItemData(
        code=540,
        str_id="acc_a_9162",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thunderstorm Droplet": LRFF13ItemData(
        code=541,
        str_id="acc_a_9170",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thunderstorm Droplet+": LRFF13ItemData(
        code=542,
        str_id="acc_a_9171",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Eye of the Storm": LRFF13ItemData(
        code=543,
        str_id="acc_a_9172",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Skeleton's Earrings": LRFF13ItemData(
        code=544,
        str_id="acc_a_9180",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Skeleton's Earrings+": LRFF13ItemData(
        code=545,
        str_id="acc_a_9181",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Skull": LRFF13ItemData(
        code=546,
        str_id="acc_a_9182",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior's Headband": LRFF13ItemData(
        code=547,
        str_id="acc_a_9190",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warrior's Headband+": LRFF13ItemData(
        code=548,
        str_id="acc_a_9191",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Rakshasa Ring": LRFF13ItemData(
        code=549,
        str_id="acc_a_9192",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Falcon Charm": LRFF13ItemData(
        code=550,
        str_id="acc_a_9200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Strahl Charm": LRFF13ItemData(
        code=551,
        str_id="acc_a_9201",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Highwind Charm": LRFF13ItemData(
        code=552,
        str_id="acc_a_9202",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Diamond Matinee Necklace": LRFF13ItemData(
        code=553,
        str_id="acc_a_9210",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Orichalc Matinee Necklace": LRFF13ItemData(
        code=554,
        str_id="acc_a_9211",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Crystal Matinee Necklace": LRFF13ItemData(
        code=555,
        str_id="acc_a_9212",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Toasty Shawl": LRFF13ItemData(
        code=556,
        str_id="acc_a_9220",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Toasty Shawl+": LRFF13ItemData(
        code=557,
        str_id="acc_a_9221",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Fuzzy Wool Shawl": LRFF13ItemData(
        code=558,
        str_id="acc_a_9222",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Guard Glove": LRFF13ItemData(
        code=559,
        str_id="acc_b_1000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Runic Ring": LRFF13ItemData(
        code=560,
        str_id="acc_b_1010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Giant's Vambrace": LRFF13ItemData(
        code=561,
        str_id="acc_b_4110",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Mage's Gloves": LRFF13ItemData(
        code=562,
        str_id="acc_b_4120",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Metal Armband": LRFF13ItemData(
        code=563,
        str_id="acc_b_4130",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Serenity Sachet": LRFF13ItemData(
        code=564,
        str_id="acc_b_4140",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Pretty Orb": LRFF13ItemData(
        code=565,
        str_id="acc_b_4150",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Star Bracelet": LRFF13ItemData(
        code=566,
        str_id="acc_b_4160",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Nacre Cameo": LRFF13ItemData(
        code=567,
        str_id="acc_b_4170",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Warding Talisman": LRFF13ItemData(
        code=568,
        str_id="acc_b_4180",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Pain Dampener": LRFF13ItemData(
        code=569,
        str_id="acc_b_4190",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "White Strap": LRFF13ItemData(
        code=570,
        str_id="acc_b_4200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Rainbow Gem": LRFF13ItemData(
        code=571,
        str_id="acc_b_4210",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Firewyrm Bracelet": LRFF13ItemData(
        code=572,
        str_id="acc_b_6030",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Watergod Bracelet": LRFF13ItemData(
        code=573,
        str_id="acc_b_6040",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thunderbird Bracelet": LRFF13ItemData(
        code=574,
        str_id="acc_b_6050",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Windwalker Bracelet": LRFF13ItemData(
        code=575,
        str_id="acc_b_6060",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Protection": LRFF13ItemData(
        code=576,
        str_id="acc_b_6100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Warding": LRFF13ItemData(
        code=577,
        str_id="acc_b_6110",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Aggression": LRFF13ItemData(
        code=578,
        str_id="acc_b_6120",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Courage": LRFF13ItemData(
        code=579,
        str_id="acc_b_6200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Will": LRFF13ItemData(
        code=580,
        str_id="acc_b_6210",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Thorn of Speed": LRFF13ItemData(
        code=581,
        str_id="acc_b_6220",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Healer's Lore": LRFF13ItemData(
        code=582,
        str_id="acc_b_7010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Collector Catalog": LRFF13ItemData(
        code=583,
        str_id="acc_b_7020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Demon Claw": LRFF13ItemData(
        code=584,
        str_id="acc_b_7100",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Beggar's Beads": LRFF13ItemData(
        code=585,
        str_id="acc_b_7110",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Dawn Gauntlets": LRFF13ItemData(
        code=586,
        str_id="acc_b_7200",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Enlister's Gloves": LRFF13ItemData(
        code=587,
        str_id="acc_b_9000",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sniper's Gloves": LRFF13ItemData(
        code=588,
        str_id="acc_b_9010",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Flameward Bangle": LRFF13ItemData(
        code=589,
        str_id="acc_b_9020",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Frostward Bangle": LRFF13ItemData(
        code=590,
        str_id="acc_b_9030",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Sparkward Bangle": LRFF13ItemData(
        code=591,
        str_id="acc_b_9040",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Stormward Bangle": LRFF13ItemData(
        code=592,
        str_id="acc_b_9050",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Kiai Wrist": LRFF13ItemData(
        code=593,
        str_id="acc_b_9060",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Forsaken Tie": LRFF13ItemData(
        code=594,
        str_id="acc_b_9070",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Tenacious Ring": LRFF13ItemData(
        code=595,
        str_id="acc_b_9080",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Lucky Dice": LRFF13ItemData(
        code=596,
        str_id="acc_b_9090",
        classification=ItemClassification.filler,
        category="Accessory",
        weight=50
    ),
    "Equilibrium": LRFF13ItemData(
        code=597,
        str_id="cos_ba00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Vengeance": LRFF13ItemData(
        code=598,
        str_id="cos_ba01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Vigilance": LRFF13ItemData(
        code=599,
        str_id="cos_ba02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Innocence": LRFF13ItemData(
        code=600,
        str_id="cos_ba03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Ultimatus": LRFF13ItemData(
        code=601,
        str_id="cos_ba04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Divergence": LRFF13ItemData(
        code=602,
        str_id="cos_ba05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Providence": LRFF13ItemData(
        code=603,
        str_id="cos_ba06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Equilibrium+": LRFF13ItemData(
        code=604,
        str_id="cos_ba08",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dark Muse": LRFF13ItemData(
        code=605,
        str_id="cos_ca00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Helter Skelter": LRFF13ItemData(
        code=606,
        str_id="cos_ca01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Electronica": LRFF13ItemData(
        code=607,
        str_id="cos_ca02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Witching Hour": LRFF13ItemData(
        code=608,
        str_id="cos_ca03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Candy Raver": LRFF13ItemData(
        code=609,
        str_id="cos_ca04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Woodland Walker": LRFF13ItemData(
        code=610,
        str_id="cos_ca05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Sand Fox": LRFF13ItemData(
        code=611,
        str_id="cos_ca06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dark Muse+": LRFF13ItemData(
        code=612,
        str_id="cos_ca08",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "L'ange Noir": LRFF13ItemData(
        code=613,
        str_id="cos_da00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Cyber Jumpsuit": LRFF13ItemData(
        code=614,
        str_id="cos_da01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Passion Rouge": LRFF13ItemData(
        code=615,
        str_id="cos_da02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "L'automne": LRFF13ItemData(
        code=616,
        str_id="cos_da03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Martial Monk": LRFF13ItemData(
        code=617,
        str_id="cos_da04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Duelist": LRFF13ItemData(
        code=618,
        str_id="cos_da05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Black Mage": LRFF13ItemData(
        code=619,
        str_id="cos_da06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dust and Shadow": LRFF13ItemData(
        code=620,
        str_id="cos_ea00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "White Mage": LRFF13ItemData(
        code=621,
        str_id="cos_ea01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Blue Mage": LRFF13ItemData(
        code=622,
        str_id="cos_ea02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Sun and Bloom": LRFF13ItemData(
        code=623,
        str_id="cos_ea03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Stone and Sand": LRFF13ItemData(
        code=624,
        str_id="cos_ea04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Hunter of the Wild": LRFF13ItemData(
        code=625,
        str_id="cos_ea05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Soldier of Peace": LRFF13ItemData(
        code=626,
        str_id="cos_ea06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Midnight Mauve": LRFF13ItemData(
        code=627,
        str_id="cos_fa00",
        classification=ItemClassification.progression,
        category="Garb",
        traits=["Key"]
    ),
    "Black Rose": LRFF13ItemData(
        code=628,
        str_id="cos_fa01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Crimson Bloom": LRFF13ItemData(
        code=629,
        str_id="cos_fa02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Icy White": LRFF13ItemData(
        code=630,
        str_id="cos_fa03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dark Orchid": LRFF13ItemData(
        code=631,
        str_id="cos_fa04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Champagne Gold": LRFF13ItemData(
        code=632,
        str_id="cos_fa05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Violet Twilight": LRFF13ItemData(
        code=633,
        str_id="cos_fa06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Splendid Admiral": LRFF13ItemData(
        code=634,
        str_id="cos_ga00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Quiet Guardian": LRFF13ItemData(
        code=635,
        str_id="cos_ga01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Loyal Servant": LRFF13ItemData(
        code=636,
        str_id="cos_ga02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Bold Vanguard": LRFF13ItemData(
        code=637,
        str_id="cos_ga03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Velvet Bouncer": LRFF13ItemData(
        code=638,
        str_id="cos_ga04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Cold Rebellion": LRFF13ItemData(
        code=639,
        str_id="cos_ga05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Red Mage": LRFF13ItemData(
        code=640,
        str_id="cos_ga06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Nocturne": LRFF13ItemData(
        code=641,
        str_id="cos_ha00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Paladin": LRFF13ItemData(
        code=642,
        str_id="cos_ha01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Deja Vu": LRFF13ItemData(
        code=643,
        str_id="cos_ha02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Danse Macabre": LRFF13ItemData(
        code=644,
        str_id="cos_ha03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "School's Out": LRFF13ItemData(
        code=645,
        str_id="cos_ha04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Lilitu": LRFF13ItemData(
        code=646,
        str_id="cos_ha05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "La Fouldre": LRFF13ItemData(
        code=647,
        str_id="cos_ha06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Heartstealer": LRFF13ItemData(
        code=648,
        str_id="cos_ia00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Primavera": LRFF13ItemData(
        code=649,
        str_id="cos_ia01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Urban Outlaw": LRFF13ItemData(
        code=650,
        str_id="cos_ia02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dangerous Blossom": LRFF13ItemData(
        code=651,
        str_id="cos_ia03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Hidden Justice": LRFF13ItemData(
        code=652,
        str_id="cos_ia04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Ignition": LRFF13ItemData(
        code=653,
        str_id="cos_ia05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Intruder": LRFF13ItemData(
        code=654,
        str_id="cos_ia06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Mist Wizard": LRFF13ItemData(
        code=655,
        str_id="cos_ja00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Watery Chorus": LRFF13ItemData(
        code=656,
        str_id="cos_ja01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Purple Lightning": LRFF13ItemData(
        code=657,
        str_id="cos_ja02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Carnaval Crusher": LRFF13ItemData(
        code=658,
        str_id="cos_ja03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Rhapsody in Rose": LRFF13ItemData(
        code=659,
        str_id="cos_ja04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Nightmare": LRFF13ItemData(
        code=660,
        str_id="cos_ja05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Amazon Warrior": LRFF13ItemData(
        code=661,
        str_id="cos_ja06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Mist Wizard+": LRFF13ItemData(
        code=662,
        str_id="cos_ja08",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dragoon": LRFF13ItemData(
        code=663,
        str_id="cos_ka00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dark Knight": LRFF13ItemData(
        code=664,
        str_id="cos_ka01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Dragon's Blood": LRFF13ItemData(
        code=665,
        str_id="cos_ka02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Sacred Knight": LRFF13ItemData(
        code=666,
        str_id="cos_ka03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Shadow Trooper": LRFF13ItemData(
        code=667,
        str_id="cos_ka04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Astral Lord": LRFF13ItemData(
        code=668,
        str_id="cos_ka05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Pallas Athena": LRFF13ItemData(
        code=669,
        str_id="cos_ka06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Siegfried": LRFF13ItemData(
        code=670,
        str_id="cos_ka08",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Miqo'te Dress": LRFF13ItemData(
        code=671,
        str_id="cos_la00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Guardian Corps": LRFF13ItemData(
        code=672,
        str_id="cos_ma00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Knight of Etro": LRFF13ItemData(
        code=673,
        str_id="cos_na00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50
    ),
    "Spira's Summoner": LRFF13ItemData(
        code=674,
        str_id="cos_oa00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Sphere Hunter": LRFF13ItemData(
        code=675,
        str_id="cos_pa00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "SOLDIER 1st Class": LRFF13ItemData(
        code=676,
        str_id="cos_ra00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Shogun": LRFF13ItemData(
        code=677,
        str_id="cos_zb00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Shining Prince": LRFF13ItemData(
        code=678,
        str_id="cos_zb01",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Dark Samurai": LRFF13ItemData(
        code=679,
        str_id="cos_zb02",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Sohei Savior": LRFF13ItemData(
        code=680,
        str_id="cos_zb03",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Utsusemi": LRFF13ItemData(
        code=681,
        str_id="cos_zb04",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Art of War": LRFF13ItemData(
        code=682,
        str_id="cos_zb05",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Flower of Battle": LRFF13ItemData(
        code=683,
        str_id="cos_zb06",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Tomb Raider": LRFF13ItemData(
        code=684,
        str_id="cos_zc00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Cosmocrator": LRFF13ItemData(
        code=685,
        str_id="cos_zd00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Moogle Queen": LRFF13ItemData(
        code=686,
        str_id="cos_ze00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Celestial Body": LRFF13ItemData(
        code=687,
        str_id="cos_zf00",
        classification=ItemClassification.filler,
        category="Garb",
        weight=50,
        traits=["DLC"]
    ),
    "Lucky Clover": LRFF13ItemData(
        code=688,
        str_id="e003",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tropical Tree": LRFF13ItemData(
        code=689,
        str_id="e004",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Single Horn": LRFF13ItemData(
        code=690,
        str_id="e010",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Antler": LRFF13ItemData(
        code=691,
        str_id="e011",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Odin's Horn": LRFF13ItemData(
        code=692,
        str_id="e012",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Halo": LRFF13ItemData(
        code=693,
        str_id="e015",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Wind-Up Halo": LRFF13ItemData(
        code=694,
        str_id="e016",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Light Bulb": LRFF13ItemData(
        code=695,
        str_id="e019",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cie'th Wings": LRFF13ItemData(
        code=696,
        str_id="e023",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Moogle Wings": LRFF13ItemData(
        code=697,
        str_id="e024",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Coronet": LRFF13ItemData(
        code=698,
        str_id="e026",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown": LRFF13ItemData(
        code=699,
        str_id="e027",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Railworker's Cap": LRFF13ItemData(
        code=700,
        str_id="e030",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Railworker's Beret": LRFF13ItemData(
        code=701,
        str_id="e031",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Black Mage's Hood": LRFF13ItemData(
        code=702,
        str_id="e032",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Scholar's Mortarboard": LRFF13ItemData(
        code=703,
        str_id="e033",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Chef's Hat": LRFF13ItemData(
        code=704,
        str_id="e034",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cute Bunny Ears": LRFF13ItemData(
        code=705,
        str_id="e037",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Onion Knight's Helm": LRFF13ItemData(
        code=706,
        str_id="e038",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gold Anchor": LRFF13ItemData(
        code=707,
        str_id="e039",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tonberry's Lantern": LRFF13ItemData(
        code=708,
        str_id="e041",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Summoner's Mask": LRFF13ItemData(
        code=709,
        str_id="e042",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Ripe Apple": LRFF13ItemData(
        code=710,
        str_id="e043",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pumpkin Head": LRFF13ItemData(
        code=711,
        str_id="e044",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tinkling Bell": LRFF13ItemData(
        code=712,
        str_id="e053",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Flower Pattern": LRFF13ItemData(
        code=713,
        str_id="e074",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Frying Pan": LRFF13ItemData(
        code=714,
        str_id="e078",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dull Grudge Knife": LRFF13ItemData(
        code=715,
        str_id="e079",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Staff of Judgment": LRFF13ItemData(
        code=716,
        str_id="e080",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Mog's Staff": LRFF13ItemData(
        code=717,
        str_id="e081",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Fragment Crystal": LRFF13ItemData(
        code=718,
        str_id="e083",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cactuar Figurine": LRFF13ItemData(
        code=719,
        str_id="e090",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cute Cactuar Figurine": LRFF13ItemData(
        code=720,
        str_id="e091",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Carbuncle Figurine": LRFF13ItemData(
        code=721,
        str_id="e092",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Mog Figurine": LRFF13ItemData(
        code=722,
        str_id="e093",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Miniflan Figurine": LRFF13ItemData(
        code=723,
        str_id="e094",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tonberry Figurine": LRFF13ItemData(
        code=724,
        str_id="e096",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Fuzzy Sheep Figurine": LRFF13ItemData(
        code=725,
        str_id="e097",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Afro": LRFF13ItemData(
        code=726,
        str_id="e098",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Serah Mask": LRFF13ItemData(
        code=727,
        str_id="e108",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Lightning Mask": LRFF13ItemData(
        code=728,
        str_id="e109",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Mog Mask": LRFF13ItemData(
        code=729,
        str_id="e110",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Retro Serah Mask": LRFF13ItemData(
        code=730,
        str_id="e111",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Retro Lightning Mask": LRFF13ItemData(
        code=731,
        str_id="e112",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Retro Mog Mask": LRFF13ItemData(
        code=732,
        str_id="e113",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Blue Flower": LRFF13ItemData(
        code=733,
        str_id="e200",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink Flower": LRFF13ItemData(
        code=734,
        str_id="e201",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "White Flower": LRFF13ItemData(
        code=735,
        str_id="e202",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Purple Flower": LRFF13ItemData(
        code=736,
        str_id="e203",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Frost Tree": LRFF13ItemData(
        code=737,
        str_id="e204",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Suspicious Mushroom": LRFF13ItemData(
        code=738,
        str_id="e205",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Toxic Mushroom": LRFF13ItemData(
        code=739,
        str_id="e206",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Noonblue Butterfly": LRFF13ItemData(
        code=740,
        str_id="e207",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sunny Butterfly": LRFF13ItemData(
        code=741,
        str_id="e208",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gold Windup Key": LRFF13ItemData(
        code=742,
        str_id="e209",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Aqua Ribbon": LRFF13ItemData(
        code=743,
        str_id="e210",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink Ribbon": LRFF13ItemData(
        code=744,
        str_id="e211",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Brass Gear": LRFF13ItemData(
        code=745,
        str_id="e212",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Chocobo Figurine": LRFF13ItemData(
        code=746,
        str_id="e213",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Chocobo Figurine": LRFF13ItemData(
        code=747,
        str_id="e214",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Purple Chocobo Figurine": LRFF13ItemData(
        code=748,
        str_id="e215",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "White Chocobo Figurine": LRFF13ItemData(
        code=749,
        str_id="e216",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Black Chocobo Figurine": LRFF13ItemData(
        code=750,
        str_id="e217",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Silver Chocobo Figurine": LRFF13ItemData(
        code=751,
        str_id="e218",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gold Chocobo Figurine": LRFF13ItemData(
        code=752,
        str_id="e219",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Youthful Parasol": LRFF13ItemData(
        code=753,
        str_id="e220",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sentimental Parasol": LRFF13ItemData(
        code=754,
        str_id="e221",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Propeller": LRFF13ItemData(
        code=755,
        str_id="e222",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Propeller": LRFF13ItemData(
        code=756,
        str_id="e223",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Moogle Bobble": LRFF13ItemData(
        code=757,
        str_id="e224",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Water Spirit Wings": LRFF13ItemData(
        code=758,
        str_id="e226",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Snowy Spirit Wings": LRFF13ItemData(
        code=759,
        str_id="e227",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Orange Newsboy Cap": LRFF13ItemData(
        code=760,
        str_id="e228",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink Newsboy Cap": LRFF13ItemData(
        code=761,
        str_id="e229",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Silk Hat": LRFF13ItemData(
        code=762,
        str_id="e230",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sky Blue Silk Hat": LRFF13ItemData(
        code=763,
        str_id="e231",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Mage's Chapeau": LRFF13ItemData(
        code=764,
        str_id="e232",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Love-struck Party Hat": LRFF13ItemData(
        code=765,
        str_id="e233",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Bubbly Party Hat": LRFF13ItemData(
        code=766,
        str_id="e234",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Prophetic Headdress": LRFF13ItemData(
        code=767,
        str_id="e235",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Vanguard Headdress": LRFF13ItemData(
        code=768,
        str_id="e236",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Strawberry Ice Cream": LRFF13ItemData(
        code=769,
        str_id="e237",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Rum Raisin Ice Cream": LRFF13ItemData(
        code=770,
        str_id="e238",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Yellow Bow Tie": LRFF13ItemData(
        code=771,
        str_id="e239",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Orange Bow Tie": LRFF13ItemData(
        code=772,
        str_id="e240",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Yellow-rimmed Glasses": LRFF13ItemData(
        code=773,
        str_id="e241",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink-rimmed Glasses": LRFF13ItemData(
        code=774,
        str_id="e242",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Twilight Shades": LRFF13ItemData(
        code=775,
        str_id="e243",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Urban Shades": LRFF13ItemData(
        code=776,
        str_id="e244",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Masquerade Mask": LRFF13ItemData(
        code=777,
        str_id="e245",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Carnival Mask": LRFF13ItemData(
        code=778,
        str_id="e246",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Regent's Mustache": LRFF13ItemData(
        code=779,
        str_id="e247",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dandy's Mustache": LRFF13ItemData(
        code=780,
        str_id="e248",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gentleman's Beard": LRFF13ItemData(
        code=781,
        str_id="e249",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Craftsman's Beard": LRFF13ItemData(
        code=782,
        str_id="e250",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Feather Pin": LRFF13ItemData(
        code=783,
        str_id="e259",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dusk Feather Pin": LRFF13ItemData(
        code=784,
        str_id="e260",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Leather Rucksack": LRFF13ItemData(
        code=785,
        str_id="e261",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink Rucksack": LRFF13ItemData(
        code=786,
        str_id="e262",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Warning Beacon": LRFF13ItemData(
        code=787,
        str_id="e263",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Emergency Beacon": LRFF13ItemData(
        code=788,
        str_id="e264",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Chocobo Chick": LRFF13ItemData(
        code=789,
        str_id="e278",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Blue Chocobo Chick": LRFF13ItemData(
        code=790,
        str_id="e279",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Purple Chocobo Chick": LRFF13ItemData(
        code=791,
        str_id="e280",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "White Chocobo Chick": LRFF13ItemData(
        code=792,
        str_id="e281",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Black Chocobo Chick": LRFF13ItemData(
        code=793,
        str_id="e282",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Silver Chocobo Chick": LRFF13ItemData(
        code=794,
        str_id="e283",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Gold Chocobo Chick": LRFF13ItemData(
        code=795,
        str_id="e284",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Red Chick": LRFF13ItemData(
        code=796,
        str_id="e285",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Blue Chick": LRFF13ItemData(
        code=797,
        str_id="e286",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Purple Chick": LRFF13ItemData(
        code=798,
        str_id="e287",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & White Chick": LRFF13ItemData(
        code=799,
        str_id="e288",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Black Chick": LRFF13ItemData(
        code=800,
        str_id="e289",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Silver Chick": LRFF13ItemData(
        code=801,
        str_id="e290",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Afro & Gold Chick": LRFF13ItemData(
        code=802,
        str_id="e291",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Silver Padlock": LRFF13ItemData(
        code=803,
        str_id="e292",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Long Gui's Shell": LRFF13ItemData(
        code=804,
        str_id="e293",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "White Guitar": LRFF13ItemData(
        code=805,
        str_id="e294",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Guitar": LRFF13ItemData(
        code=806,
        str_id="e295",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Replica PSICOM Epaulet": LRFF13ItemData(
        code=807,
        str_id="e297",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Celebrity's Charm": LRFF13ItemData(
        code=808,
        str_id="e298",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Golden Flower": LRFF13ItemData(
        code=809,
        str_id="e301",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crimson Flower": LRFF13ItemData(
        code=810,
        str_id="e302",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Festive Tree": LRFF13ItemData(
        code=811,
        str_id="e303",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Delicious Mushroom": LRFF13ItemData(
        code=812,
        str_id="e304",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Twilight Butterfly": LRFF13ItemData(
        code=813,
        str_id="e305",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Silver Windup Key": LRFF13ItemData(
        code=814,
        str_id="e306",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Yellow Ribbon": LRFF13ItemData(
        code=815,
        str_id="e307",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Nickel Gear": LRFF13ItemData(
        code=816,
        str_id="e308",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Chocobo Figurine": LRFF13ItemData(
        code=817,
        str_id="e309",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Summery Parasol": LRFF13ItemData(
        code=818,
        str_id="e310",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Yellow Propeller": LRFF13ItemData(
        code=819,
        str_id="e311",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pink Moogle Bobble": LRFF13ItemData(
        code=820,
        str_id="e312",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Nymph Wings": LRFF13ItemData(
        code=821,
        str_id="e313",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Blue Newsboy Cap": LRFF13ItemData(
        code=822,
        str_id="e314",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Formal Silk Hat": LRFF13ItemData(
        code=823,
        str_id="e315",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Mage's Chapeau": LRFF13ItemData(
        code=824,
        str_id="e316",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Thrilling Party Hat": LRFF13ItemData(
        code=825,
        str_id="e317",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key", "Always"]
    ),
    "Ceremonial Headdress": LRFF13ItemData(
        code=826,
        str_id="e318",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Mint Chip Ice Cream": LRFF13ItemData(
        code=827,
        str_id="e319",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Red Bow Tie": LRFF13ItemData(
        code=828,
        str_id="e320",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Black-rimmed Glasses": LRFF13ItemData(
        code=829,
        str_id="e321",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dark Knight's Shades": LRFF13ItemData(
        code=830,
        str_id="e322",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Queen's Mask": LRFF13ItemData(
        code=831,
        str_id="e323",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Bushy Mustache": LRFF13ItemData(
        code=832,
        str_id="e324",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Seadog's Beard": LRFF13ItemData(
        code=833,
        str_id="e325",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lebreau's Rainbow Tattoo": LRFF13ItemData(
        code=834,
        str_id="e326",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gadot's Red Emblem": LRFF13ItemData(
        code=835,
        str_id="e327",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tribal Tattoo": LRFF13ItemData(
        code=836,
        str_id="e328",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "NORA Logo": LRFF13ItemData(
        code=837,
        str_id="e329",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Chocobo Feather Pin": LRFF13ItemData(
        code=838,
        str_id="e330",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dragon Hide Backpack": LRFF13ItemData(
        code=839,
        str_id="e331",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Caution Beacon": LRFF13ItemData(
        code=840,
        str_id="e332",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Guardian Corps Badge": LRFF13ItemData(
        code=841,
        str_id="e333",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Replica Pilot's Badge": LRFF13ItemData(
        code=842,
        str_id="e334",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Replica PSICOM Emblem": LRFF13ItemData(
        code=843,
        str_id="e335",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gold Medal": LRFF13ItemData(
        code=844,
        str_id="e336",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Chocobo Chick": LRFF13ItemData(
        code=845,
        str_id="e338",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Afro & Yellow Chick": LRFF13ItemData(
        code=846,
        str_id="e339",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Gold Padlock": LRFF13ItemData(
        code=847,
        str_id="e340",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Adamantoise Shell": LRFF13ItemData(
        code=848,
        str_id="e341",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Electric Guitar": LRFF13ItemData(
        code=849,
        str_id="e342",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "PSICOM Officer Epaulets": LRFF13ItemData(
        code=850,
        str_id="e344",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lady's Brooch": LRFF13ItemData(
        code=851,
        str_id="e345",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lightning's Shades": LRFF13ItemData(
        code=852,
        str_id="e500",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Reflective Shades": LRFF13ItemData(
        code=853,
        str_id="e501",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Elegant Shades": LRFF13ItemData(
        code=854,
        str_id="e502",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Balmy Shades": LRFF13ItemData(
        code=855,
        str_id="e503",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dancefloor Shades": LRFF13ItemData(
        code=856,
        str_id="e504",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Ocean Shades": LRFF13ItemData(
        code=857,
        str_id="e505",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dreamy Shades": LRFF13ItemData(
        code=858,
        str_id="e506",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "City Shades": LRFF13ItemData(
        code=859,
        str_id="e507",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Wild Shades": LRFF13ItemData(
        code=860,
        str_id="e508",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Whimsy Shades": LRFF13ItemData(
        code=861,
        str_id="e509",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Killer Shades": LRFF13ItemData(
        code=862,
        str_id="e510",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Playboy Shades": LRFF13ItemData(
        code=863,
        str_id="e511",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Exotic Shades": LRFF13ItemData(
        code=864,
        str_id="e512",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Scholar's Glasses": LRFF13ItemData(
        code=865,
        str_id="e513",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Business Eyewear": LRFF13ItemData(
        code=866,
        str_id="e514",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Steamy Glasses": LRFF13ItemData(
        code=867,
        str_id="e515",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Girlish Glasses": LRFF13ItemData(
        code=868,
        str_id="e516",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cool Glasses": LRFF13ItemData(
        code=869,
        str_id="e517",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Green Glasses": LRFF13ItemData(
        code=870,
        str_id="e518",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Retro Scopes": LRFF13ItemData(
        code=871,
        str_id="e519",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Heart Glasses": LRFF13ItemData(
        code=872,
        str_id="e520",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Smiley Glasses": LRFF13ItemData(
        code=873,
        str_id="e521",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Frosty Glasses": LRFF13ItemData(
        code=874,
        str_id="e522",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Angelic Glasses": LRFF13ItemData(
        code=875,
        str_id="e523",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cyber Scanners": LRFF13ItemData(
        code=876,
        str_id="e524",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Monoculus Mask": LRFF13ItemData(
        code=877,
        str_id="e525",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Raven Mask": LRFF13ItemData(
        code=878,
        str_id="e526",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Golden Mask": LRFF13ItemData(
        code=879,
        str_id="e527",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Moonlight Mask": LRFF13ItemData(
        code=880,
        str_id="e528",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crimson Mask": LRFF13ItemData(
        code=881,
        str_id="e529",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pioneer's Eyepatch": LRFF13ItemData(
        code=882,
        str_id="e530",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Zebra-print Eyepatch": LRFF13ItemData(
        code=883,
        str_id="e531",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Snakeskin Eyepatch": LRFF13ItemData(
        code=884,
        str_id="e532",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lovely Eyepatch": LRFF13ItemData(
        code=885,
        str_id="e533",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Glam Hat": LRFF13ItemData(
        code=886,
        str_id="e534",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Thief's Silk Hat": LRFF13ItemData(
        code=887,
        str_id="e535",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lady's Silk Hat": LRFF13ItemData(
        code=888,
        str_id="e536",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Clown's Silk Hat": LRFF13ItemData(
        code=889,
        str_id="e537",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cowboy Hat": LRFF13ItemData(
        code=890,
        str_id="e538",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Straw Hat": LRFF13ItemData(
        code=891,
        str_id="e539",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Snakeskin Hat": LRFF13ItemData(
        code=892,
        str_id="e540",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Safari Hat": LRFF13ItemData(
        code=893,
        str_id="e541",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Boater Hat": LRFF13ItemData(
        code=894,
        str_id="e542",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Vacation Hat": LRFF13ItemData(
        code=895,
        str_id="e543",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Green Straw Hat": LRFF13ItemData(
        code=896,
        str_id="e544",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Floppy Sun Hat": LRFF13ItemData(
        code=897,
        str_id="e545",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Painter's Beret": LRFF13ItemData(
        code=898,
        str_id="e546",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Order of Salvation Cap": LRFF13ItemData(
        code=899,
        str_id="e547",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dogtooth Beret": LRFF13ItemData(
        code=900,
        str_id="e548",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pro's Beret": LRFF13ItemData(
        code=901,
        str_id="e549",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sailor's Tricorne": LRFF13ItemData(
        code=902,
        str_id="e550",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Hotblooded Tricorne": LRFF13ItemData(
        code=903,
        str_id="e551",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Brigand's Tricorne": LRFF13ItemData(
        code=904,
        str_id="e552",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Priest's Tricorne": LRFF13ItemData(
        code=905,
        str_id="e553",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Witch's Pointy Hat": LRFF13ItemData(
        code=906,
        str_id="e554",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Scholar's Peaked Hat": LRFF13ItemData(
        code=907,
        str_id="e555",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dapper Hat": LRFF13ItemData(
        code=908,
        str_id="e556",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Hermit's Cap": LRFF13ItemData(
        code=909,
        str_id="e557",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown of Passion": LRFF13ItemData(
        code=910,
        str_id="e558",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown of Purity": LRFF13ItemData(
        code=911,
        str_id="e559",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown of Youth": LRFF13ItemData(
        code=912,
        str_id="e560",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown of Light": LRFF13ItemData(
        code=913,
        str_id="e561",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Crown of Splendor": LRFF13ItemData(
        code=914,
        str_id="e562",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Bow of Aestheticism": LRFF13ItemData(
        code=915,
        str_id="e563",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Passionate Corsage": LRFF13ItemData(
        code=916,
        str_id="e564",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sweet Corsage": LRFF13ItemData(
        code=917,
        str_id="e565",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Perky Corsage": LRFF13ItemData(
        code=918,
        str_id="e566",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lunar Circlet": LRFF13ItemData(
        code=919,
        str_id="e567",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Honored Circlet": LRFF13ItemData(
        code=920,
        str_id="e568",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Brave Circlet": LRFF13ItemData(
        code=921,
        str_id="e569",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Holy Circlet": LRFF13ItemData(
        code=922,
        str_id="e570",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "White Cat Ears": LRFF13ItemData(
        code=923,
        str_id="e571",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Black Cat Ears": LRFF13ItemData(
        code=924,
        str_id="e572",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Violet Cat Ears": LRFF13ItemData(
        code=925,
        str_id="e573",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Wildcat Ears": LRFF13ItemData(
        code=926,
        str_id="e574",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Adult Bunny Ears": LRFF13ItemData(
        code=927,
        str_id="e575",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Enticing Bunny Ears": LRFF13ItemData(
        code=928,
        str_id="e576",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Wild Bunny Ears": LRFF13ItemData(
        code=929,
        str_id="e577",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dark Devil Ears": LRFF13ItemData(
        code=930,
        str_id="e578",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Dazzling Devil Ears": LRFF13ItemData(
        code=931,
        str_id="e579",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pure Angel Ears": LRFF13ItemData(
        code=932,
        str_id="e580",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Cautious Devil Ears": LRFF13ItemData(
        code=933,
        str_id="e581",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pure Earrings": LRFF13ItemData(
        code=934,
        str_id="e582",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Pure Pendant": LRFF13ItemData(
        code=935,
        str_id="e583",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Heaven's Banner": LRFF13ItemData(
        code=936,
        str_id="e584",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Egotist's Banner": LRFF13ItemData(
        code=937,
        str_id="e585",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Herald's Banner": LRFF13ItemData(
        code=938,
        str_id="e586",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Lord's Banner": LRFF13ItemData(
        code=939,
        str_id="e587",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Fairy Tail": LRFF13ItemData(
        code=940,
        str_id="e588",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Imp Tail": LRFF13ItemData(
        code=941,
        str_id="e589",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Merry Tail": LRFF13ItemData(
        code=942,
        str_id="e590",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Untamed Tail": LRFF13ItemData(
        code=943,
        str_id="e591",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Fluffy Tail": LRFF13ItemData(
        code=944,
        str_id="e592",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Shadow Tail": LRFF13ItemData(
        code=945,
        str_id="e593",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Wagging Tail": LRFF13ItemData(
        code=946,
        str_id="e594",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Leopard Tail": LRFF13ItemData(
        code=947,
        str_id="e595",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Maiden's Beret": LRFF13ItemData(
        code=948,
        str_id="e596",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Guard's Cap": LRFF13ItemData(
        code=949,
        str_id="e597",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Warm Beret": LRFF13ItemData(
        code=950,
        str_id="e598",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Herringbone Beret": LRFF13ItemData(
        code=951,
        str_id="e599",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Deathless Mask": LRFF13ItemData(
        code=952,
        str_id="e600",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        weight=50,
        traits=["DLC"]
    ),
    "White Mage's Hat": LRFF13ItemData(
        code=953,
        str_id="e601",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Moogle Hat": LRFF13ItemData(
        code=954,
        str_id="e602",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        weight=50,
        traits=["DLC"]
    ),
    "Chocobo Girl's Cap": LRFF13ItemData(
        code=955,
        str_id="e603",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Chocoberet": LRFF13ItemData(
        code=956,
        str_id="e604",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Ivy Banner": LRFF13ItemData(
        code=957,
        str_id="e605",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Earth Banner": LRFF13ItemData(
        code=958,
        str_id="e606",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sun Banner": LRFF13ItemData(
        code=959,
        str_id="e607",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sky Banner": LRFF13ItemData(
        code=960,
        str_id="e608",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Apricot Banner": LRFF13ItemData(
        code=961,
        str_id="e609",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Banner of Charity": LRFF13ItemData(
        code=962,
        str_id="e610",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Sapling Banner": LRFF13ItemData(
        code=963,
        str_id="e611",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Tiara of the Goddess": LRFF13ItemData(
        code=964,
        str_id="e612",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        weight=50,
        traits=["DLC"]
    ),
    "Shogun's Mustache": LRFF13ItemData(
        code=965,
        str_id="e702",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Millionaire's Mustache": LRFF13ItemData(
        code=966,
        str_id="e703",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Servant's Mustache": LRFF13ItemData(
        code=967,
        str_id="e704",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Saint's Beard": LRFF13ItemData(
        code=968,
        str_id="e705",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Scholar's Beard": LRFF13ItemData(
        code=969,
        str_id="e706",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Politician's Beard": LRFF13ItemData(
        code=970,
        str_id="e707",
        classification=ItemClassification.progression_deprioritized_skip_balancing,
        category="Adornment",
        traits=["Key"]
    ),
    "Bronzed Medal": LRFF13ItemData(
        code=971,
        str_id="gil_l_000",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Silvered Medal": LRFF13ItemData(
        code=972,
        str_id="gil_l_010",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Crystal Medal": LRFF13ItemData(
        code=973,
        str_id="gil_l_020",
        classification=ItemClassification.filler,
        category="Material",
        weight=5440
    ),
    "Gold Dust": LRFF13ItemData(
        code=974,
        str_id="gil_r_000",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Platinum Ore": LRFF13ItemData(
        code=975,
        str_id="gil_r_010",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Ether": LRFF13ItemData(
        code=976,
        str_id="it_atel",
        classification=ItemClassification.filler,
        category="Item",
        weight=1530
    ),
    "Bravery Potion": LRFF13ItemData(
        code=977,
        str_id="it_brave",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Elixir": LRFF13ItemData(
        code=978,
        str_id="it_elixir",
        classification=ItemClassification.filler,
        category="Item",
        weight=540
    ),
    "Enaero Potion": LRFF13ItemData(
        code=979,
        str_id="it_enaero",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "Enfire Potion": LRFF13ItemData(
        code=980,
        str_id="it_enfire",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "Enfrost Potion": LRFF13ItemData(
        code=981,
        str_id="it_enfrost",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "Enthunder Potion": LRFF13ItemData(
        code=982,
        str_id="it_enthunder",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "X-Potion": LRFF13ItemData(
        code=983,
        str_id="it_expotion",
        classification=ItemClassification.filler,
        category="Item",
        weight=6210
    ),
    "Faith Potion": LRFF13ItemData(
        code=984,
        str_id="it_faith",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Holy Water": LRFF13ItemData(
        code=985,
        str_id="it_grace",
        classification=ItemClassification.filler,
        category="Item",
        weight=6210
    ),
    "Vigilance Potion": LRFF13ItemData(
        code=986,
        str_id="it_guts",
        classification=ItemClassification.filler,
        category="Item",
        weight=6210
    ),
    "Haste Potion": LRFF13ItemData(
        code=987,
        str_id="it_haste",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Hero's Potion": LRFF13ItemData(
        code=988,
        str_id="it_hero",
        classification=ItemClassification.filler,
        category="Item",
        weight=2160
    ),
    "Turbo Ether": LRFF13ItemData(
        code=989,
        str_id="it_hiatel",
        classification=ItemClassification.filler,
        category="Item",
        weight=810
    ),
    "Hi-Potion": LRFF13ItemData(
        code=990,
        str_id="it_hpotion",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Refresher": LRFF13ItemData(
        code=991,
        str_id="it_lowelxr",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Phoenix Wing": LRFF13ItemData(
        code=992,
        str_id="it_phenxbl",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Phoenix Down": LRFF13ItemData(
        code=993,
        str_id="it_phenxtal",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Potion": LRFF13ItemData(
        code=994,
        str_id="it_potion",
        classification=ItemClassification.filler,
        category="Item",
        weight=12600
    ),
    "Protect Potion": LRFF13ItemData(
        code=995,
        str_id="it_protect",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Regen Potion": LRFF13ItemData(
        code=996,
        str_id="it_regen",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Reraise Potion": LRFF13ItemData(
        code=997,
        str_id="it_reraise",
        classification=ItemClassification.filler,
        category="Item",
        weight=2160
    ),
    "Shell Potion": LRFF13ItemData(
        code=998,
        str_id="it_shell",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Mega Remedy": LRFF13ItemData(
        code=999,
        str_id="it_unico",
        classification=ItemClassification.filler,
        category="Item",
        weight=4410
    ),
    "Remedy": LRFF13ItemData(
        code=1000,
        str_id="it_universal",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Warrior's Potion": LRFF13ItemData(
        code=1001,
        str_id="it_upper",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "Veil Potion": LRFF13ItemData(
        code=1002,
        str_id="it_veil",
        classification=ItemClassification.filler,
        category="Item",
        weight=8820
    ),
    "Crusader's Potion": LRFF13ItemData(
        code=1003,
        str_id="it_war",
        classification=ItemClassification.filler,
        category="Item",
        weight=3060
    ),
    "Nektar of the Gods Omega": LRFF13ItemData(
        code=1004,
        str_id="it_ydrink5",
        classification=ItemClassification.filler,
        category="Item",
        weight=2160
    ),
    "Bronze Malistone": LRFF13ItemData(
        code=1005,
        str_id="mat_abi_0_00",
        classification=ItemClassification.filler,
        category="Material",
        weight=22400
    ),
    "Silver Malistone": LRFF13ItemData(
        code=1006,
        str_id="mat_abi_0_01",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Gold Malistone": LRFF13ItemData(
        code=1007,
        str_id="mat_abi_0_02",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Platinum Malistone": LRFF13ItemData(
        code=1008,
        str_id="mat_abi_0_03",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Mythril Malistone": LRFF13ItemData(
        code=1009,
        str_id="mat_abi_0_04",
        classification=ItemClassification.filler,
        category="Material",
        weight=5440
    ),
    "Adamant Malistone": LRFF13ItemData(
        code=1010,
        str_id="mat_abi_0_05",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Scarletite Malistone": LRFF13ItemData(
        code=1011,
        str_id="mat_abi_0_06",
        classification=ItemClassification.filler,
        category="Material",
        weight=2720
    ),
    "Orichalc Malistone": LRFF13ItemData(
        code=1012,
        str_id="mat_abi_0_07",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Crystal Malistone": LRFF13ItemData(
        code=1013,
        str_id="mat_abi_0_08",
        classification=ItemClassification.filler,
        category="Material",
        weight=1440
    ),
    "Mighty Material": LRFF13ItemData(
        code=1014,
        str_id="mat_cus_0_00",
        classification=ItemClassification.filler,
        category="Material",
        weight=22400
    ),
    "Sword Polisher": LRFF13ItemData(
        code=1015,
        str_id="mat_cus_0_01",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Shield Polisher": LRFF13ItemData(
        code=1016,
        str_id="mat_cus_0_02",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Holy Forgefire": LRFF13ItemData(
        code=1017,
        str_id="mat_cus_0_03",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Demonic Forgefire": LRFF13ItemData(
        code=1018,
        str_id="mat_cus_0_04",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Life Smeltwater": LRFF13ItemData(
        code=1019,
        str_id="mat_cus_0_05",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Soul Smeltwater": LRFF13ItemData(
        code=1020,
        str_id="mat_cus_0_06",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Forgefire of Chaos": LRFF13ItemData(
        code=1021,
        str_id="mat_cus_0_07",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Forgefire of Order": LRFF13ItemData(
        code=1022,
        str_id="mat_cus_0_08",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Tattered Leather": LRFF13ItemData(
        code=1023,
        str_id="mat_z_000",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Vibrant Ooze": LRFF13ItemData(
        code=1024,
        str_id="mat_z_001",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Niblet Hairball": LRFF13ItemData(
        code=1025,
        str_id="mat_z_002",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Slug Sweet": LRFF13ItemData(
        code=1026,
        str_id="mat_z_003",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Monster Mince": LRFF13ItemData(
        code=1027,
        str_id="mat_z_004",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Clear Ooze": LRFF13ItemData(
        code=1028,
        str_id="mat_z_007",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Green Leather": LRFF13ItemData(
        code=1029,
        str_id="mat_z_008",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Radial Bearing": LRFF13ItemData(
        code=1030,
        str_id="mat_z_009",
        classification=ItemClassification.filler,
        category="Material",
        weight=15680
    ),
    "Goblot Hairball": LRFF13ItemData(
        code=1031,
        str_id="mat_z_010",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Arboreal Spore": LRFF13ItemData(
        code=1032,
        str_id="mat_z_011",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Dead Man's Teeth": LRFF13ItemData(
        code=1033,
        str_id="mat_z_012",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Chipped Fang": LRFF13ItemData(
        code=1034,
        str_id="mat_z_013",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Shattered Bone": LRFF13ItemData(
        code=1035,
        str_id="mat_z_014",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Goopy Goo": LRFF13ItemData(
        code=1036,
        str_id="mat_z_015",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Pot Shard": LRFF13ItemData(
        code=1037,
        str_id="mat_z_016",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Dried Scale": LRFF13ItemData(
        code=1038,
        str_id="mat_z_017",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Wonder Gel": LRFF13ItemData(
        code=1039,
        str_id="mat_z_018",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Poisonous Sting": LRFF13ItemData(
        code=1040,
        str_id="mat_z_019",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Motor Coil": LRFF13ItemData(
        code=1041,
        str_id="mat_z_020",
        classification=ItemClassification.filler,
        category="Material",
        weight=11040
    ),
    "Ether Coil": LRFF13ItemData(
        code=1042,
        str_id="mat_z_021",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Demon Spicule": LRFF13ItemData(
        code=1043,
        str_id="mat_z_022",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Organic Carapace": LRFF13ItemData(
        code=1044,
        str_id="mat_z_024",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Firewyrm Scale": LRFF13ItemData(
        code=1045,
        str_id="mat_z_028",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Quality Machine Oil": LRFF13ItemData(
        code=1046,
        str_id="mat_z_029",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Sinister Fang": LRFF13ItemData(
        code=1047,
        str_id="mat_z_030",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Stormdragon Down": LRFF13ItemData(
        code=1048,
        str_id="mat_z_031",
        classification=ItemClassification.filler,
        category="Material",
        weight=3840
    ),
    "Green Monster Moss": LRFF13ItemData(
        code=1049,
        str_id="mat_z_032",
        classification=ItemClassification.filler,
        category="Material",
        weight=5440
    ),
    "Desert Rose": LRFF13ItemData(
        code=1050,
        str_id="mat_z_033",
        classification=ItemClassification.filler,
        category="Material",
        weight=5440
    ),
    "Single Eye": LRFF13ItemData(
        code=1051,
        str_id="mat_z_035",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "AMP Chip": LRFF13ItemData(
        code=1052,
        str_id="mat_z_036",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Cactuar Doll": LRFF13ItemData(
        code=1053,
        str_id="mat_z_044",
        classification=ItemClassification.filler,
        category="Material",
        weight=1920
    ),
    "Liquid Glass": LRFF13ItemData(
        code=1054,
        str_id="mat_z_045",
        classification=ItemClassification.filler,
        category="Material",
        weight=7840
    ),
    "Prytwen": LRFF13ItemData(
        code=1055,
        str_id="shi_ba00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Pendragon": LRFF13ItemData(
        code=1056,
        str_id="shi_ba01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Dame du Lac": LRFF13ItemData(
        code=1057,
        str_id="shi_ba02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Guard of Avalon": LRFF13ItemData(
        code=1058,
        str_id="shi_ba03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Knight's Pledge": LRFF13ItemData(
        code=1059,
        str_id="shi_ba04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Double Cross": LRFF13ItemData(
        code=1060,
        str_id="shi_ca00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Deicide": LRFF13ItemData(
        code=1061,
        str_id="shi_ca01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Blasphemy": LRFF13ItemData(
        code=1062,
        str_id="shi_ca02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Infidel": LRFF13ItemData(
        code=1063,
        str_id="shi_ca03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Renegade": LRFF13ItemData(
        code=1064,
        str_id="shi_ca04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Ghostly Bloom": LRFF13ItemData(
        code=1065,
        str_id="shi_da00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Il Nome Della Rosa": LRFF13ItemData(
        code=1066,
        str_id="shi_da01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Gilded Lily": LRFF13ItemData(
        code=1067,
        str_id="shi_da02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Noblesse Veronique": LRFF13ItemData(
        code=1068,
        str_id="shi_da03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Les Fleurs du Mal": LRFF13ItemData(
        code=1069,
        str_id="shi_da04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Ultima Shield": LRFF13ItemData(
        code=1070,
        str_id="shi_ea00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Hesperides": LRFF13ItemData(
        code=1071,
        str_id="shi_ea01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Juno Sospita": LRFF13ItemData(
        code=1072,
        str_id="shi_ea02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Megalesia": LRFF13ItemData(
        code=1073,
        str_id="shi_ea03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Nemesis": LRFF13ItemData(
        code=1074,
        str_id="shi_ea04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Night Lotus": LRFF13ItemData(
        code=1075,
        str_id="shi_ea08",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Deirdre's Tears": LRFF13ItemData(
        code=1076,
        str_id="shi_fa00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Cleopatra's Praise": LRFF13ItemData(
        code=1077,
        str_id="shi_fa01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Iseult's Lament": LRFF13ItemData(
        code=1078,
        str_id="shi_fa02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Kore Soteira": LRFF13ItemData(
        code=1079,
        str_id="shi_fa03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Juliet's Sorrow": LRFF13ItemData(
        code=1080,
        str_id="shi_fa04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Dragoon Gauntlet": LRFF13ItemData(
        code=1081,
        str_id="shi_ga00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Yale Gauntlet": LRFF13ItemData(
        code=1082,
        str_id="shi_ga01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Chiron Gauntlet": LRFF13ItemData(
        code=1083,
        str_id="shi_ga02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Echidna Gauntlet": LRFF13ItemData(
        code=1084,
        str_id="shi_ga03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Apis Gauntlet": LRFF13ItemData(
        code=1085,
        str_id="shi_ga04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Aquamarine Waltz": LRFF13ItemData(
        code=1086,
        str_id="shi_ha00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Amethyst Anthem": LRFF13ItemData(
        code=1087,
        str_id="shi_ha01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Carnelian Choir": LRFF13ItemData(
        code=1088,
        str_id="shi_ha02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Emerald Ensemble": LRFF13ItemData(
        code=1089,
        str_id="shi_ha03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Crystal Silence": LRFF13ItemData(
        code=1090,
        str_id="shi_ha04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Dark Discord": LRFF13ItemData(
        code=1091,
        str_id="shi_ha05",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Lominsan Escutcheon": LRFF13ItemData(
        code=1092,
        str_id="shi_ia00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Ul'dahn Crest": LRFF13ItemData(
        code=1093,
        str_id="shi_ia01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Gridanian Sigil": LRFF13ItemData(
        code=1094,
        str_id="shi_ia02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Guardian Corps Shield": LRFF13ItemData(
        code=1095,
        str_id="shi_ja00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Goddess's Grace": LRFF13ItemData(
        code=1096,
        str_id="shi_ka00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50
    ),
    "Summoner's Shield": LRFF13ItemData(
        code=1097,
        str_id="shi_la00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Guardian's Protector": LRFF13ItemData(
        code=1098,
        str_id="shi_ma00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "SOLDIER's Band": LRFF13ItemData(
        code=1099,
        str_id="shi_oa00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Thunderstruck": LRFF13ItemData(
        code=1100,
        str_id="shi_zb00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Final Border": LRFF13ItemData(
        code=1101,
        str_id="shi_zb01",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Nightwalker": LRFF13ItemData(
        code=1102,
        str_id="shi_zb02",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Fealty": LRFF13ItemData(
        code=1103,
        str_id="shi_zb03",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Kaminari": LRFF13ItemData(
        code=1104,
        str_id="shi_zb04",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Warning Sign": LRFF13ItemData(
        code=1105,
        str_id="shi_zb05",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Rasa": LRFF13ItemData(
        code=1106,
        str_id="shi_zb06",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Riot Shield": LRFF13ItemData(
        code=1107,
        str_id="shi_zc00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Abyss Gate": LRFF13ItemData(
        code=1108,
        str_id="shi_zd00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Mog's Shield": LRFF13ItemData(
        code=1109,
        str_id="shi_ze00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Aegis Shield": LRFF13ItemData(
        code=1110,
        str_id="shi_zf00",
        classification=ItemClassification.filler,
        category="Shield",
        weight=50,
        traits=["DLC"]
    ),
    "Hyperion": LRFF13ItemData(
        code=1111,
        str_id="wea_ba00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Asterion": LRFF13ItemData(
        code=1112,
        str_id="wea_ba01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Pygmalion": LRFF13ItemData(
        code=1113,
        str_id="wea_ba02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Deucalion": LRFF13ItemData(
        code=1114,
        str_id="wea_ba03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Endymion": LRFF13ItemData(
        code=1115,
        str_id="wea_ba04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Scramasax": LRFF13ItemData(
        code=1116,
        str_id="wea_ca00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Szczerbiec": LRFF13ItemData(
        code=1117,
        str_id="wea_ca01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Morgenstern": LRFF13ItemData(
        code=1118,
        str_id="wea_ca02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Macuahuitl": LRFF13ItemData(
        code=1119,
        str_id="wea_ca03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Godendag": LRFF13ItemData(
        code=1120,
        str_id="wea_ca04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Femme Fatale": LRFF13ItemData(
        code=1121,
        str_id="wea_da00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Carmen's Dance": LRFF13ItemData(
        code=1122,
        str_id="wea_da01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Morgan le Fay": LRFF13ItemData(
        code=1123,
        str_id="wea_da02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Delilah's Temptation": LRFF13ItemData(
        code=1124,
        str_id="wea_da03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Salome's Kiss": LRFF13ItemData(
        code=1125,
        str_id="wea_da04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Ultima Weapon": LRFF13ItemData(
        code=1126,
        str_id="wea_ea00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Liberator": LRFF13ItemData(
        code=1127,
        str_id="wea_ea01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Salvation": LRFF13ItemData(
        code=1128,
        str_id="wea_ea02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Stigma": LRFF13ItemData(
        code=1129,
        str_id="wea_ea03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Immortal Order": LRFF13ItemData(
        code=1130,
        str_id="wea_ea04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Crimson Blitz": LRFF13ItemData(
        code=1131,
        str_id="wea_ea08",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Devil's Daughter": LRFF13ItemData(
        code=1132,
        str_id="wea_fa00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Izanami": LRFF13ItemData(
        code=1133,
        str_id="wea_fa01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Satanic Sister": LRFF13ItemData(
        code=1134,
        str_id="wea_fa02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Succubus Claw": LRFF13ItemData(
        code=1135,
        str_id="wea_fa03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Hades' Pride": LRFF13ItemData(
        code=1136,
        str_id="wea_fa04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Wyvern Lance": LRFF13ItemData(
        code=1137,
        str_id="wea_ga00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Seagod's Spear": LRFF13ItemData(
        code=1138,
        str_id="wea_ga01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Ramuh's Horn": LRFF13ItemData(
        code=1139,
        str_id="wea_ga02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Demon Claw": LRFF13ItemData(
        code=1140,
        str_id="wea_ga03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Hades' Fang": LRFF13ItemData(
        code=1141,
        str_id="wea_ga04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Kikuichimonji": LRFF13ItemData(
        code=1142,
        str_id="wea_ha00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Masamune": LRFF13ItemData(
        code=1143,
        str_id="wea_ha01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Heaven's Cloud": LRFF13ItemData(
        code=1144,
        str_id="wea_ha02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Demon Knife": LRFF13ItemData(
        code=1145,
        str_id="wea_ha03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Kusanagi": LRFF13ItemData(
        code=1146,
        str_id="wea_ha04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Brass Falcon": LRFF13ItemData(
        code=1147,
        str_id="wea_ia00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Callais Hawk": LRFF13ItemData(
        code=1148,
        str_id="wea_ia01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Nightingale": LRFF13ItemData(
        code=1149,
        str_id="wea_ia02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Vulture": LRFF13ItemData(
        code=1150,
        str_id="wea_ia03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Vedfolnir": LRFF13ItemData(
        code=1151,
        str_id="wea_ia04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Magician's Wand": LRFF13ItemData(
        code=1152,
        str_id="wea_ja00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Astromancer's Scepter": LRFF13ItemData(
        code=1153,
        str_id="wea_ja01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Asteria's Staff": LRFF13ItemData(
        code=1154,
        str_id="wea_ja02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Necromancer's Cane": LRFF13ItemData(
        code=1155,
        str_id="wea_ja03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Philosopher's Rod": LRFF13ItemData(
        code=1156,
        str_id="wea_ja04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Double Saber": LRFF13ItemData(
        code=1157,
        str_id="wea_ka00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Godly Gambrel": LRFF13ItemData(
        code=1158,
        str_id="wea_ka01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Tower Blade": LRFF13ItemData(
        code=1159,
        str_id="wea_ka02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Black Gantry": LRFF13ItemData(
        code=1160,
        str_id="wea_ka03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Heaven's Bridge": LRFF13ItemData(
        code=1161,
        str_id="wea_ka04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Lominsan Cutlass": LRFF13ItemData(
        code=1162,
        str_id="wea_la00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Ul'dahn Blade": LRFF13ItemData(
        code=1163,
        str_id="wea_la01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Gridanian Sword": LRFF13ItemData(
        code=1164,
        str_id="wea_la02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Blazefire Saber": LRFF13ItemData(
        code=1165,
        str_id="wea_ma00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Overture": LRFF13ItemData(
        code=1166,
        str_id="wea_na00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Shadow Hunter": LRFF13ItemData(
        code=1167,
        str_id="wea_oa00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Endless Paradox": LRFF13ItemData(
        code=1168,
        str_id="wea_oa01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Chaos's Revenge": LRFF13ItemData(
        code=1169,
        str_id="wea_oa02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Double Deity": LRFF13ItemData(
        code=1170,
        str_id="wea_oa03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Demon's Mace": LRFF13ItemData(
        code=1171,
        str_id="wea_oa04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Destroyer": LRFF13ItemData(
        code=1172,
        str_id="wea_oa05",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Shard Blade": LRFF13ItemData(
        code=1173,
        str_id="wea_oa06",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Flesh Render": LRFF13ItemData(
        code=1174,
        str_id="wea_oa07",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Death Herald": LRFF13ItemData(
        code=1175,
        str_id="wea_oa08",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Grim Reaper": LRFF13ItemData(
        code=1176,
        str_id="wea_oa09",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Executioner's Axe": LRFF13ItemData(
        code=1177,
        str_id="wea_oa10",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Headhunter": LRFF13ItemData(
        code=1178,
        str_id="wea_oa11",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Brittle Bone": LRFF13ItemData(
        code=1179,
        str_id="wea_oa12",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Bonecracker": LRFF13ItemData(
        code=1180,
        str_id="wea_oa13",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Sickle of the Faithful": LRFF13ItemData(
        code=1181,
        str_id="wea_oa14",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Battleaxe of the Believer": LRFF13ItemData(
        code=1182,
        str_id="wea_oa15",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Gagnrad": LRFF13ItemData(
        code=1183,
        str_id="wea_oa16",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Bladed Lance": LRFF13ItemData(
        code=1184,
        str_id="wea_oa17",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50
    ),
    "Summoner's Staff": LRFF13ItemData(
        code=1185,
        str_id="wea_pa00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Brotherhood": LRFF13ItemData(
        code=1186,
        str_id="wea_qa00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Buster Sword": LRFF13ItemData(
        code=1187,
        str_id="wea_sa00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Thirteen Nights": LRFF13ItemData(
        code=1188,
        str_id="wea_zb00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Rising Sun": LRFF13ItemData(
        code=1189,
        str_id="wea_zb01",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Cloud Veil": LRFF13ItemData(
        code=1190,
        str_id="wea_zb02",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Treasure Hold": LRFF13ItemData(
        code=1191,
        str_id="wea_zb03",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Heavenly Fan": LRFF13ItemData(
        code=1192,
        str_id="wea_zb04",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Cruel Grace": LRFF13ItemData(
        code=1193,
        str_id="wea_zb05",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Jikishinkage": LRFF13ItemData(
        code=1194,
        str_id="wea_zb06",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Survivor's Axe": LRFF13ItemData(
        code=1195,
        str_id="wea_zc00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Crocea Mors": LRFF13ItemData(
        code=1196,
        str_id="wea_zd00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Mog's Staff": LRFF13ItemData(
        code=1197,
        str_id="wea_ze00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Excalibur": LRFF13ItemData(
        code=1198,
        str_id="wea_zf00",
        classification=ItemClassification.filler,
        category="Weapon",
        weight=50,
        traits=["DLC"]
    ),
    "Army of One": LRFF13ItemData(
        code=1199,
        str_id="at900_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Curaga": LRFF13ItemData(
        code=1200,
        str_id="ti000_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Arise": LRFF13ItemData(
        code=1201,
        str_id="ti020_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Esunada": LRFF13ItemData(
        code=1202,
        str_id="ti030_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Quake": LRFF13ItemData(
        code=1203,
        str_id="ti500_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Decoy": LRFF13ItemData(
        code=1204,
        str_id="ti600_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Teleport": LRFF13ItemData(
        code=1205,
        str_id="ti810_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Escape": LRFF13ItemData(
        code=1206,
        str_id="ti830_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Chronostasis": LRFF13ItemData(
        code=1207,
        str_id="ti840_00",
        classification=ItemClassification.useful,
        category="EP Ability"
    ),
    "Proof of Courage": LRFF13ItemData(
        code=1208,
        str_id="key_b_00",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Violet Amulet": LRFF13ItemData(
        code=1209,
        str_id="key_b_01",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Lapis Lazuli": LRFF13ItemData(
        code=1210,
        str_id="key_b_02",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Power Booster": LRFF13ItemData(
        code=1211,
        str_id="key_b_03",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Moogle Dust": LRFF13ItemData(
        code=1212,
        str_id="key_b_04",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Old-Fashioned Photo Frame": LRFF13ItemData(
        code=1213,
        str_id="key_b_05",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Etro's Forbidden Tome": LRFF13ItemData(
        code=1214,
        str_id="key_b_06",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Broken Gyroscope": LRFF13ItemData(
        code=1215,
        str_id="key_b_07",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Golden Scarab": LRFF13ItemData(
        code=1216,
        str_id="key_b_08",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Key to the Sand Gate": LRFF13ItemData(
        code=1217,
        str_id="key_b_09",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Key to the Green Gate": LRFF13ItemData(
        code=1218,
        str_id="key_b_10",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Bandit's Bloodseal": LRFF13ItemData(
        code=1219,
        str_id="key_b_11",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Oath of the Merchants Guild": LRFF13ItemData(
        code=1220,
        str_id="key_b_12",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Jade Hair Comb": LRFF13ItemData(
        code=1221,
        str_id="key_b_16",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Bronze Pocket Watch": LRFF13ItemData(
        code=1222,
        str_id="key_b_17",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Chocobo Girl's Phone No.": LRFF13ItemData(
        code=1223,
        str_id="key_b_20",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Rubber Ball": LRFF13ItemData(
        code=1224,
        str_id="key_ball",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Crux Base": LRFF13ItemData(
        code=1225,
        str_id="key_d_base",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Pilgrim's Crux": LRFF13ItemData(
        code=1226,
        str_id="key_d_key",
        classification=ItemClassification.progression,
        category="Key",
        duplicate_amount=14
    ),
    "Loupe": LRFF13ItemData(
        code=1227,
        str_id="key_d_lupe",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Tablet": LRFF13ItemData(
        code=1228,
        str_id="key_d_sekiban",
        classification=ItemClassification.progression,
        category="Key",
        duplicate_amount=3
    ),
    "Crux Tip": LRFF13ItemData(
        code=1229,
        str_id="key_d_top",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Crux Body": LRFF13ItemData(
        code=1230,
        str_id="key_d_wing",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Thunderclap Cap": LRFF13ItemData(
        code=1231,
        str_id="key_j_kino",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Green Carbuncle Doll": LRFF13ItemData(
        code=1232,
        str_id="key_kb_g",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Red Carbuncle Doll": LRFF13ItemData(
        code=1233,
        str_id="key_kb_r",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Talbot's Gratitude": LRFF13ItemData(
        code=1234,
        str_id="key_kimochi",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Supply Sphere Password": LRFF13ItemData(
        code=1235,
        str_id="key_kyu_pass",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Phantom Rose": LRFF13ItemData(
        code=1236,
        str_id="key_l_hana",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Service Entrance Key": LRFF13ItemData(
        code=1237,
        str_id="key_l_kagi",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Proof of Legendary Title": LRFF13ItemData(
        code=1238,
        str_id="key_l_kishin",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Quill Pen": LRFF13ItemData(
        code=1239,
        str_id="key_l_pen",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Shaolong Gui Shell": LRFF13ItemData(
        code=1240,
        str_id="key_niku",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Mandragora Root": LRFF13ItemData(
        code=1241,
        str_id="key_ninjin",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Proof of Overcoming Limits": LRFF13ItemData(
        code=1242,
        str_id="key_p_toppa",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fragment of Radiance": LRFF13ItemData(
        code=1243,
        str_id="key_s_hiai",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fragment of Mischief": LRFF13ItemData(
        code=1244,
        str_id="key_s_kairaku",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fragment of Courage": LRFF13ItemData(
        code=1245,
        str_id="key_s_kanki",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Beloved's Gift": LRFF13ItemData(
        code=1246,
        str_id="key_s_okuri",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fragment of Smiles": LRFF13ItemData(
        code=1247,
        str_id="key_s_zyouai",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Seedhunter Membership Card": LRFF13ItemData(
        code=1248,
        str_id="key_soulcd",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Spectral Elixir": LRFF13ItemData(
        code=1249,
        str_id="key_sp_bt",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Aryas Apple": LRFF13ItemData(
        code=1250,
        str_id="key_w_apple",
        classification=ItemClassification.progression,
        category="Key",
        duplicate_amount=3
    ),
    "Plate Metal Fragment": LRFF13ItemData(
        code=1251,
        str_id="key_w_buhin1",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Silvered Metal Fragment": LRFF13ItemData(
        code=1252,
        str_id="key_w_buhin2",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Golden Metal Fragment": LRFF13ItemData(
        code=1253,
        str_id="key_w_buhin3",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Data Recorder": LRFF13ItemData(
        code=1254,
        str_id="key_w_data",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Moogle Fragment": LRFF13ItemData(
        code=1255,
        str_id="key_w_mogsoul",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Goddess Glyphs": LRFF13ItemData(
        code=1256,
        str_id="key_w_moji1",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Chaos Glyphs": LRFF13ItemData(
        code=1257,
        str_id="key_w_moji2",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Mystery Egg": LRFF13ItemData(
        code=1258,
        str_id="key_w_tamago",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Vegetable Seed": LRFF13ItemData(
        code=1259,
        str_id="key_w_tane",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Gysahl Greens": LRFF13ItemData(
        code=1260,
        str_id="key_w_yasai_t",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Steak a la Civet": LRFF13ItemData(
        code=1261,
        str_id="key_y_cream",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "ID Card": LRFF13ItemData(
        code=1262,
        str_id="key_y_id",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Musical Treasure Sphere Key": LRFF13ItemData(
        code=1263,
        str_id="key_y_kagi1",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Nostalgic Score: Chorus": LRFF13ItemData(
        code=1264,
        str_id="key_y_kagi2",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Nostalgic Score: Refrain": LRFF13ItemData(
        code=1265,
        str_id="key_y_kagi3",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Father's Letter": LRFF13ItemData(
        code=1266,
        str_id="key_y_letter",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Nostalgic Score: Coda": LRFF13ItemData(
        code=1267,
        str_id="key_y_rappa",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Gordon Gourmet's Recipe": LRFF13ItemData(
        code=1268,
        str_id="key_y_recipe",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Serah's Pendant": LRFF13ItemData(
        code=1269,
        str_id="key_y_serap",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Sneaking-In Special Ticket": LRFF13ItemData(
        code=1270,
        str_id="key_y_ticket",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Flanitor Notes": LRFF13ItemData(
        code=1271,
        str_id="libra_m079",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Cactair Notes": LRFF13ItemData(
        code=1272,
        str_id="libra_m253_afr",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Cathedral Sentry Notes": LRFF13ItemData(
        code=1273,
        str_id="libra_m291",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Patron's Personal Guard Notes": LRFF13ItemData(
        code=1274,
        str_id="libra_m292",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Fanatic Notes": LRFF13ItemData(
        code=1275,
        str_id="libra_m293",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Desmond Notes": LRFF13ItemData(
        code=1276,
        str_id="libra_m330",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Earth Eater Notes": LRFF13ItemData(
        code=1277,
        str_id="libra_m355",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Study of the Depths": LRFF13ItemData(
        code=1278,
        str_id="libra_m370",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Study of Despair": LRFF13ItemData(
        code=1279,
        str_id="libra_m375",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Prophecy of the Future": LRFF13ItemData(
        code=1280,
        str_id="libra_m380",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Prophecy of Aspiration": LRFF13ItemData(
        code=1281,
        str_id="libra_m381",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Holy Revelations": LRFF13ItemData(
        code=1282,
        str_id="libra_m387",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Gurangatch Notes": LRFF13ItemData(
        code=1283,
        str_id="libra_m406",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Prophecy of Rebirth": LRFF13ItemData(
        code=1284,
        str_id="libra_m745",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Study of the Savage": LRFF13ItemData(
        code=1285,
        str_id="libra_m770",
        classification=ItemClassification.filler,
        category="Key"
    ),
    "Cursed Dragon Claw": LRFF13ItemData(
        code=1286,
        str_id="key_behi_tume",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Arithmometer": LRFF13ItemData(
        code=1287,
        str_id="key_d_keisan",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Monster Flesh": LRFF13ItemData(
        code=1288,
        str_id="key_d_niku",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Fragment of Kindness": LRFF13ItemData(
        code=1289,
        str_id="key_s_hunnu",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Civet Musk": LRFF13ItemData(
        code=1290,
        str_id="key_y_bashira",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "Music Satchel": LRFF13ItemData(
        code=1291,
        str_id="key_y_kaban",
        classification=ItemClassification.progression,
        category="Key"
    ),
    "10 Gil": LRFF13ItemData(
        code=1292,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=500,
        amount=10,
        duplicate_amount=0
    ),
    "500 Gil": LRFF13ItemData(
        code=1293,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=7000,
        amount=500,
        duplicate_amount=0
    ),
    "1000 Gil": LRFF13ItemData(
        code=1294,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=9000,
        amount=1000,
        duplicate_amount=0
    ),
    "2500 Gil": LRFF13ItemData(
        code=1295,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=6000,
        amount=2500,
        duplicate_amount=0
    ),
    "7500 Gil": LRFF13ItemData(
        code=1296,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=4000,
        amount=7500,
        duplicate_amount=0
    ),
    "20000 Gil": LRFF13ItemData(
        code=1297,
        str_id="",
        classification=ItemClassification.filler,
        category="Gil",
        weight=1000,
        amount=20000,
        duplicate_amount=0
    ),
}

item_table = {name: data.code for name, data in item_data_table.items()}
inv_item_table = {data.code: name for name, data in item_data_table.items()}

filler_items = [name for name, data in item_data_table.items()
                if data.classification == ItemClassification.filler and data.weight > 0]
filler_weights = [item_data_table[name].weight for name in filler_items]
