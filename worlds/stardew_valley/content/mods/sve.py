from ..game_content import ContentPack, StardewContent
from ..mod_registry import register_mod_content_pack
from ..override import override
from ..vanilla.ginger_island import ginger_island_content_pack as ginger_island_content_pack
from ...data import villagers_data, fish_data
from ...mods.mod_data import ModNames
from ...strings.region_names import Region


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
        fish_data.dulse_seaweed,

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
