from .ginger_island import ginger_island_content_pack as ginger_island_content_pack
from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack, StardewContent
from ...data import fish_data
from ...data.game_item import GenericSource, ItemTag
from ...data.harvest import HarvestCropSource
from ...strings.crop_names import Fruit
from ...strings.region_names import Region
from ...strings.seed_names import Seed


class QiBoardContentPack(ContentPack):
    def harvest_source_hook(self, content: StardewContent):
        content.untag_item(Seed.qi_bean, ItemTag.CROPSANITY_SEED)


qi_board_content_pack = QiBoardContentPack(
    "Qi Board (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
        ginger_island_content_pack.name,
    ),
    harvest_sources={
        # This one is a bit special, because it's only available during the special order, but it can be found from like, everywhere.
        Seed.qi_bean: (GenericSource(regions=(Region.qi_walnut_room,)),),
        Fruit.qi_fruit: (HarvestCropSource(seed=Seed.qi_bean),),
    },
    fishes=(
        fish_data.ms_angler,
        fish_data.son_of_crimsonfish,
        fish_data.glacierfish_jr,
        fish_data.legend_ii,
        fish_data.radioactive_carp,
    )
)
