
chao_name_conversion = {
	"!": 0x01,
	"!": 0x02,
	"#": 0x03,
	"$": 0x04,
	"%": 0x05,
	"&": 0x06,
	"\\": 0x07,
	"(": 0x08,
	")": 0x09,
	"*": 0x0A,
	"+": 0x0B,
	",": 0x0C,
	"-": 0x0D,
	".": 0x0E,
	"/": 0x0F,

	"0": 0x10,
	"1": 0x11,
	"2": 0x12,
	"3": 0x13,
	"4": 0x14,
	"5": 0x15,
	"6": 0x16,
	"7": 0x17,
	"8": 0x18,
	"9": 0x19,
	":": 0x1A,
	";": 0x1B,
	"<": 0x1C,
	"=": 0x1D,
	">": 0x1E,
	"?": 0x1F,

	"@": 0x20,
	"A": 0x21,
	"B": 0x22,
	"C": 0x23,
	"D": 0x24,
	"E": 0x25,
	"F": 0x26,
	"G": 0x27,
	"H": 0x28,
	"I": 0x29,
	"J": 0x2A,
	"K": 0x2B,
	"L": 0x2C,
	"M": 0x2D,
	"N": 0x2E,
	"O": 0x2F,

	"P": 0x30,
	"Q": 0x31,
	"R": 0x32,
	"S": 0x33,
	"T": 0x34,
	"U": 0x35,
	"V": 0x36,
	"W": 0x37,
	"X": 0x38,
	"Y": 0x39,
	"Z": 0x3A,
	"[": 0x3B,
	"¥": 0x3C,
	"]": 0x3D,
	"^": 0x3E,
	"_": 0x3F,

	"`": 0x40,
	"a": 0x41,
	"b": 0x42,
	"c": 0x43,
	"d": 0x44,
	"e": 0x45,
	"f": 0x46,
	"g": 0x47,
	"h": 0x48,
	"i": 0x49,
	"j": 0x4A,
	"k": 0x4B,
	"l": 0x4C,
	"m": 0x4D,
	"n": 0x4E,
	"o": 0x4F,

	"p": 0x50,
	"q": 0x51,
	"r": 0x52,
	"s": 0x53,
	"t": 0x54,
	"u": 0x55,
	"v": 0x56,
	"w": 0x57,
	"x": 0x58,
	"y": 0x59,
	"z": 0x5A,
	"{": 0x5B,
	"|": 0x5C,
	"}": 0x5D,
	"~": 0x5E,
	" ": 0x5F,
}

sample_chao_names = [
	"Aginah",
	"Biter",
	"Steve",
	"Ryley",
	"Watcher",
	"Acrid",
	"Sheik",
	"Lunais",
	"Samus",
	"The Kid",
	"Jack",
	"Sir Lee",
	"Viridian",
	"Rouhi",
	"Toad",
	"Merit",
	"Ridley",
	"Hornet",
	"Carl",
	"Raynor",
	"Dixie",
	"Wolnir",
	"Mario",
	"Gary",
	"Wayne",
	"Kevin",
	"J.J.",
	"Maxim",
	"Redento",
	"Caesar",
	"Abigail",
	"Link",
	"Ninja",
	"Roxas",
	"Marin",
	"Yorgle",
	"DLC",
	"Mina",
	"Sans",
	"Lan",
	"Rin",
	"Doomguy",
	"Guide",
	"May",
	"Hubert",
	"Corvus",
	"Nigel",
	"Benjamin",
	"Gooey",
	"Maddy",
	"AFGNCAAP",
	"Reinhardt",
	"Claire",
	"Yoshi",
	"Peasley",
	"Faux",
	"Naija",
	"Kaiba",
	"Hat Kid",
	"TzTokJad",
	"Sora",
	"WoodMan",
	"Yachty",
	"Grieve",
	"Portia",
	"Graves",
	"Kaycee",
	"Ghandi",
	"Medli",
	"Jak",
	"Wario",
	"Theo",
]

