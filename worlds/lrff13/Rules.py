from typing import Callable, Dict, List, Tuple
from BaseClasses import CollectionState, Item
from .RuleLogic import state_has_at_least, item_is_category, state_has_category

rule_data_list: List[Callable[[CollectionState, int], bool]] = [
    lambda state, player:
    True,  # Rule 0
    lambda state, player:
    state.has("Pilgrim's Crux", player),  # Rule 1
    lambda state, player:
    state.has("MQ4", player, 2),  # Rule 2
    lambda state, player:
    state.has("MQ4", player, 3),  # Rule 3
    lambda state, player:
    state.has("Tablet", player, 3),  # Rule 4
    lambda state, player:
    state.has("Tablet", player, 2),  # Rule 5
    lambda state, player:
    state.has("Arithmometer", player),  # Rule 6
    lambda state, player:
    state.has("Loupe", player),  # Rule 7
    lambda state, player:
    state.has("MQ4", player),  # Rule 8
    lambda state, player:
    (state.has("Monster Flesh", player) and
     state.has("MQ4", player, 3)),  # Rule 9
    lambda state, player:
    (state.has("Tablet", player) and
     state.has("MQ4", player, 4) and
     state.has("MQDone", player)),  # Rule 10
    lambda state, player:
    (state.has("Tablet", player, 3) and
     state.has("Crux Base", player) and
     state.has("Crux Tip", player) and
     state.has("Crux Body", player)),  # Rule 11
    lambda state, player:
    state.has("Supply Sphere Password", player),  # Rule 12
    lambda state, player:
    state.has("MQ1", player, 3),  # Rule 13
    lambda state, player:
    state.has("MQ1", player, 4),  # Rule 14
    lambda state, player:
    state.has("MQ1", player, 2),  # Rule 15
    lambda state, player:
    state.has("MQ1", player, 5),  # Rule 16
    lambda state, player:
    state.has("Day", player, 2),  # Rule 17
    lambda state, player:
    (state.has("Thunderclap Cap", player) and
     state.has("Shaolong Gui Shell", player) and
     state.has("Mandragora Root", player)),  # Rule 18
    lambda state, player:
    (state.has("Green Carbuncle Doll", player) and
     state.has("Red Carbuncle Doll", player)),  # Rule 19
    lambda state, player:
    (state.has("Spectral Elixir", player) and
     state.has("MQ1", player, 2)),  # Rule 20
    lambda state, player:
    (state.has("Supply Sphere Password", player) and
     state.has("MQ1", player, 2)),  # Rule 21
    lambda state, player:
    (state.has("Cursed Dragon Claw", player) and
     state.has("MQ1", player, 2)),  # Rule 22
    lambda state, player:
    (state.has("MQ1", player, 2) and
     state.has("Seedhunter Membership Card", player)),  # Rule 23
    lambda state, player:
    (state.has("Rubber Ball", player) and
     state.has("MQ1", player, 5)),  # Rule 24
    lambda state, player:
    state.has("Rubber Ball", player),  # Rule 25
    lambda state, player:
    state.has("Q_Saint", player),  # Rule 26
    lambda state, player:
    (state.has("Quill Pen", player) and
     state.has("MQ1", player, 4)),  # Rule 27
    lambda state, player:
    (state.has("Phantom Rose", player) and
     state.has("MQ1", player, 5)),  # Rule 28
    lambda state, player:
    (state.has("Q_BuriedPassion", player) and
     state.has("MQ1", player, 5)),  # Rule 29
    lambda state, player:
    state.has("MQ3", player, 3),  # Rule 30
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("MQ3", player)),  # Rule 31
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Q_RightStuff", player) and
     state.has("MQ3", player)),  # Rule 32
    lambda state, player:
    (state.has("MQ3", player, 2) and
     state.has("Q_FuzzySearch", player)),  # Rule 33
    lambda state, player:
    state.has("MQ3", player, 2),  # Rule 34
    lambda state, player:
    (state.has("Data Recorder", player) and
     state.has("MQ3", player, 3)),  # Rule 35
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Q_Father", player) and
     state.has("MQ3", player)),  # Rule 36
    lambda state, player:
    state.has("Q_OldMan", player),  # Rule 37
    lambda state, player:
    (state.has("Aryas Apple", player, 2) and
     state.has("MQ3", player, 2)),  # Rule 38
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Fragment of Mischief", player) and
     state.has("Fragment of Radiance", player) and
     state.has("Fragment of Smiles", player) and
     state.has("Fragment of Courage", player) and
     state.has("Fragment of Kindness", player)),  # Rule 39
    lambda state, player:
    state.has("Q_RoundUp", player),  # Rule 40
    lambda state, player:
    state.has("Q_Peace", player),  # Rule 41
    lambda state, player:
    state.has("Q_Cure", player),  # Rule 42
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Goddess Glyphs", player) and
     state.has("Chaos Glyphs", player) and
     state.has("Plate Metal Fragment", player) and
     state.has("Silvered Metal Fragment", player) and
     state.has("Golden Metal Fragment", player) and
     state.has("MQ3", player, 3)),  # Rule 43
    lambda state, player:
    state.has("MQ3", player, 4),  # Rule 44
    lambda state, player:
    (state.has("Q_DDA", player) and
     state.has("Q_RoundUp", player)),  # Rule 45
    lambda state, player:
    state.has("Q_DDA", player),  # Rule 46
    lambda state, player:
    (state.has("Goddess Glyphs", player) and
     state.has("Chaos Glyphs", player) and
     state.has("MQ3", player, 3)),  # Rule 47
    lambda state, player:
    state.has("MQ2", player, 2),  # Rule 48
    lambda state, player:
    state.has("MQ2", player),  # Rule 49
    lambda state, player:
    state.has("Musical Treasure Sphere Key", player),  # Rule 50
    lambda state, player:
    state.has("MQ2", player, 3),  # Rule 51
    lambda state, player:
    state.has("MQ5", player),  # Rule 52
    lambda state, player:
    state.has("MQ2", player, 4),  # Rule 53
    lambda state, player:
    (state.has("MQ2", player, 2) and
     state.has("Midnight Mauve", player)),  # Rule 54
    lambda state, player:
    state.has("Music Satchel", player),  # Rule 55
    lambda state, player:
    state.has("Father's Letter", player),  # Rule 56
    lambda state, player:
    state.has("MQDone", player),  # Rule 57
    lambda state, player:
    (state.has("Civet Musk", player) and
     state.has("Gordon Gourmet's Recipe", player) and
     state.has("Steak a la Civet", player)),  # Rule 58
    lambda state, player:
    (state.has("Nostalgic Score: Chorus", player) and
     state.has("Nostalgic Score: Refrain", player) and
     state.has("Nostalgic Score: Coda", player)),  # Rule 59
    lambda state, player:
    (state.has("MQ2", player, 2) and
     state_has_category(state, player, "Adornment", 55)),  # Rule 60
    lambda state, player:
    (state.has("MQ2", player, 4) and
     state.has("Q_Adorn", player)),  # Rule 61
    lambda state, player:
    (state.has("MQ2", player, 2) and
     state.has("Q_Death", player)),  # Rule 62
    lambda state, player:
    state.has("Civet Musk", player),  # Rule 63
    lambda state, player:
    (state.has("Civet Musk", player) and
     state.has("Gordon Gourmet's Recipe", player)),  # Rule 64
    lambda state, player:
    state.has("Day", player),  # Rule 65
    lambda state, player:
    state.has("Day", player, 3),  # Rule 66
    lambda state, player:
    state.has("Day", player, 4),  # Rule 67
    lambda state, player:
    state.has("Day", player, 5),  # Rule 68
    lambda state, player:
    state.has("Day", player, 6),  # Rule 69
    lambda state, player:
    (state.has("MQDone", player) and
     state.has("Day", player, 6)),  # Rule 70
    lambda state, player:
    (state.has("MQDone", player, 2) and
     state.has("Day", player, 6)),  # Rule 71
    lambda state, player:
    (state.has("MQDone", player, 3) and
     state.has("Day", player, 6)),  # Rule 72
    lambda state, player:
    (state.has("MQDone", player, 4) and
     state.has("Day", player, 6)),  # Rule 73
    lambda state, player:
    (state.has("MQDone", player, 5) and
     state.has("Day", player, 6)),  # Rule 74
    lambda state, player:
    (state.has("MQDone", player, 5) and
     state.has("Day", player, 6) and
     state.has("MQ1", player, 5) and
     state.has("MQ2", player, 4) and
     state.has("MQ3", player, 4) and
     state.has("MQ4", player, 6) and
     state.has("MQ5", player, 2)),  # Rule 75
    lambda state, player:
    (state.has("C_Miracle", player) and
     state.has("C_Banned", player)),  # Rule 76
    lambda state, player:
    (state.has("C_Child", player) and
     state.has("C_Security", player)),  # Rule 77
    lambda state, player:
    state.has("C_Ranks", player),  # Rule 78
    lambda state, player:
    (state.has("C_Flower", player) and
     state.has("C_Bio", player)),  # Rule 79
    lambda state, player:
    (state.has("Tablet", player, 3) and
     state.has("MQ4", player, 6)),  # Rule 80
    lambda state, player:
    state.has("C_Charm", player),  # Rule 81
    lambda state, player:
    state.has("Q_Food", player),  # Rule 82
    lambda state, player:
    (state.has("Day", player, 6) and
     state.has("MQDone", player) and
     state.has("C_Pride", player)),  # Rule 83
    lambda state, player:
    (state.has("Day", player, 6) and
     state.has("MQDone", player, 3) and
     state.has("C_Pride", player, 2)),  # Rule 84
    lambda state, player:
    state.has("MQ1", player),  # Rule 85
    lambda state, player:
    (state.has("C_Song", player) and
     state.has("C_Grave", player)),  # Rule 86
    lambda state, player:
    (state.has("C_Inventive", player) and
     state.has("C_Puppet", player)),  # Rule 87
    lambda state, player:
    (state.has("C_Slay", player) and
     state.has("C_Teeth", player)),  # Rule 88
    lambda state, player:
    (state.has("C_Revenge", player) and
     state.has("C_Gratitude", player)),  # Rule 89
    lambda state, player:
    (state.has("Proof of Legendary Title", player) and
     state.has("Day", player, 3)),  # Rule 90
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Day", player, 3)),  # Rule 91
    lambda state, player:
    state.has("Q_Hunter", player),  # Rule 92
    lambda state, player:
    state.has("Q_Forebears", player),  # Rule 93
    lambda state, player:
    (state.has("C_Drum", player) and
     state.has("C_Below", player)),  # Rule 94
    lambda state, player:
    (state.has("Day", player, 6) and
     state.has("MQDone", player)),  # Rule 95
    lambda state, player:
    (state.has("C_Forget", player) and
     state.has("C_Thanks", player)),  # Rule 96
    lambda state, player:
    (state.has("C_Fresh", player) and
     state.has("C_Plea", player) and
     state.has("C_Gatekeeper", player)),  # Rule 97
    lambda state, player:
    (state.has("C_Future", player) and
     state.has("C_Brain", player)),  # Rule 98
    lambda state, player:
    state.has("Gysahl Greens", player),  # Rule 99
    lambda state, player:
    state.has("C_Chow", player),  # Rule 100
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Day", player)),  # Rule 101
    lambda state, player:
    (state.has("C_Sun", player) and
     state.has("C_Moon", player)),  # Rule 102
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Q_Peace", player)),  # Rule 103
    lambda state, player:
    (state.has("C_Soulful", player) and
     state.has("C_Inspiration", player)),  # Rule 104
    lambda state, player:
    (state.has("C_Youth", player) and
     state.has("C_Colors", player)),  # Rule 105
    lambda state, player:
    (state.has("C_Secret", player) and
     state.has("C_Dangerous", player) and
     state.has("C_Spell", player)),  # Rule 106
    lambda state, player:
    (state.has("Jade Hair Comb", player) and
     state.has("Bronze Pocket Watch", player) and
     state.has("MQ2", player)),  # Rule 107
    lambda state, player:
    (state.has("Chocobo Girl's Phone No.", player) and
     state.has("Q_Actress", player)),  # Rule 108
    lambda state, player:
    (state.has("Beloved's Gift", player) and
     state.has("MQ5", player)),  # Rule 109
    lambda state, player:
    state.has("MQDone", player, 4),  # Rule 110
    lambda state, player:
    (state.has("Key to the Sand Gate", player) and
     state.has("Key to the Green Gate", player) and
     state.has("MQDone", player, 4)),  # Rule 111
    lambda state, player:
    (state.has("Bandit's Bloodseal", player) and
     state.has("Oath of the Merchants Guild", player) and
     state.has("MQDone", player, 4)),  # Rule 112
    lambda state, player:
    (state.has("Proof of Courage", player) and
     state.has("MQ1", player, 5)),  # Rule 113
    lambda state, player:
    (state.has("Violet Amulet", player) and
     state.has("MQ1", player, 5)),  # Rule 114
    lambda state, player:
    (state.has("Lapis Lazuli", player) and
     state.has("MQ2", player, 2)),  # Rule 115
    lambda state, player:
    (state.has("Power Booster", player) and
     state.has("Q_Death", player)),  # Rule 116
    lambda state, player:
    (state.has("Moogle Dust", player) and
     state.has("MQ3", player, 2)),  # Rule 117
    lambda state, player:
    (state.has("Old-Fashioned Photo Frame", player) and
     state.has("MQ3", player, 2)),  # Rule 118
    lambda state, player:
    (state.has("Etro's Forbidden Tome", player) and
     state.has("MQ3", player, 4)),  # Rule 119
    lambda state, player:
    (state.has("Broken Gyroscope", player) and
     state.has("Day", player, 2)),  # Rule 120
    lambda state, player:
    (state.has("Golden Scarab", player) and
     state.has("MQ4", player, 3)),  # Rule 121
    lambda state, player:
    state.has("Seedhunter Membership Card", player),  # Rule 122
    lambda state, player:
    (state.has("Seedhunter Membership Card", player) and
     state.has("Moogle Fragment", player)),  # Rule 123
    lambda state, player:
    state.has("MQDone", player, 3),  # Rule 124
    lambda state, player:
    state.has("MQDone", player, 2),  # Rule 125
    lambda state, player:
    (state.has("MQ4", player, 5) and
     state.has("Crux Base", player) and
     state.has("Crux Tip", player) and
     state.has("Crux Body", player)),  # Rule 126
    lambda state, player:
    (state.has("MQ1", player, 4) and
     state.has("Day", player, 2)),  # Rule 127
    lambda state, player:
    (state.has("MQ3", player, 3) and
     state.has("Day", player, 3)),  # Rule 128
    lambda state, player:
    (state.has("MQ2", player, 3) and
     state.has("Serah's Pendant", player) and
     state.has("Day", player, 3)),  # Rule 129
    lambda state, player:
    (state.has("MQ3", player, 3) and
     state.has("Fragment of Mischief", player) and
     state.has("Fragment of Radiance", player) and
     state.has("Fragment of Smiles", player) and
     state.has("Fragment of Courage", player) and
     state.has("Fragment of Kindness", player) and
     state.has("Day", player, 3)),  # Rule 130
    lambda state, player:
    state.has("Sneaking-In Special Ticket", player),  # Rule 131
    lambda state, player:
    (state.has("MQ2", player) and
     state.has("ID Card", player)),  # Rule 132
    lambda state, player:
    (state.has("MQ3", player) and
     state.has("Gysahl Greens", player)),  # Rule 133
    lambda state, player:
    (state.has("MQ4", player, 3) and
     state.has("Tablet", player)),  # Rule 134
    lambda state, player:
    (state.has("MQ4", player, 4) and
     state.has("Tablet", player, 3)),  # Rule 135
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("MQ3", player, 3)),  # Rule 136
    lambda state, player:
    state.has("MQDone", player, 5),  # Rule 137
    lambda state, player:
    (state.has("Sneaking-In Special Ticket", player) and
     state.has("ID Card", player) and
     state.has("MQ2", player, 2)),  # Rule 138
    lambda state, player:
    (state.has("Sneaking-In Special Ticket", player) and
     state.has("ID Card", player) and
     state.has("Midnight Mauve", player) and
     state.has("MQ2", player, 3)),  # Rule 139
    lambda state, player:
    (state.has("Sneaking-In Special Ticket", player) and
     state.has("ID Card", player) and
     state.has("Midnight Mauve", player) and
     state.has("Serah's Pendant", player) and
     state.has("MQ2", player, 4)),  # Rule 140
    lambda state, player:
    state.has("MQ3", player),  # Rule 141
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("MQ3", player, 2)),  # Rule 142
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("MQ3", player, 4)),  # Rule 143
    lambda state, player:
    (state.has("Tablet", player, 3) and
     state.has("MQ4", player, 5)),  # Rule 144
    lambda state, player:
    (state.has("Tablet", player, 3) and
     state.has("Crux Base", player) and
     state.has("Crux Tip", player) and
     state.has("Crux Body", player) and
     state.has("MQ4", player, 6)),  # Rule 145
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("Fragment of Mischief", player) and
     state.has("Fragment of Radiance", player) and
     state.has("Fragment of Smiles", player) and
     state.has("Fragment of Courage", player) and
     state.has("Fragment of Kindness", player) and
     state.has("MQ5", player)),  # Rule 146
    lambda state, player:
    (state.has("Gysahl Greens", player) and
     state.has("MQ5", player)),  # Rule 147
    lambda state, player:
    (state.has("Beloved's Gift", player) and
     state.has("Gysahl Greens", player) and
     state.has("MQ5", player)),  # Rule 148
    lambda state, player:
    (state.has("Moogle Fragment", player) and
     state.has("Gysahl Greens", player) and
     state.has("Seedhunter Membership Card", player) and
     state.has("MQ5", player)),  # Rule 149
]

