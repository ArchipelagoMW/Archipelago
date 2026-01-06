from dataclasses import dataclass

from Options import PerGameCommonOptions, FreeText


class PackName(FreeText): #todo autopopulate with loaded packs
    """
    enter modpack name here
    Integrated packs: ["Vanilla", "Bob's"]
    """
    display_name = "Modpack"
    default = "Bob's"

@dataclass
class PackOptions(PerGameCommonOptions):
    """
    This options adds options for pack selection
    """
    packname: PackName