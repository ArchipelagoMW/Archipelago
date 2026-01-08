"""
Classes and functions related to AP locations for Metroid: Zero Mission
"""

from typing import NamedTuple
from .items import AP_MZM_ID_BASE


class LocationData(NamedTuple):
    region: str
    id: int | None
    force_sound: int | None = None

    @property
    def code(self):
        if self.id is None:
            return None
        return self.id + AP_MZM_ID_BASE


# Location numbers/order and some names from Biospark's MZM Randomizer.
# Events in any region must be at the end of its table for the client to work correctly

brinstar_location_table = {
    "Brinstar Morph Ball": LocationData("Brinstar Start", 0),
    "Brinstar Morph Ball Cannon": LocationData("Brinstar Start", 1),
    "Brinstar Long Beam": LocationData("Brinstar Main", 2),
    "Brinstar Ceiling E-Tank": LocationData("Brinstar Start", 3),
    "Brinstar Main Shaft Left Alcove": LocationData("Brinstar Main", 4),
    "Brinstar Ballspark": LocationData("Brinstar Main", 5),
    "Brinstar Ripper Climb": LocationData("Brinstar Main", 6),
    "Brinstar Speed Booster Shortcut": LocationData("Brinstar Main", 7),
    "Brinstar Varia Suit": LocationData("Brinstar Varia Area", 8),
    "Brinstar Worm Drop": LocationData("Brinstar Main", 9),
    "Brinstar Acid Near Varia": LocationData("Brinstar Varia Area", 10),
    "Brinstar First Missile": LocationData("Brinstar Main", 11),
    "Brinstar Behind Hive": LocationData("Brinstar Main", 12),
    "Brinstar Under Bridge": LocationData("Brinstar Main", 13),
    "Brinstar Post-Hive in Wall": LocationData("Brinstar Past Hives", 14),
    "Brinstar Upper Pillar": LocationData("Brinstar Top", 15),
    "Brinstar Behind Bombs": LocationData("Brinstar Past Hives", 16),
    "Brinstar Bomb": LocationData("Brinstar Past Hives", 17),
    "Brinstar Post-Hive Pillar": LocationData("Brinstar Past Hives", 18)
}

kraid_location_table = {
    "Kraid Behind Giant Hoppers": LocationData("Kraid Left Shaft", 19),
    "Kraid Save Room Tunnel": LocationData("Kraid Main", 20),
    "Kraid Zipline Morph Jump": LocationData("Kraid Main", 21),
    "Kraid Quad Ball Cannon Room": LocationData("Kraid Left Shaft", 22),
    "Kraid Unknown Item Statue": LocationData("Kraid Left Shaft", 23),
    "Kraid Acid Ballspark": LocationData("Kraid Main", 24),
    "Kraid Speed Booster": LocationData("Kraid Bottom", 25),
    "Kraid Under Acid Worm": LocationData("Kraid Acid Worm Area", 26),
    "Kraid Right Hall Pillar": LocationData("Kraid Main", 27),
    "Kraid Acid Fall": LocationData("Kraid Bottom", 28),
    "Kraid Zipline Activator Room": LocationData("Kraid Acid Worm Area", 29),
    "Kraid Speed Jump": LocationData("Kraid Main", 30),
    "Kraid Upper Right Morph Ball Cannon": LocationData("Kraid Main", 31),
    "Kraid Zipline Activator": LocationData("Kraid Acid Worm Area", None),
    "Kraid": LocationData("Kraid Bottom", None)
}

norfair_location_table = {
    "Norfair Lava Dive Left": LocationData("Lower Norfair", 32),
    "Norfair Lava Dive Right": LocationData("Lower Norfair", 33),
    "Norfair Screw Attack": LocationData("Norfair Screw Attack Area", 34),
    "Norfair Next to Screw Attack": LocationData("Norfair Screw Attack Area", 35),
    "Norfair Hallway to Crateria": LocationData("Norfair Main", 36),
    "Norfair Under Crateria Elevator": LocationData("Norfair Main", 37),
    "Norfair Wave Beam": LocationData("Lower Norfair", 38),
    "Norfair Bomb Trap": LocationData("Norfair Under Brinstar Elevator", 39),
    "Norfair Heated Room Below Wave - Left": LocationData("Lower Norfair", 40),
    "Norfair Heated Room Below Wave - Right": LocationData("Lower Norfair", 41),
    "Norfair Heated Room Under Brinstar Elevator": LocationData("Norfair Under Brinstar Elevator", 42),
    "Norfair Behind Lower Super Missile Door - Left": LocationData("Norfair Behind Super Door", 43),
    "Norfair Behind Lower Super Missile Door - Right": LocationData("Norfair Behind Super Door", 44),
    "Norfair Ice Beam": LocationData("Norfair Upper Right Shaft", 45),
    "Norfair Heated Room Above Ice Beam": LocationData("Norfair Upper Right Shaft", 46),
    "Norfair Hi-Jump": LocationData("Norfair Lower Right Shaft", 47),
    "Norfair Big Room": LocationData("Norfair Right Shaft", 48),
    "Norfair Behind Top Chozo Statue": LocationData("Norfair Behind Ice Beam", 49),
    "Norfair Larva Ceiling": LocationData("Norfair Bottom", 50),
    "Norfair Right Shaft Near Hi-Jump": LocationData("Norfair LRS By Hi-Jump", 51),
    "Norfair Right Shaft Bottom": LocationData("Norfair Bottom", 52)
}

