from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data.animal import IncubatorSource, Animal, AnimalName
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
        Animal(AnimalName.chicken,
               required_building=Building.coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=800),
                   # For now there is no way to obtain the starter item, so this adds additional rules in the system for nothing.
                   # IncubatorSource(AnimalProduct.egg_starter)
               )),
        Animal(AnimalName.cow,
               required_building=Building.barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1500),
               )),
        Animal(AnimalName.goat,
               required_building=Building.big_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=4000),
               )),
        Animal(AnimalName.duck,
               required_building=Building.big_coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=1200),
                   # For now there is no way to obtain the starter item, so this adds additional rules in the system for nothing.
                   # IncubatorSource(AnimalProduct.duck_egg_starter)
               )),
        Animal(AnimalName.sheep,
               required_building=Building.deluxe_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal(AnimalName.rabbit,
               required_building=Building.deluxe_coop,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=8000),
               )),
        Animal(AnimalName.pig,
               required_building=Building.deluxe_barn,
               sources=(
                   ShopSource(shop_region=Region.ranch, money_price=16000),
               )),
        Animal(AnimalName.void_chicken,
               required_building=Building.big_coop,
               sources=(
                   IncubatorSource(AnimalProduct.void_egg_starter),
               )),
        Animal(AnimalName.golden_chicken,
               required_building=Building.big_coop,
               sources=(
                   IncubatorSource(AnimalProduct.golden_egg_starter),
               )),
        Animal(AnimalName.dinosaur,
               required_building=Building.big_coop,
               sources=(
                   # We should use the starter item here, but since the dinosaur egg is also an artifact, it's part of the museum rules
                   # and I do not want to touch it yet.
                   # IncubatorSource(AnimalProduct.dinosaur_egg_starter),
                   IncubatorSource(AnimalProduct.dinosaur_egg),
               )),
    )
)
