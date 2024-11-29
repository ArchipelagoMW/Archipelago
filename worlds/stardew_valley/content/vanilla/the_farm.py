from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data.building import Animal
from ...data.harvest import FruitBatsSource, MushroomCaveSource
from ...data.shop import ShopSource
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.region_names import Region

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
    },
    animals=(
        Animal("Chicken",
               required_building="Coop",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=800),
               )),
        Animal("Cow",
               required_building="Barn",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1500),
               )),
        Animal("Goat",
               required_building="Big Barn",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=4000),
               )),
        Animal("Duck",
               required_building="Big Coop",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1200),
               )),
        Animal("Sheep",
               required_building="Deluxe Barn",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal("Rabbit",
               required_building="Deluxe Coop",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal("Pig",
               required_building="Deluxe Barn",
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=16000),
               )),
    )
)