totally_real_item_names: dict[str, list[str]] = {
	"Bumper Stickers": [
		"Bonus Score",
		"Boosting Bumper",
	],

	"Castlevania 64": [
		"Earth card",
		"Venus card",
		"Ax",
		"Storehouse Key",
	],

	"Celeste 64": [
		"Blueberry",
		"Side Flip",
		"Triple Dash Refills",
		"Swap Blocks",
		"Dream Blocks",
	],

	"Celeste (Open World)": [
		"Green Boosters",
		"Triple Dash Refills",
		"Rising Platforms",
		"Red Bubbles",
		"Granny's Car Keys",
		"Blueberry",
	],

	"Civilization VI": [
		"Advanced Trebuchets",
		"The Wheel 2",
		"NFTs",
	],

	"Donkey Kong Country 3": [
		"Progressive Car Upgrade",
		"Bonus Token",
	],

	"Factorio": [
		"logistic-ai",
		"progressive-militia",
		"progressive-stronger-explosives",
		"uranium-food",
	],

	"A Hat in Time": [
		"Fire Hat",
		"69 Pons",
		"Relic (Green Canyon)",
		"Relic (Cooler Cow)",
		"Time Fragment",
	],

	"Hollow Knight": [
		"Shortnail",
		"Runmaster",
	],

	"Jak and Daxter The Precursor Legacy": [
		"69 Precursor Orbs",
		"Jump Roll",
		"Roll Kick",
	],

	"Kirby's Dream Land 3": [
		"CooCoo",
	],

	"Kingdom Hearts 2": [
		"Courage Form",
		"Auto Courage",
		"Donald Defender",
		"Goofy Blizzard",
		"Ultimate Weapon",
	],

	"Lingo": [
		"Art Gallery (First Floor)",
		"Color Hunt - Pink Barrier",
	],

	"A Link to the Past": [
		"Mallet",
		"Lava Rod",
		"Master Knife",
		"Slippers",
		"Spade",
		"Big Key (Dark Palace)",
		"Big Key (Hera Tower)",
	],

	"Links Awakening DX": [
		"Song of the Sky Whale",
		"Gryphon Shoes",
		"Wing Key",
		"Strength Anklet",
	],

	"Mario & Luigi Superstar Saga": [
		"Mega Nut",
	],

	"The Messenger": [
		"Key of Anger",
		"Time Shard (69)",
		"Hydro",
	],

	"Muse Dash": [
		"U.N. Owen Was Her",
		"Renai Circulation",
		"Flyers",
	],

	"Noita": [
		"Gold (69)",
		"Sphere",
		"Melee Die",
	],

	"Ocarina of Time": [
		"Jar",
		"Whistle of Space",
		"Rito Tunic",
		"Boss Key (Forest Haven)",
		"Boss Key (Swamp Palace)",
		"Boss Key (Great Bay Temple)",
	],

	"Old School Runescape": [
		"Area: Taverly",
		"Area: Meiyerditch",
		"Fire Cape",
	],

	"Overcooked! 2": [
		"Kitchen Sink",
	],

	"Paint": [
		"AI Enhance",
		"Paint Bucket",
		"Pen",
	],

	"Pokemon Red and Blue": [
		"Rock Badge",
		"Key Card",
		"Pikachu",
		"Eevee",
		"HM02 Strength",
		"HM05 Fly",
		"HM01 Surf",
		"Card Key 12F",
	],

	"Risk of Rain 2": [
		"Dio's Worst Enemy",
		"Stage 5",
		"Mythical Item",
	],

	"Rogue Legacy": [
		"Progressive Astromancers",
		"Progressive Chefs",
		"The Living Safe",
		"Lady Quinn",
	],

	"Saving Princess": [
		"Fire Spreadshot",
		"Volcano Key",
		"Frozen Key",
	],

	"Secret of Evermore": [
		"Mantis Claw",
		"Progressive pants",
		"Deflect",
	],

	"shapez": [
		"Spinner",
		"Toggle",
		"Slicer",
		"Splitter",
	],

	"SMZ3": [
		"Cane of Bryan",
	],

	"Sonic Adventure 2 Battle": [
		"Pink Chaos Emerald",
		"Black Chaos Emerald",
		"Tails - Large Cannon",
		"Eggman - Bazooka",
		"Eggman - Booster",
		"Knuckles - Shades",
		"Sonic - Magic Shoes",
		"Shadow - Bounce Bracelet",
		"Rouge - Air Necklace",
		"Big Key (Eggman's Pyramid)",
	],

	"Starcraft 2": [
		"Sensor Bunker",
		"Phantom",
		"Soldier",
	],

	"Stardew Valley": [
		"Van Repair",
		"Ship Repair",
		"Autumn",
		"Galaxy Knife",
		"Green Cabbage Seeds",
		"Casket",
		"Pet Moonlight Jelly",
		"Adventurer's Guild Key",
	],

	"Super Mario Land 2": [
		"Luigi Coin",
		"Luigi Zone Progression",
		"Hard Mode",
	],

	"Super Metroid": [
		"Plasma Suit",
		"Gravity Beam",
		"Hi-Jump Ball",
	],

	"Super Mario 64": [
		"Cannon Unlock LLL",
		"Feather Cap",
	],

	"Super Mario World": [
		"Progressive Yoshi",
		"Purple Switch Palace",
		"Cape Feather",
		"Fire Flower",
		"Cling",
		"Twirl Jump",
	],

	"Timespinner": [
		"Timespinner Cog 1",
		"Leg Cannon",
	],

	"TUNIC": [
		"Ladder To West Forest",
		"Money x69",
		"Page 69",
		"Master Sword",
	],

	"The Wind Waker": [
		"Ballad of Storms",
		"Wind God's Song",
		"Earth God's Song",
		"Ordon's Pearl",
	],

	"The Witness": [
		"Visible Dots",
	],

	"Yacht Dice": [
		"Category One of a Kind",
		"Category Fuller House",
	],

	"Yoshi's Island": [
		"Ear of Luigi",
		"+69 Stars",
		"Water Melon",
		"World 7 Gate",
		"Small Spring Ball",
	],

	"Yu-Gi-Oh! 2006": [
		"DUELIST ALLIANCE",
		"DUEL OVERLOAD",
		"POWER OF THE ELEMENTS",
		"S:P Little Knight",
		"Red-Eyes Dark Dragoon",
		"Maxx C"
	],
}

