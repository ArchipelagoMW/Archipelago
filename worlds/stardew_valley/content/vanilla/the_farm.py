from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data.harvest import FruitBatsSource, MushroomCaveSource
from ...strings.forageable_names import Forageable, Mushroom

the_farm = ContentPack(
    "The Farm (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        # Fruit cave
        Forageable.blackberry: (
            FruitBatsSource(),
        ),
        Forageable.salmonberry: (
            FruitBatsSource(),
        ),
        Forageable.spice_berry: (
            FruitBatsSource(),
        ),
        Forageable.wild_plum: (
            FruitBatsSource(),
        ),

        # Mushrooms
        Mushroom.common: (
            MushroomCaveSource(),
        ),
        Mushroom.chanterelle: (
            MushroomCaveSource(),
        ),
        Mushroom.morel: (
            MushroomCaveSource(),
        ),
        Mushroom.purple: (
            MushroomCaveSource(),
        ),
        Mushroom.red: (
            MushroomCaveSource(),
        ),
    }
)
