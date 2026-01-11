from enum import Enum, auto
from typing import NamedTuple


class SSHintType(Enum):
    """
    Represents a hint type in Skyward Sword.
    """

    STONE = auto()  # Max 8 hints per stone
    FI = auto()  # Max 64 hints
    SONG = auto()  # Song hints

    ALWAYS = auto()
    SOMETIMES = auto()
    ITEM = auto()
    BARREN = auto()
    JUNK = auto()


class SSHint(NamedTuple):
    """
    Represents a hint in Skyward Sword.
    """

    code: int
    region: str
    type: SSHintType
    checked_flag: list[
        int, int, int
    ]  # [ flag_bit (0x0-0xF), flag_value (0x01-0x80), story flag address (ending in zero)]


class SSLocationHint:
    """
    Represents a location hint in Skyward Sword.
    """

    location: str = ""
    aplocation: str = ""
    region: str = ""
    player_to_receive: str = ""
    item: str = ""

    def __init__(self, loc, world):
        self.location = loc

        # Set aplocation property to handle batreaux's rewards
        if self.location.startswith("Batreaux's House - "):
            if world.get_location(self.location).ogname is None:
                raise Exception(f"OG location name for batreaux reward is none: {self.location}")
            self.aplocation = world.get_location(self.location).ogname
        else:
            self.aplocation = self.location

    def to_stone_text(self) -> str:
        return f"They say that <r<{self.location}>> has <b+<{self.player_to_receive}'s>> <y<{self.item}>>."

    def to_fi_text(self) -> str:
        return f"My readings suggest that <r<{self.location}>> has <b+<{self.player_to_receive}'s>> <y<{self.item}>>."
    
    def to_log_text(self) -> str:
        return f"{self.location} has {self.player_to_receive}'s {self.item}."


class SSItemHint:
    """
    Represents an item hint in Skyward Sword.
    """

    item: str = ""
    player_to_find: str = ""
    location: str = ""
    region: str = ""

    def __init__(self, itm):
        self.item = itm

    def to_stone_text(self) -> str:
        return f"They say that your <y<{self.item}>> can be found by <b+<{self.player_to_find}>> at <r<{self.location}>>."

    def to_fi_text(self) -> str:
        return f"My readings suggest that your <y<{self.item}>> can be found by <b+<{self.player_to_find}>> at <r<{self.location}>>."
    
    def to_log_text(self) -> str:
        return f"Your {self.item} is in {self.player_to_find}'s world at {self.location}."


class SSJunkHint:
    """
    Represents a junk (filler) hint in Skyward Sword
    """

    text: str = ""

    def __init__(self, text):
        self.text = text

    def to_stone_text(self) -> str:
        return self.text

    def to_fi_text(self) -> str:
        return self.text.replace("They say", "I conjecture")
    
    def to_log_text(self) -> str:
        return self.text