all_exits = [
	0x00,  # Lobby to Neutral
	0x01,  # Lobby to Hero
	0x02,  # Lobby to Dark
	0x03,  # Lobby to Kindergarten
	0x04,  # Neutral to Lobby
	0x05,  # Neutral to Cave
	0x06,  # Neutral to Transporter
	0x07,  # Hero to Lobby
	0x08,  # Hero to Transporter
	0x09,  # Dark to Lobby
	0x0A,  # Dark to Transporter
	0x0B,  # Cave to Neutral
	0x0C,  # Cave to Race
	0x0D,  # Cave to Karate
	0x0E,  # Race to Cave
	0x0F,  # Karate to Cave
	0x10,  # Transporter to Neutral
	#0x11,  # Transporter to Hero
	#0x12,  # Transporter to Dark
	0x13,  # Kindergarten to Lobby
]

all_destinations = [
	0x07,  # Lobby
	0x07,
	0x07,
	0x07,
	0x01,  # Neutral
	0x01,
	0x01,
	0x02,  # Hero
	0x02,
	0x03,  # Dark
	0x03,
	0x09,  # Cave
	0x09,
	0x09,
	0x05,  # Chao Race
	0x0A,  # Chao Karate
	0x0C,  # Transporter
	#0x0C,
	#0x0C,
	0x06,  # Kindergarten
]

multi_rooms = [
	0x07,
	0x01,
	0x02,
	0x03,
	0x09,
]

single_rooms = [
	0x05,
	0x0A,
	0x0C,
	0x06,
]

room_to_exits_map = {
	0x07: [0x00, 0x01, 0x02, 0x03],
	0x01: [0x04, 0x05, 0x06],
	0x02: [0x07, 0x08],
	0x03: [0x09, 0x0A],
	0x09: [0x0B, 0x0C, 0x0D],
	0x05: [0x0E],
	0x0A: [0x0F],
	0x0C: [0x10],#, 0x11, 0x12],
	0x06: [0x13],
}

exit_to_room_map = {
	0x00: 0x07,  # Lobby to Neutral
	0x01: 0x07,  # Lobby to Hero
	0x02: 0x07,  # Lobby to Dark
	0x03: 0x07,  # Lobby to Kindergarten
	0x04: 0x01,  # Neutral to Lobby
	0x05: 0x01,  # Neutral to Cave
	0x06: 0x01,  # Neutral to Transporter
	0x07: 0x02,  # Hero to Lobby
	0x08: 0x02,  # Hero to Transporter
	0x09: 0x03,  # Dark to Lobby
	0x0A: 0x03,  # Dark to Transporter
	0x0B: 0x09,  # Cave to Neutral
	0x0C: 0x09,  # Cave to Race
	0x0D: 0x09,  # Cave to Karate
	0x0E: 0x05,  # Race to Cave
	0x0F: 0x0A,  # Karate to Cave
	0x10: 0x0C,  # Transporter to Neutral
	#0x11: 0x0C,  # Transporter to Hero
	#0x12: 0x0C,  # Transporter to Dark
	0x13: 0x06,  # Kindergarten to Lobby
}

valid_kindergarten_exits = [
	0x04,  # Neutral to Lobby
	0x05,  # Neutral to Cave
	0x07,  # Hero to Lobby
	0x09,  # Dark to Lobby
]