location_rule_data_table: Dict[str, Callable[[CollectionState, int], bool]] = {
    "Dead Dunes - Golden Scarab Treasure": rule_data_list[0],
    "Dead Dunes - Oasis Lighthouse Treasure (1)": rule_data_list[1],
    "Dead Dunes - Grave of the Colossi Shrine Treasure": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Treasure (1)": rule_data_list[0],
    "Dead Dunes - Golden Chamber Lower Treasure": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Treasure (2)": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Treasure (3)": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Treasure (4)": rule_data_list[0],
    "Dead Dunes - Ruffian Outdoor Treasure": rule_data_list[0],
    "Dead Dunes - Dry Floodlands Treasure (1)": rule_data_list[0],
    "Dead Dunes - Oasis Lighthouse Treasure (2)": rule_data_list[1],
    "Dead Dunes - Oasis Lighthouse Treasure (3)": rule_data_list[1],
    "Dead Dunes - Atomos's Sand Treasure (1)": rule_data_list[0],
    "Dead Dunes - Grave of the Colossi Treasure (1)": rule_data_list[0],
    "Dead Dunes - Grave of the Colossi Treasure (2)": rule_data_list[1],
    "Dead Dunes - Grave of the Colossi Treasure (3)": rule_data_list[0],
    "Dead Dunes - Atomos's Sand Treasure (2)": rule_data_list[0],
    "Dead Dunes - Ruffian 2nd Floor Treasure": rule_data_list[0],
    "Dead Dunes - Temple Ruins Chamber of Dusk (Upper) Treasure": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Upper) Treasure (1)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Upper) Treasure (2)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Upper) Treasure (3)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Lower) Treasure (1)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Lower) Treasure (2)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Chamber of Plenilune (Lower) Treasure (3)": rule_data_list[2],
    "Dead Dunes - Temple Ruins Sacred Grove Treasure": rule_data_list[3],
    "Dead Dunes - Temple Ruins Golden Chamber (Upper) Treasure (1)": rule_data_list[3],
    "Dead Dunes - Dry Floodlands Shrine Treasure": rule_data_list[0],
    "Dead Dunes - Temple Ruins Golden Chamber (Lower) Treasure (1)": rule_data_list[3],
    "Dead Dunes - Temple Ruins Golden Chamber (Lower) Treasure (2)": rule_data_list[3],
    "Dead Dunes - Temple Ruins Golden Chamber (Lower) Treasure (3)": rule_data_list[3],
    "Dead Dunes - Temple Ruins Scorched Earth (Lower) Treasure": rule_data_list[3],
    "Dead Dunes - Temple Ruins Scorched Earth (Upper) Treasure (1)": rule_data_list[3],
    "Dead Dunes - Temple Ruins Scorched Earth (Upper) Treasure (2)": rule_data_list[3],
    "Dead Dunes - Temple Ruins Golden Chamber (Upper) Treasure (2)": rule_data_list[3],
    "Dead Dunes - Atomos's Sands Shrine Treasure": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Treasure (5)": rule_data_list[0],
    "Dead Dunes - Dry Floodlands Treasure (2)": rule_data_list[0],
    "Dead Dunes - Grave of the Colossi Shrine Tablet": rule_data_list[1],
    "Dead Dunes - Dry Floodlands Shrine Tablet": rule_data_list[1],
    "Dead Dunes - Atomos's Sands Shrine Tablet": rule_data_list[1],
    "Dead Dunes - Temple Ruins Mural Crux Base": rule_data_list[4],
    "Dead Dunes - Temple Ruins Mural Crux Body": rule_data_list[5],
    "Dead Dunes - Temple Ruins Mural Crux Tip": rule_data_list[5],
    "Dead Dunes - Temple Ruins Bhakti Reward": rule_data_list[0],
    "Dead Dunes - Grave of the Colossi Pilgrim's Crux": rule_data_list[0],
    "Dead Dunes - Temple Ruins Scorched Earth Pilgrim's Crux (1)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Golden Chamber (Lower) Pilgrim's Crux (1)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Scorched Earth Pilgrim's Crux (2)": rule_data_list[0],
    "Dead Dunes - Dry Floodlands Pilgrim's Crux": rule_data_list[0],
    "Dead Dunes - Atomos's Sands Pilgrim's Crux": rule_data_list[0],
    "Dead Dunes - Giant's Sandbox Pilgrim's Crux": rule_data_list[0],
    "Dead Dunes - Temple Ruins Sacred Grove Pilgrim's Crux (1)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Sacred Grove Pilgrim's Crux (2)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Golden Chamber (Upper) Pilgrim's Crux (1)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Sacred Grove Pilgrim's Crux (3)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Golden Chamber (Upper) Pilgrim's Crux (2)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Sacred Grove Pilgrim's Crux (4)": rule_data_list[0],
    "Dead Dunes - Temple Ruins Golden Chamber (Lower) Pilgrim's Crux (2)": rule_data_list[0],
    "Dead Dunes - Atomos's Sands Loupe": rule_data_list[0],
    "Dead Dunes - The Life of a Machine Quest (1)": rule_data_list[3],
    "Dead Dunes - The Life of a Machine Quest (2)": rule_data_list[3],
    "Dead Dunes - Old Rivals Quest (1)": rule_data_list[6],
    "Dead Dunes - Old Rivals Quest (2)": rule_data_list[6],
    "Dead Dunes - His Wife's Dream Quest (1)": rule_data_list[6],
    "Dead Dunes - His Wife's Dream Quest (2)": rule_data_list[6],
    "Dead Dunes - Tool of the Trade Quest (1)": rule_data_list[7],
    "Dead Dunes - Tool of the Trade Quest (2)": rule_data_list[7],
    "Dead Dunes - Adonis's Audition Quest (1)": rule_data_list[8],
    "Dead Dunes - Adonis's Audition Quest (2)": rule_data_list[8],
    "Dead Dunes - What Rough Beast Slouches Quest (1)": rule_data_list[9],
    "Dead Dunes - What Rough Beast Slouches Quest (2)": rule_data_list[9],
    "Dead Dunes - Skeletons In The Closet Quest (1)": rule_data_list[10],
    "Dead Dunes - Skeletons In The Closet Quest (2)": rule_data_list[10],
    "Dead Dunes - Last One Standing Quest (1)": rule_data_list[0],
    "Dead Dunes - Last One Standing Quest (2)": rule_data_list[0],
    "Dead Dunes - Last One Standing Quest (3)": rule_data_list[0],
    "Dead Dunes - What Rough Beast Slouches Libra Notes": rule_data_list[3],
    "Dead Dunes - Dead Dunes Boss Drop": rule_data_list[11],
    "Dead Dunes - Aeronite Missable Drop": rule_data_list[0],
    "Luxerion - Cathedral Proof Of Courage": rule_data_list[0],
    "Luxerion - Pilgrim's Passage Violet Amulet Treasure": rule_data_list[0],
    "Luxerion - North Station Plaza Treasure": rule_data_list[0],
    "Luxerion - The Avenue Treasure": rule_data_list[0],
    "Luxerion - Gallery Steps Treasure": rule_data_list[0],
    "Luxerion - 2nd Ave Treasure": rule_data_list[0],
    "Luxerion - Pilgrim's Passage (Grassy) Treasure": rule_data_list[0],
    "Luxerion - Old Theater Platform Treasure": rule_data_list[0],
    "Luxerion - The Warren Mangled Hill Treasure": rule_data_list[0],
    "Luxerion - South Station (Supply Sphere) Treasure": rule_data_list[12],
    "Luxerion - Warehouse District (Supply Sphere) Treasure": rule_data_list[12],
    "Luxerion - Residences (Supply Sphere) Treasure": rule_data_list[12],
    "Luxerion - Forsaken Graveyard Treasure (1)": rule_data_list[13],
    "Luxerion - Den Of Shadows Treasure (1)": rule_data_list[14],
    "Luxerion - Luxerion After 1st Phone (1)": rule_data_list[15],
    "Luxerion - Den Of Shadows Treasure (2)": rule_data_list[14],
    "Luxerion - Luxerion After 1st Phone (2)": rule_data_list[15],
    "Luxerion - Luxerion After 1st Phone (3)": rule_data_list[15],
    "Luxerion - Luxerion Marketplace Treasure": rule_data_list[0],
    "Luxerion - Forsaken Graveyard Treasure (2)": rule_data_list[13],
    "Luxerion - 1st Ave Rubber Ball": rule_data_list[16],
    "Luxerion - Marketplace Doll": rule_data_list[0],
    "Luxerion - North Station Plaza Doll": rule_data_list[0],
    "Luxerion - Warehouse District Thunderclap Cap": rule_data_list[0],
    "Luxerion - Luxerion Proof of Legendary Title": rule_data_list[17],
    "Luxerion - Luxerion Ghost Phantom Rose": rule_data_list[0],
    "Luxerion - Luxerion Marketplace Pen": rule_data_list[0],
    "Luxerion - Baird Seedhunter Membership Card": rule_data_list[0],
    "Luxerion - Virgil Supply Sphere Password": rule_data_list[15],
    "Luxerion - Buy Shaolong Gui Shell": rule_data_list[0],
    "Luxerion - Buy Mandragora Root": rule_data_list[0],
    "Luxerion - Chocobo Emporium Spectral Elixir": rule_data_list[18],
    "Luxerion - The Things She Lost Quest (1)": rule_data_list[19],
    "Luxerion - The Things She Lost Quest (2)": rule_data_list[19],
    "Luxerion - Where Are You, Holmes? Quest (1)": rule_data_list[0],
    "Luxerion - Where Are You, Holmes? Quest (2)": rule_data_list[0],
    "Luxerion - Where Are You, Holmes? Quest (3)": rule_data_list[0],
    "Luxerion - Like Clockwork Quest (1)": rule_data_list[14],
    "Luxerion - Like Clockwork Quest (2)": rule_data_list[14],
    "Luxerion - Dying Wish Quest (1)": rule_data_list[20],
    "Luxerion - Dying Wish Quest (2)": rule_data_list[20],
    "Luxerion - Suspicious Spheres Quest (1)": rule_data_list[21],
    "Luxerion - Suspicious Spheres Quest (2)": rule_data_list[21],
    "Luxerion - Born From Chaos Quest (1)": rule_data_list[22],
    "Luxerion - Born From Chaos Quest (2)": rule_data_list[22],
    "Luxerion - Born From Chaos Quest (3)": rule_data_list[22],
    "Luxerion - Born From Chaos Quest (4)": rule_data_list[22],
    "Luxerion - Soul Seeds Quest (1)": rule_data_list[23],
    "Luxerion - Soul Seeds Quest (2)": rule_data_list[23],
    "Luxerion - Faster Than Lightning Quest (1)": rule_data_list[15],
    "Luxerion - Faster Than Lightning Quest (2)": rule_data_list[15],
    "Luxerion - Treasured Ball Quest (1)": rule_data_list[24],
    "Luxerion - Treasured Ball Quest (2)": rule_data_list[24],
    "Luxerion - Talbot's Gratitude": rule_data_list[25],
    "Luxerion - The Angel's Tears Quest (1)": rule_data_list[15],
    "Luxerion - The Angel's Tears Quest (2)": rule_data_list[15],
    "Luxerion - The Saint's Stone Quest (1)": rule_data_list[16],
    "Luxerion - The Saint's Stone Quest (2)": rule_data_list[16],
    "Luxerion - The Saint's Stone Quest (3)": rule_data_list[16],
    "Luxerion - Aremiah Service Entrance Key": rule_data_list[26],
    "Luxerion - Whither Faith Quest (1)": rule_data_list[0],
    "Luxerion - Whither Faith Quest (2)": rule_data_list[0],
    "Luxerion - The Avid Reader Quest (1)": rule_data_list[16],
    "Luxerion - The Avid Reader Quest (2)": rule_data_list[16],
    "Luxerion - Buried Passion Quest (1)": rule_data_list[27],
    "Luxerion - Buried Passion Quest (2)": rule_data_list[27],
    "Luxerion - The Girl Who Cried Wolf Quest (1)": rule_data_list[16],
    "Luxerion - The Girl Who Cried Wolf Quest (2)": rule_data_list[16],
    "Luxerion - Stuck in a Gem Quest (1)": rule_data_list[0],
    "Luxerion - Stuck in a Gem Quest (2)": rule_data_list[0],
    "Luxerion - Get the Girl Quest (1)": rule_data_list[16],
    "Luxerion - Get the Girl Quest (2)": rule_data_list[16],
    "Luxerion - A Rose By Any Other Name Quest (1)": rule_data_list[28],
    "Luxerion - A Rose By Any Other Name Quest (2)": rule_data_list[28],
    "Luxerion - A Rose By Any Other Name Quest (3)": rule_data_list[28],
    "Luxerion - A Rose By Any Other Name Quest (4)": rule_data_list[28],
    "Luxerion - Voices from the Grave Quest (1)": rule_data_list[16],
    "Luxerion - Voices from the Grave Quest (2)": rule_data_list[16],
    "Luxerion - To Save the Sinless Quest (1)": rule_data_list[29],
    "Luxerion - To Save the Sinless Quest (2)": rule_data_list[29],
    "Luxerion - Replace Chronostasis": rule_data_list[0],
    "Luxerion - Luxerion Boss Drop": rule_data_list[14],
    "Luxerion - Luxerion Boss+ Only Missable Drop": rule_data_list[14],
    "Wildlands - Moogle Village Moogle Dust Treasure": rule_data_list[0],
    "Wildlands - Research Camp Photo Frame Treasure": rule_data_list[0],
    "Wildlands - Poltae Etro's Forbidden Tome": rule_data_list[0],
    "Wildlands - Eremite Plains Broken Gyroscope Treasure": rule_data_list[30],
    "Wildlands - Aryas Village Treasure (1)": rule_data_list[0],
    "Wildlands - Jagd Woods Treasure": rule_data_list[30],
    "Wildlands - The Grasslands Treasure (1)": rule_data_list[30],
    "Wildlands - Poltae Treasure (1)": rule_data_list[30],
    "Wildlands - Canopus Farms Treasure": rule_data_list[0],
    "Wildlands - Rocky Crag Treasure (1)": rule_data_list[30],
    "Wildlands - The Grasslands Treasure (2)": rule_data_list[30],
    "Wildlands - Aryas Village Treasure (2)": rule_data_list[0],
    "Wildlands - The Grasslands Treasure (3)": rule_data_list[30],
    "Wildlands - Eremite Plains Treasure (1)": rule_data_list[30],
    "Wildlands - Eremite Plains Treasure (2)": rule_data_list[30],
    "Wildlands - Moogle Village Treasure": rule_data_list[30],
    "Wildlands - City of Ruins Treasure": rule_data_list[30],
    "Wildlands - Rocky Crag Treasure (2)": rule_data_list[30],
    "Wildlands - Rocky Crag Treasure (3)": rule_data_list[30],
    "Wildlands - Aryas Village Treasure (3)": rule_data_list[30],
    "Wildlands - Poltae Treasure (2)": rule_data_list[0],
    "Wildlands - Eremite Plains Crash Site Fragment": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (1)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (2)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (3)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (4)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (5)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (6)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (7)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (8)": rule_data_list[30],
    "Wildlands - Goddess Temple Treasure (9)": rule_data_list[30],
    "Wildlands - Dr Gysahl's Gysahl Greens": rule_data_list[0],
    "Wildlands - Aryas Village Beloved's Gift Treasure": rule_data_list[0],
    "Wildlands - Sarala Vegatable Seeds": rule_data_list[31],
    "Wildlands - A Father's Request Quest (1)": rule_data_list[31],
    "Wildlands - A Father's Request Quest (2)": rule_data_list[31],
    "Wildlands - The Hunter's Challenge Quest (1)": rule_data_list[32],
    "Wildlands - The Hunter's Challenge Quest (2)": rule_data_list[32],
    "Wildlands - The Hunter's Challenge Quest (3)": rule_data_list[32],
    "Wildlands - A Final Cure Quest (1)": rule_data_list[31],
    "Wildlands - A Final Cure Quest (2)": rule_data_list[31],
    "Wildlands - A Final Cure Quest (3)": rule_data_list[31],
    "Wildlands - Fuzzy Search Quest (1)": rule_data_list[0],
    "Wildlands - Fuzzy Search Quest (2)": rule_data_list[0],
    "Wildlands - Fuzzy Search Quest (3)": rule_data_list[0],
    "Wildlands - Round 'em Up Quest (1)": rule_data_list[33],
    "Wildlands - Round 'em Up Quest (2)": rule_data_list[33],
    "Wildlands - Chocobo Cheer Quest (1)": rule_data_list[34],
    "Wildlands - Chocobo Cheer Quest (2)": rule_data_list[34],
    "Wildlands - Chocobo Cheer Quest (3)": rule_data_list[34],
    "Wildlands - Peace and Quiet, Kupo Quest (1)": rule_data_list[0],
    "Wildlands - Peace and Quiet, Kupo Quest (2)": rule_data_list[0],
    "Wildlands - Peace and Quiet, Kupo Quest (3)": rule_data_list[0],
    "Wildlands - Saving an Angel Quest (1)": rule_data_list[31],
    "Wildlands - Saving an Angel Quest (2)": rule_data_list[31],
    "Wildlands - Omega Point Quest (1)": rule_data_list[35],
    "Wildlands - Omega Point Quest (2)": rule_data_list[35],
    "Wildlands - The Old Man and the Field Quest (1)": rule_data_list[36],
    "Wildlands - The Old Man and the Field Quest (2)": rule_data_list[36],
    "Wildlands - Land of our Forebears Quest (1)": rule_data_list[37],
    "Wildlands - Land of our Forebears Quest (2)": rule_data_list[37],
    "Wildlands - A Taste of the Past Quest (1)": rule_data_list[38],
    "Wildlands - A Taste of the Past Quest (2)": rule_data_list[38],
    "Wildlands - A Taste of the Past Quest (3)": rule_data_list[38],
    "Wildlands - Dog, Doctor and Assistant Quest (1)": rule_data_list[34],
    "Wildlands - Dog, Doctor and Assistant Quest (2)": rule_data_list[34],
    "Wildlands - Main Quest 5 (1)": rule_data_list[39],
    "Wildlands - Main Quest 5 (2)": rule_data_list[39],
    "Wildlands - Main Quest 5 (3)": rule_data_list[39],
    "Wildlands - The Right Stuff Quest (1)": rule_data_list[31],
    "Wildlands - The Right Stuff Quest (2)": rule_data_list[31],
    "Wildlands - The Secret Lives of Sheep Quest (1)": rule_data_list[40],
    "Wildlands - The Secret Lives of Sheep Quest (2)": rule_data_list[40],
    "Wildlands - Where Are You, Moogle? Quest (1)": rule_data_list[41],
    "Wildlands - Where Are You, Moogle? Quest (2)": rule_data_list[41],
    "Wildlands - Where Are You, Moogle? Quest (3)": rule_data_list[41],
    "Wildlands - Mercy of a Goddess Quest (1)": rule_data_list[42],
    "Wildlands - Mercy of a Goddess Quest (2)": rule_data_list[42],
    "Wildlands - The Grail of Valhalla Quest (1)": rule_data_list[43],
    "Wildlands - The Grail of Valhalla Quest (2)": rule_data_list[43],
    "Wildlands - The Grail of Valhalla Quest (3)": rule_data_list[43],
    "Wildlands - To Live in Chaos Quest (1)": rule_data_list[44],
    "Wildlands - To Live in Chaos Quest (2)": rule_data_list[44],
    "Wildlands - To Live in Chaos Quest (3)": rule_data_list[44],
    "Wildlands - Killing Time Quest (1)": rule_data_list[30],
    "Wildlands - Killing Time Quest (2)": rule_data_list[30],
    "Wildlands - Matchmaker Quest (1)": rule_data_list[45],
    "Wildlands - Matchmaker Quest (2)": rule_data_list[45],
    "Wildlands - Mother and Daughter Quest (1)": rule_data_list[46],
    "Wildlands - Mother and Daughter Quest (2)": rule_data_list[46],
    "Wildlands - The Secret Lives of Sheep Mystery Egg": rule_data_list[40],
    "Wildlands - Goddess Temple Goddess Glyphs": rule_data_list[30],
    "Wildlands - Goddess Temple Chaos Glyphs": rule_data_list[30],
    "Wildlands - Poltae Plate Metal Fragment": rule_data_list[47],
    "Wildlands - Poltae Silvered Metal Fragment": rule_data_list[47],
    "Wildlands - Poltae Gold Metal Fragment": rule_data_list[47],
    "Wildlands - Research Camp Data Recorder": rule_data_list[30],
    "Wildlands - Aryas Village Apple (1)": rule_data_list[30],
    "Wildlands - Aryas Village Apple (2)": rule_data_list[30],
    "Wildlands - Aryas Village Apple (3)": rule_data_list[30],
    "Wildlands - Wildlands Boss Drop": rule_data_list[30],
    "Yusnaan - Reveler's Quarter Lapis Lazuli Treasure": rule_data_list[0],
    "Yusnaan - Industrial Area Power Booster": rule_data_list[48],
    "Yusnaan - Tunnel Oath of the Merchants Guild Treasure": rule_data_list[0],
    "Yusnaan - Industrial Area Jade Hair Comb": rule_data_list[48],
    "Yusnaan - Industrial Area Bronze Pocket Watch": rule_data_list[48],
    "Yusnaan - Chocobo Girl Poster": rule_data_list[0],
    "Yusnaan - Glutton's Quarter Treasure (1)": rule_data_list[0],
    "Yusnaan - Aromatic Market Treasure": rule_data_list[0],
    "Yusnaan - Central Ave Treasure": rule_data_list[0],
    "Yusnaan - Coliseum Square Treasure": rule_data_list[0],
    "Yusnaan - Tour Guide Sneaking-In Special Ticket": rule_data_list[0],
    "Yusnaan - Warehouse District Id Card": rule_data_list[49],
    "Yusnaan - Coliseum Square (Musical) Treasure": rule_data_list[50],
    "Yusnaan - Cactuar Statue (Musical) Treasure": rule_data_list[50],
    "Yusnaan - Station (Musical) Treasure": rule_data_list[50],
    "Yusnaan - Cactuar Statue Treasure": rule_data_list[0],
    "Yusnaan - Reveler's Quarter Treasure (1)": rule_data_list[0],
    "Yusnaan - Augur's Quarter Treasure (1)": rule_data_list[48],
    "Yusnaan - Patron's Palace Treasure (1)": rule_data_list[51],
    "Yusnaan - Hawker's Row Treasure": rule_data_list[0],
    "Yusnaan - Augur's Quarter Treasure (2)": rule_data_list[48],
    "Yusnaan - Warehouse District Treasure": rule_data_list[49],
    "Yusnaan - Augur's Quarter Treasure (3)": rule_data_list[48],
    "Yusnaan - Supply Line Treasure": rule_data_list[49],
    "Yusnaan - Industrial Area Treasure": rule_data_list[49],
    "Yusnaan - Lower City Treasure": rule_data_list[0],
    "Yusnaan - Glutton's Quarter Treasure (2)": rule_data_list[0],
    "Yusnaan - Reveler's Quarter Treasure (2)": rule_data_list[0],
    "Yusnaan - Patron's Palace Treasure (2)": rule_data_list[51],
    "Yusnaan - Patron's Palace Treasure (3)": rule_data_list[51],
    "Yusnaan - Patron's Palace Treasure (4)": rule_data_list[51],
    "Yusnaan - Patron's Palace Treasure (5)": rule_data_list[51],
    "Yusnaan - Slaughterhouse Special Fragment of Courage": rule_data_list[52],
    "Yusnaan - Slaughterhouse (1)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (2)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (3)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (4)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (5)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (6)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (7)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (8)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (9)": rule_data_list[0],
    "Yusnaan - Slaughterhouse (10)": rule_data_list[0],
    "Yusnaan - The Fighting Actress Slaughterhouse (1)": rule_data_list[48],
    "Yusnaan - The Fighting Actress Slaughterhouse (2)": rule_data_list[48],
    "Yusnaan - The Fighting Actress Slaughterhouse (3)": rule_data_list[48],
    "Yusnaan - The Fighting Actress Slaughterhouse (4)": rule_data_list[48],
    "Yusnaan - Tanbam's Taboo Slaughterhouse": rule_data_list[53],
    "Yusnaan - Chocobo Girl Miqo'te Dress": rule_data_list[0],
    "Yusnaan - Director Femme Fetale": rule_data_list[54],
    "Yusnaan - Fireworks in a Bottle Quest (1)": rule_data_list[48],
    "Yusnaan - Fireworks in a Bottle Quest (2)": rule_data_list[48],
    "Yusnaan - The Fighting Actress Quest (1)": rule_data_list[48],
    "Yusnaan - The Fighting Actress Quest (2)": rule_data_list[48],
    "Yusnaan - Songless Diva Quest (1)": rule_data_list[55],
    "Yusnaan - Songless Diva Quest (2)": rule_data_list[55],
    "Yusnaan - Stolen Things Quest (1)": rule_data_list[56],
    "Yusnaan - Stolen Things Quest (2)": rule_data_list[56],
    "Yusnaan - Fireworks for a Steal Quest (1)": rule_data_list[48],
    "Yusnaan - Fireworks for a Steal Quest (2)": rule_data_list[48],
    "Yusnaan - A Testing Proposition Quest (1)": rule_data_list[0],
    "Yusnaan - A Testing Proposition Quest (2)": rule_data_list[0],
    "Yusnaan - Last Date Quest (1)": rule_data_list[53],
    "Yusnaan - Last Date Quest (2)": rule_data_list[53],
    "Yusnaan - Free Will Quest (1)": rule_data_list[57],
    "Yusnaan - Free Will Quest (2)": rule_data_list[57],
    "Yusnaan - Free Will Quest (3)": rule_data_list[57],
    "Yusnaan - Friends Forever Quest (1)": rule_data_list[53],
    "Yusnaan - Friends Forever Quest (2)": rule_data_list[53],
    "Yusnaan - Friends Forever Quest (3)": rule_data_list[53],
    "Yusnaan - Family Food Quest (1)": rule_data_list[58],
    "Yusnaan - Family Food Quest (2)": rule_data_list[58],
    "Yusnaan - Tanbam's Taboo Quest (1)": rule_data_list[53],
    "Yusnaan - Tanbam's Taboo Quest (2)": rule_data_list[53],
    "Yusnaan - Play It for Me Quest (1)": rule_data_list[59],
    "Yusnaan - Play It for Me Quest (2)": rule_data_list[59],
    "Yusnaan - Adoring Adornments Quest (1)": rule_data_list[60],
    "Yusnaan - Adoring Adornments Quest (2)": rule_data_list[60],
    "Yusnaan - Adoring Candice Quest (1)": rule_data_list[61],
    "Yusnaan - Adoring Candice Quest (2)": rule_data_list[61],
    "Yusnaan - Adoring Candice Quest (3)": rule_data_list[61],
    "Yusnaan - Death Safari Quest (1)": rule_data_list[48],
    "Yusnaan - Death Safari Quest (2)": rule_data_list[48],
    "Yusnaan - Death Safari Quest (3)": rule_data_list[48],
    "Yusnaan - Death Safari Quest (4)": rule_data_list[48],
    "Yusnaan - Death Safari Quest (5)": rule_data_list[48],
    "Yusnaan - Death Game Quest (1)": rule_data_list[62],
    "Yusnaan - Death Game Quest (2)": rule_data_list[62],
    "Yusnaan - Death Game Quest (3)": rule_data_list[62],
    "Yusnaan - Morris Musical Treasure Sphere Key": rule_data_list[0],
    "Yusnaan - Patron's Palace Serah's Pendant": rule_data_list[51],
    "Yusnaan - Gordon Gourmet's Recipe": rule_data_list[63],
    "Yusnaan - Seedy Steak a la Civet": rule_data_list[64],
    "Yusnaan - Gregory Father's Letter": rule_data_list[0],
    "Yusnaan - Tanbam's Taboo Libra Notes": rule_data_list[53],
    "Yusnaan - Yusnaan Boss Drop": rule_data_list[51],
    "Ark - Initial 3rd Garb (1)": rule_data_list[0],
    "Ark - Initial 3rd Garb (2)": rule_data_list[0],
    "Ark - Initial 3rd Garb (3)": rule_data_list[0],
    "Ark - Ark Day 1 (1)": rule_data_list[0],
    "Ark - Ark Day 1 (2)": rule_data_list[0],
    "Ark - Ark Day 1 (3)": rule_data_list[0],
    "Ark - Ark Day 1 (4)": rule_data_list[0],
    "Ark - Ark Day 1 (5)": rule_data_list[0],
    "Ark - Ark Day 2 (1)": rule_data_list[65],
    "Ark - Ark Day 2 (2)": rule_data_list[65],
    "Ark - Ark Day 2 (3)": rule_data_list[65],
    "Ark - Ark Day 3 (1)": rule_data_list[17],
    "Ark - Ark Day 4 (1)": rule_data_list[66],
    "Ark - Ark Day 4 (2)": rule_data_list[66],
    "Ark - Ark Day 5 (1)": rule_data_list[67],
    "Ark - Ark Day 6 (1)": rule_data_list[68],
    "Ark - Ark Day 7": rule_data_list[69],
    "Ark - Ark Day 8": rule_data_list[70],
    "Ark - Ark Day 9": rule_data_list[71],
    "Ark - Ark Day 10": rule_data_list[72],
    "Ark - Ark Day 11": rule_data_list[73],
    "Ark - Ark Day 12": rule_data_list[74],
    "Ark - Ark Final Day (1)": rule_data_list[74],
    "Ark - Ark Final Day (2)": rule_data_list[74],
    "Ark - Ark Final Day (3)": rule_data_list[74],
    "Ark - Ark Extra Day": rule_data_list[75],
    "Ark - Replace Curaga": rule_data_list[0],
    "Ark - Replace Teleport": rule_data_list[0],
    "Ark - Replace Escape": rule_data_list[0],
    "CoP Dead Dunes - Flower in the Sands CoP Quest (1)": rule_data_list[65],
    "CoP Dead Dunes - Flower in the Sands CoP Quest (2)": rule_data_list[65],
    "CoP Dead Dunes - Biologically Speaking CoP Quest (1)": rule_data_list[65],
    "CoP Dead Dunes - Biologically Speaking CoP Quest (2)": rule_data_list[65],
    "CoP Dead Dunes - The Real Client CoP Quest (1)": rule_data_list[76],
    "CoP Dead Dunes - The Real Client CoP Quest (2)": rule_data_list[76],
    "CoP Dead Dunes - The Real Client CoP Quest (3)": rule_data_list[76],
    "CoP Dead Dunes - For My Child CoP Quest (1)": rule_data_list[66],
    "CoP Dead Dunes - For My Child CoP Quest (2)": rule_data_list[66],
    "CoP Dead Dunes - For My Child CoP Quest (3)": rule_data_list[66],
    "CoP Dead Dunes - Bandits' New Weapon CoP Quest (1)": rule_data_list[77],
    "CoP Dead Dunes - Bandits' New Weapon CoP Quest (2)": rule_data_list[77],
    "CoP Dead Dunes - Bandits' New Weapon CoP Quest (3)": rule_data_list[77],
    "CoP Dead Dunes - Banned Goods CoP Quest (1)": rule_data_list[65],
    "CoP Dead Dunes - Banned Goods CoP Quest (2)": rule_data_list[65],
    "CoP Dead Dunes - Banned Goods CoP Quest (3)": rule_data_list[65],
    "CoP Dead Dunes - Climbing The Ranks I CoP Quest (1)": rule_data_list[66],
    "CoP Dead Dunes - Climbing The Ranks I CoP Quest (2)": rule_data_list[66],
    "CoP Dead Dunes - Miracle Vintage CoP Quest (1)": rule_data_list[67],
    "CoP Dead Dunes - Miracle Vintage CoP Quest (2)": rule_data_list[67],
    "CoP Dead Dunes - Miracle Vintage CoP Quest (3)": rule_data_list[67],
    "CoP Dead Dunes - Climbing The Ranks II CoP Quest (1)": rule_data_list[78],
    "CoP Dead Dunes - Climbing The Ranks II CoP Quest (2)": rule_data_list[78],
    "CoP Dead Dunes - Heightened Security CoP Quest (1)": rule_data_list[67],
    "CoP Dead Dunes - Heightened Security CoP Quest (2)": rule_data_list[67],
    "CoP Dead Dunes - Heightened Security CoP Quest (3)": rule_data_list[67],
    "CoP Dead Dunes - Desert Cleanup CoP Quest (1)": rule_data_list[79],
    "CoP Dead Dunes - Desert Cleanup CoP Quest (2)": rule_data_list[79],
    "CoP Dead Dunes - Desert Cleanup CoP Quest (3)": rule_data_list[79],
    "CoP Dead Dunes - A Treasure for a God CoP Quest (1)": rule_data_list[80],
    "CoP Dead Dunes - A Treasure for a God CoP Quest (2)": rule_data_list[80],
    "CoP Dead Dunes - Lucky Charm CoP Quest (1)": rule_data_list[0],
    "CoP Dead Dunes - Lucky Charm CoP Quest (2)": rule_data_list[0],
    "CoP Dead Dunes - Supply and Demand CoP Quest (1)": rule_data_list[81],
    "CoP Dead Dunes - Supply and Demand CoP Quest (2)": rule_data_list[81],
    "CoP Dead Dunes - Supply and Demand CoP Quest (3)": rule_data_list[81],
    "CoP Dead Dunes - A New Application CoP Quest (1)": rule_data_list[82],
    "CoP Dead Dunes - A New Application CoP Quest (2)": rule_data_list[82],
    "CoP Dead Dunes - A New Application CoP Quest (3)": rule_data_list[82],
    "CoP Dead Dunes - Pride And Greed I CoP Quest (1)": rule_data_list[66],
    "CoP Dead Dunes - Pride And Greed I CoP Quest (2)": rule_data_list[66],
    "CoP Dead Dunes - Pride And Greed I CoP Quest (3)": rule_data_list[66],
    "CoP Dead Dunes - Pride And Greed II CoP Quest (1)": rule_data_list[83],
    "CoP Dead Dunes - Pride And Greed II CoP Quest (2)": rule_data_list[83],
    "CoP Dead Dunes - Pride And Greed II CoP Quest (3)": rule_data_list[83],
    "CoP Dead Dunes - Pride And Greed III CoP Quest (1)": rule_data_list[84],
    "CoP Dead Dunes - Pride And Greed III CoP Quest (2)": rule_data_list[84],
    "CoP Dead Dunes - Pride And Greed III CoP Quest (3)": rule_data_list[84],
    "CoP Luxerion - Revenge Is Sweet CoP Quest (1)": rule_data_list[85],
    "CoP Luxerion - Revenge Is Sweet CoP Quest (2)": rule_data_list[85],
    "CoP Luxerion - Gift of Gratitude CoP Quest (1)": rule_data_list[85],
    "CoP Luxerion - Gift of Gratitude CoP Quest (2)": rule_data_list[85],
    "CoP Luxerion - Gift of Gratitude CoP Quest (3)": rule_data_list[85],
    "CoP Luxerion - A Song for God CoP Quest (1)": rule_data_list[66],
    "CoP Luxerion - A Song for God CoP Quest (2)": rule_data_list[66],
    "CoP Luxerion - A Song for God CoP Quest (3)": rule_data_list[66],
    "CoP Luxerion - Slay the Machine CoP Quest (1)": rule_data_list[66],
    "CoP Luxerion - Slay the Machine CoP Quest (2)": rule_data_list[66],
    "CoP Luxerion - Enchanted Brush CoP Quest (1)": rule_data_list[86],
    "CoP Luxerion - Enchanted Brush CoP Quest (2)": rule_data_list[86],
    "CoP Luxerion - Enchanted Brush CoP Quest (3)": rule_data_list[86],
    "CoP Luxerion - Heretics' Beasts CoP Quest (1)": rule_data_list[87],
    "CoP Luxerion - Heretics' Beasts CoP Quest (2)": rule_data_list[87],
    "CoP Luxerion - Heretics' Beasts CoP Quest (3)": rule_data_list[87],
    "CoP Luxerion - Grave of a Bounty Hunter CoP Quest (1)": rule_data_list[68],
    "CoP Luxerion - Grave of a Bounty Hunter CoP Quest (2)": rule_data_list[68],
    "CoP Luxerion - Grave of a Bounty Hunter CoP Quest (3)": rule_data_list[68],
    "CoP Luxerion - Inventive Seamstress CoP Quest (1)": rule_data_list[85],
    "CoP Luxerion - Inventive Seamstress CoP Quest (2)": rule_data_list[85],
    "CoP Luxerion - Puppeteer's Lament CoP Quest (1)": rule_data_list[68],
    "CoP Luxerion - Puppeteer's Lament CoP Quest (2)": rule_data_list[68],
    "CoP Luxerion - Puppeteer's Lament CoP Quest (3)": rule_data_list[68],
    "CoP Luxerion - Revenge has Teeth CoP Quest (1)": rule_data_list[68],
    "CoP Luxerion - Revenge has Teeth CoP Quest (2)": rule_data_list[68],
    "CoP Luxerion - Night Patrol CoP Quest (1)": rule_data_list[88],
    "CoP Luxerion - Night Patrol CoP Quest (2)": rule_data_list[88],
    "CoP Luxerion - Night Patrol CoP Quest (3)": rule_data_list[88],
    "CoP Luxerion - Trapped CoP Quest (1)": rule_data_list[89],
    "CoP Luxerion - Trapped CoP Quest (2)": rule_data_list[89],
    "CoP Luxerion - Trapped CoP Quest (3)": rule_data_list[89],
    "CoP Luxerion - Trapped CoP Quest (4)": rule_data_list[89],
    "CoP Luxerion - Mythical Badge CoP Quest (1)": rule_data_list[90],
    "CoP Luxerion - Mythical Badge CoP Quest (2)": rule_data_list[90],
    "CoP Luxerion - Mythical Badge CoP Quest (3)": rule_data_list[90],
    "CoP Wildlands - Sun Flower CoP Quest (1)": rule_data_list[65],
    "CoP Wildlands - Sun Flower CoP Quest (2)": rule_data_list[65],
    "CoP Wildlands - Moon Flower CoP Quest (1)": rule_data_list[65],
    "CoP Wildlands - Moon Flower CoP Quest (2)": rule_data_list[65],
    "CoP Wildlands - Moon Flower CoP Quest (3)": rule_data_list[65],
    "CoP Wildlands - Secret of the Chocoborel CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - Secret of the Chocoborel CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - Secret of the Chocoborel CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - Wildlands In Danger! CoP Quest (1)": rule_data_list[91],
    "CoP Wildlands - Wildlands In Danger! CoP Quest (2)": rule_data_list[91],
    "CoP Wildlands - Wildlands In Danger! CoP Quest (3)": rule_data_list[91],
    "CoP Wildlands - Hunting the Hunter CoP Quest (1)": rule_data_list[92],
    "CoP Wildlands - Hunting the Hunter CoP Quest (2)": rule_data_list[92],
    "CoP Wildlands - Hunting the Hunter CoP Quest (3)": rule_data_list[92],
    "CoP Wildlands - Forget Me Not CoP Quest (1)": rule_data_list[65],
    "CoP Wildlands - Forget Me Not CoP Quest (2)": rule_data_list[65],
    "CoP Wildlands - Forget Me Not CoP Quest (3)": rule_data_list[65],
    "CoP Wildlands - A Word of Thanks CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - A Word of Thanks CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - A Word of Thanks CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - Fresh Fertilizer CoP Quest (1)": rule_data_list[93],
    "CoP Wildlands - Fresh Fertilizer CoP Quest (2)": rule_data_list[93],
    "CoP Wildlands - Fresh Fertilizer CoP Quest (3)": rule_data_list[93],
    "CoP Wildlands - For the Future CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - For the Future CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - For the Future CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - Dumpling Cook-Off CoP Quest (1)": rule_data_list[94],
    "CoP Wildlands - Dumpling Cook-Off CoP Quest (2)": rule_data_list[94],
    "CoP Wildlands - Dumpling Cook-Off CoP Quest (3)": rule_data_list[94],
    "CoP Wildlands - Brain Over Brawn CoP Quest (1)": rule_data_list[95],
    "CoP Wildlands - Brain Over Brawn CoP Quest (2)": rule_data_list[95],
    "CoP Wildlands - Brain Over Brawn CoP Quest (3)": rule_data_list[95],
    "CoP Wildlands - Hunter's Challenge CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - Hunter's Challenge CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - Hunter's Challenge CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - A Secret Wish CoP Quest (1)": rule_data_list[96],
    "CoP Wildlands - A Secret Wish CoP Quest (2)": rule_data_list[96],
    "CoP Wildlands - A Secret Wish CoP Quest (3)": rule_data_list[96],
    "CoP Wildlands - Moghan's Plea CoP Quest (1)": rule_data_list[41],
    "CoP Wildlands - Moghan's Plea CoP Quest (2)": rule_data_list[41],
    "CoP Wildlands - Moghan's Plea CoP Quest (3)": rule_data_list[41],
    "CoP Wildlands - What's in a Brew? CoP Quest (1)": rule_data_list[97],
    "CoP Wildlands - What's in a Brew? CoP Quest (2)": rule_data_list[97],
    "CoP Wildlands - What's in a Brew? CoP Quest (3)": rule_data_list[97],
    "CoP Wildlands - What's in a Brew? CoP Quest (4)": rule_data_list[97],
    "CoP Wildlands - A Prayer to a Goddess CoP Quest (1)": rule_data_list[98],
    "CoP Wildlands - A Prayer to a Goddess CoP Quest (2)": rule_data_list[98],
    "CoP Wildlands - A Prayer to a Goddess CoP Quest (3)": rule_data_list[98],
    "CoP Wildlands - Gatekeeper's Curiosity CoP Quest (1)": rule_data_list[68],
    "CoP Wildlands - Gatekeeper's Curiosity CoP Quest (2)": rule_data_list[68],
    "CoP Wildlands - Echoes of a Drum CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - Echoes of a Drum CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - Echoes of a Drum CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - A Voice From Below CoP Quest (1)": rule_data_list[66],
    "CoP Wildlands - A Voice From Below CoP Quest (2)": rule_data_list[66],
    "CoP Wildlands - A Voice From Below CoP Quest (3)": rule_data_list[66],
    "CoP Wildlands - Chocobo Chow CoP Quest (1)": rule_data_list[99],
    "CoP Wildlands - Chocobo Chow CoP Quest (2)": rule_data_list[99],
    "CoP Wildlands - Chocobo Chow CoP Quest (3)": rule_data_list[99],
    "CoP Wildlands - Sylkis Secrets CoP Quest (1)": rule_data_list[100],
    "CoP Wildlands - Sylkis Secrets CoP Quest (2)": rule_data_list[100],
    "CoP Wildlands - Sylkis Secrets CoP Quest (3)": rule_data_list[100],
    "CoP Wildlands - Digging Mole CoP Quest (1)": rule_data_list[101],
    "CoP Wildlands - Digging Mole CoP Quest (2)": rule_data_list[101],
    "CoP Wildlands - Digging Mole CoP Quest (3)": rule_data_list[101],
    "CoP Wildlands - Two Together CoP Quest (1)": rule_data_list[102],
    "CoP Wildlands - Two Together CoP Quest (2)": rule_data_list[102],
    "CoP Wildlands - Two Together CoP Quest (3)": rule_data_list[102],
    "CoP Wildlands - Emergency Treatment CoP Quest (1)": rule_data_list[34],
    "CoP Wildlands - Emergency Treatment CoP Quest (2)": rule_data_list[34],
    "CoP Wildlands - Emergency Treatment CoP Quest (3)": rule_data_list[34],
    "CoP Wildlands - Moogle Gourmand CoP Quest (1)": rule_data_list[103],
    "CoP Wildlands - Moogle Gourmand CoP Quest (2)": rule_data_list[103],
    "CoP Wildlands - Moogle Gourmand CoP Quest (3)": rule_data_list[103],
    "CoP Yusnaan - Secret Machine CoP Quest (1)": rule_data_list[65],
    "CoP Yusnaan - Secret Machine CoP Quest (2)": rule_data_list[65],
    "CoP Yusnaan - Soulful Horn CoP Quest (1)": rule_data_list[17],
    "CoP Yusnaan - Soulful Horn CoP Quest (2)": rule_data_list[17],
    "CoP Yusnaan - Soulful Horn CoP Quest (3)": rule_data_list[17],
    "CoP Yusnaan - A Dangerous Cocktail CoP Quest (1)": rule_data_list[66],
    "CoP Yusnaan - A Dangerous Cocktail CoP Quest (2)": rule_data_list[66],
    "CoP Yusnaan - Source of Inspiration CoP Quest (1)": rule_data_list[68],
    "CoP Yusnaan - Source of Inspiration CoP Quest (2)": rule_data_list[68],
    "CoP Yusnaan - Youth Potion CoP Quest (1)": rule_data_list[95],
    "CoP Yusnaan - Youth Potion CoP Quest (2)": rule_data_list[95],
    "CoP Yusnaan - Youth Potion CoP Quest (3)": rule_data_list[95],
    "CoP Yusnaan - Beast Summoner CoP Quest (1)": rule_data_list[104],
    "CoP Yusnaan - Beast Summoner CoP Quest (2)": rule_data_list[104],
    "CoP Yusnaan - Beast Summoner CoP Quest (3)": rule_data_list[104],
    "CoP Yusnaan - What Seekers Seek CoP Quest (1)": rule_data_list[105],
    "CoP Yusnaan - What Seekers Seek CoP Quest (2)": rule_data_list[105],
    "CoP Yusnaan - What Seekers Seek CoP Quest (3)": rule_data_list[105],
    "CoP Yusnaan - True Colors CoP Quest (1)": rule_data_list[68],
    "CoP Yusnaan - True Colors CoP Quest (2)": rule_data_list[68],
    "CoP Yusnaan - True Colors CoP Quest (3)": rule_data_list[68],
    "CoP Yusnaan - Ultimate Craving CoP Quest (1)": rule_data_list[106],
    "CoP Yusnaan - Ultimate Craving CoP Quest (2)": rule_data_list[106],
    "CoP Yusnaan - Ultimate Craving CoP Quest (3)": rule_data_list[106],
    "CoP Yusnaan - Ultimate Craving CoP Quest (4)": rule_data_list[106],
    "CoP Yusnaan - Spell for Spell CoP Quest (1)": rule_data_list[95],
    "CoP Yusnaan - Spell for Spell CoP Quest (2)": rule_data_list[95],
    "CoP Yusnaan - Spell for Spell CoP Quest (3)": rule_data_list[95],
    "CoP Yusnaan - Unfired Firework CoP Quest (1)": rule_data_list[53],
    "CoP Yusnaan - Unfired Firework CoP Quest (2)": rule_data_list[53],
    "CoP Yusnaan - Unfired Firework CoP Quest (3)": rule_data_list[53],
    "CoP Yusnaan - Time Doesn't Heal CoP Quest (1)": rule_data_list[107],
    "CoP Yusnaan - Time Doesn't Heal CoP Quest (2)": rule_data_list[107],
    "CoP Yusnaan - Time Doesn't Heal CoP Quest (3)": rule_data_list[107],
    "CoP Yusnaan - A Man for a Chocobo Girl CoP Quest (1)": rule_data_list[108],
    "CoP Yusnaan - A Man for a Chocobo Girl CoP Quest (2)": rule_data_list[108],
    "CoP Yusnaan - A Man for a Chocobo Girl CoP Quest (3)": rule_data_list[108],
    "CoP Yusnaan - Rebuilding CoP Quest (1)": rule_data_list[53],
    "CoP Yusnaan - Rebuilding CoP Quest (2)": rule_data_list[53],
    "CoP Global - Global: Key To Her Heart CoP Quest (1)": rule_data_list[109],
    "CoP Global - Global: Key To Her Heart CoP Quest (2)": rule_data_list[109],
    "CoP Global - Global: Key To Her Heart CoP Quest (3)": rule_data_list[109],
    "CoP Global - Global: Roadworks I CoP Quest (1)": rule_data_list[110],
    "CoP Global - Global: Roadworks I CoP Quest (2)": rule_data_list[110],
    "CoP Global - Global: Roadworks I CoP Quest (3)": rule_data_list[110],
    "CoP Global - Global: Roadworks II CoP Quest (1)": rule_data_list[111],
    "CoP Global - Global: Roadworks II CoP Quest (2)": rule_data_list[111],
    "CoP Global - Global: Roadworks II CoP Quest (3)": rule_data_list[111],
    "CoP Global - Global: Roadworks III CoP Quest (1)": rule_data_list[112],
    "CoP Global - Global: Roadworks III CoP Quest (2)": rule_data_list[112],
    "CoP Global - Global: Roadworks III CoP Quest (3)": rule_data_list[112],
    "CoP Global - Global: A Girl's Challenge CoP Quest (1)": rule_data_list[113],
    "CoP Global - Global: A Girl's Challenge CoP Quest (2)": rule_data_list[113],
    "CoP Global - Global: What's Left Behind CoP Quest (1)": rule_data_list[114],
    "CoP Global - Global: What's Left Behind CoP Quest (2)": rule_data_list[114],
    "CoP Global - Global: Seeing The Dawn CoP Quest (1)": rule_data_list[115],
    "CoP Global - Global: Seeing The Dawn CoP Quest (2)": rule_data_list[115],
    "CoP Global - Global: Staying Sharp CoP Quest (1)": rule_data_list[116],
    "CoP Global - Global: Staying Sharp CoP Quest (2)": rule_data_list[116],
    "CoP Global - Global: Where Moogles Be CoP Quest (1)": rule_data_list[117],
    "CoP Global - Global: Where Moogles Be CoP Quest (2)": rule_data_list[117],
    "CoP Global - Global: Fading Prayer CoP Quest (1)": rule_data_list[118],
    "CoP Global - Global: Fading Prayer CoP Quest (2)": rule_data_list[118],
    "CoP Global - Global: Forbidden Tome CoP Quest (1)": rule_data_list[119],
    "CoP Global - Global: Forbidden Tome CoP Quest (2)": rule_data_list[119],
    "CoP Global - Global: Shoot For The Sky CoP Quest (1)": rule_data_list[120],
    "CoP Global - Global: Shoot For The Sky CoP Quest (2)": rule_data_list[120],
    "CoP Global - Global: Shoot For The Sky CoP Quest (3)": rule_data_list[120],
    "CoP Global - Global: Digging Mysteries CoP Quest (1)": rule_data_list[121],
    "CoP Global - Global: Digging Mysteries CoP Quest (2)": rule_data_list[121],
    "CoP Global - Global: Digging Mysteries CoP Quest (3)": rule_data_list[121],
    "Soul Seeds/Unappraised - 10 Soul Seeds": rule_data_list[122],
    "Soul Seeds/Unappraised - 20 Soul Seeds": rule_data_list[122],
    "Soul Seeds/Unappraised - 30 Soul Seeds": rule_data_list[122],
    "Soul Seeds/Unappraised - 40 Soul Seeds": rule_data_list[122],
    "Soul Seeds/Unappraised - 50 Soul Seeds": rule_data_list[122],
    "Soul Seeds/Unappraised - Soul Seeds Fragment of Radiance": rule_data_list[123],
    "Soul Seeds/Unappraised - 1 Unappraised": rule_data_list[7],
    "Soul Seeds/Unappraised - 5 Unappraised": rule_data_list[7],
    "Soul Seeds/Unappraised - 10 Unappraised": rule_data_list[7],
    "Soul Seeds/Unappraised - 20 Unappraised": rule_data_list[7],
    "Soul Seeds/Unappraised - 50 Unappraised": rule_data_list[7],
    "Ultimate Lair - Floor 1 Hoplite Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 2 Niblet Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 3 Zaltys Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 4 Gaunt Omega Drop": rule_data_list[125],
    "Ultimate Lair - Floor 5 Gremlin Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 6 Dreadnought Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 7 Gorgonopsid Omega Drop": rule_data_list[125],
    "Ultimate Lair - Floor 8 Goblot Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 9 Gurangatch Omega Drop": rule_data_list[125],
    "Ultimate Lair - Floor 10 Ectopudding Omega Drop": rule_data_list[125],
    "Ultimate Lair - Floor 11 Miniflan Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 12 Aster Protoflorian Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 13 Schrodinger Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 14 Goblin Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 15 Reaver Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 16 Meonekton Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 17 Cactuar Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 18 Triffid Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 19 Cyclops Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 20 Skeleton Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 21 Desert Sahagin Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 22 Earth Eater Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 23 Skata'ne Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 24 Hanuman Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 25 Zomok Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 26 Dryad Omega Drop": rule_data_list[57],
    "Ultimate Lair - Floor 27 Rafflesia Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 28 Chocobo Eater Omega Drop": rule_data_list[124],
    "Ultimate Lair - Floor 29 UL Treasure": rule_data_list[57],
    "Ultimate Lair - Floor 30 UL Treasure": rule_data_list[57],
    "Ultimate Lair - Floor 31 UL Treasure": rule_data_list[57],
    "Ultimate Lair - Floor 32 UL Treasure": rule_data_list[57],
    "Ultimate Lair - Ultimate Lair Boss Drop": rule_data_list[110],
    "Ultimate Lair - Ultimate Lair Boss Reward": rule_data_list[110],
    "Final Day - Arcangeli Omega Drop": rule_data_list[74],
    "Final Day - Sugriva Omega Drop": rule_data_list[74],
    "Final Day - Chimera Omega Drop": rule_data_list[74],
    "Final Day - Final Day Altar Of Salvation": rule_data_list[74],
    "Final Day - Final Day Altar Of Judgment": rule_data_list[74],
    "Final Day - Final Day Altar Of Atonement": rule_data_list[74],
    "Final Day - Final Day Altar Of Birth": rule_data_list[74],
    "Final Day - Final Day Temple Of Light (1)": rule_data_list[74],
    "Final Day - Final Day Temple Of Light (2)": rule_data_list[74],
    "Final Day - Final Day Temple Of Light (3)": rule_data_list[74],
    "Final Day - Final Day Ultima Weapon": rule_data_list[74],
    "Final Day - Final Day Ultima Shield": rule_data_list[74],
    "Dead Dunes - Cactair Fragment of Kindness": rule_data_list[1],
    "Dead Dunes - Goblots Arithmometer": rule_data_list[1],
    "Dead Dunes - Aeronite Monster Flesh": rule_data_list[72],
    "Luxerion - Zomok Cursed Dragon Claw": rule_data_list[0],
    "Yusnaan - Gremlins Music Satchel": rule_data_list[0],
    "Yusnaan - Schrodinger Civet Musk": rule_data_list[0],
    "Ark Day 0 Event (1)": rule_data_list[0],
    "Ark Day 1 Event (1)": rule_data_list[0],
    "Ark Day 2 Event (1)": rule_data_list[65],
    "Ark Day 3 Event (1)": rule_data_list[17],
    "Ark Day 4 Event (1)": rule_data_list[66],
    "Ark Day 5 Event (1)": rule_data_list[67],
    "Ark Day 6 Event (1)": rule_data_list[68],
    "Main Quest 4 Event (1)": rule_data_list[126],
    "Main Quest 4 Event (2)": rule_data_list[126],
    "Main Quest 1 Event (1)": rule_data_list[127],
    "Main Quest 1 Event (2)": rule_data_list[127],
    "Main Quest 3 Event (1)": rule_data_list[128],
    "Main Quest 3 Event (2)": rule_data_list[128],
    "Main Quest 2 Event (1)": rule_data_list[129],
    "Main Quest 2 Event (2)": rule_data_list[129],
    "Main Quest 5 Event (1)": rule_data_list[130],
    "Main Quest 5 Event (2)": rule_data_list[130],
    "The Things She Lost Quest Event (1)": rule_data_list[19],
    "Where Are You, Holmes? Quest Event (1)": rule_data_list[0],
    "Like Clockwork Quest Event (1)": rule_data_list[14],
    "Dying Wish Quest Event (1)": rule_data_list[20],
    "Suspicious Spheres Quest Event (1)": rule_data_list[21],
    "Born From Chaos Quest Event (1)": rule_data_list[22],
    "Soul Seeds Quest Event (1)": rule_data_list[23],
    "Faster Than Lightning Quest Event (1)": rule_data_list[15],
    "Treasured Ball Quest Event (1)": rule_data_list[24],
    "The Angel's Tears Quest Event (1)": rule_data_list[15],
    "The Saint's Stone Quest Event (1)": rule_data_list[16],
    "Whither Faith Quest Event (1)": rule_data_list[0],
    "The Avid Reader Quest Event (1)": rule_data_list[16],
    "Buried Passion Quest Event (1)": rule_data_list[27],
    "The Girl Who Cried Wolf Quest Event (1)": rule_data_list[16],
    "Stuck in a Gem Quest Event (1)": rule_data_list[0],
    "Get the Girl Quest Event (1)": rule_data_list[16],
    "A Rose By Any Other Name Quest Event (1)": rule_data_list[28],
    "Voices from the Grave Quest Event (1)": rule_data_list[16],
    "To Save the Sinless Quest Event (1)": rule_data_list[29],
    "The Life of a Machine Quest Event (1)": rule_data_list[3],
    "Old Rivals Quest Event (1)": rule_data_list[6],
    "His Wife's Dream Quest Event (1)": rule_data_list[6],
    "Tool of the Trade Quest Event (1)": rule_data_list[7],
    "Adonis's Audition Quest Event (1)": rule_data_list[8],
    "What Rough Beast Slouches Quest Event (1)": rule_data_list[9],
    "Skeletons In The Closet Quest Event (1)": rule_data_list[10],
    "Last One Standing Quest Event (1)": rule_data_list[0],
    "A Father's Request Quest Event (1)": rule_data_list[31],
    "The Hunter's Challenge Quest Event (1)": rule_data_list[32],
    "A Final Cure Quest Event (1)": rule_data_list[31],
    "Fuzzy Search Quest Event (1)": rule_data_list[0],
    "Round 'em Up Quest Event (1)": rule_data_list[33],
    "Chocobo Cheer Quest Event (1)": rule_data_list[34],
    "Peace and Quiet, Kupo Quest Event (1)": rule_data_list[0],
    "Saving an Angel Quest Event (1)": rule_data_list[31],
    "Omega Point Quest Event (1)": rule_data_list[35],
    "The Old Man and the Field Quest Event (1)": rule_data_list[36],
    "Land of our Forebears Quest Event (1)": rule_data_list[37],
    "A Taste of the Past Quest Event (1)": rule_data_list[38],
    "Dog, Doctor and Assistant Quest Event (1)": rule_data_list[34],
    "The Right Stuff Quest Event (1)": rule_data_list[31],
    "The Secret Lives of Sheep Quest Event (1)": rule_data_list[40],
    "Where Are You, Moogle? Quest Event (1)": rule_data_list[41],
    "Mercy of a Goddess Quest Event (1)": rule_data_list[42],
    "The Grail of Valhalla Quest Event (1)": rule_data_list[43],
    "To Live in Chaos Quest Event (1)": rule_data_list[44],
    "Killing Time Quest Event (1)": rule_data_list[30],
    "Matchmaker Quest Event (1)": rule_data_list[45],
    "Mother and Daughter Quest Event (1)": rule_data_list[46],
    "Fireworks in a Bottle Quest Event (1)": rule_data_list[48],
    "The Fighting Actress Quest Event (1)": rule_data_list[48],
    "Songless Diva Quest Event (1)": rule_data_list[55],
    "Stolen Things Quest Event (1)": rule_data_list[56],
    "Fireworks for a Steal Quest Event (1)": rule_data_list[48],
    "A Testing Proposition Quest Event (1)": rule_data_list[0],
    "Last Date Quest Event (1)": rule_data_list[53],
    "Free Will Quest Event (1)": rule_data_list[57],
    "Friends Forever Quest Event (1)": rule_data_list[53],
    "Family Food Quest Event (1)": rule_data_list[58],
    "Tanbam's Taboo Quest Event (1)": rule_data_list[53],
    "Play It for Me Quest Event (1)": rule_data_list[59],
    "Adoring Adornments Quest Event (1)": rule_data_list[60],
    "Adoring Candice Quest Event (1)": rule_data_list[61],
    "Death Safari Quest Event (1)": rule_data_list[48],
    "Death Game Quest Event (1)": rule_data_list[62],
    "Main Quest 1-1 Event (1)": rule_data_list[0],
    "Main Quest 1-2 Event (1)": rule_data_list[85],
    "Main Quest 1-3 Event (1)": rule_data_list[15],
    "Main Quest 1-4 Event (1)": rule_data_list[13],
    "Main Quest 2-1 cyclops Event (1)": rule_data_list[131],
    "Main Quest 2-1 Event (1)": rule_data_list[132],
    "Main Quest 2-2 Event (1)": rule_data_list[54],
    "Main Quest 3-1 Event (1)": rule_data_list[0],
    "Main Quest 3-2 Event (1)": rule_data_list[133],
    "Main Quest 3-3 Flight Event (1)": rule_data_list[34],
    "Main Quest 4-1 Event (1)": rule_data_list[0],
    "Main Quest 4-2 Event (1)": rule_data_list[8],
    "Main Quest 4-3 Event (1)": rule_data_list[2],
    "Main Quest 4-4 First Tablet placed Event (1)": rule_data_list[134],
    "Main Quest 4-4 Event (1)": rule_data_list[135],
    "Main Quest 5 start Event (1)": rule_data_list[136],
    "Victory Event (1)": rule_data_list[137],
    "Banned Goods Event (1)": rule_data_list[65],
    "Miracle Vintage Event (1)": rule_data_list[67],
    "For My Child Event (1)": rule_data_list[66],
    "Heightened Security Event (1)": rule_data_list[67],
    "Climbing the Ranks I Event (1)": rule_data_list[66],
    "Climbing the Ranks II Event (1)": rule_data_list[78],
    "Flower in the Sands Event (1)": rule_data_list[65],
    "Biologically Speaking Event (1)": rule_data_list[65],
    "Lucky Charm Event (1)": rule_data_list[0],
    "Pride and Greed I Event (1)": rule_data_list[66],
    "Pride and Greed II Event (1)": rule_data_list[83],
    "Pride and Greed III Event (1)": rule_data_list[84],
    "Revenge is Sweet Event (1)": rule_data_list[0],
    "Gift of Gratitude Event (1)": rule_data_list[0],
    "A Song for God Event (1)": rule_data_list[66],
    "Grave of a Bounty Hunter Event (1)": rule_data_list[68],
    "Inventive Seamstress Event (1)": rule_data_list[85],
    "Puppeteer's Lament Event (1)": rule_data_list[68],
    "Slay the Machine Event (1)": rule_data_list[66],
    "Revenge Has Teeth Event (1)": rule_data_list[68],
    "Sun Flower Event (1)": rule_data_list[65],
    "Moon Flower Event (1)": rule_data_list[65],
    "Forget Me Not Event (1)": rule_data_list[65],
    "A Word of Thanks Event (1)": rule_data_list[66],
    "Fresh Fertilizer Event (1)": rule_data_list[93],
    "For the Future Event (1)": rule_data_list[66],
    "Echoes of a Drum Event (1)": rule_data_list[66],
    "A Voice from Below Event (1)": rule_data_list[66],
    "Brain Over Brawn Event (1)": rule_data_list[95],
    "Hunter's Challenge Event (1)": rule_data_list[66],
    "Moghan's Plea Event (1)": rule_data_list[41],
    "Gatekeeper's Curiosity Event (1)": rule_data_list[68],
    "Chocobo Chow Event (1)": rule_data_list[99],
    "Secret Machine Event (1)": rule_data_list[65],
    "Soulful Horn Event (1)": rule_data_list[17],
    "A Dangerous Cocktail Event (1)": rule_data_list[66],
    "A Man for a Chocobo Girl Event (1)": rule_data_list[108],
    "Source of Inspiration Event (1)": rule_data_list[68],
    "True Colors Event (1)": rule_data_list[68],
    "Youth Potion Event (1)": rule_data_list[95],
    "Spell for Spell Event (1)": rule_data_list[95],
    "0-1 Hint Event (1)": rule_data_list[0],
    "1-1 Hint Event (1)": rule_data_list[85],
    "1-2 Hint Event (1)": rule_data_list[15],
    "1-3 Hint Event (1)": rule_data_list[13],
    "1-4 Hint Event (1)": rule_data_list[14],
    "1-5 Hint Event (1)": rule_data_list[16],
    "2-1 Hint Event (1)": rule_data_list[138],
    "2-2 Hint Event (1)": rule_data_list[139],
    "2-3 Hint Event (1)": rule_data_list[140],
    "3-1 Hint Event (1)": rule_data_list[141],
    "3-2 Hint Event (1)": rule_data_list[142],
    "3-3 Hint Event (1)": rule_data_list[143],
    "4-1 Hint Event (1)": rule_data_list[8],
    "4-2 Hint Event (1)": rule_data_list[2],
    "4-3 Hint Event (1)": rule_data_list[3],
    "4-4 Hint Event (1)": rule_data_list[144],
    "4-5 Hint Event (1)": rule_data_list[145],
    "5-1 Hint Event (1)": rule_data_list[146],
    "5-2 Hint Event (1)": rule_data_list[147],
    "5-3 Hint Event (1)": rule_data_list[148],
    "5-4 Hint Event (1)": rule_data_list[149],
    "5-5 Hint Event (1)": rule_data_list[147],
    "5-6 Hint Event (1)": rule_data_list[1],
}