ridley_location_table = {
    "Ridley Southwest Puzzle Top": LocationData("Ridley SW Puzzle", 53),
    "Ridley Southwest Puzzle Bottom": LocationData("Ridley SW Puzzle", 54),
    "Ridley West Pillar": LocationData("Ridley Left Shaft", 55),
    "Ridley Behind Unknown Statue": LocationData("Ridley Room", 56),
    "Ridley Unknown Item Statue": LocationData("Ridley Room", 57),
    "Ridley Fake Floor": LocationData("Ridley Left Shaft", 58),
    "Ridley Upper Ball Cannon Puzzle": LocationData("Central Ridley", 59),
    "Ridley Lower Ball Cannon Puzzle": LocationData("Central Ridley", 60),
    "Ridley Imago Super Missile": LocationData("Ridley Main", 61),
    "Ridley After Sidehopper Hall Upper": LocationData("Central Ridley", 62),
    "Ridley After Sidehopper Hall Lower": LocationData("Central Ridley", 63),
    "Ridley Long Hall": LocationData("Ridley Right Shaft", 64),
    "Ridley Center Pillar": LocationData("Central Ridley", 65),
    "Ridley Ball Room Lower": LocationData("Central Ridley", 66),
    "Ridley Ball Room Upper": LocationData("Central Ridley", 67),
    "Ridley Fake Lava Under Floor": LocationData("Ridley Right Shaft", 68),
    "Ridley Under Owls": LocationData("Central Ridley", 69),
    "Ridley Northeast Corner": LocationData("Ridley Right Shaft", 70),
    "Ridley Bomb Puzzle": LocationData("Ridley Speed Puzzles", 71),
    "Ridley Speed Jump": LocationData("Ridley Speed Puzzles", 72),
    "Ridley": LocationData("Ridley Room", None)
}

tourian_location_table = {
    "Tourian Left of Mother Brain": LocationData("Tourian", 73),
    "Tourian Under Mother Brain": LocationData("Tourian", 74),
    "Mother Brain": LocationData("Tourian", None)
}

crateria_location_table = {
    "Crateria Landing Site Ballspark": LocationData("Lower Crateria", 75),
    "Crateria Power Grip": LocationData("Crateria Power Grip", 76),
    "Crateria Moat": LocationData("Lower Crateria", 77),
    "Crateria Statue Water": LocationData("Lower Crateria", 78),
    "Crateria Unknown Item Statue": LocationData("Lower Crateria", 79),
    "Crateria East Ballspark": LocationData("Upper Right Crateria", 80),
    "Crateria Northeast Corner": LocationData("Upper Right Crateria", 81)
}

chozodia_location_table = {
    "Chozodia Upper Crateria Door": LocationData("Chozodia Ruins", 82),
    "Chozodia Bomb Maze": LocationData("Chozodia Under Tube", 83),
    "Chozodia Zoomer Maze": LocationData("Chozodia Under Tube", 84),
    "Chozodia Ruins East of Upper Crateria Door": LocationData("Chozodia Ruins", 85),
    "Chozodia Chozo Ghost Area Morph Tunnel Above Water": LocationData("Chozodia Ruins Test Area", 86),
    "Chozodia Chozo Ghost Area Underwater": LocationData("Chozodia Ruins Test Area", 87),
    "Chozodia Triple Crawling Pirates": LocationData("Chozodia Ruins", 88),
    "Chozodia Left of Glass Tube": LocationData("Chozodia Under Tube", 89),
    "Chozodia Lava Dive": LocationData("Chozodia Ruins Test Area", 90),
    "Chozodia Original Power Bomb": LocationData("Chozodia Original Power Bomb Room", 91),
    "Chozodia Next to Original Power Bomb": LocationData("Chozodia Original Power Bomb Room", 92),
    "Chozodia Right of Glass Tube": LocationData("Chozodia Under Tube", 93),
    "Chozodia Chozo Ghost Area Long Shinespark": LocationData("Chozodia Ruins Test Area", 94),
    "Chozodia Pirate Pitfall Trap": LocationData("Chozodia Mothership Upper", 95),
    "Chozodia Behind Workbot": LocationData("Chozodia Mothership Upper", 96),
    "Chozodia Ceiling Near Map Station": LocationData("Chozodia Mothership Lower", 97),
    "Chozodia Under Mecha Ridley Hallway": LocationData("Chozodia Mecha Ridley Hallway", 98),
    "Chozodia Southeast Corner in Hull": LocationData("Chozodia Mothership Lower", 99),
    "Chozodia Ruins Test Reward": LocationData("Chozodia Ruins Test Area", 100, force_sound=0x4A),
    "Chozo Ghost": LocationData("Chozodia Ruins Test Area", None),
    "Mecha Ridley": LocationData("Chozodia Mecha Ridley Hallway", None),
    "Chozodia Space Pirate's Ship": LocationData("Chozodia Mecha Ridley Hallway", None)
}

