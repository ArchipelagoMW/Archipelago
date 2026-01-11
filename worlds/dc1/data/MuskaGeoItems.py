from typing import List

from BaseClasses import ItemClassification
from worlds.dc1.Items import DarkCloudItem
from worlds.dc1.Options import DarkCloudOptions

ids = {
    "Progressive Chief's House": 971110400,
    "Progressive Jibubu's House": 971110401,
    "Progressive Zabo's House": 971110402,
    "Progressive 3 Sisters' House": 971110403,
    "Progressive Brooke's House": 971110404,
    "Progressive Enga's House": 971110405,
    "Progressive Prisoner Cabin": 971110406,
    "Progressive Toto's House": 971110407,
    "Progressive Totem Pole A": 971110408,
    "Progressive Totem Pole B": 971110409,
    "Progressive Totem Pole C": 971110410,
    "Progressive Oasis": 971110411,
    "Muska Lacka Trees": 971110412,
    "Muska Lacka Road": 971110413
  }

# Required for Ungaga
sister_ids = ["Progressive 3 Sisters' House", "Progressive 3 Sisters' House", "Progressive 3 Sisters' House",
              "Progressive 3 Sisters' House", "Progressive 3 Sisters' House", "Progressive 3 Sisters' House",
              "Progressive 3 Sisters' House"]

# 3 required for boss fight
chief_ids = ["Progressive Chief's House", "Progressive Chief's House",
             "Progressive Chief's House", "Progressive Chief's House"]
zabo_ids = ["Progressive Zabo's House", "Progressive Zabo's House", "Progressive Zabo's House",
            "Progressive Zabo's House", "Progressive Zabo's House"]
enga_ids = ["Progressive Enga's House", "Progressive Enga's House", "Progressive Enga's House",
            "Progressive Enga's House", "Progressive Enga's House", "Progressive Enga's House"]

jibubu_ids = ["Progressive Jibubu's House", "Progressive Jibubu's House",
              "Progressive Jibubu's House", "Progressive Jibubu's House"]
brooke_ids = ["Progressive Brooke's House", "Progressive Brooke's House",
              "Progressive Brooke's House", "Progressive Brooke's House"]
toto_ids = ["Progressive Toto's House", "Progressive Toto's House", "Progressive Toto's House",
            "Progressive Toto's House", "Progressive Toto's House"]

prisoner_ids = ["Progressive Prisoner Cabin", "Progressive Prisoner Cabin",
                "Progressive Prisoner Cabin", "Progressive Prisoner Cabin"]
oasis_ids = ["Progressive Oasis", "Progressive Oasis", "Progressive Oasis"]
totem_ids = ["Progressive Totem Pole A", "Progressive Totem Pole B", "Progressive Totem Pole C",
             "Progressive Totem Pole A", "Progressive Totem Pole B", "Progressive Totem Pole C"]
misc_ids = ["Muska Lacka Trees", "Muska Lacka Trees", "Muska Lacka Road", "Muska Lacka Road",
            "Muska Lacka Road", "Muska Lacka Road", "Muska Lacka Road"]


mc_required = ["Progressive Chief's House", "Progressive Enga's House", "Progressive Toto's House"]
mc_useful = ["Progressive Jibubu's House", "Progressive Jibubu's House", "Progressive Brooke's House",
             "Progressive Prisoner Cabin", "Progressive Oasis"]
mc_filler = ["Progressive Totem Pole A", "Progressive Totem Pole B", "Progressive Totem Pole C"]


required = sister_ids
# Jibubu gives fruit of eden, Brooke runs a shop, Toto gives a nice sword
useful = jibubu_ids + brooke_ids + toto_ids
filler = prisoner_ids + oasis_ids + totem_ids + misc_ids

def create_muska_atla(options: DarkCloudOptions, player: int) -> List["DarkCloudItem"]:
    items = []
    
    muska_required = required.copy() + mc_required.copy()
    muska_useful = useful.copy()
    muska_filler = filler.copy()

    if options.boss_goal == 4 or options.all_bosses:
        muska_required.extend(chief_ids + zabo_ids + enga_ids + ["Progressive Zabo's House"])
    else:
        if options.miracle_sanity:
            muska_required.append("Progressive Zabo's House")
        else:
            muska_useful.append("Progressive Zabo's House")
        muska_filler.extend(chief_ids)
        # Zabo gives Double Impact, Enga a buster sword + storage
        muska_useful.extend(zabo_ids + enga_ids)

    if options.miracle_sanity:
        muska_required.extend(mc_useful)
        muska_required.extend(mc_filler)
    else:
        muska_useful.extend(mc_useful)
        muska_filler.extend(mc_filler)

    for i in muska_required:
        items.append(DarkCloudItem(i, ItemClassification.progression, ids[i], player))

    for i in muska_useful:
        items.append(DarkCloudItem(i, ItemClassification.useful, ids[i], player))

    for i in muska_filler:
        items.append(DarkCloudItem(i, ItemClassification.filler, ids[i], player))

    # print(len(items))
    # print (items)
    return items

