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
    for text_id, hint in hint_texts.items():
        if not hint:
            hint = rnd.choice(hints).format(*rnd.choice(useless_hint))
        formatted = formatText(hint, skip_names=True)
        if len(formatted) > 97:
            formatted = formatted[:96] + formatted[-1:]
        rom.texts[int(text_id)] = formatted

    for text_id in range(0x200, 0x20C, 2):
        rom.texts[text_id] = formatText("Read this book?", ask="YES  NO")


def generate_hint_texts(world):
    our_items = [
        location.item for location in world.multiworld.get_filled_locations()
        if location.item.player == world.player
        and not location.is_event
        and not location.locked
        and not location.item.name in world.options.in_game_hint_excluded_items
    ]
    world.random.shuffle(our_items)
    our_items.sort(key=lambda item: item.name in world.options.in_game_hint_priority_items)

    hint_data = {}
    def gen_hint(i):
        if i >= world.options.in_game_hint_count or not our_items:
            return None
        else:
            item = our_items.pop()

        if isinstance(item.location, LinksAwakeningLocation):
            location_name = item.location.ladxr_item.metadata.name
        else:
            location_name = item.location.name

        hint = f"Your {item.name} is at {location_name}"
        if item.location.player != world.player:
            player_name = world.multiworld.player_name[item.location.player]
            hint += f" in {player_name}'s world."
        else:
            hint += " in your world."

        return {
            "text": hint,
            "location": item.location.address,
            "player": item.location.player,
        }
    text_ids = hint_text_ids.copy()
    world.random.shuffle(text_ids)
    for i, text_id in enumerate(text_ids):
        hint_data[str(text_id)] = gen_hint(i)
    return hint_data
