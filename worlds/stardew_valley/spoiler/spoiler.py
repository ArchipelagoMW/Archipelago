from typing import TextIO

from BaseClasses import Spoiler

from ..bundles.bundle_room import BundleRoom
from ..content import StardewContent
from ..data_randomization.randomized_data_writer import add_randomized_data_to_spoiler_log
from ..options import BundleRandomization, EntranceRandomization, StardewValleyOptions


def write_spoiler_header(spoiler_handle: TextIO, player: int, options: StardewValleyOptions, randomized_entrances: dict[str, str] | None, spoiler: Spoiler) -> None:
    add_entrances_to_spoiler_log(player, options, randomized_entrances, spoiler)


def write_spoiler_middle(spoiler_handle: TextIO, player_name: str, content: StardewContent, options: StardewValleyOptions, modified_bundles: list[BundleRoom], help_wanted_quests: dict[str, str]) -> None:
    add_bundles_to_spoiler_log(spoiler_handle, player_name, options, modified_bundles)
    add_help_wanted_to_spoiler_log(spoiler_handle, player_name, options, help_wanted_quests)
    add_randomized_data_to_spoiler_log(spoiler_handle, player_name, content, options)


def add_entrances_to_spoiler_log(player: int, options: StardewValleyOptions, randomized_entrances: dict[str, str] | None, spoiler: Spoiler):
    if options.entrance_randomization == EntranceRandomization.option_disabled or randomized_entrances is None:
        return
    for original_entrance, replaced_entrance in randomized_entrances.items():
        spoiler.set_entrance(original_entrance, replaced_entrance, "entrance", player)


def add_bundles_to_spoiler_log(spoiler_handle: TextIO, player_name: str, options: StardewValleyOptions, modified_bundles: list[BundleRoom]):
    if options.bundle_randomization == BundleRandomization.option_vanilla:
        return
    spoiler_handle.write(f"\n\nCommunity Center ({player_name}):\n")
    for room in modified_bundles:
        for bundle in room.bundles:
            spoiler_handle.write(f"\t[{room.name}] {bundle.name} ({bundle.number_required} required):\n")
            for i, item in enumerate(bundle.items):
                if "Basic" in item.quality:
                    quality = ""
                else:
                    quality = f" ({item.quality.split(' ')[0]})"
                spoiler_handle.write(f"\t\t{item.amount}x {item.get_item()}{quality}\n")


def add_help_wanted_to_spoiler_log(spoiler_handle: TextIO, player_name: str, options: StardewValleyOptions, help_wanted_quests: dict[str, str]):
    if options.quest_locations <= 0 or len(help_wanted_quests) <= 0:
        return
    spoiler_handle.write(f"\n\nHelp Wanted Quests ({player_name}):\n")
    for quest_name, quest_value in help_wanted_quests.items():
        spoiler_handle.write(f"\t{quest_name}: {quest_value}\n")