full_location_table = {
    **brinstar_location_table,
    **kraid_location_table,
    **norfair_location_table,
    **ridley_location_table,
    **tourian_location_table,
    **crateria_location_table,
    **chozodia_location_table
}

location_count = sum(loc.id is not None for loc in full_location_table.values())

mzm_location_name_groups = {
    "Brinstar": {name for name, loc in brinstar_location_table.items() if loc.id is not None},
    "Kraid": {name for name, loc in kraid_location_table.items() if loc.id is not None},
    "Upper Norfair": {
        "Norfair Hallway to Crateria",
        "Norfair Under Crateria Elevator",
        "Norfair Bomb Trap",
        "Norfair Heated Room Under Brinstar Elevator",
        "Norfair Ice Beam",
        "Norfair Heated Room Above Ice Beam",
        "Norfair Hi-Jump",
        "Norfair Big Room",
        "Norfair Behind Top Chozo Statue",
        "Norfair Right Shaft Near Hi-Jump",
    },
    "Lower Norfair": {
        "Norfair Lava Dive Left",
        "Norfair Lava Dive Right",
        "Norfair Screw Attack",
        "Norfair Next to Screw Attack",
        "Norfair Wave Beam",
        "Norfair Heated Room Below Wave - Right",
        "Norfair Heated Room Below Wave - Left",
        "Norfair Behind Lower Super Missile Door - Right",
        "Norfair Behind Lower Super Missile Door - Left",
        "Norfair Larva Ceiling",
        "Norfair Right Shaft Bottom",
    },
    "Ridley": {name for name, loc in ridley_location_table.items() if loc.id is not None},
    "Tourian": {name for name, loc in tourian_location_table.items() if loc.id is not None},
    "Crateria": {name for name, loc in crateria_location_table.items() if loc.id is not None},
    "Chozo Ruins": {
        "Chozodia Upper Crateria Door",
        "Chozodia Ruins East of Upper Crateria Door",
        "Chozodia Chozo Ghost Area Morph Tunnel Above Water",
        "Chozodia Chozo Ghost Area Underwater",
        "Chozodia Triple Crawling Pirates",
        "Chozodia Lava Dive",
    },
    "Mother Ship": {
        "Chozodia Bomb Maze",
        "Chozodia Zoomer Maze",
        "Chozodia Left of Glass Tube",
        "Chozodia Original Power Bomb",
        "Chozodia Next to Original Power Bomb",
        "Chozodia Right of Glass Tube",
        "Chozodia Chozo Ghost Area Long Shinespark",
        "Chozodia Pirate Pitfall Trap",
        "Chozodia Behind Workbot",
        "Chozodia Ceiling Near Map Station",
        "Chozodia Under Mecha Ridley Hallway",
        "Chozodia Southeast Corner in Hull",
    },
    "Chozo Statues": {
        "Brinstar Long Beam",
        "Brinstar Varia Suit",
        "Brinstar Bomb",
        "Kraid Unknown Item Statue",
        "Kraid Speed Booster",
        "Norfair Screw Attack",
        "Norfair Wave Beam",
        "Norfair Ice Beam",
        "Norfair Hi-Jump",
        "Ridley Unknown Item Statue",
        "Crateria Unknown Item Statue",
    },
    "Freestanding Items": {
        "Brinstar Morph Ball",
        "Brinstar Worm Drop",
        "Crateria Power Grip",
    },
    "Energy Tanks": {
        "Brinstar Ceiling E-Tank",
        "Brinstar Post-Hive Pillar",
        "Brinstar Acid Near Varia",
        "Kraid Zipline Activator Room",
        "Kraid Speed Jump",
        "Norfair Larva Ceiling",
        "Ridley Behind Unknown Statue",
        "Ridley Fake Floor",
        "Ridley Under Owls",
        "Chozodia Left of Glass Tube",
        "Chozodia Chozo Ghost Area Long Shinespark",
        "Chozodia Under Mecha Ridley Hallway",
    },
    "Shinespark Puzzles": {
        "Brinstar Ballspark",
        "Kraid Acid Ballspark",
        "Ridley Bomb Puzzle",
        "Ridley Speed Jump",
        "Tourian Left of Mother Brain",  # Can be done with a spaceboost, but that's also a bit tough
        "Crateria Landing Site Ballspark",
        "Crateria East Ballspark",
        "Crateria Northeast Corner",
        "Chozodia Chozo Ghost Area Long Shinespark",
    },
}
