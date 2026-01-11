from ..rules import *
from ... import StaticEncounterData, TradeEncounterData

legendary: dict[str, StaticEncounterData] = {
    "Guidance Chamber Static Encounter": StaticEncounterData((638, 0), (638, 0), "Mistralton Cave Inner", None, None),
    "Trial Chamber Static Encounter": StaticEncounterData((639, 0), (639, 0), "Trial Chamber", None, can_use_strength),
    "Rumination Field Static Encounter": StaticEncounterData((640, 0), (640, 0), "Pinwheel Forest East", None, can_encounter_swords_of_justice),
    "Abundant Shrine Static Encounter": StaticEncounterData((645, 0), (645, 0), "Abundant Shrine", randomized_wild, has_forces_of_nature),
    "Giant Chasm Static Encounter": StaticEncounterData((646, 0), (646, 0), "Giant Chasm Inner Cave", None, None),
    "Liberty Garden Static Encounter": StaticEncounterData((494, 0), (494, 0), "Liberty Garden", None, None),
    "Dragonspiral Tower Static Encounter": StaticEncounterData((643, 0), (644, 0), "Dragonspiral Tower", None, can_beat_ghetsis),
    "Roaming Encounter": StaticEncounterData((641, 0), (642, 0), "Route 7", None, can_beat_ghetsis),
}

gift: dict[str, StaticEncounterData] = {
    "Marvelous Bridge Sold Encounter": StaticEncounterData((129, 0), (129, 0), "Marvelous Bridge", None, None),
    "Route 18 Egg Encounter": StaticEncounterData((636, 0), (636, 0), "Route 18", None, None),
    "Dreamyard Gift Encounter": StaticEncounterData((511, 0), (511, 0), "Dreamyard Entrance", disabled, None),  # will require being randomized
    "Castelia City Gift Encounter": StaticEncounterData((570, 0), (570, 0), "Castelia City", randomized_wild, has_celebi),
}

fossils: dict[str, StaticEncounterData] = {
    "Root Fossil Reanimation": StaticEncounterData((345, 0), (345, 0), "Nacrene City", None, has_root_fossil),
    "Claw Fossil Reanimation": StaticEncounterData((347, 0), (347, 0), "Nacrene City", None, has_claw_fossil),
    "Helix Fossil Reanimation": StaticEncounterData((138, 0), (138, 0), "Nacrene City", None, has_helix_fossil),
    "Dome Fossil Reanimation": StaticEncounterData((140, 0), (140, 0), "Nacrene City", None, has_dome_fossil),
    "Old Amber Reanimation": StaticEncounterData((142, 0), (142, 0), "Nacrene City", None, has_old_amber),
    "Armor Fossil Reanimation": StaticEncounterData((410, 0), (410, 0), "Nacrene City", None, has_armor_fossil),
    "Skull Fossil Reanimation": StaticEncounterData((408, 0), (408, 0), "Nacrene City", None, has_skull_fossil),
    "Cover Fossil Reanimation": StaticEncounterData((564, 0), (564, 0), "Nacrene City", None, has_cover_fossil),
    "Plume Fossil Reanimation": StaticEncounterData((566, 0), (566, 0), "Nacrene City", None, has_plume_fossil),
}

trade: dict[str, TradeEncounterData] = {
    "Nacrene City Trade Encounter": TradeEncounterData((548, 0), (546, 0), 546, 548, "Nacrene City"),
    "Driftveil City Trade Encounter": TradeEncounterData((550, 0), (550, 1), 572, 572, "Driftveil City"),
    "Route 7 Trade Encounter": TradeEncounterData((587, 0), (587, 0), 525, 525, "Route 7"),
    "Route 15 Trade Encounter": TradeEncounterData((479, 0), (479, 0), 132, 132, "Route 15"),
    "Undella Town Trade Encounter": TradeEncounterData((446, 0), (446, 0), 573, 573, "Undella Town"),
}

static: dict[str, StaticEncounterData] = {
    "Desert Resort Static Encounter 1": StaticEncounterData((555, 0), (555, 0), "Desert Resort", None, has_rage_candy_bar),
    "Desert Resort Static Encounter 2": StaticEncounterData((555, 0), (555, 0), "Desert Resort", None, has_rage_candy_bar),
    "Desert Resort Static Encounter 3": StaticEncounterData((555, 0), (555, 0), "Desert Resort", None, has_rage_candy_bar),
    "Desert Resort Static Encounter 4": StaticEncounterData((555, 0), (555, 0), "Desert Resort", None, has_rage_candy_bar),
    "Desert Resort Static Encounter 5": StaticEncounterData((555, 0), (555, 0), "Desert Resort", None, has_rage_candy_bar),
    "Dreamyard Static Encounter": StaticEncounterData((518, 0), (518, 0), "Dreamyard Basement", None, None),
    "Relic Castle Static Encounter": StaticEncounterData((637, 0), (637, 0), "Relic Castle Basement", None, None),
    "Route 6 Item Encounter 1": StaticEncounterData((590, 0), (590, 0), "Route 6", None, None),
    "Route 6 Item Encounter 2": StaticEncounterData((590, 0), (590, 0), "Route 6", None, None),
    "Route 10 Item Encounter 1": StaticEncounterData((590, 0), (590, 0), "Route 10", None, None),
    "Route 10 Item Encounter 2": StaticEncounterData((590, 0), (590, 0), "Route 10", None, None),
    "Route 10 Item Encounter 3": StaticEncounterData((591, 0), (591, 0), "Route 10", None, None),
    "Route 10 Item Encounter 4": StaticEncounterData((591, 0), (591, 0), "Route 10", None, None),
    "Lostlorn Forest Static Encounter": StaticEncounterData((571, 0), (571, 0), "Lostlorn Forest", randomized_wild, has_legendary_beasts),
}
