from BaseClasses import ItemClassification
from worlds.dc1.Items import DarkCloudItem
from worlds.dc1.Options import DarkCloudOptions

ids = {
    "Progressive Ruty's Store": 971110300,
    "Progressive Suzy's Store": 971110301,
    "Progressive Lana's Store": 971110302,
    "Progressive Jack's Store": 971110303,
    "Progressive Joker's House": 971110304,
    "Progressive Divining House": 971110305,
    "Progressive Cathedral": 971110306,
    "Progressive Basker's Store": 971110307,
    "Progressive King's Hideout": 971110308,
    "Progressive Sheriff's Office": 971110309,
    "Progressive Fountain": 971110310,
    "Progressive Leaning Tower": 971110311,
    "Queens Trees": 971110312,
    "Queens Road": 971110313
  }

king_ids = ["Progressive King's Hideout", "Progressive King's Hideout", "Progressive King's Hideout",
            "Progressive King's Hideout", "Progressive King's Hideout", "Progressive King's Hideout",
            "Progressive King's Hideout"]
cathedral_ids = ["Progressive Cathedral", "Progressive Cathedral", "Progressive Cathedral",
                 "Progressive Cathedral"]
joker_ids = ["Progressive Joker's House", "Progressive Joker's House",
             "Progressive Joker's House", "Progressive Joker's House", "Progressive Joker's House"]

# Note for MCs: Ruty has an ice gem in the middle fish cart
ruty_ids = ["Progressive Ruty's Store", "Progressive Ruty's Store",
            "Progressive Ruty's Store", "Progressive Ruty's Store"]
suzy_ids = ["Progressive Suzy's Store", "Progressive Suzy's Store", "Progressive Suzy's Store"]
lana_ids = ["Progressive Lana's Store", "Progressive Lana's Store"]
jack_ids = ["Progressive Jack's Store",
            "Progressive Jack's Store","Progressive Jack's Store", "Progressive Jack's Store",
            "Progressive Jack's Store"]
basker_ids = ["Progressive Basker's Store",
              "Progressive Basker's Store", "Progressive Basker's Store", "Progressive Basker's Store",
              "Progressive Basker's Store"]
sheriff_ids = ["Progressive Sheriff's Office", "Progressive Sheriff's Office",
               "Progressive Sheriff's Office", "Progressive Sheriff's Office", "Progressive Sheriff's Office",
               "Progressive Sheriff's Office"]
fountain_ids = ["Progressive Fountain", "Progressive Fountain", "Progressive Fountain"]
tower_ids = ["Progressive Leaning Tower", "Progressive Leaning Tower"]

other_ids = ["Queens Trees", "Queens Trees", "Queens Road", "Queens Road",
             "Queens Road", "Queens Road", "Queens Road", "Queens Road"]

# TODO split these lists into 2 based on items that spawn from the first half of a dungeon or the second
# Atla that give MCs by content quality (unless handled otherwise). If MC shuffle is on, these all need to be required
# Sheriff completion is required for Joker's house access inside, yielding a fruit o eden
mc_useful = ["Progressive Suzy's Store", "Progressive Suzy's Store", "Progressive Lana's Store",
             "Progressive Lana's Store", "Progressive Sheriff's Office", "Progressive Basker's Store",
             "Progressive Fountain", "Progressive Leaning Tower", ] + sheriff_ids + joker_ids
mc_filler = ["Progressive Ruty's Store", "Progressive Suzy's Store", "Progressive Lana's Store","Progressive Basker's Store", ]

# Always required/useful/filler items
# Jack's Store has a parfait
required = king_ids + ["Progressive Jack's Store", "Progressive Jack's Store", "Progressive Joker's House", "Progressive Cathedral"]
useful = jack_ids + suzy_ids + ruty_ids
filler = other_ids + fountain_ids + tower_ids + lana_ids + basker_ids


def create_queens_atla(options: DarkCloudOptions, player: int) -> list["DarkCloudItem"]:
    """Create atla items for Norune Village based on option settings."""
    items = []

    queens_required = required.copy()
    queens_useful = useful.copy()
    queens_filler = filler.copy()

    if options.boss_goal == 3 or options.all_bosses:
        queens_required.extend(["Progressive Divining House", "Progressive Divining House", "Progressive Divining House", "Progressive Divining House"])
    else:
        if options.miracle_sanity:
            queens_required.extend(["Progressive Divining House", "Progressive Divining House"])
        else:
            queens_useful.extend(["Progressive Divining House", "Progressive Divining House"])
        queens_filler.extend(["Progressive Divining House", "Progressive Divining House"])

    if options.all_bosses or options.boss_goal == 3:
        queens_required.extend(cathedral_ids)
    else:
        queens_filler.extend(cathedral_ids)

    if options.miracle_sanity:
        queens_required.extend(mc_useful)
        queens_required.extend(mc_filler)
    else:
        queens_useful.extend(mc_useful)
        queens_filler.extend(mc_filler)

    for i in queens_required:
        items.append(DarkCloudItem(i, ItemClassification.progression, ids[i], player))

    for i in queens_useful:
        items.append(DarkCloudItem(i, ItemClassification.useful, ids[i], player))

    for i in queens_filler:
        items.append(DarkCloudItem(i, ItemClassification.filler, ids[i], player))

    # print(len(items))
    # print (items)
    return items

