from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.LogicHelper import (
    include_hidden_items,
    include_lose_recruits,
    include_mike_games,
    include_recruits,
    include_secret_bosses_items_reward,
)
from worlds.deltarune.Rules import (
    have_susie,
    have_kris,
    have_actions,
    have_ralsei,
    can_recruit_guei,
    can_recruit_balthizard,
    can_recruit_bibliox,
    can_recruit_mizzle,
    can_recruit_miss_mizzle,
    can_recruit_wicabel,
    can_recruit_winglade,
    can_recruit_organikk,
    can_lost_chapter4,
    speedrun_glitch_logic,
    annoying_farming_logic,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_1]), have_susie
    )
    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_2]), have_susie
    )

    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_castle_town_lanino_elnina_challenge]),
        (
            (have_kris | (have_actions & (have_susie | have_ralsei)))
                | annoying_farming_logic # You can fight them but it's really long and annoying
        ),
    )

    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_third_sanctuary_annoying_dog]), Has(items[ItemIDs.sheetmusic])
    )

    world.set_rule(  # You can get this by doing dark sanctuary skip, so it's glitched
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_jackenstein_gift]),
        have_kris | speedrun_glitch_logic,
    )

    world.set_rule(world.get_location(locations[LocationIDs.ch4_dark_sanctuary_climbing_tutorial_chest]), have_kris)

    if include_mike_games(world) and world.options.exclude_mike_platinum.value == 1:
        world.get_location(locations[LocationIDs.ch4_mike_pluey_platinum]).progress_type = LocationProgressType.EXCLUDED
        world.get_location(locations[LocationIDs.ch4_mike_battat_platinum]).progress_type = (
            LocationProgressType.EXCLUDED
        )
        world.get_location(locations[LocationIDs.ch4_mike_jongler_platinum]).progress_type = (
            LocationProgressType.EXCLUDED
        )

    if include_recruits(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_guei]), can_recruit_guei)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_balthizard]), can_recruit_balthizard)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_bibliox]), can_recruit_bibliox)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_mizzle]), can_recruit_mizzle)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_miss_mizzle]), can_recruit_miss_mizzle)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_winglade]), can_recruit_winglade)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_organikk]), can_recruit_organikk)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_wicabel]), can_recruit_wicabel)

    if include_lose_recruits(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_guei]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_balthizard]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_bibliox]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_mizzle]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_miss_mizzle]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_winglade]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_organikk]), can_lost_chapter4)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_wicabel]), can_lost_chapter4)


def handle_locked_items(world: "DeltaruneWorld"):
    if not include_secret_bosses_items_reward(world):
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_1]).place_locked_item(
            world.create_item(items[ItemIDs.justiceaxe])
        )
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_2]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )

    # Hidden Items
    if not include_hidden_items(world):
        world.get_location(locations[LocationIDs.ch4_second_sanctuary_man]).place_locked_item(
            world.create_item(items[ItemIDs.chapter_4_egg])
        )
        world.get_location(locations[LocationIDs.ch4_second_sanctuary_moss]).place_locked_item(
            world.create_item(items[ItemIDs.sacred_moss])
        )
        world.get_location(locations[LocationIDs.ch4_third_sanctuary_annoying_dog]).place_locked_item(
            world.create_item(items[ItemIDs.dogdollar])
        )
