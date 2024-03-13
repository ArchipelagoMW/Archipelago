from .ginger_island import ginger_island as ginger_island_content_pack
from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data

qi_board = ContentPack(
    "Qi Board (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
        ginger_island_content_pack.name,
    ),
    fishes=(
        fish_data.ms_angler,
        fish_data.son_of_crimsonfish,
        fish_data.glacierfish_jr,
        fish_data.legend_ii,
        fish_data.radioactive_carp,
    )
)
