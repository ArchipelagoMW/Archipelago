from typing import Dict

from worlds.AutoWorld import World
from worlds.yugioh06.boosterpacks_data import booster_pack_data
from worlds.yugioh06.logic import get_cards_in_first_pack
from .card_data import cards

all_rarities = [
    "Common",
    "Rare",
    "Super Rare",
    "Ultra Rare",
    "Secret Rare"
]


def create_chaos_packs(world: World):
    beater_in_first_pack = get_cards_in_first_pack(world, "Beaters")
    monster_removal_in_first_pack = get_cards_in_first_pack(world, "Monster Removal")
    backrow_removal_in_first_pack = get_cards_in_first_pack(world, "Backrow Removal")

    all_cards = list(cards.keys())
    pack_data = dict(booster_pack_data)
    forced_placements = set(world.progression_cards_in_booster)
    packs: Dict[str, Dict[str, str]] = {}
    starting_booster_name = world.starting_booster
    starting_booster_contents = {}
    # place beaters and removal to start with
    for card in beater_in_first_pack:
        starting_booster_contents[card] = "Common"
        forced_placements.remove(card)
    for card in monster_removal_in_first_pack:
        starting_booster_contents[card] = "Common"
        forced_placements.remove(card)
    for card in backrow_removal_in_first_pack:
        starting_booster_contents[card] = "Common"
        forced_placements.remove(card)
    packs[starting_booster_name] = starting_booster_contents

    # place all progression items
    for c in forced_placements:
        in_pack = world.random.choice(list(pack_data.keys()))
        if in_pack in packs:
            secrets_in_pack = len([r for r in packs[in_pack].values() if r == "Secret Rare"])
            ultras_in_pack = len([r for r in packs[in_pack].values() if r == "Ultra Rare"])
            supers_in_pack = len([r for r in packs[in_pack].values() if r == "Super Rare"])
            rares_in_pack = len([r for r in packs[in_pack].values() if r == "Rare"])
            commons_in_pack = len([r for r in packs[in_pack].values() if r == "Common"])
        else:
            secrets_in_pack = 0
            ultras_in_pack = 0
            supers_in_pack = 0
            rares_in_pack = 0
            commons_in_pack = 0
            packs[in_pack] = {}
        rarity = world.random.choices(all_rarities, [
            pack_data[in_pack].commons - commons_in_pack,
            pack_data[in_pack].rares - rares_in_pack,
            pack_data[in_pack].super_rares - supers_in_pack,
            pack_data[in_pack].ultra_rares - ultras_in_pack,
            pack_data[in_pack].secret_rares - secrets_in_pack,
        ])[0]
        packs[in_pack][c] = rarity

    # choose the rest at random
    for in_pack, data in pack_data.items():
        if in_pack in packs:
            secrets_in_pack = len([r for r in packs[in_pack].values() if r == "Secret Rare"])
            ultras_in_pack = len([r for r in packs[in_pack].values() if r == "Ultra Rare"])
            supers_in_pack = len([r for r in packs[in_pack].values() if r == "Super Rare"])
            rares_in_pack = len([r for r in packs[in_pack].values() if r == "Rare"])
            commons_in_pack = len([r for r in packs[in_pack].values() if r == "Common"])
            cards_placed = len(packs[in_pack])
        else:
            secrets_in_pack = 0
            ultras_in_pack = 0
            supers_in_pack = 0
            rares_in_pack = 0
            commons_in_pack = 0
            cards_placed = 0
            packs[in_pack] = {}
        for i in range(0, data.cards_in_set - cards_placed):
            rarity = world.random.choices(all_rarities, [
                pack_data[in_pack].commons - commons_in_pack,
                pack_data[in_pack].rares - rares_in_pack,
                pack_data[in_pack].super_rares - supers_in_pack,
                pack_data[in_pack].ultra_rares - ultras_in_pack,
                pack_data[in_pack].secret_rares - secrets_in_pack,
            ])[0]
            if rarity == "Common":
                commons_in_pack += 1
            elif rarity == "Rare":
                rares_in_pack += 1
            elif rarity == "Super Rare":
                supers_in_pack += 1
            elif rarity == "Ultra Rare":
                ultras_in_pack += 1
            elif rarity == "Secret Rare":
                secrets_in_pack += 1
            card = world.random.choice([con for con in all_cards if con not in packs[in_pack]])
            packs[in_pack][card] = rarity
    return packs
