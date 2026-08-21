from .pelican_town import pelican_town as pelican_town_content_pack
from ..game_content import ContentPack
from ...data import fish_data, villagers_data
from ...data.game_item import Tag, ItemTag
from ...data.harvest import ForagingSource
from ...data.hats_data import Hats
from ...data.monster_data import MonsterSource
from ...data.requirement import ToolRequirement, RegionRequirement
from ...logic.tailoring_logic import TailoringSource
from ...logic.time_logic import MAX_MONTHS
from ...strings.fish_names import Fish
from ...strings.forageable_names import Forageable, Mushroom
from ...strings.monster_names import Monster
from ...strings.region_names import Region
from ...strings.tool_names import Tool

the_mines = ContentPack(
    "The Mines (Vanilla)",
    dependencies=(
        pelican_town_content_pack.name,
    ),
    harvest_sources={
        Forageable.cave_carrot: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.mines_floor_10,), other_requirements=(ToolRequirement(Tool.hoe),)),
        ),
        Mushroom.red: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.mines_floor_95,)),
        ),
        Mushroom.purple: (
            Tag(ItemTag.FORAGE),
            ForagingSource(regions=(Region.mines_floor_95,)),
        )
    },
    fishes=(
        fish_data.ghostfish,
        fish_data.ice_pip,
        fish_data.lava_eel,
        fish_data.stonefish,
    ),
    villagers=(
        villagers_data.dwarf,
    ),
    hat_sources={
        Hats.logo_cap: (Tag(ItemTag.HAT), TailoringSource(tailoring_items=(Fish.lava_eel,)),),
        Hats.hard_hat: (Tag(ItemTag.HAT), MonsterSource(monsters=(Monster.duggy, Monster.duggy_dangerous, Monster.magma_duggy,),
                                                             amount_tier=3,
                                                             other_requirements=(RegionRequirement(region=Region.adventurer_guild),)),),
        Hats.skeleton_mask: (Tag(ItemTag.HAT), MonsterSource(monsters=(Monster.skeleton, Monster.skeleton_mage, Monster.skeleton_dangerous,),
                                                                  amount_tier=MAX_MONTHS,
                                                                  other_requirements=(RegionRequirement(region=Region.adventurer_guild),)),),
        Hats.squires_helmet: (Tag(ItemTag.HAT), MonsterSource(monsters=(Monster.metal_head,),
                                                                   amount_tier=MAX_MONTHS),),
    },
)
