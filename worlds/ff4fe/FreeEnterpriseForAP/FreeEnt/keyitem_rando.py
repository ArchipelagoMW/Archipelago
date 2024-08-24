from . import databases
from . import core_rando
from .rewards import RewardSlot, ItemReward
from .address import *

# vignette time measurements for reference:
#   start time:                1B 0F 00 00  = 39F frames
#   time at end fadeout:       1E C9 00 00
#   locked time after fadeout: 28 CB 00 00  = 2FBC frames

def apply(env):
    # item location assignments are handled by core_rando

    # create a randomized order for displaying the vignette locations
    vignette_slot_order = list(range(1, RewardSlot.MAX_COUNT))
    vignette_slot_order.remove(int(RewardSlot.fixed_crystal))
    env.rnd.shuffle(vignette_slot_order)
    vignette_slot_order.append(0x00)
    env.add_binary(BusAddress(0x21d200), vignette_slot_order, as_script=True)

    # export treasure chest locations for vignettes
    treasure_dbview = databases.get_treasure_dbview()
    chest_vignette_locations = []
    for slot in core_rando.CHEST_ITEM_SLOTS:
        position = env.meta['miab_locations'][slot]
        treasure = treasure_dbview.find_one(lambda t: t.map == position[0] and t.index == position[1])
        vig_map = treasure.map[1:]
        vig_x = treasure.x
        vig_y = treasure.y

        chest_vignette_locations.append('##map.{} {:02X} {:02X}'.format(vig_map, vig_x, vig_y))

    env.add_substitution('miab vignette positions', '\n'.join(chest_vignette_locations))
