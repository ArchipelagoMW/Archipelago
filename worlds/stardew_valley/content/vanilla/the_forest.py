from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data.building import Animal
from ...data.game_item import ItemTag, Tag
from ...data.shop import ShopSource
from ...strings.book_names import Book
from ...strings.region_names import Region

marnies_ranch = ContentPack(
    "Marnie's Ranch (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    shop_sources={
        Book.animal_catalogue: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_POWER),
            ShopSource(money_price=5000, shop_region=Region.ranch),),
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
