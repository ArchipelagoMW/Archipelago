from BaseClasses import ItemClassification

# F71EDB

class CrankyHint():
    type: str
    level: str
    world: str
    bonus: str
    item: str
    classification: int
    player: str

    def __init__(self, type: str, level: str, world: str, bonus: int, item: str, classification: int, player: str):
        self.type = type
        self.level = level[0:20]
        self.world = world[0:20]
        self.bonus = str(bonus)
        self.item = item[0:30]
        self.classification = classification
        self.player = player[0:16]


class WrinklyHint():
    item: str
    location: list
    player: str
    game: str

    def __init__(self, item: str, location: str, player: str, game: str):
        self.item = item[0:30]
        self.player = player[0:16]
        self.location = [
            location[0:30],
            location[30:60],
            location[60:90],
        ]
        self.game = game[0:30]


cranky_location_text = {
    "Clear": [
        [
           #"********************************"
            "",
            "Try beating a level",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Get good and beat",
            "LEVEL",
        ],
        [
           #"********************************"
            "",
            "Don't keep looking at me,",
            "beat LEVEL",
        ],
        [
           #"********************************"
            "",
            "Complete LEVEL",
        ],
        [
           #"********************************"
            "",
            "Use your skills and conquer",
            "LEVEL",
        ],
        [
           #"********************************"
            "",
            "Clear a level",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "A stage at WORLD",
            "needs to be cleared",
        ],
        [
           #"********************************"
            "",
            "LEVEL requires",
            "to be masterfully beaten",
        ],
    ],
    "Bonus": [
        [
           #"********************************"
            "",
            "Complete a bonus somewhere",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Complete bonus NUM somewhere",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "Find and clear the bonus NUM",
            "at LEVEL",
        ],
        [
           #"********************************"
            "",
            "A secret in WORLD",
            "needs to be conquered",
        ],
        [
           #"********************************"
            "",
            "A secret in LEVEL",
            "needs to be found",
        ],
        [
           #"********************************"
            "",
            "Masterfully clear bonus NUM",
            "at LEVEL",
        ],
    ],
    "DK Coin": [
        [
           #"********************************"
            "",
            "Grab one of my giant coins",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Bring me back my token",
            "from LEVEL",
        ],
        [
           #"********************************"
            "",
            "Hey chump! WORLD",
            "has one of my coins. Collect it",
        ],
        [
           #"********************************"
            "",
            "Retrieve a shiny object",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Collect a huge token",
            "at LEVEL",
        ],
        [
           #"********************************"
            "",
            "Obtain LEVEL's",
            "huge coin at WORLD",
        ],
    ],
    "KONG": [
        [
           #"********************************"
            "",
            "Spell your species' name",
            "at LEVEL",
        ],
        [
           #"********************************"
            "",
            "Collect four shiny trinkets",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Learn to properly arrange",
            "letters in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Obtain all letters in",
            "LEVEL",
        ],
        [
           #"********************************"
            "",
            "Keep track of your shiny",
            "objects in WORLD",
        ],
        [
           #"********************************"
            "",
            "Seek four panels which spell",
            "something at WORLD"
        ],
    ],
    "Swanky": [
        [
           #"********************************"
            "",
            "Get along with the Kong",
            "with a big smile",
        ],
        [
           #"********************************"
            "",
            "Complete a trivia",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "",
            "Answer correctly to Swanky",
        ],
        [
           #"********************************"
            "",
            "Answer correctly to Swanky",
            "at WORLD"
        ],
        [
           #"********************************"
            "",
            "Pay up some coins to Swanky",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Swanky at WORLD",
            "wants a few questions answered"
        ],
    ],
    "Banana Coin": [
        [
           #"********************************"
            "",
            "Get yourself a little bit rich",
            "at WORLD",
        ],
        [
           #"********************************"
            "Collect a golden metal",
            "with a banana image",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Bring some cash from",
            "LEVEL",
        ],
    ],
    "Red Balloon": [
        [
           #"********************************"
            "",
            "Get a red balloon",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "Obtain a device with air inside",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "Obtain a device with air inside",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Find a 1-Up balloon",
            "in LEVEL",
        ],
    ],
    "Green Balloon": [
        [
           #"********************************"
            "",
            "Get a green balloon",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "Obtain a round green object",
            "in WORLD",
        ],
        [
           #"********************************"
            "",
            "Obtain a round green object",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Find a 2-Up balloon",
            "in LEVEL",
        ],
    ],
    "Blue Balloon": [
        [
           #"********************************"
            "",
            "Get a blue balloon",
            "in WORLD",
        ],
        [
           #"********************************"
            "The most precious and rare",
            "floating device",
            "from WORLD",
        ],
        [
           #"********************************"
            "The most precious and rare",
            "floating device",
            "from LEVEL",
        ],
        [
           #"********************************"
            "",
            "Find a 3-Up balloon",
            "in LEVEL",
        ],
    ],
    "Banana Bunch": [
        [
           #"********************************"
            "Someone told me that you",
            "need to get some bananas",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Collect a yellow floating",
            "object at WORLD",
        ],
        [
           #"********************************"
            "Collect a delicious floating",
            "that rotates on its own axis",
            "in LEVEL",
        ],
        [
           #"********************************"
            "",
            "Get a bundle of bananas",
            "at WORLD",
        ],
        [
           #"********************************"
            "",
            "Collect a bundle of bananas",
            "at LEVEL",
        ],
    ],
}

