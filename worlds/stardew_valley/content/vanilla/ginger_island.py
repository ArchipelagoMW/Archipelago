from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import villagers_data, fish_data
from ...data.harvest import ForagingSource
from ...strings.forageable_names import Forageable
from ...strings.region_names import Region

ginger_island_content_pack = ContentPack(
    "Ginger Island (Vanilla)",
    weak_dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.dragon_tooth: (
            ForagingSource(regions=(Region.volcano_floor_10,)),
        ),
        Forageable.ginger: (
            ForagingSource(regions=(Region.island_west,)),
        ),
        Forageable.magma_cap: (
            ForagingSource(regions=(Region.volcano_floor_5,)),
        ),
    },
    fishes=(
        # TODO override region so no need to add inaccessible regions in logic
        fish_data.blue_discus,
        fish_data.lionfish,
        fish_data.midnight_carp,
        fish_data.pufferfish,
        fish_data.stingray,
        fish_data.super_cucumber,
        fish_data.tilapia,
        fish_data.tuna
    ),
    villagers=(
        villagers_data.leo,
    )
)
