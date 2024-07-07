from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ...data.artisan import MachineSource
from ...data.game_item import ItemTag, Tag
from ...data.shop import ShopSource
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.book_names import ModBook
from ...strings.craftable_names import ModCraftable, ModMachine
from ...strings.fish_names import ModTrash
from ...strings.metal_names import all_artifacts, all_fossils
from ...strings.region_names import LogicRegion
from ...strings.skill_names import ModSkill


class ArchaeologyContentPack(ContentPack):
    def artisan_good_hook(self, content: StardewContent):
        # Done as honestly there are too many display items to put into the initial registration traditionally.
        display_types = [ModCraftable.wooden_display, ModCraftable.hardwood_display]
        display_items = all_artifacts + all_fossils
        rusty_scrap_machine_rules = []
        for item in display_items:
            if item in all_artifacts:
                rusty_scrap_machine_rules.append(MachineSource(item=str(item), machine=ModMachine.grinder))
            for display_type in display_types:
                if item == "Trilobite":
                    product_name = f"{display_type}: Trilobite Fossil"
                else:
                    product_name = f"{display_type}: {item}"

                if "Wooden" in display_type:
                    content.source_item(product_name, MachineSource(item=str(item), machine=ModMachine.preservation_chamber))
                else:
                    content.source_item(product_name, MachineSource(item=str(item), machine=ModMachine.hardwood_preservation_chamber))
        # Done as there are too many artifacts that suffice for this rule, and realistically a machine will always be bijective in use save
        # this, so it's hard to argue a change.
        content.source_item(ModTrash.rusty_scrap, *tuple(rusty_scrap_machine_rules))


register_mod_content_pack(ArchaeologyContentPack(
    ModNames.archaeology,
    shop_sources={
        ModBook.digging_like_worms: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ShopSource(money_price=500, shop_region=LogicRegion.bookseller_1),),
    },
    skills=(Skill(name=ModSkill.archaeology, has_mastery=False),),

))
