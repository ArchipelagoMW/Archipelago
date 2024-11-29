from __future__ import annotations

from graphlib import TopologicalSorter
from typing import Iterable, Mapping, Callable

from .game_content import StardewContent, ContentPack, StardewFeatures
from .vanilla.base import base_game as base_game_content_pack
from ..data.game_item import GameItem, ItemSource


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

    for pack in packs_to_finalize:
        pack.finalize_hook(content)

    # Maybe items without source should be removed at some point
    return content


def register_pack(content: StardewContent, pack: ContentPack):
    # register regions

    # register entrances

    register_sources_and_call_hook(content, pack.harvest_sources, pack.harvest_source_hook)
    register_sources_and_call_hook(content, pack.shop_sources, pack.shop_source_hook)
    register_sources_and_call_hook(content, pack.crafting_sources, pack.crafting_hook)
    register_sources_and_call_hook(content, pack.artisan_good_sources, pack.artisan_good_hook)

    for fish in pack.fishes:
        content.fishes[fish.name] = fish
    pack.fish_hook(content)

    for villager in pack.villagers:
        content.villagers[villager.name] = villager
    pack.villager_hook(content)

    for skill in pack.skills:
        content.skills[skill.name] = skill
    pack.skill_hook(content)

    # register_quests

    # ...

    content.registered_packs.add(pack.name)


def register_sources_and_call_hook(content: StardewContent,
                                   sources_by_item_name: Mapping[str, Iterable[ItemSource]],
                                   hook: Callable[[StardewContent], None]):
    for item_name, sources in sources_by_item_name.items():
        item = content.game_items.setdefault(item_name, GameItem(item_name))
        item.add_sources(sources)

        for source in sources:
            for requirement_name, tags in source.requirement_tags.items():
                requirement_item = content.game_items.setdefault(requirement_name, GameItem(requirement_name))
                requirement_item.add_tags(tags)

    hook(content)


def prune_inaccessible_items(content: StardewContent):
    for item in list(content.game_items.values()):
        if not item.sources:
            content.game_items.pop(item.name)
