from __future__ import annotations

from typing import Iterable

from .game_content import StardewContent, ContentPack, StardewFeatures
from .vanilla.base import base_game as base_game_content_pack
from ..data.game_item import GameItem

try:
    from graphlib import TopologicalSorter
except ImportError:
    from graphlib_backport import TopologicalSorter  # noqa


def unpack_content(features: StardewFeatures, packs: Iterable[ContentPack]) -> StardewContent:
    # Base game is always registered first.
    content = StardewContent(features)
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
            register_pack(content, packs_by_name[pack_name])
            sorter.done(pack_name)

    return content


def register_pack(content: StardewContent, pack: ContentPack):
    # register game item

    # register regions

    # register entrances

    for item_name, sources in pack.harvest_sources.items():
        item = content.game_items.setdefault(item_name, GameItem(item_name))
        item.add_sources(sources)
    pack.harvest_source_hook(content)

    for fish in pack.fishes:
        content.fishes[fish.name] = fish
    pack.fish_hook(content)

    for villager in pack.villagers:
        content.villagers[villager.name] = villager
    pack.villager_hook(content)

    # register_skills

    # register_quests

    # ...

    content.registered_packs.add(pack.name)
