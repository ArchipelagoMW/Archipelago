from worlds.factorio_bobs import FactorioModpack, modpacks
from worlds.factorio_bobs.packDevUtils.Packname import pack_name


def get_modpack(pn=pack_name) -> FactorioModpack:

    modpack: FactorioModpack = modpacks[pn]
    modpack.init_items()
    modpack.init_locations()
    modpack.init_pack_check()

    return modpack