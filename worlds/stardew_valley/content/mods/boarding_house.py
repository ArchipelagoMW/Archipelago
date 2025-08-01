from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data
from ...mods.mod_data import ModNames

register_mod_content_pack(ContentPack(
    ModNames.boarding_house,
    villagers=(
        villagers_data.gregory,
        villagers_data.sheila,
        villagers_data.joel,
    )
))