HINT_TABLE: dict[str, SSHint] = {
    "Fi Hint": SSHint(
        0,
        None,
        SSHintType.FI,
        [0xD, 0x10, 0x805A9AD0],  # Flag 36 (Tunic)
    ),
    "Central Skyloft - Gossip Stone on Waterfall Island": SSHint(
        1,
        "Central Skyloft",
        SSHintType.STONE,
        [0x3, 0x40, 0x805A9B40],  # Flag 960
    ),
    "Sky - Gossip Stone on Lumpy Pumpkin": SSHint(
        2,
        "Sky",
        SSHintType.STONE,
        [0x3, 0x80, 0x805A9B40],  # Flag 961
    ),
    "Sky - Gossip Stone on Volcanic Island": SSHint(
        3,
        "Sky",
        SSHintType.STONE,
        [0x2, 0x01, 0x805A9B40],  # Flag 962
    ),
    "Sky - Gossip Stone on Bamboo Island": SSHint(
        4,
        "Sky",
        SSHintType.STONE,
        [0x2, 0x02, 0x805A9B40],  # Flag 963
    ),
    "Thunderhead - Gossip Stone near Bug Heaven": SSHint(
        5,
        "Thunderhead",
        SSHintType.STONE,
        [0x2, 0x04, 0x805A9B40],  # Flag 964
    ),
    "Sealed Grounds - Gossip Stone behind the Temple": SSHint(
        6,
        "Sealed Grounds",
        SSHintType.STONE,
        [0x2, 0x08, 0x805A9B40],  # Flag 965
    ),
    "Faron Woods - Gossip Stone in Deep Woods": SSHint(
        7,
        "Faron Woods",
        SSHintType.STONE,
        [0x2, 0x10, 0x805A9B40],  # Flag 966
    ),
    "Lake Floria - Gossip Stone outside Ancient Cistern": SSHint(
        8,
        "Lake Floria",
        SSHintType.STONE,
        [0x2, 0x20, 0x805A9B40],  # Flag 967
    ),
    "Eldin Volcano - Gossip Stone next to Earth Temple": SSHint(
        9,
        "Eldin Volcano",
        SSHintType.STONE,
        [0x2, 0x40, 0x805A9B40],  # Flag 968
    ),
    "Eldin Volcano - Gossip Stone in Thrill Digger Cave": SSHint(
        10,
        "Eldin Volcano",
        SSHintType.STONE,
        [0x2, 0x80, 0x805A9B40],  # Flag 969
    ),
    "Eldin Volcano - Gossip Stone in Lower Platform Cave": SSHint(
        11,
        "Eldin Volcano",
        SSHintType.STONE,
        [0x5, 0x01, 0x805A9B40],  # Flag 970
    ),
    "Eldin Volcano - Gossip Stone in Upper Platform Cave": SSHint(
        12,
        "Eldin Volcano",
        SSHintType.STONE,
        [0x5, 0x02, 0x805A9B40],  # Flag 971
    ),
    "Volcano Summit - Gossip Stone near Second Thirsty Frog": SSHint(
        13,
        "Volcano Summit",
        SSHintType.STONE,
        [0x5, 0x04, 0x805A9B40],  # Flag 972
    ),
    "Volcano Summit - Gossip Stone in Waterfall Area": SSHint(
        14,
        "Volcano Summit",
        SSHintType.STONE,
        [0x5, 0x08, 0x805A9B40],  # Flag 973
    ),
    "Temple of Time - Gossip Stone in Temple of Time Area": SSHint(
        15,
        "Lanayru Desert",
        SSHintType.STONE,
        [0x5, 0x10, 0x805A9B40],  # Flag 974
    ),
    "Lanayru Sand Sea - Gossip Stone in Shipyard": SSHint(
        16,
        "Lanayru Sand Sea",
        SSHintType.STONE,
        [0x5, 0x20, 0x805A9B40],  # Flag 975
    ),
    "Lanayru Caves - Gossip Stone in Center": SSHint(
        17,
        "Lanayru Caves",
        SSHintType.STONE,
        [0x5, 0x40, 0x805A9B40],  # Flag 976
    ),
    "Lanayru Caves - Gossip Stone towards Lanayru Gorge": SSHint(
        18,
        "Lanayru Caves",
        SSHintType.STONE,
        [0x5, 0x80, 0x805A9B40],  # Flag 977
    ),
    "Song of the Hero - Trial Hint": SSHint(
        19,
        None,
        SSHintType.SONG,
        [0x4, 0x01, 0x805A9B40],  # Flag 978
    ),
    "Farore's Courage - Trial Hint": SSHint(
        20,
        None,
        SSHintType.SONG,
        [0x5, 0x80, 0x805A9AE0],  # Flag 71
    ),
    "Nayru's Wisdom - Trial Hint": SSHint(
        21,
        None,
        SSHintType.SONG,
        [0x9, 0x20, 0x805A9AE0],  # Flag 72
    ),
    "Din's Power - Trial Hint": SSHint(
        22,
        None,
        SSHintType.SONG,
        [0x9, 0x40, 0x805A9AE0],  # Flag 73
    ),
}

