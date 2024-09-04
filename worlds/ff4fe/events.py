from .locations import LocationData
boss_names = {
     'D. Mist': 'D. Mist',
     'Officer': 'Officer',
     'Octomamm': 'Octomamm',
     'Antlion': 'Antlion',
     'MomBomb': 'MomBomb',
     'Fabul Gauntlet': 'Fabul Gauntlet',
     'Milon': 'Milon',
     'Milon Z.': 'Milon Z.',
     'Mirror Cecil': 'Mirror Cecil',
     'Guards': 'Guards',
     'Karate': 'Karate',
     'Baigan': 'Baigan',
     'Kainazzo': 'Kainazzo',
     'Dark Elf': 'Dark Elf',
     'Magus Sisters': 'Magus Sisters',
     'Valvalis': 'Valvalis',
     'Calbrena': 'Calbrena',
     'Golbez': 'Golbez',
     'Lugae': 'Lugae',
     'Dark Imps': 'Dark Imps',
     'King and Queen': 'King and Queen',
     'Rubicant': 'Rubicant',
     'EvilWall': 'EvilWall',
     'Asura': 'Asura',
     'Leviatan': 'Leviatan',
     'Odin': 'Odin',
     'Bahamut': 'Bahamut',
     'Elements': 'Elements',
     'CPU': 'CPU',
     'Pale Dim': 'Pale Dim',
     'Wyvern': 'Wyvern',
     'Plague': 'Plague',
     'D. Lunars': 'D. Lunars',
     'Ogopogo': 'Ogopogo',
}

boss_event_data = [
     ("Overworld", "MistCave", "D. Mist Slot"),
     ("Overworld", "Kaipo", "Officer Slot"),
     ("Overworld", "WateryPass", "Octomamm Slot"),
     ("Overworld", "AntlionCave", "Antlion Slot"),
     ("Overworld", "MountHobs", "MomBomb Slot"),
     ("Overworld", "Fabul", "Fabul Gauntlet Slot"),
     ("Overworld", "MountOrdeals", "Milon Slot"),
     ("Overworld", "MountOrdeals", "Milon Z. Slot"),
     ("Overworld", "MountOrdeals", "Mirror Cecil Slot"),
     ("Overworld", "BaronWeaponShop", "Karate Slot"),
     ("Overworld", "BaronWeaponShop", "Guards Slot"),
     ("Overworld", "Sewer", "Baigan Slot"),
     ("Overworld", "BaronCastle", "Kainazzo Slot"),
     ("Overworld", "CaveMagnes", "Dark Elf Slot"),
     ("Overworld", "Zot", "Magus Sisters Slot"),
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
     ("Moon", "LunarCore", "D. Lunars Slot"),
     ("Moon", "LunarCore", "Ogopogo Slot"),
     ("Moon", "LunarCore", "Zeromus")
]

boss_events = []
boss_status_events = {k: (f"{boss} Defeated") for k, boss in boss_names.items()}
boss_slots = [(f"{boss} Slot Defeated") for k, boss in boss_names.items()]

boss_slot_keys = [boss for boss in boss_names.keys()]

for event in boss_event_data:
    boss_events.append(LocationData(event[2], event[0], event[1], 0xFFFF, True))
