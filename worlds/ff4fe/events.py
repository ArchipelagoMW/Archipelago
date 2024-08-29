from .locations import LocationData

boss_event_data = [
     ("Overworld", "MistCave", "D. Mist Slot"),
     ("Overworld", "Kaipo", "Officer Slot"),
     ("Overworld", "WateryPass", "Octomamm Slot"),
     ("Overworld", "AntlionCave", "Antlion Slot"),
     ("Overworld", "MountHobs", "Mombomb Slot"),
     ("Overworld", "Fabul", "Fabul Gauntlet Slot"),
     ("Overworld", "MountOrdeals", "Milon Slot"),
     ("Overworld", "MountOrdeals", "Milonz Slot"),
     ("Overworld", "MountOrdeals", "Mirror Cecil Slot"),
     ("Overworld", "BaronWeaponShop", "Karate Slot"),
     ("Overworld", "BaronWeaponShop", "Guard Slot"),
     ("Overworld", "Sewer", "Baigan Slot"),
     ("Overworld", "BaronCastle", "Kainazzo Slot"),
     ("Overworld", "CaveMagnes", "Darkelf Slot"),
     ("Overworld", "Zot", "Magus Slot"),
     ("Overworld", "Zot", "Valvalis Slot"),
     ("Underworld", "DwarfCastle", "Calbrena Slot"),
     ("Underworld", "DwarfCastle", "Golbez Slot"),
     ("Overworld", "LowerBabil", "Lugae Slot"),
     ("Overworld", "LowerBabil", "Dark Imp Slot"),
     ("Underworld", "UpperBabil", "King and Queen Slot"),
     ("Underworld", "UpperBabil", "Rubicant Slot"),
     ("Underworld", "SealedCave", "Evilwall Slot"),
     ("Underworld", "Feymarch", "Asura Slot"),
     ("Underworld", "Feymarch", "Leviatan Slot"),
     ("Overworld", "BaronCastle", "Odin Slot"),
     ("Moon", "BahamutCave", "Bahamut Slot"),
     ("Moon", "Giant", "Elements Slot"),
     ("Moon", "Giant", "CPU Slot"),
     ("Moon", "LunarCore", "Pale Dim Slot"),
     ("Moon", "LunarCore", "Wyvern Slot"),
     ("Moon", "LunarCore", "Plague Slot"),
     ("Moon", "LunarCore", "D. Lunar Slot"),
     ("Moon", "LunarCore", "Ogopogo Slot"),
     ("Moon", "LunarCore", "Zeromus")
]

boss_events = []

boss_slot_names = [boss[2] for boss in boss_event_data]

for event in boss_event_data:
    boss_events.append(LocationData(event[2], event[0], event[1], 0xFFFF, True))
