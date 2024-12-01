from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data.animal import IncubatorSource
from ...data.building import Animal
from ...data.harvest import FruitBatsSource, MushroomCaveSource
from ...data.shop import ShopSource
from ...strings.animal_product_names import AnimalProduct
from ...strings.building_names import Building
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
               required_building=Building.coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=800),
                   IncubatorSource(AnimalProduct.egg_starter)
               )),
        Animal("Cow",
               required_building=Building.barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1500),
               )),
        Animal("Goat",
               required_building=Building.big_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=4000),
               )),
        Animal("Duck",
               required_building=Building.big_coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1200),
                   IncubatorSource(AnimalProduct.duck_egg_starter)
               )),
        Animal("Sheep",
               required_building=Building.deluxe_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal("Rabbit",
               required_building=Building.deluxe_coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal("Pig",
               required_building=Building.deluxe_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=16000),
               )),
        Animal("Void Chicken",
               required_building=Building.big_coop,
               sources=(
                   IncubatorSource(AnimalProduct.void_egg_starter),
               )),
        Animal("Golden Chicken",
               required_building=Building.big_coop,
               sources=(
                   IncubatorSource(AnimalProduct.golden_egg_starter),
               )),
        Animal("Dinosaur",
               required_building=Building.big_coop,
               sources=(
                   IncubatorSource(AnimalProduct.dinosaur_egg_starter),
               )),
    )
)
