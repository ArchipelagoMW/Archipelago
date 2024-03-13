from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data, fish_data
from ...mods.mod_data import ModNames

register_mod_content_pack(ContentPack(
    ModNames.distant_lands,
    fishes=(
        fish_data.void_minnow,
        fish_data.purple_algae,
        fish_data.swamp_leech,
        fish_data.giant_horsehoe_crab,
    ),
    villagers=(
        villagers_data.zic,
    )
))