cranky_rarity_text = {
    ItemClassification.filler: [
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send a worthless item.",
            "",
            "",
        ],
        [
           #"********************************"
            "to send a worthless item",
            "to PLAYER",
            "",
        ],
    ],
    ItemClassification.useful: [
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send something useful",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something useful.",
            "",
        ],
        [
           #"********************************"
            "to send an item that may be",
            "good enough for someone.",
            "",
        ],
        [
           #"********************************"
            "to make PLAYER",
            "slightly happy.",
            "",
        ],
        [
           #"********************************"
            "to make PLAYER",
            "slightly happy.",
            "",
        ],
    ],
    ItemClassification.progression: [
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send something good",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something good.",
            "",
            "",
        ],
        [
           #"********************************"
            "to send a very much",
            "needed item.",
            "",
        ],
        [
           #"********************************"
            "to send a very much",
            "needed item to",
            "PLAYER",
        ],
    ],
    ItemClassification.trap: [
        [
           #"********************************"
            "to send something goood",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something goood.",
            "",
        ],
        [
           #"********************************"
            "to send something usefull",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something usefull.",
            "",
            "",
        ],
        [
           #"********************************"
            "to send a trap.",
            "",
            "",
        ],
        [
           #"********************************"
            "to send a trap.",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something reallly good.",
            "",
            "",
        ],
        [
           #"********************************"
            "to send something reallly good.",
            "to PLAYER",
            "",
        ],
    ],
    ItemClassification.progression | ItemClassification.useful: [
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send a very much",
            "needed item.",
            "",
        ],
        [
           #"********************************"
            "to send a very much",
            "needed item to",
            "PLAYER",
        ],
    ],
    ItemClassification.progression | ItemClassification.trap: [
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send a questionable but",
            "needed item.",
            "",
        ],
        [
           #"********************************"
            "to send a questionable but",
            "needed item to",
            "PLAYER",
        ],
    ],
    0xFF: [ # Handles weird classifications
        [
           #"********************************"
            "to send",
            "ITEM",
            "",
        ],
        [
           #"********************************"
            "to send",
            "ITEM",
            "to PLAYER",
        ],
        [
           #"********************************"
            "to send something",
            "to PLAYER",
            "",
        ],
        [
           #"********************************"
            "to send something.",
            "",
            "",
        ],
    ]
}

wrinkly_hint_text = [
    [
        #"********************************"
        "",
        "ITEM",
        "can be found at",
        "LOCATION",
    ],
    [
        #"********************************"
        "",
        "",
        "ITEM",
        "is at PLAYER's world",
        "",
        "",
    ],
    [
        #"********************************"
        "",
        "ITEM",
        "is at PLAYER's",
        "LOCATION",
    ],
    [
        #"********************************"
        "",
        "ITEM",
        "is in someone's",
        "GAME",
        "",
        "",
    ],
    [
        #"********************************"
        "",
        "PLAYER's world has",
        "one of your important items at",
        "LOCATION",
    ],
]