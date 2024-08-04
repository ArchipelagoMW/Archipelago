from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ..override import override
from ..vanilla.ginger_island import ginger_island_content_pack as ginger_island_content_pack
from ...data import villagers_data, fish_data
from ...data.harvest import ForagingSource
from ...data.requirement import YearRequirement
from ...mods.mod_data import ModNames
from ...strings.crop_names import Fruit
from ...strings.fish_names import WaterItem
from ...strings.flower_names import Flower
from ...strings.forageable_names import Mushroom, Forageable
from ...strings.region_names import Region, SVERegion
from ...strings.season_names import Season


class SVEContentPack(ContentPack):

    def fish_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            content.fishes.pop(fish_data.baby_lunaloo.name)
            content.fishes.pop(fish_data.clownfish.name)
            content.fishes.pop(fish_data.lunaloo.name)
            content.fishes.pop(fish_data.seahorse.name)
            content.fishes.pop(fish_data.shiny_lunaloo.name)
            content.fishes.pop(fish_data.starfish.name)
            content.fishes.pop(fish_data.sea_sponge.name)

            # Remove Highlands fishes at it requires 2 Lance hearts for the quest to access it
            content.fishes.pop(fish_data.daggerfish.name)
            content.fishes.pop(fish_data.gemfish.name)

            # Remove Fable Reef fishes at it requires 8 Lance hearts for the event to access it
            content.fishes.pop(fish_data.torpedo_trout.name)

    def villager_hook(self, content: StardewContent):
        if ginger_island_content_pack.name not in content.registered_packs:
            # Remove Lance if Ginger Island is not in content since he is first encountered in Volcano Forge
            content.villagers.pop(villagers_data.lance.name)


register_mod_content_pack(SVEContentPack(
    ModNames.sve,
    weak_dependencies=(
        ginger_island_content_pack.name,
        ModNames.jasper,  # To override Marlon and Gunther
    ),
    harvest_sources={
        Mushroom.red: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.summer, Season.fall)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.purple: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.morel: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Mushroom.chanterelle: (
            ForagingSource(regions=(SVERegion.forest_west,), seasons=(Season.fall,)), ForagingSource(regions=(SVERegion.sprite_spring_cave,), )
        ),
        Flower.tulip: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.blue_jazz: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring,)),),
        Flower.summer_spangle: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.sunflower: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.summer,)),),
        Flower.fairy_rose: (ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.fall,)),),
        Fruit.ancient_fruit: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring, Season.summer, Season.fall), other_requirements=(YearRequirement(3),)),
            ForagingSource(regions=(SVERegion.sprite_spring_cave,)),
        ),
        Fruit.sweet_gem_berry: (
            ForagingSource(regions=(SVERegion.sprite_spring,), seasons=(Season.spring, Season.summer, Season.fall), other_requirements=(YearRequirement(3),)),
        ),

        # Fable Reef
        WaterItem.coral: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        Forageable.rainbow_shell: (ForagingSource(regions=(SVERegion.fable_reef,)),),
        WaterItem.sea_urchin: (ForagingSource(regions=(SVERegion.fable_reef,)),),
    },
    fishes=(
        fish_data.baby_lunaloo,  # Removed when no ginger island
        fish_data.bonefish,
        fish_data.bull_trout,
        fish_data.butterfish,
        fish_data.clownfish,  # Removed when no ginger island
        fish_data.daggerfish,
        fish_data.frog,
        fish_data.gemfish,
        fish_data.goldenfish,
        fish_data.grass_carp,
        fish_data.king_salmon,
        fish_data.kittyfish,
        fish_data.lunaloo,  # Removed when no ginger island
        fish_data.meteor_carp,
        fish_data.minnow,
        fish_data.puppyfish,
        fish_data.radioactive_bass,
        fish_data.seahorse,  # Removed when no ginger island
        fish_data.shiny_lunaloo,  # Removed when no ginger island
        fish_data.snatcher_worm,
        fish_data.starfish,  # Removed when no ginger island
        fish_data.torpedo_trout,
        fish_data.undeadfish,
        fish_data.void_eel,
        fish_data.water_grub,
        fish_data.sea_sponge,  # Removed when no ginger island

    ),
    villagers=(
        villagers_data.claire,
        villagers_data.lance,  # Removed when no ginger island
        villagers_data.mommy,
        villagers_data.sophia,
        villagers_data.victor,
        villagers_data.andy,
        villagers_data.apples,
        villagers_data.gunther,
        villagers_data.martin,
        villagers_data.marlon,
        villagers_data.morgan,
        villagers_data.scarlett,
        villagers_data.susan,
        villagers_data.morris,
        # The wizard leaves his tower on sunday, for like 1 hour... Good enough for entrance rando!
        override(villagers_data.wizard, locations=(Region.wizard_tower, Region.forest), bachelor=True, mod_name=ModNames.sve),
    )
))
