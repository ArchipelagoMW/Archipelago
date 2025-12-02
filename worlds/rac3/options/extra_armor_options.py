from Options import Choice
from worlds.rac3 import RAC3OPTION


class ExtraArmorUpgrade(Choice):
    """
    Determines how many extra progressive ArmorUpgrade items are included in the item pool. 1~2 is recommended.
    """
    display_name = RAC3OPTION.EXTRA_ARMOR_UPGRADE
    option_no_extra = 0
    option_extra_1 = 1
    option_extra_2 = 2
    option_extra_3 = 3
    option_extra_4 = 4
    default = 0
