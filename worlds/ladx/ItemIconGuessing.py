BLOCKED_ASSOCIATIONS = [
    # MAX_ARROWS_UPGRADE, MAX_BOMBS_UPGRADE, MAX_POWDER_UPGRADE
    # arrows and bombs will be matched to arrow and bomb respectively through pluralization
    "ARROWS",
    "BOMBS",
    "MAX",
    "UPGRADE",

    "TAIL",     # TAIL_KEY
    "ANGLER",   # ANGLER_KEY
    "FACE",     # FACE_KEY
    "BIRD",     # BIRD_KEY
    "SLIME",    # SLIME_KEY
    "NIGHTMARE",# NIGHTMARE_KEY

    "BLUE",     # BLUE_TUNIC
    "RED",      # RED_TUNIC

    "TRADING",  # TRADING_ITEM_*
    "ITEM",     # TRADING_ITEM_*

    "BAD",      # BAD_HEART_CONTAINER
    "GOLD",     # GOLD_LEAF
    "MAGIC",    # MAGIC_POWDER, MAGIC_ROD
    "MESSAGE",  # MESSAGE (Master Stalfos' Message)
    "PEGASUS",  # PEGASUS_BOOTS
    "PIECE",    # HEART_PIECE, PIECE_OF_POWER
    "POWER",    # POWER_BRACELET, PIECE_OF_POWER
    "SINGLE",   # SINGLE_ARROW
    "STONE",    # STONE_BEAK

    "BEAK1",
    "BEAK2",
    "BEAK3",
    "BEAK4",
    "BEAK5",
    "BEAK6",
    "BEAK7",
    "BEAK8",

    "COMPASS1",
    "COMPASS2",
    "COMPASS3",
    "COMPASS4",
    "COMPASS5",
    "COMPASS6",
    "COMPASS7",
    "COMPASS8",

    "MAP1",
    "MAP2",
    "MAP3",
    "MAP4",
    "MAP5",
    "MAP6",
    "MAP7",
    "MAP8",
]

