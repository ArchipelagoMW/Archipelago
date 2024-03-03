from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import villagers_data

ginger_island = ContentPack(
    "Ginger Island (Vanilla)",
    weak_dependencies=(
        pelican_town_content_pack.name,
    ),
    villagers=(
        villagers_data.leo,
    )
)
