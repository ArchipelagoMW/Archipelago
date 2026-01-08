from collections import Counter
import random

from .game import Game
from .item_data import Item, Items, unique_items
from .location_data import Location, majorLocs, eTankLocs
from .solver import solve

_minor_logic_items = {
    Items.DamageAmp: 6,
    Items.AccelCharge: 6,
    Items.Energy: 16,
    Items.SpaceJumpBoost: 8,
    Items.SmallAmmo: 12,
    Items.LargeAmmo: 18
}
""" minors placed with logic """

_minor_non_logic_items = {
    Items.Refuel: 7,
    Items.SmallAmmo: 26,
}
""" items placed without logic """


def available_major_locations(game: Game) -> list[Location]:
    _, _, locs = solve(game)
    locs = [
        loc
        for loc in locs
        if (loc["fullitemname"] in majorLocs or loc["fullitemname"] in eTankLocs) and loc["item"] is None
    ]
    return locs


def available_minor_locations(game: Game) -> list[Location]:
    _, _, locs = solve(game)
    locs = [
        loc
        for loc in locs
        if (not (loc["fullitemname"] in majorLocs or loc["fullitemname"] in eTankLocs)) and loc["item"] is None
    ]
    return locs


def fill_major_minor(game: Game) -> bool:
    for loc in game.all_locations.values():
        loc["item"] = None

    # if game.options.cypher_items == CypherItems.SmallAmmo:
    #     game.all_locations["Shrine Of The Animate Spark"]["item"] = Items.Energy
    #     game.all_locations["Enervation Chamber"]["item"] = Items.SmallAmmo
    #     # TODO: remove 1 small ammo and 1 etank from item pools
    #     game.item_placement_spoiler += f"Shrine Of The Animate Spark - - - {Items.Energy.name}\n"
    #     game.item_placement_spoiler += f"Enervation Chamber - - - {Items.SmallAmmo.name}\n"

    locs = available_major_locations(game)
    loc = random.choice(locs)
    loc["item"] = Items.Missile
    game.item_placement_spoiler += f"{loc['fullitemname']} - - - {Items.Missile.name}\n"

    locs = available_major_locations(game)
    loc = random.choice(locs)
    loc["item"] = Items.GravityBoots
    game.item_placement_spoiler += f"{loc['fullitemname']} - - - {Items.GravityBoots.name}\n"

    prog_items: list[Item] = sorted(unique_items)  # sort because iterating through set will not be the same every time
    assert len(prog_items) == len(set(prog_items)), "duplicate majors?"
    for it, n in _minor_logic_items.items():
        prog_items.extend([it for _ in range(n)])
    prog_items.remove(Items.Missile)
    prog_items.remove(Items.GravityBoots)

    major_items: Counter[Item] = Counter()
    for item in prog_items:
        if (item in unique_items or item == Items.Energy):
            major_items[item] += 1

    fail_count = 0
    while len(prog_items) and fail_count < 100:
        item = random.choice(prog_items)
        if major_items[Items.Morph] > 0 and random.random() < 0.75:
            item = Items.Morph
        elif major_items[Items.Bombs] > 0 and random.random() < 0.25:
            item = Items.Bombs
        elif major_items[Items.Aqua] > 0 and random.random() < 0.125:
            item = Items.Aqua
        elif major_items[Items.PowerBomb] > 0 and random.random() < 0.125:
            item = Items.PowerBomb
        elif major_items[Items.SpeedBooster] > 0 and random.random() < 0.125:
            item = Items.SpeedBooster
        if (item in unique_items or item == Items.Energy):
            locs = available_major_locations(game)
            if len(locs) == 0:
                return False
            loc = random.choice(locs)
            loc["item"] = item
            after_locs = available_major_locations(game)
            if len(after_locs) == 0 and sum(major_items.values()) > 1:
                loc["item"] = None
                fail_count += 1
                continue
            game.item_placement_spoiler += f"{loc['fullitemname']} - - - {item.name}\n"
            # print(f"DEBUG: {item[0]} placed at {loc['fullitemname']}")
            # print(f"  then: {[lo['fullitemname'] for lo in after_locs]}")
            major_items[item] -= 1
        else:  # not major
            locs = available_minor_locations(game)
            if len(locs) == 0:
                fail_count += 1
                continue
            loc = random.choice(locs)
            loc["item"] = item
            game.item_placement_spoiler += f"{loc['fullitemname']} - - - {item.name}\n"
        prog_items.remove(item)
    if len(prog_items):
        print(f"MM failed with {len(prog_items)} remaining")
        return False

    extra_items: list[Item] = []
    for it, n in _minor_non_logic_items.items():
        extra_items.extend([it for _ in range(n)])

    random.shuffle(extra_items)
    locs = available_minor_locations(game)
    assert len(extra_items) == len(locs), f"{len(extra_items)=}, {len(locs)=}"

    for i in range(len(extra_items)):
        locs[i]["item"] = extra_items[i]
        game.item_placement_spoiler += f"{locs[i]['fullitemname']} - - - {extra_items[i].name}\n"

    completable, _, accessible_locations = solve(game)
    done = completable and len(accessible_locations) == len(game.all_locations)
    if done:
        print("Item placements successful.")
        game.item_placement_spoiler += "Item placements successful.\n"
    return done