# Single word synonyms for Link's Awakening items, for generic matching.
SYNONYMS = {
    # POWER_BRACELET
    'ANKLET': 'POWER_BRACELET',
    'ARMLET': 'POWER_BRACELET',
    'BAND': 'POWER_BRACELET',
    'BANGLE': 'POWER_BRACELET',
    'BRACER': 'POWER_BRACELET',
    'CARRY': 'POWER_BRACELET',
    'CIRCLET': 'POWER_BRACELET',
    'CROISSANT': 'POWER_BRACELET',
    'GAUNTLET': 'POWER_BRACELET',
    'GLOVE': 'POWER_BRACELET',
    'RING': 'POWER_BRACELET',
    'STRENGTH': 'POWER_BRACELET',

    # SHIELD
    'AEGIS': 'SHIELD',
    'BUCKLER': 'SHIELD',
    'SHLD': 'SHIELD',

    # BOW
    'BALLISTA': 'BOW',

    # HOOKSHOT
    'GRAPPLE': 'HOOKSHOT',
    'GRAPPLING': 'HOOKSHOT',
    'ROPE': 'HOOKSHOT',

    # MAGIC_ROD
    'BEAM': 'MAGIC_ROD',
    'CANE': 'MAGIC_ROD',
    'STAFF': 'MAGIC_ROD',
    'WAND': 'MAGIC_ROD',

    # PEGASUS_BOOTS
    'BOOT': 'PEGASUS_BOOTS',
    'GREAVES': 'PEGASUS_BOOTS',
    'RUN': 'PEGASUS_BOOTS',
    'SHOE': 'PEGASUS_BOOTS',
    'SPEED': 'PEGASUS_BOOTS',

    # OCARINA
    'FLUTE': 'OCARINA',
    'RECORDER': 'OCARINA',

    # FEATHER
    'JUMP': 'FEATHER',
    'PLUME': 'FEATHER',
    'WING': 'FEATHER',

    # SHOVEL
    'DIG': 'SHOVEL',

    # MAGIC_POWDER
    'BAG': 'MAGIC_POWDER',
    'CASE': 'MAGIC_POWDER',
    'DUST': 'MAGIC_POWDER',
    'POUCH': 'MAGIC_POWDER',
    'SACK': 'MAGIC_POWDER',

    # BOMB
    'BLAST': 'BOMB',
    'BOMBCHU': 'BOMB',
    'FIRECRACKER': 'BOMB',
    'TNT': 'BOMB',

    # SWORD
    'BLADE': 'SWORD',
    'CUT': 'SWORD',
    'DAGGER': 'SWORD',
    'DIRK': 'SWORD',
    'EDGE': 'SWORD',
    'EPEE': 'SWORD',
    'EXCALIBUR': 'SWORD',
    'FALCHION': 'SWORD',
    'KATANA': 'SWORD',
    'KNIFE': 'SWORD',
    'MACHETE': 'SWORD',
    'MASAMUNE': 'SWORD',
    'MURASAME': 'SWORD',
    'SABER': 'SWORD',
    'SABRE': 'SWORD',
    'SCIMITAR': 'SWORD',
    'SLASH': 'SWORD',

    # FLIPPERS
    'FLIPPER': 'FLIPPERS',
    'SWIM': 'FLIPPERS',

    # MEDICINE
    'BOTTLE': 'MEDICINE',
    'FLASK': 'MEDICINE',
    'LEMONADE': 'MEDICINE',
    'POTION': 'MEDICINE',
    'TEA': 'MEDICINE',

    # TAIL_KEY

    # ANGLER_KEY

    # FACE_KEY

    # BIRD_KEY

    # SLIME_KEY

    # GOLD_LEAF
    'HERB': 'GOLD_LEAF',

    # RUPEES_20
    'COIN': 'RUPEES_20',
    'MONEY': 'RUPEES_20',
    'RUPEE': 'RUPEES_20',

    # RUPEES_50

    # RUPEES_100

    # RUPEES_200

    # RUPEES_500
    'GEM': 'RUPEES_500',
    'JEWEL': 'RUPEES_500',

    # SEASHELL
    'CARAPACE': 'SEASHELL',
    'CONCH': 'SEASHELL',
    'SHELL': 'SEASHELL',

    # MESSAGE (master stalfos message)
    'NOTHING': 'MESSAGE',
    'TRAP': 'MESSAGE',

    # BOOMERANG
    'BOOMER': 'BOOMERANG',

    # HEART_PIECE

    # BOWWOW
    'BEAST': 'BOWWOW',
    'PET': 'BOWWOW',

    # ARROWS_10

    # SINGLE_ARROW
    'MISSILE': 'SINGLE_ARROW',
    'QUIVER': 'SINGLE_ARROW',

    # ROOSTER
    'BIRD': 'ROOSTER',
    'CHICKEN': 'ROOSTER',
    'CUCCO': 'ROOSTER',
    'FLY': 'ROOSTER',
    'GRIFFIN': 'ROOSTER',
    'GRYPHON': 'ROOSTER',

    # MAX_POWDER_UPGRADE

    # MAX_BOMBS_UPGRADE

    # MAX_ARROWS_UPGRADE

    # RED_TUNIC

    # BLUE_TUNIC
    'ARMOR': 'BLUE_TUNIC',
    'MAIL': 'BLUE_TUNIC',
    'SUIT': 'BLUE_TUNIC',

    # HEART_CONTAINER
    'TANK': 'HEART_CONTAINER',

    # TOADSTOOL
    'FUNGAL': 'TOADSTOOL',
    'FUNGUS': 'TOADSTOOL',
    'MUSHROOM': 'TOADSTOOL',
    'SHROOM': 'TOADSTOOL',

    # GUARDIAN_ACORN
    'NUT': 'GUARDIAN_ACORN',
    'SEED': 'GUARDIAN_ACORN',

    # KEY
    'DOOR': 'KEY',
    'GATE': 'KEY',
    'KEY': 'KEY', # Without this, foreign keys show up as nightmare keys
    'LOCK': 'KEY',
    'PANEL': 'KEY',
    'UNLOCK': 'KEY',

    # NIGHTMARE_KEY

    # MAP

    # COMPASS

    # STONE_BEAK
    'FOSSIL': 'STONE_BEAK',
    'RELIC': 'STONE_BEAK',

    # SONG1
    'BOLERO': 'SONG1',
    'LULLABY': 'SONG1',
    'MELODY': 'SONG1',
    'MINUET': 'SONG1',
    'NOCTURNE': 'SONG1',
    'PRELUDE': 'SONG1',
    'REQUIEM': 'SONG1',
    'SERENADE': 'SONG1',
    'SONG': 'SONG1',

    # SONG2
    'FISH': 'SONG2',
    'SURF': 'SONG2',

    # SONG3
    'FROG': 'SONG3',

    # INSTRUMENT1
    'CELLO': 'INSTRUMENT1',
    'GUITAR': 'INSTRUMENT1',
    'LUTE': 'INSTRUMENT1',
    'VIOLIN': 'INSTRUMENT1',

    # INSTRUMENT2
    'HORN': 'INSTRUMENT2',

    # INSTRUMENT3
    'BELL': 'INSTRUMENT3',
    'CHIME': 'INSTRUMENT3',

    # INSTRUMENT4
    'HARP': 'INSTRUMENT4',
    'KANTELE': 'INSTRUMENT4',

    # INSTRUMENT5
    'MARIMBA': 'INSTRUMENT5',
    'XYLOPHONE': 'INSTRUMENT5',

    # INSTRUMENT6 (triangle)

    # INSTRUMENT7
    'KEYBOARD': 'INSTRUMENT7',
    'ORGAN': 'INSTRUMENT7',
    'PIANO': 'INSTRUMENT7',

    # INSTRUMENT8
    'DRUM': 'INSTRUMENT8',

    # TRADING_ITEM_YOSHI_DOLL
    'DINOSAUR': 'TRADING_ITEM_YOSHI_DOLL',
    'DRAGON': 'TRADING_ITEM_YOSHI_DOLL',
    'TOY': 'TRADING_ITEM_YOSHI_DOLL',

    # TRADING_ITEM_RIBBON
    'HAIRBAND': 'TRADING_ITEM_RIBBON',
    'HAIRPIN': 'TRADING_ITEM_RIBBON',

    # TRADING_ITEM_DOG_FOOD
    'CAN': 'TRADING_ITEM_DOG_FOOD',

    # TRADING_ITEM_BANANAS
    'BANANA': 'TRADING_ITEM_BANANAS',

    # TRADING_ITEM_STICK
    'BRANCH': 'TRADING_ITEM_STICK',
    'TWIG': 'TRADING_ITEM_STICK',

    # TRADING_ITEM_HONEYCOMB
    'BEEHIVE': 'TRADING_ITEM_HONEYCOMB',
    'HIVE': 'TRADING_ITEM_HONEYCOMB',
    'HONEY': 'TRADING_ITEM_HONEYCOMB',

    # TRADING_ITEM_PINEAPPLE
    'FOOD': 'TRADING_ITEM_PINEAPPLE',
    'FRUIT': 'TRADING_ITEM_PINEAPPLE',
    'GOURD': 'TRADING_ITEM_PINEAPPLE',

    # TRADING_ITEM_HIBISCUS
    'FLOWER': 'TRADING_ITEM_HIBISCUS',
    'PETAL': 'TRADING_ITEM_HIBISCUS',

    # TRADING_ITEM_LETTER
    'CARD': 'TRADING_ITEM_LETTER',
    'MESSAGE': 'TRADING_ITEM_LETTER',

    # TRADING_ITEM_BROOM
    'SWEEP': 'TRADING_ITEM_BROOM',

    # TRADING_ITEM_FISHING_HOOK
    'CLAW': 'TRADING_ITEM_FISHING_HOOK',

    # TRADING_ITEM_NECKLACE
    'AMULET': 'TRADING_ITEM_NECKLACE',
    'BEADS': 'TRADING_ITEM_NECKLACE',
    'PEARLS': 'TRADING_ITEM_NECKLACE',
    'PENDANT': 'TRADING_ITEM_NECKLACE',
    'ROSARY': 'TRADING_ITEM_NECKLACE',

    # TRADING_ITEM_SCALE

    # TRADING_ITEM_MAGNIFYING_GLASS
    'FINDER': 'TRADING_ITEM_MAGNIFYING_GLASS',
    'LENS': 'TRADING_ITEM_MAGNIFYING_GLASS',
    'MIRROR': 'TRADING_ITEM_MAGNIFYING_GLASS',
    'SCOPE': 'TRADING_ITEM_MAGNIFYING_GLASS',
    'XRAY': 'TRADING_ITEM_MAGNIFYING_GLASS',

    # PIECE_OF_POWER
    'TRIANGLE': 'PIECE_OF_POWER',
    'POWER': 'PIECE_OF_POWER',
    'TRIFORCE': 'PIECE_OF_POWER',
}

