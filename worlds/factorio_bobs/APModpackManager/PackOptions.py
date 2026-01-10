from dataclasses import dataclass

from Options import PerGameCommonOptions, TextChoice
from worlds.factorio_bobs import modpacks

pack_doc = "\n".join([f"{pack.packName}: {pack.downloadLocation}" for pack in modpacks.values()])

class PackName(TextChoice):
    __doc__ = ("The modpack to be used in game \n"
               f"Installed packs: \n{pack_doc}")
    display_name = "Modpack"

    # dynamically adds options
    locals().update({f"option_{pack_name}": pack_id for pack_id, pack_name in enumerate(modpacks.keys())})

@dataclass
class PackOptions(PerGameCommonOptions):
    """
    This options adds options for pack selection
    """
    packname: PackName