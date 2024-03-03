from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ..override import override
from ..vanilla.ginger_island import ginger_island as ginger_island_content_pack
from ...data import villagers_data
from ...mods.mod_data import ModNames


class SVEContentPack(ContentPack):

    def villager_hook(self, content: StardewContent):
        # Remove lance if Ginger Island is not in content
        if ginger_island_content_pack.name not in content.registered_packs:
            content.villagers.pop(villagers_data.lance.name)


register_mod_content_pack(SVEContentPack(
    ModNames.sve,
    weak_dependencies=(
        ginger_island_content_pack.name,
        ModNames.jasper,  # To override Marlon and Gunther
    ),
    villagers=(
        villagers_data.claire,
        villagers_data.lance,
        villagers_data.mommy,
        villagers_data.sophia,
        villagers_data.victor,
        villagers_data.andy,
        villagers_data.apples,
        villagers_data.gunther,
        villagers_data.martin,
        villagers_data.marlon,
        villagers_data.morgan,
        villagers_data.scarlett,
        villagers_data.susan,
        villagers_data.morris,
        override(villagers_data.wizard, bachelor=True, mod_name=ModNames.sve),
    )
))