# For generic multi-word matches.
PHRASES = {
    'BIG KEY': 'NIGHTMARE_KEY',
    'BOSS KEY': 'NIGHTMARE_KEY',
    'HEART PIECE': 'HEART_PIECE',
    'PIECE OF HEART': 'HEART_PIECE',
}

# All following will only be used to match items for the specific game.
# Item names will be uppercased when comparing.
# Can be multi-word.
GAME_SPECIFIC_PHRASES = {
    'Final Fantasy': {
        'OXYALE': 'MEDICINE',
        'VORPAL': 'SWORD',
        'XCALBER': 'SWORD',
    },

    'The Legend of Zelda': {
        'WATER OF LIFE': 'MEDICINE',
    },

    'The Legend of Zelda - Oracle of Seasons': {
        'RARE PEACH STONE': 'HEART_PIECE',
    },

    'Noita': {
        'ALL-SEEING EYE': 'TRADING_ITEM_MAGNIFYING_GLASS',  # lets you find secrets
    },

    'Ocarina of Time': {
        'COJIRO': 'ROOSTER',
    },

    'SMZ3': {
        'BIGKEY': 'NIGHTMARE_KEY',
        'BYRNA': 'MAGIC_ROD',
        'HEARTPIECE': 'HEART_PIECE',
        'POWERBOMB': 'BOMB',
        'SOMARIA': 'MAGIC_ROD',
        'SUPER': 'SINGLE_ARROW',
    },

    'Sonic Adventure 2 Battle': {
        'CHAOS EMERALD': 'PIECE_OF_POWER',
    },

    'Super Mario 64': {
        'POWER STAR': 'PIECE_OF_POWER',
    },

    'Super Mario World': {
        'P-BALLOON': 'FEATHER',
    },

    'Super Metroid': {
        'POWER BOMB': 'BOMB',
    },

    'The Witness': {
        'BONK': 'BOMB',
        'BUNKER LASER': 'INSTRUMENT4',
        'DESERT LASER': 'INSTRUMENT5',
        'JUNGLE LASER': 'INSTRUMENT4',
        'KEEP LASER': 'INSTRUMENT7',
        'MONASTERY LASER': 'INSTRUMENT1',
        'POWER SURGE': 'BOMB',
        'PUZZLE SKIP': 'GOLD_LEAF',
        'QUARRY LASER': 'INSTRUMENT8',
        'SHADOWS LASER': 'INSTRUMENT1',
        'SHORTCUTS': 'KEY',
        'SLOWNESS': 'BOMB',
        'SWAMP LASER': 'INSTRUMENT2',
        'SYMMETRY LASER': 'INSTRUMENT6',
        'TOWN LASER': 'INSTRUMENT3',
        'TREEHOUSE LASER': 'INSTRUMENT2',
        'WATER PUMPS': 'KEY',
    },

    'TUNIC': {
        "AURA'S GEM": 'SHIELD',  # card that enhances the shield
        'DUSTY': 'TRADING_ITEM_BROOM',  # a broom
        'HERO RELIC - HP': 'TRADING_ITEM_HIBISCUS',
        'HERO RELIC - MP': 'TOADSTOOL',
        'HERO RELIC - SP': 'FEATHER',
        'HP BERRY': 'GUARDIAN_ACORN',
        'HP OFFERING': 'TRADING_ITEM_HIBISCUS',  # a flower
        'LUCKY CUP': 'HEART_CONTAINER',  # card with a heart on it
        'INVERTED ASH': 'MEDICINE',  # card with a potion on it
        'MAGIC ORB': 'HOOKSHOT',
        'MP BERRY': 'GUARDIAN_ACORN',
        'MP OFFERING': 'TOADSTOOL',  # a mushroom
        'QUESTAGON': 'PIECE_OF_POWER',  # triforce piece equivalent
        'SP OFFERING': 'FEATHER',  # a feather
        'SPRING FALLS': 'TRADING_ITEM_HIBISCUS',  # a flower
    },

    'FNaFW': {
        'Freddy': 'TRADING_ITEM_YOSHI_DOLL', # all of these are animatronics, aka dolls.
        'Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Foxy': 'TRADING_ITEM_YOSHI_DOLL',
        'Toy Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Toy Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Toy Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Mangle': 'TRADING_ITEM_YOSHI_DOLL',
        'Balloon Boy': 'TRADING_ITEM_YOSHI_DOLL',
        'JJ': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom BB': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom Mangle': 'TRADING_ITEM_YOSHI_DOLL',
        'Withered Foxy': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom Foxy': 'TRADING_ITEM_YOSHI_DOLL',
        'Withered Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Withered Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Withered Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Shadow Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Marionette': 'TRADING_ITEM_YOSHI_DOLL',
        'Phantom Marionette': 'TRADING_ITEM_YOSHI_DOLL',
        'Golden Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Paperpals': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare Freddy': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare Foxy': 'TRADING_ITEM_YOSHI_DOLL',
        'Endo 01': 'TRADING_ITEM_YOSHI_DOLL',
        'Endo 02': 'TRADING_ITEM_YOSHI_DOLL',
        'Plushtrap': 'TRADING_ITEM_YOSHI_DOLL',
        'Endoplush': 'TRADING_ITEM_YOSHI_DOLL',
        'Springtrap': 'TRADING_ITEM_YOSHI_DOLL',
        'RWQFSFASXC': 'TRADING_ITEM_YOSHI_DOLL',
        'Crying Child': 'TRADING_ITEM_YOSHI_DOLL',
        'Funtime Foxy': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare Fredbear': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare': 'TRADING_ITEM_YOSHI_DOLL',
        'Fredbear': 'TRADING_ITEM_YOSHI_DOLL',
        'Spring Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Jack-O-Chica': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmare BB': 'TRADING_ITEM_YOSHI_DOLL',
        'Coffee': 'TRADING_ITEM_YOSHI_DOLL',
        'Jack-O-Bonnie': 'TRADING_ITEM_YOSHI_DOLL',
        'Purpleguy': 'TRADING_ITEM_YOSHI_DOLL',
        'Nightmarionne': 'TRADING_ITEM_YOSHI_DOLL',
        'Mr. Chipper': 'TRADING_ITEM_YOSHI_DOLL',
        'Animdude': 'TRADING_ITEM_YOSHI_DOLL',
        'Progressive Endoskeleton': 'BLUE_TUNIC', # basically armor you wear to give you more defense
        '25 Tokens': 'RUPEES_20', # money
        '50 Tokens': 'RUPEES_50',
        '100 Tokens': 'RUPEES_100',
        '250 Tokens': 'RUPEES_200',
        '500 Tokens': 'RUPEES_500',
        '1000 Tokens': 'RUPEES_500',
        '2500 Tokens': 'RUPEES_500',
        '5000 Tokens': 'RUPEES_500',
    },
}