item_rule_data_table: Dict[str, Callable[[Item], bool]] = {
    "Ark - Initial 3rd Garb (1)": lambda item: item_is_category(item.name, "Garb"),
    "Ark - Initial 3rd Garb (2)": lambda item: item_is_category(item.name, "Weapon"),
    "Ark - Initial 3rd Garb (3)": lambda item: item_is_category(item.name, "Shield"),
}

entrance_rule_data_table: Dict[Tuple[str, str], Callable[[CollectionState, int], bool]] = {
    ("Initial", "Ark"): rule_data_list[0],
    ("Luxerion", "Dead Dunes"): rule_data_list[17],
    ("Ark", "Luxerion"): rule_data_list[0],
    ("Luxerion", "Wildlands"): rule_data_list[17],
    ("Luxerion", "Yusnaan"): rule_data_list[17],
    ("Dead Dunes", "CoP Dead Dunes"): rule_data_list[17],
    ("Luxerion", "CoP Luxerion"): rule_data_list[17],
    ("Wildlands", "CoP Wildlands"): rule_data_list[17],
    ("Yusnaan", "CoP Yusnaan"): rule_data_list[17],
    ("Ark", "CoP Global"): rule_data_list[17],
    ("Dead Dunes", "Soul Seeds/Unappraised"): rule_data_list[17],
    ("Ark", "Ultimate Lair"): rule_data_list[66],
    ("Ark", "Final Day"): rule_data_list[137],
}
