from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data, villagers_data
from ...data.harvest import ForagingSource
from ...strings.forageable_names import Forageable
from ...strings.region_names import Region

the_desert = ContentPack(
    "The Desert (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.cactus_fruit: (
            ForagingSource(regions=(Region.desert,)),
        ),
        Forageable.coconut: (
            ForagingSource(regions=(Region.desert,)),
        ),
        Forageable.purple_mushroom: (
            ForagingSource(regions=(Region.skull_cavern_25,)),
        )
    },
    fishes=(
        fish_data.sandfish,
        fish_data.scorpion_carp,
    ),
    villagers=(
        villagers_data.sandy,
    ),
)
