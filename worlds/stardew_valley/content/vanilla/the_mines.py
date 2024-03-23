from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data, villagers_data
from ...data.harvest import ForagingSource
from ...strings.forageable_names import Forageable
from ...strings.region_names import Region

the_mines = ContentPack(
    "The Mines (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.cave_carrot: (
            ForagingSource(regions=(Region.mines_floor_10,), requires_hoe=True),
        ),
        Forageable.purple_mushroom: (
            ForagingSource(regions=(Region.mines_floor_95,)),
        )
    },
    fishes=(
        fish_data.ghostfish,
        fish_data.ice_pip,
        fish_data.lava_eel,
        fish_data.stonefish,
    ),
    villagers=(
        villagers_data.dwarf,
    ),
)
