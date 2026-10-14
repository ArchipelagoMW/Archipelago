from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, Has
from worlds.deltarune.LogicHelper import all_recruits_route
from worlds.deltarune.Options import (
    AllowDoomBoardWithoutAllCharacters,
    MacGuffinChapter3,
    RandomizeSecretBosses,
    ShadowMantleHolderAsSecretBoss,
)
from worlds.deltarune.Regions import Regions, add_location_to_region, get_entrance_name
from worlds.deltarune.chapter_3.Locations import chapter3_locations
from worlds.deltarune.Rules import (
    have_actions,
    have_kris_susie_and_ralsei,
    have_kris,
    have_susie_or_ralsei,
    annoying_farming_logic,
)
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import LocationIDs, locations

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    couch_cliffs = Region(Regions.ch3_couch_cliffs, world.player, world.multiworld)
    board_1 = Region(Regions.ch3_board_1, world.player, world.multiworld)
    sword_1 = Region(Regions.ch3_sword_1, world.player, world.multiworld)
    green_room = Region(Regions.ch3_green_room, world.player, world.multiworld)
    board_2 = Region(Regions.ch3_board_2, world.player, world.multiworld)
    sword_2 = Region(Regions.ch3_sword_2, world.player, world.multiworld)
    doom_board = Region(Regions.ch3_doom_board, world.player, world.multiworld)
    tv_world = Region(Regions.ch3_tv_world, world.player, world.multiworld)
    sword_3 = Region(Regions.ch3_sword_3, world.player, world.multiworld)
    cold_place = Region(Regions.ch3_cold_place, world.player, world.multiworld)
    fountain = Region(Regions.ch3_fountain, world.player, world.multiworld)

    regions = [
        couch_cliffs,
        board_1,
        sword_1,
        green_room,
        board_2,
        sword_2,
        doom_board,
        tv_world,
        sword_3,
        cold_place,
        fountain,
    ]

    for region in regions:
        if region.name in chapter3_locations:
            add_location_to_region(region, chapter3_locations[region.name], world)
        world.multiworld.regions.append(region)

    world.get_region(Regions.chapter_3).connect(couch_cliffs)

    # Require at least one character for Elnina Lanino
    couch_cliffs.connect(
        board_1,
        rule=(
            have_kris  # Kris can solo the fight
            | (
                have_susie_or_ralsei
                & (
                    have_actions  # Susie or Ralsei can do the fight if they have actions
                    | annoying_farming_logic
                    # Or an obscure tactic is fighting Elnina Lanino, though it takes TOO LONG
                )
            )
        ),
    )

    board_1.connect(green_room)
    board_1.connect(sword_1, rule=Has(items[ItemIDs.odd_controller]))

    green_room.connect(board_2, rule=Has(items[ItemIDs.board_2_cartridge]))

    # Require all characters for Turning off Zapper during Doom Board
    board_2.connect(
        doom_board,
        rule=have_kris_susie_and_ralsei
        | OptionFilter(AllowDoomBoardWithoutAllCharacters, AllowDoomBoardWithoutAllCharacters.option_true),
    )
    board_2.connect(sword_2, rule=Has(items[ItemIDs.ice_key]) & Has(items[ItemIDs.odd_controller]))

    doom_board.connect(tv_world, rule=Has(items[ItemIDs.vip_pass]))

    tv_world.connect(
        sword_3,
        rule=(
            Has(items[ItemIDs.shelter_key])
            & Has(items[ItemIDs.ice_key])
            & Has(items[ItemIDs.odd_controller])
            & have_kris
        ),
    )
    tv_world.connect(world.get_region(Regions.lost_rabbick))

    mantle_mandatory = CanReachLocation(
        locations[LocationIDs.ch3_mantle_defeat],
        options=[
            OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory),
            OptionFilter(ShadowMantleHolderAsSecretBoss, 1),
        ],
        filtered_resolution=True,
    )

    if all_recruits_route(world):
        all_recruits = (
            CanReachLocation(locations[LocationIDs.ch3_recruit_shadowguy])
            & CanReachLocation(locations[LocationIDs.ch3_recruit_pippins])
            & CanReachLocation(locations[LocationIDs.ch3_recruit_shuttah])
            & CanReachLocation(locations[LocationIDs.ch3_recruit_water_cooler])
            & CanReachLocation(locations[LocationIDs.ch3_recruit_zapper])
            & CanReachLocation(locations[LocationIDs.ch3_recruit_ribbick])
        )
        tv_world.connect(
            cold_place,
            rule=mantle_mandatory & all_recruits & Has(items[ItemIDs.remote_battery], FromOption(MacGuffinChapter3)),
        )
    else:
        tv_world.connect(
            cold_place,
            rule=mantle_mandatory & Has(items[ItemIDs.remote_battery], FromOption(MacGuffinChapter3)),
        )

    cold_place.connect(
        fountain,
        rule=CanReachLocation(
            locations[LocationIDs.ch3_cold_place_knight_defeat_item_1],
            options=[OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory)],
            filtered_resolution=True,
        ),
    )
