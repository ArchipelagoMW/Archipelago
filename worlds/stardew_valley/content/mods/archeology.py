from ..game_content import ContentPack
from ..mod_registry import register_mod_content_pack
from ...data.game_item import ItemTag, Tag
from ...data.shop import ShopSource
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.book_names import ModBook
from ...strings.region_names import LogicRegion
from ...strings.skill_names import ModSkill

register_mod_content_pack(ContentPack(
    ModNames.archaeology,
    shop_sources={
        ModBook.digging_like_worms: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(money_price=500, shop_region=LogicRegion.bookseller_1),),
    },
    skills=(Skill(name=ModSkill.archaeology, has_mastery=False),),

))
