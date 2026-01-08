from typing import Any, TYPE_CHECKING

from worlds.rac3.constants.data.location import UT_MAPPING
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION

if TYPE_CHECKING:
    from worlds.rac3 import RaC3World


def setup_options_from_slot_data(world: "RaC3World") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if world.game in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough[world.game]
            world.options.start_inventory_from_pool.value = world.passthrough[RAC3OPTION.START_INVENTORY_FROM_POOL]
            world.options.starting_weapons.value = world.passthrough[RAC3OPTION.STARTING_WEAPONS]
            world.options.bolt_and_xp_multiplier.value = world.passthrough[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
            world.options.enable_progressive_weapons.value = world.passthrough[RAC3OPTION.ENABLE_PROGRESSIVE_WEAPONS]
            world.options.armor_upgrade.value = world.passthrough[RAC3OPTION.ARMOR_UPGRADE]
            world.options.skill_points.value = world.passthrough[RAC3OPTION.SKILL_POINTS]
            world.options.trophies.value = world.passthrough[RAC3OPTION.TROPHIES]
            world.options.titanium_bolts.value = world.passthrough[RAC3OPTION.TITANIUM_BOLTS]
            world.options.nanotech_milestones.value = world.passthrough[RAC3OPTION.NANOTECH_MILESTONES]
            world.options.ship_nose = world.passthrough[RAC3OPTION.SHIP_NOSE]
            world.options.ship_wings = world.passthrough[RAC3OPTION.SHIP_WINGS]
            world.options.ship_skin = world.passthrough[RAC3OPTION.SHIP_SKIN]
            world.options.skin = world.passthrough[RAC3OPTION.SKIN]
            world.options.traps_enabled.value = world.passthrough[RAC3OPTION.ENABLE_TRAPS]
            world.options.trap_weight.value = world.passthrough[RAC3OPTION.TRAP_WEIGHT]
            world.options.rangers.value = world.passthrough[RAC3OPTION.RANGERS]
            world.options.arena.value = world.passthrough[RAC3OPTION.ARENA]
            world.options.vidcomics.value = world.passthrough[RAC3OPTION.VIDCOMICS]
            world.options.exclude_locations.value = world.passthrough[RAC3OPTION.EXCLUDE]
            world.options.deathlink.value = world.passthrough[RAC3OPTION.DEATHLINK]
            world.options.vr_challenges.value = world.passthrough[RAC3OPTION.VR_CHALLENGES]
            world.options.sewer_crystals.value = world.passthrough[RAC3OPTION.SEWER_CRYSTALS]
            world.options.sewer_limitation.value = world.passthrough[RAC3OPTION.SEWER_LIMITATION]
            world.options.nanotech_limitation.value = world.passthrough[RAC3OPTION.NANOTECH_LIMITATION]
            world.options.weapon_vendors.value = world.passthrough[RAC3OPTION.WEAPON_VENDORS]
            world.options.filler_weight.value = world.passthrough[RAC3OPTION.FILLER_WEIGHT]
            world.options.one_hp_challenge.value = world.passthrough[RAC3OPTION.ONE_HP_CHALLENGE]
        else:
            world.using_ut = False
    else:
        world.using_ut = False


def map_page_index(data: str) -> int:
    if data:
        return RAC3_REGION_DATA_TABLE[data].ID
    else:
        return RAC3_REGION_DATA_TABLE[RAC3REGION.GALAXY].ID


tracker_world: dict[str, Any] = {
    "map_page_maps": "maps/maps.json",
    "map_page_locations": "locations/locations.json",
    "map_page_setting_key": r'rac3_current_planet_{player}_{team}',
    "map_page_index": map_page_index,
    "poptracker_name_mapping": UT_MAPPING,
}
