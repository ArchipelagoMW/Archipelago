from worlds.dc1.Options import DarkCloudOptions
from BaseClasses import ItemClassification
from worlds.dc1.Items import DarkCloudItem

ids = {
    "Progressive Pao's House": 971110200,
    "Progressive Cacao's House": 971110201,
    "Progressive Bunbuku's House": 971110202,
    "Progressive Kye's House": 971110203,
    "Progressive Baron's House": 971110204,
    "Progressive Couscous's House": 971110205,
    "Progressive Gob's House": 971110206,
    "Progressive Mushroom House": 971110207,
    "Progressive Well 1": 971110208,
    "Progressive Well 2": 971110209,
    "Progressive Well 3": 971110210,
    "Progressive Watermill 1": 971110211,
    "Progressive Watermill 2": 971110212,
    "Progressive Watermill 3": 971110213,
    "Progressive Owl Shop": 971110214,
    "Matataki Trees": 971110215,
    "Progressive Matataki River": 971110216,
    "Matataki Bridge": 971110217,
    "Earth A": 971110218,
    "Earth B": 971110219,
  }

cacao_ids = ["Progressive Cacao's House", "Progressive Cacao's House", "Progressive Cacao's House",
             "Progressive Cacao's House", "Progressive Cacao's House", "Progressive Cacao's House",
             "Progressive Cacao's House"]
mush_ids = ["Progressive Mushroom House", "Progressive Mushroom House", "Progressive Mushroom House",
            "Progressive Mushroom House", "Progressive Mushroom House"]
# Two pieces are needed to reach all MCs in the house, one for the second half of the dungeon
mush_ids_mc = ["Progressive Mushroom House"]
mush_ids_mc2 = ["Progressive Mushroom House"]

pao_ids = ["Progressive Pao's House",
           "Progressive Pao's House", "Progressive Pao's House", "Progressive Pao's House"]

baron_ids = ["Progressive Baron's House", "Progressive Baron's House", "Progressive Baron's House",
             "Progressive Baron's House", "Progressive Baron's House"]

bunbuku_ids = ["Progressive Bunbuku's House", "Progressive Bunbuku's House",
               "Progressive Bunbuku's House", "Progressive Bunbuku's House"]

kye_ids = ["Progressive Kye's House", "Progressive Kye's House", "Progressive Kye's House", "Progressive Kye's House"]

# Fruit and gourd, rest is filler (rewards aren't that great)
couscous_ids = ["Progressive Couscous's House", "Progressive Couscous's House",
                "Progressive Couscous's House", "Progressive Couscous's House"]

# House has a fruit, house reward is a weapon for goro so marking the whole thing useful except for MCs
gob_ids = ["Progressive Gob's House", "Progressive Gob's House",
           "Progressive Gob's House", "Progressive Gob's House", "Progressive Gob's House"]

# Inside has a gourd, so first 2 pieces are minimum useful.  Reward is a shop so the rest useful
owl_ids = ["Progressive Owl Shop", "Progressive Owl Shop", "Progressive Owl Shop", "Progressive Owl Shop"]
well_ids = ["Progressive Well 1","Progressive Well 1", "Progressive Well 1", "Progressive Well 1", "Progressive Well 1",
            "Progressive Well 2","Progressive Well 2", "Progressive Well 2", "Progressive Well 2", "Progressive Well 2",
            "Progressive Well 3","Progressive Well 3", "Progressive Well 3", "Progressive Well 3", "Progressive Well 3"]

# Each watermill has MCs, 2 have gourds
watermill_ids = ["Progressive Watermill 1", "Progressive Watermill 1", "Progressive Watermill 2",
                 "Progressive Watermill 2", "Progressive Watermill 3", "Progressive Watermill 3",]

# Only 5 are required for progression, could take 3 out as useful?
river_ids = ["Progressive Matataki River", "Progressive Matataki River", "Progressive Matataki River", "Progressive Matataki River",
             "Progressive Matataki River", "Progressive Matataki River", "Progressive Matataki River", "Progressive Matataki River"]
other_ids = ["Matataki Trees", "Matataki Trees", "Matataki Bridge"]


# Atla that give MCs by content quality (unless handled otherwise). If MC shuffle is on, these all need to be required
mc_useful = ["Progressive Owl Shop", "Progressive Owl Shop",
             "Progressive Bunbuku's House",
             "Progressive Baron's House", "Progressive Pao's House", "Progressive Pao's House", ]
mc_filler = ["Progressive Watermill 1", "Progressive Bunbuku's House", ]

mc_useful_2 = ["Progressive Kye's House", "Progressive Kye's House", "Progressive Kye's House",
               "Progressive Couscous's House", "Progressive Gob's House",
               "Progressive Watermill 2", "Progressive Watermill 3", ]
mc_filler_2 = ["Progressive Bunbuku's House",]
# Always required/useful/filler items
required = river_ids + cacao_ids
useful = pao_ids + baron_ids + gob_ids + owl_ids
filler = ["Earth A", "Earth B"] + other_ids + bunbuku_ids + couscous_ids + kye_ids + watermill_ids + well_ids


def create_matataki_atla(options: DarkCloudOptions, player: int) -> list["DarkCloudItem"]:
    """Create atla items for Matataki Village based on option settings."""

    items = []

    matataki_required = required.copy()
    matataki_useful = useful.copy()
    matataki_filler = filler.copy()

    # Mush house is only full required if Utan is required
    if options.all_bosses or options.boss_goal == 2:
        matataki_required.extend(mush_ids)
        matataki_required.extend(mush_ids_mc)
        matataki_required.extend(mush_ids_mc2)
    else:
        matataki_useful.extend(mush_ids)
        if options.miracle_sanity:
            matataki_required.extend(mush_ids_mc)
            matataki_required.extend(mush_ids_mc2)
        else:
            matataki_useful.extend(mush_ids_mc)
            matataki_useful.extend(mush_ids_mc2)

    if options.miracle_sanity:
        matataki_required.extend(mc_useful)
        matataki_required.extend(mc_useful_2)
        matataki_required.extend(mc_filler)
        matataki_required.extend(mc_filler_2)
    else:
        matataki_useful.extend(mc_useful)
        matataki_useful.extend(mc_useful_2)
        matataki_filler.extend(mc_filler)
        matataki_filler.extend(mc_filler_2)

    for i in matataki_required:
        items.append(DarkCloudItem(i, ItemClassification.progression, ids[i], player))

    for i in matataki_useful:
        items.append(DarkCloudItem(i, ItemClassification.useful, ids[i], player))

    for i in matataki_filler:
        items.append(DarkCloudItem(i, ItemClassification.filler, ids[i], player))

    return items
