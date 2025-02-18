from .locations.items import *
from .utils import formatText
from BaseClasses import ItemClassification
from ..Locations import LinksAwakeningLocation


hint_text_ids = [
    # Overworld owl statues
    0x1B6, 0x1B7, 0x1B8, 0x1B9, 0x1BA, 0x1BB, 0x1BC, 0x1BD, 0x1BE, 0x22D,

    0x288, 0x280,  # D1
    0x28A, 0x289, 0x281,  # D2
    0x282, 0x28C, 0x28B,  # D3
    0x283,  # D4
    0x28D, 0x284,  # D5
    0x285, 0x28F, 0x28E,  # D6
    0x291, 0x290, 0x286,  # D7
    0x293, 0x287, 0x292,  # D8
    0x263,  # D0

    # Hint books
    0x267,  # color dungeon
    0x201,  # Pre open: 0x200
    0x203,  # Pre open: 0x202
    0x205,  # Pre open: 0x204
    0x207,  # Pre open: 0x206
    0x209,  # Pre open: 0x208
    0x20B,  # Pre open: 0x20A
]

hint_items = (POWER_BRACELET, SHIELD, BOW, HOOKSHOT, MAGIC_ROD, PEGASUS_BOOTS, OCARINA, FEATHER, SHOVEL,
              MAGIC_POWDER, SWORD, FLIPPERS, TAIL_KEY, ANGLER_KEY, FACE_KEY,
              BIRD_KEY, SLIME_KEY, GOLD_LEAF, BOOMERANG, BOWWOW)

hints = [
    "{0} is at {1}",
    "If you want {0} start looking in {1}",
    "{1} holds {0}",
    "They say that {0} is at {1}",
    "You might want to look in {1} for a secret",
]
useless_hint = [
    ("Egg", "Mt. Tamaranch"),
    ("Marin", "Mabe Village"),
    ("Marin", "Mabe Village"),
    ("Witch", "Koholint Prairie"),
    ("Mermaid", "Martha's Bay"),
    ("Nothing", "Tabahl Wasteland"),
    ("Animals", "Animal Village"),
    ("Sand", "Yarna Desert"),
]


def addHints(rom, rnd, hint_texts):
    hint_texts_copy = hint_texts.copy()
    text_ids = hint_text_ids.copy()
    rnd.shuffle(text_ids)
    for text_id in text_ids:
        hint = hint_texts_copy.pop()
        if not hint:
            hint = rnd.choice(hints).format(*rnd.choice(useless_hint))
        rom.texts[text_id] = formatText(hint)

    for text_id in range(0x200, 0x20C, 2):
        rom.texts[text_id] = formatText("Read this book?", ask="YES  NO")


def generate_hint_texts(world):
    JUNK_HINT = 0.33
    RANDOM_HINT= 0.66
    # USEFUL_HINT = 1.0
    # TODO: filter events, filter unshuffled keys
    all_items = world.multiworld.get_items()
    our_items = [item for item in all_items
                 if item.player == world.player
                 and item.location
                 and item.code is not None
                 and item.location.show_in_spoiler]
    our_useful_items = [item for item in our_items if ItemClassification.progression in item.classification]
    hint_texts = []
    def gen_hint():
        chance = world.random.uniform(0, 1)
        if chance < JUNK_HINT:
            return None
        elif chance < RANDOM_HINT:
            location = world.random.choice(our_items).location
        else: # USEFUL_HINT
            location = world.random.choice(our_useful_items).location

        if location.item.player == world.player:
            name = "Your"
        else:
            name = f"{world.multiworld.player_name[location.item.player]}'s"
            # filter out { and } since they cause issues with string.format later on
            name = name.replace("{", "").replace("}", "")

        if isinstance(location, LinksAwakeningLocation):
            location_name = location.ladxr_item.metadata.name
        else:
            location_name = location.name

        hint = f"{name} {location.item} is at {location_name}"
        if location.player != world.player:
            # filter out { and } since they cause issues with string.format later on
            player_name = world.multiworld.player_name[location.player].replace("{", "").replace("}", "")
            hint += f" in {player_name}'s world"

        # Cap hint size at 85
        # Realistically we could go bigger but let's be safe instead
        hint = hint[:85]
        return hint
    for _ in hint_text_ids:
        hint_texts.append(gen_hint())
    return hint_texts
