from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachEntrance, CanReachLocation, CanReachRegion, Has
from worlds.deltarune.LogicHelper import all_recruits_route, normal_route, weird_route
from worlds.deltarune.Options import (
    ChosenRoute,
    MacGuffinChapter2,
    RandomizeSecretBosses,
    RecruitsSanity,
    SpeedrunGlitchesAsLogic,
)
from worlds.deltarune.Regions import Regions, add_location_to_region, get_entrance_name
from worlds.deltarune.chapter_2.Locations import chapter2_locations
from worlds.deltarune.Rules import (
    have_actions,
    have_kris_or_susie,
    have_kris,
    have_kris_or_noelle,
    have_kris_or_ralsei,
    have_kris_susie_or_ralsei,
    have_noelle,
    speedrun_glitch_logic,
)
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import LocationIDs, locations

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    castle_town = Region(Regions.ch2_castle_town, world.player, world.multiworld)
    dojo = Region(Regions.ch2_dojo, world.player, world.multiworld)
    cyber_field = Region(Regions.ch2_cyber_field, world.player, world.multiworld)
    cyber_field_post_dj = Region(Regions.ch2_cyber_field_post_dj, world.player, world.multiworld)
    music_shop = Region(Regions.ch2_music_shop, world.player, world.multiworld)
    trash_zone_no_character_requirement = Region(
        Regions.ch2_trash_zone_no_character_required, world.player, world.multiworld
    )
    trash_zone = Region(Regions.ch2_trash_zone, world.player, world.multiworld)
    cyber_city = Region(Regions.ch2_cyber_city, world.player, world.multiworld)
    cyber_city_post_toilet = Region(Regions.ch2_cyber_city_post_toilet, world.player, world.multiworld)
    mansion_lobby_warp_door = Region(Regions.ch2_mansion_lobby_warp_door, world.player, world.multiworld)
    mansion_both_route = Region(Regions.ch2_mansion_both_route, world.player, world.multiworld)
    mansion_recruits = Region(Regions.ch2_mansion_recruits, world.player, world.multiworld)
    recruit_werewerewire = Region(Regions.ch2_recruit_werewerewire, world.player, world.multiworld)
    spamton_neo = Region(Regions.ch2_spamton_neo, world.player, world.multiworld)

    regions = [
        castle_town,
        dojo,
        cyber_field,
        cyber_field_post_dj,
        music_shop,
        trash_zone_no_character_requirement,
        trash_zone,
        cyber_city,
        cyber_city_post_toilet,
        mansion_lobby_warp_door,
        mansion_both_route,
        mansion_recruits,
        recruit_werewerewire,
        spamton_neo,
    ]

    for region in regions:
        if region.name in chapter2_locations:
            add_location_to_region(region, chapter2_locations[region.name], world)
        world.multiworld.regions.append(region)

    world.get_region(Regions.chapter_2).connect(castle_town)

    # Require Kris or Susie for the werewire fight
    world.get_region(Regions.chapter_2).connect(
        cyber_field,
        rule=have_kris_or_susie,
    )

    castle_town.connect(dojo)

    # Require actions and at least one character for DJ-fight unless you ww into the fight (but can't end it) or Bagel Overflow to mansion and come back with plot value updated
    cyber_field.connect(
        cyber_field_post_dj,
        rule=(have_actions & have_kris_susie_or_ralsei),
    )
    cyber_field.connect(
        trash_zone_no_character_requirement,
        get_entrance_name(cyber_field, trash_zone_no_character_requirement, "BagelOverflow"),
        rule=speedrun_glitch_logic,
    )
    cyber_field_post_dj.connect(music_shop)
    # Require Safety vest and at least one character for berdly fight or Bagel Overflow to Trash Zone
    cyber_field_post_dj.connect(
        trash_zone_no_character_requirement,
        rule=(Has(items[ItemIDs.safety_vest]) & have_kris_susie_or_ralsei),
    )

    if normal_route(world):
        spamton_shop = Region(Regions.ch2_spamton_shop, world.player, world.multiworld)
        swatch_cafe = Region(Regions.ch2_swatch_cafe, world.player, world.multiworld)
        cyber_city_spamton_fight = Region(Regions.ch2_cyber_city_spamton_fight, world.player, world.multiworld)
        cyber_city_post_spamton = Region(Regions.ch2_cyber_city_post_spamton, world.player, world.multiworld)
        mansion_lobby_main_route = Region(Regions.ch2_mansion_lobby_main_route, world.player, world.multiworld)
        mansion_main_route = Region(Regions.ch2_mansion_main_route, world.player, world.multiworld)
        mansion_basement = Region(Regions.ch2_mansion_basement, world.player, world.multiworld)
        tunnel_of_love = Region(Regions.ch2_tunnel_of_love, world.player, world.multiworld)
        fountain = Region(Regions.ch2_fountain, world.player, world.multiworld)

        regions_normal_route = [
            spamton_shop,
            swatch_cafe,
            cyber_city_spamton_fight,
            cyber_city_post_spamton,
            mansion_lobby_main_route,
            mansion_main_route,
            mansion_basement,
            tunnel_of_love,
            fountain,
        ]

        # Mansion warp door unavailable during weird route to prevent you locking yourself out of the route
        cyber_field.connect(
            mansion_lobby_warp_door,
            get_entrance_name(cyber_field, mansion_lobby_warp_door, "BagelOverflow"),
            rule=speedrun_glitch_logic,
        )
        mansion_lobby_warp_door.connect(
            cyber_field_post_dj,
            get_entrance_name(mansion_lobby_warp_door, cyber_field_post_dj, "Plot update after BagelOverflow"),
        )
        mansion_lobby_warp_door.connect(
            cyber_city,
            get_entrance_name(mansion_lobby_warp_door, cyber_city, "Plot update after BagelOverflow"),
            rule=have_kris_susie_or_ralsei,
        )
        mansion_lobby_warp_door.connect(
            trash_zone,
            get_entrance_name(mansion_lobby_warp_door, trash_zone, "Plot update after BagelOverflow"),
            rule=have_kris_susie_or_ralsei,
        )

        for region in regions_normal_route:
            if region.name in chapter2_locations:
                add_location_to_region(region, chapter2_locations[region.name], world)
            world.multiworld.regions.append(region)

        trash_zone_no_character_requirement.connect(
            trash_zone,
            get_entrance_name(trash_zone_no_character_requirement, trash_zone, "Normal Route"),
            rule=have_kris_or_noelle,
        )

        # Require Kris or Noelle for the Virovirokun after noelle
        trash_zone_no_character_requirement.connect(
            cyber_city,
            get_entrance_name(trash_zone_no_character_requirement, cyber_city, "Normal Route"),
            rule=have_kris_or_noelle,
        )

        cyber_city.connect(
            cyber_city_post_toilet,
            get_entrance_name(cyber_city, cyber_city_post_toilet, "Normal Route"),
            rule=have_kris_or_noelle,
        )

        cyber_field.connect(
            mansion_lobby_main_route,
            get_entrance_name(cyber_field, mansion_lobby_main_route, "BagelOverflow"),
            rule=speedrun_glitch_logic,
        )

        # MAIN ROUTE REGION CONNECTIONS
        # Require Kris for Spamton fight unless you skip it with an Interaction Slide
        cyber_city_post_toilet.connect(cyber_city_spamton_fight, rule=have_kris)
        cyber_city_post_toilet.connect(
            cyber_city_post_spamton,
            get_entrance_name(cyber_city_post_toilet, cyber_city_post_spamton, "Interaction Slide"),
            rule=speedrun_glitch_logic,
        )
        cyber_city_spamton_fight.connect(cyber_city_post_spamton)
        cyber_city_post_spamton.connect(mansion_lobby_main_route)

        mansion_lobby_main_route.connect(swatch_cafe)
        mansion_lobby_main_route.connect(mansion_lobby_warp_door)
        # Require you to being able to spare spamton
        mansion_lobby_main_route.connect(
            spamton_shop,
            rule=CanReachRegion(Regions.ch2_cyber_city_spamton_fight),
        )
        mansion_lobby_main_route.connect(
            mansion_main_route,
            rule=Has(items[ItemIDs.mansion_reservation]),
        )

        mansion_main_route.connect(mansion_recruits)
        mansion_main_route.connect(mansion_both_route)
        mansion_main_route.connect(tunnel_of_love, rule=have_kris_or_ralsei)

        tunnel_of_love.connect(recruit_werewerewire)

        mansion_main_route.connect(
            mansion_basement,
            rule=Has(items[ItemIDs.keygen])
            & CanReachRegion(Regions.ch2_cyber_city_post_spamton)
            & (have_kris | Has(glitched_item_name)),
        )
        mansion_basement.connect(
            spamton_neo, get_entrance_name(mansion_basement, spamton_neo), rule=Has(items[ItemIDs.emptydisk])
        )

        secret_boss_mandatory = CanReachEntrance(get_entrance_name(mansion_basement, spamton_neo)) | [
            OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory, operator="ne")
        ]

        if all_recruits_route(world):
            all_recruits = (
                CanReachLocation(locations[LocationIDs.ch2_recruit_werewire])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_tasque])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_virovirokun])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_poppup])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_ambyu_lance])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_maus])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_swatchling])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_tasque_manager])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_mauswheel])
                & CanReachLocation(locations[LocationIDs.ch2_recruit_werewerewire])
            )

            tunnel_of_love.connect(
                fountain,
                rule=all_recruits
                & secret_boss_mandatory
                & Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)),
            )
        else:
            tunnel_of_love.connect(
                fountain,
                rule=secret_boss_mandatory & Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)),
            )

    if weird_route(world):
        thornring = Region(Regions.ch2_thornring, world.player, world.multiworld)
        mansion_lobby_weird_route = Region(Regions.ch2_mansion_lobby_weird_route, world.player, world.multiworld)
        fountain_weird_route = Region(Regions.ch2_fountain_weird_route, world.player, world.multiworld)

        regions_weird_route = [thornring, mansion_lobby_weird_route, fountain_weird_route]

        for region in regions_weird_route:
            if region.name in chapter2_locations:
                add_location_to_region(region, chapter2_locations[region.name], world)
            world.multiworld.regions.append(region)

        cyber_field.connect(
            thornring, get_entrance_name(cyber_field, thornring, "Bagel Overflow"), rule=speedrun_glitch_logic
        )

        trash_zone_no_character_requirement.connect(
            trash_zone,
            get_entrance_name(trash_zone_no_character_requirement, trash_zone, "Weird Route"),
            rule=have_noelle,
        )

        # Require Kris or Noelle for the Virovirokun after noelle
        trash_zone_no_character_requirement.connect(
            cyber_city,
            get_entrance_name(trash_zone_no_character_requirement, cyber_city, "Weird Route"),
            rule=have_noelle,
        )

        cyber_city.connect(
            cyber_city_post_toilet,
            get_entrance_name(cyber_city, cyber_city_post_toilet, "Weird Route"),
            rule=have_noelle,
        )

        cyber_city.connect(thornring)

        # WEIRD ROUTE REGION CONNECTIONS
        # Moved after creating items because we don't know yet how many progressive item is the thornring
        # cyber_city.connect(mansion_lobby_weird_route, rule=can_snowgrave(world))

        mansion_lobby_weird_route.connect(mansion_lobby_warp_door)
        mansion_lobby_weird_route.connect(mansion_recruits)
        mansion_lobby_weird_route.connect(recruit_werewerewire)
        mansion_lobby_weird_route.connect(
            mansion_both_route,
            get_entrance_name(mansion_lobby_weird_route, mansion_both_route, "Singapore Wrong Warp"),
            rule=speedrun_glitch_logic,
        )
        mansion_lobby_weird_route.connect(
            spamton_neo,
            rule=Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)) & have_kris,
        )
        mansion_lobby_weird_route.connect(
            fountain_weird_route,
            rule=Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)) & have_kris,
        )
