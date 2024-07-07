from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ...data import villagers_data
from ...data.harvest import ForagingSource
from ...data.requirement import QuestRequirement
from ...mods.mod_data import ModNames
from ...strings.quest_names import ModQuest
from ...strings.region_names import Region
from ...strings.seed_names import DistantLandsSeed


class AlectoContentPack(ContentPack):

    def harvest_source_hook(self, content: StardewContent):
        if ModNames.distant_lands in content.registered_packs:
            content.game_items.pop(DistantLandsSeed.void_mint)
            content.game_items.pop(DistantLandsSeed.vile_ancient_fruit)
            content.source_item(DistantLandsSeed.void_mint,
                                ForagingSource(regions=(Region.witch_swamp,), other_requirements=(QuestRequirement(ModQuest.WitchOrder),)),),
            content.source_item(DistantLandsSeed.vile_ancient_fruit,
                                ForagingSource(regions=(Region.witch_swamp,), other_requirements=(QuestRequirement(ModQuest.WitchOrder),)), ),


register_mod_content_pack(ContentPack(
    ModNames.alecto,
    weak_dependencies=(
        ModNames.distant_lands,  # For Witch's order
    ),
    villagers=(
        villagers_data.alecto,
    )

))
