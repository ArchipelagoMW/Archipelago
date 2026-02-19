from worlds.factorio_bobs import FactorioModpack, modpacks

# pack_name = "bob's angel's"
pack_name = "baketorio"
# pack_name = "bob's"
# pack_name = "vanilla"

def get_modpack(pn=pack_name) -> FactorioModpack:

    modpack: FactorioModpack = modpacks[pn]
    modpack.init_items()
    modpack.init_locations()
    modpack.init_pack_check()

    return modpack