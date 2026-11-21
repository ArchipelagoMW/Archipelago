from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ...data.artisan import MachineSource
from ...data.game_item import ItemTag, Tag
from ...data.harvest import ArtifactSpotSource
from ...data.requirement import SkillRequirement
from ...data.skill import Skill
from ...mods.mod_data import ModNames
from ...strings.ap_names.mods.mod_items import ModBooks
from ...strings.craftable_names import ModMachine
from ...strings.fish_names import ModTrash
from ...strings.metal_names import all_artifacts, all_fossils, Fossil
from ...strings.skill_names import ModSkill


def source_display_items(item: str, content: StardewContent):
    wood_display = f"Wooden Display: {item}"
    hardwood_display = f"Hardwood Display: {item}"
    if item == Fossil.trilobite:
        wood_display = f"Wooden Display: Trilobite Fossil"
        hardwood_display = f"Hardwood Display: Trilobite Fossil"
    content.source_item(wood_display, MachineSource(item=str(item), machine=ModMachine.preservation_chamber))
    content.source_item(hardwood_display, MachineSource(item=str(item), machine=ModMachine.hardwood_preservation_chamber))


class ArchaeologyContentPack(ContentPack):
    def artisan_good_hook(self, content: StardewContent):
        # Done as honestly there are too many display items to put into the initial registration traditionally.
        display_items = all_artifacts + all_fossils
        for item in display_items:
            source_display_items(item, content)
        content.source_item(ModTrash.rusty_scrap, *(MachineSource(item=artifact, machine=ModMachine.grinder) for artifact in all_artifacts))


register_mod_content_pack(ArchaeologyContentPack(
    ModNames.archaeology,
    skills=(Skill(name=ModSkill.archaeology, has_mastery=False),),
    harvest_sources={
        ModBooks.digging_like_worms: (
            Tag(ItemTag.BOOK, ItemTag.BOOK_SKILL),
            ArtifactSpotSource(amount=22,  # I'm just copying Jack Be Nimble's chances for now -reptar
                               other_requirements=(SkillRequirement(ModSkill.archaeology, 2),)),
        )
    }

))