HINT_DISTRIBUTIONS = {
    "Standard": {
        "fi": 0,
        "hints_per_stone": 2,
        "max_order": 3,
        "distribution": {
            "always": {"order": 0, "weight": 0.0, "fixed": 0, "copies": 1},
            "sometimes": {"order": 1, "weight": 1.0, "fixed": 6, "copies": 1},
            "item": {"order": 2, "weight": 2.0, "fixed": 6, "copies": 1},
            "junk": {"order": 3, "weight": 0.5, "fixed": 0, "copies": 1},
        },
    },
    "Junk": {
        "fi": 0,
        "hints_per_stone": 2,
        "max_order": 0,
        "distribution": {
            "junk": {"order": 0, "weight": 1.0, "fixed": 0, "copies": 1},
        },
    },
}

SONG_HINT_TO_TRIAL_GATE = {
    "Song of the Hero - Trial Hint": "trial_gate_on_skyloft",
    "Farore's Courage - Trial Hint": "trial_gate_in_faron_woods",
    "Nayru's Wisdom - Trial Hint": "trial_gate_in_lanayru_desert",
    "Din's Power - Trial Hint": "trial_gate_in_eldin_volcano",
}

JUNK_HINT_TEXT = [
    "They say that crashing in BiT is easy.",
    "They say that bookshelves can talk",
    "They say that people who love the Bug Net also like Trains",
    "They say that there is a Gossip Stone by the Temple of Time",
    "They say there's a 35% chance for Fire Sanctuary Boss Key to be Heetle Locked",
    "They say 64bit left Fire Sanctuary without learning Ballad of the Goddess",
    "They say that Ancient Cistern is haunted by the ghosts of softlocked Links",
    "They say the Potion Lady is still holding onto a Spiral Charge for CJ",
    "They say there is a chest underneath the party wheel in Lanayru",
    "They say that you need the hero's tunic to sleep on the main part of Skyloft",
    "They say that you need to Hot the Spile to defeat Imprisoned 2",
    "They say whenever Spiral Charge is on a trial, a seed roller goes mysteriously missing",
    "They say that Eldin Trial is vanilla whenever it is required",
    "They say that gymnast86 won the first randomizer tournament and retired immediately after",
    "They say that Mogmas don't understand Minesweeper",
    "They say that you can win a race by abandoning Lanayru to check Cawlin's Letter",
    "They say that tornados spawn frequently in the Sky",
    "They say Scrapper gets easily tilted",
    "They say there is a chest on the cliffs by the Goddess Statue",
    "They say that entering Ancient Cistern with no B items has a 1% chance of success",
    "They say that Glittering Spores are the best bird drugs",
    "They say that the Ancient Automaton fears danger darts",
    "They say the single tumbling plant is required every seed",
    "They say that your battery is low",
    "They say that you just have to get the right checks to win",
    "They say that rushing Peatrice is the play",
    "They say there is a 0.0000001164% chance your RNG won't change",
    "If only we could go Back in Time and name the glitch properly...",
    'They say that there is something called a "hash" that makes it easier for people to verify that they are playing the right seed',
    "They say that the bad seed rollers are still in the car, seeking for a safe refugee",
    "Have you heard the tragedy of Darth Kolok the Pause? I thought not, it's not a story the admins would tell you",
    "Lanayru Sand Sea is the most hated region in the game, because Sand is coarse, rough and gets everywhere",
    "They say that rice has magical properties when visiting Yerbal",
    "They say that Jannon is still jammin to this day",
    "They say that there is only one place where the Slingshot beats the Bow",
    "They say that Koloktos waiting caused a civil war among players",
    "They say that there is a settings combination which needs 0 checks to be completed",
    "They say that avoiding Fledge's item from a fresh file is impossible",
    "... astronomically ...",
    "They say that you can open the chest behind bars in LMF after raising said bars",
    "They say that you look like you have a Questions",
    "They say that HD randomizer development is delayed by a day every time someone asks about it in the Discord",
    "The disc could not be read. Refer to the Wii Operations Manual for details.",
    "They say that a massive storm brews over the Lanayru Sand Sea due to Tentalus' immense size",
]
