import typing
from random import Random

from BaseClasses import Location, Item
from .Locations import major_location_names

if typing.TYPE_CHECKING:
    from . import MetroidFusionWorld

items_to_hint = [
	'Missile Data',	'Morph Ball', 'Charge Beam', 'Level 1 Keycard',	'Bomb Data',
	'Hi-Jump', 'Speed Booster',	'Level 2 Keycard', 'Super Missile',	'Varia Suit',
	'Level 3 Keycard', 'Ice Missile', 'Power Bomb Data', 'Space Jump', 'Plasma Beam',
	'Gravity Suit',	'Level 4 Keycard', 'Diffusion Missile',	'Wave Beam', 'Screw Attack', 'Ice Beam'
]

class HintedPair():
    location: Location
    item: Item

    def __init__(self, location: Location, item: Item):
        self.location = location
        self.item = item

    def __eq__(self, other: "HintedPair"):
        return self.location == other.location

    def __hash__(self):
        return hash((self.location.name, self.item.name))

def build_hint_text(world: "MetroidFusionWorld", hinted_pair: HintedPair):
    if world.player == hinted_pair.item.player:
        item_text = f"Your [COLOR=3]{hinted_pair.item.name}[/COLOR]"
    else:
        item_text = (f"[COLOR=4]{world.multiworld.get_player_name(hinted_pair.item.player)}'s[/COLOR] "
                     f"[COLOR=3]{hinted_pair.item.name}[/COLOR]")
    if world.player == hinted_pair.location.player:
        location_text = f"your [COLOR=2]{hinted_pair.location.name}[/COLOR]"
    else:
        location_text = (f"[COLOR=4]{world.multiworld.get_player_name(hinted_pair.location.player)}'s[/COLOR] "
                         f"[COLOR=2]{hinted_pair.location.name}[/COLOR]")
    return f"{item_text} can be found at {location_text}."

def create_hints(world: "MetroidFusionWorld") -> tuple[list[str], list[HintedPair]]:
    hinted_pairs: set[HintedPair] = set()

    hinted_locations = world.random.sample(major_location_names, 5)
    for location in hinted_locations:
        location_object = world.get_location(location)
        item_object = location_object.item
        hinted_pairs.add(HintedPair(location_object, item_object))

    hinted_items = world.random.sample(items_to_hint, 5)
    for item in hinted_items:
        locations = world.multiworld.find_item_locations(item, world.player)
        if len(locations) > 0:
            location_object = locations[0]
            item_object = location_object.item
            hinted_pairs.add(HintedPair(location_object, item_object))

    while len(hinted_pairs) < 11:
        new_location = world.random.choice(sorted(list(world.get_locations())))
        if new_location.address is not None:
            new_pair = HintedPair(new_location, new_location.item)
            hinted_pairs.add(new_pair)

    hinted_pair_list = list(hinted_pairs)
    hinted_pair_list.sort(key=lambda pair: pair.location.name)
    world.random.shuffle(hinted_pair_list)
    hint_texts = []
    for pair in hinted_pair_list:
        hint_texts.append(build_hint_text(world, pair))
    return hint_texts, hinted_pair_list