from Options import ItemDict
from worlds.rac3 import RAC3ITEM, RAC3OPTION
from worlds.rac3.constants.data.item import filler_data


class FillerWeight(ItemDict):
    """
    Sets the relative weights of filler items in the item pool.
    A higher value increases the likelihood of a particular filler item to appear in the item pool.
    If progressive weapons are enabled, weapon xp automatically gets removed from the pool.
    """
    display_name = RAC3OPTION.FILLER_WEIGHT
    min = 0
    max = 100
    valid_keys = filler_data.keys()
    default = {
        # RAC3ITEM.TITANIUM_BOLT: 0,
        RAC3ITEM.WEAPON_XP: 5,
        RAC3ITEM.PLAYER_XP: 5,
        RAC3ITEM.BOLTS: 10,
        RAC3ITEM.JACKPOT: 10,
    }
