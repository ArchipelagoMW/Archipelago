from __future__ import annotations

from graphlib import TopologicalSorter
from typing import Iterable, Mapping, Callable

from .game_content import StardewContent, ContentPack, StardewFeatures
from .override import override
from .vanilla.base import base_game as base_game_content_pack
from .vanilla.ginger_island import ginger_island_content_pack
from ..data.craftable_data import all_crafting_recipes_by_name
from ..data.game_item import Source
from ..regions.vanilla_content_packs import ginger_island_regions
from ..regions.vanilla_data import vanilla_regions


def unpack_content(features: StardewFeatures, packs: Iterable[ContentPack]) -> StardewContent:
    # Base game is always registered first.
    content = StardewContent(features)
    packs_to_finalize = [base_game_content_pack]
    register_pack(content, base_game_content_pack)

    # Content packs are added in order based on their dependencies
    sorter = TopologicalSorter()
    packs_by_name = {p.name: p for p in packs}

    # Build the dependency graph
    for name, pack in packs_by_name.items():
        sorter.add(name,
                   *pack.dependencies,
                   *(wd for wd in pack.weak_dependencies if wd in packs_by_name))

    # Graph is traversed in BFS
    sorter.prepare()
    while sorter.is_active():
        # Packs get shuffled in TopologicalSorter, most likely due to hash seeding.
        for pack_name in sorted(sorter.get_ready()):
            pack = packs_by_name[pack_name]
            register_pack(content, pack)
            sorter.done(pack_name)
            packs_to_finalize.append(pack)

    prune_inaccessible_items(content)
    prune_inaccessible_regions(content)

    for pack in packs_to_finalize:
        pack.finalize_hook(content)

    # Maybe items without source should be removed at some point
    return content


def register_pack(content: StardewContent, pack: ContentPack):
    # register regions

    # register entrances

    register_sources_and_call_hook(content, pack.harvest_sources, pack.harvest_source_hook)
    register_sources_and_call_hook(content, pack.shop_sources, pack.shop_source_hook)
    register_sources_and_call_hook(content, pack.artisan_good_sources, pack.artisan_good_hook)

    for fish in pack.fishes:
        content.fishes[fish.name] = fish
    pack.fish_hook(content)

    for villager in pack.villagers:
        content.villagers[villager.name] = villager
    pack.villager_hook(content)

    for building in pack.farm_buildings:
        content.farm_buildings[building.name] = building
    pack.farm_building_hook(content)

    for tool_upgrade in pack.tool_upgrades:
        content.tool_upgrades[tool_upgrade.tool_upgrade_name] = tool_upgrade
    pack.tool_upgrade_hook(content)

    for animal in pack.animals:
        content.animals[animal.name] = animal
    pack.animal_hook(content)

    for skill in pack.skills:
        content.skills[skill.name] = skill
    pack.skill_hook(content)

    for hat, sources in pack.hat_sources.items():
        item = content.source_item(hat.clarified_name, *sources)
        # Some sources may be filtered out. We don't want to register a hat without source.
        if item.sources:
            content.hats[hat.name] = hat
    pack.hat_source_hook(content)

    for festival in pack.festivals:
        content.festivals[festival.name] = festival
    pack.festival_source_hook(content)

    for cooking_recipe in pack.cooking_recipes:
        content.festivals[cooking_recipe.name] = cooking_recipe
    pack.cooking_recipe_source_hook(content)

    register_sources_and_call_hook(content, pack.crafting_sources, pack.crafting_hook)

    # register_quests

    # ...

    content.registered_packs.add(pack.name)


def register_sources_and_call_hook(content: StardewContent,
                                   sources_by_item_name: Mapping[str, Iterable[Source]],
                                   hook: Callable[[StardewContent], None]):
    for item_name, sources in sources_by_item_name.items():
        content.source_item(item_name, *sources)
    hook(content)


def prune_inaccessible_items(content: StardewContent):
    for item in list(content.game_items.values()):
        # This crafting recipe stuff can be replaced once crafts are added to content packs
        if not item.sources and item.name not in all_crafting_recipes_by_name:
            content.game_items.pop(item.name)


def prune_inaccessible_regions(content: StardewContent):
    inaccessible_regions = []
    allowed_regions = [region.name for region in vanilla_regions]
    if ginger_island_content_pack.name not in content.registered_packs:
        inaccessible_regions.extend([region.name for region in ginger_island_regions if region.name not in allowed_regions])
    prune_inaccessible_fish_regions(content, inaccessible_regions)


def prune_inaccessible_fish_regions(content: StardewContent, inaccessible_regions: list[str]):
    for fish_name, fish_content in content.fishes.items():
        pruned_regions = tuple([region for region in fish_content.locations if region not in inaccessible_regions])
        content.fishes[fish_name] = override(fish_content, locations=pruned_regions)
