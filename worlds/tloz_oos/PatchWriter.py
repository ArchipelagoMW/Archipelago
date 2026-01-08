import json
from collections import defaultdict

from typing import TYPE_CHECKING
from worlds.tloz_oos.patching.ProcedurePatch import OoSProcedurePatch
from .data.Constants import *
from . import OracleOfSeasonsOptions

if TYPE_CHECKING:
    from . import OracleOfSeasonsWorld


def oos_create_ap_procedure_patch(world: "OracleOfSeasonsWorld") -> OoSProcedurePatch:
    patch = OoSProcedurePatch()

    patch.player = world.player
    patch.player_name = world.multiworld.get_player_name(world.player)

    patch_data = {
        "version": f"{world.world_version.as_simple_string()}",
        "seed": world.multiworld.seed,
        "options": world.options.as_dict(
            *[option_name for option_name in OracleOfSeasonsOptions.type_hints
              if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_patch")]),
        "samasa_gate_sequence": " ".join([str(x) for x in world.samasa_gate_code]),
        "lost_woods_item_sequence": world.lost_woods_item_sequence,
        "lost_woods_main_sequence": world.lost_woods_main_sequence,
        "default_seasons": world.default_seasons,
        "old_man_rupee_values": world.old_man_rupee_values,
        "dungeon_entrances": {a.replace(" entrance", ""): b.replace("enter ", "")
                              for a, b in world.dungeon_entrances.items()},
        "locations": {},
        "subrosia_portals": world.portal_connections,
        "shop_prices": world.shop_prices,
        "subrosia_seaside_location": world.random.randint(0, 3),
        "region_hints": world.region_hints,
    }

    for loc in world.multiworld.get_locations(world.player):
        # Skip event locations which are not real in-game locations that need to be patched
        if loc.address is None:
            continue
        if loc.item.player == loc.player:
            patch_data["locations"][loc.name] = {
                "item": loc.item.name
            }
        else:
            patch_data["locations"][loc.name] = {
                "item": loc.item.name,
                "player": world.multiworld.get_player_name(loc.item.player),
                "progression": loc.item.advancement
            }

    patch_data_item_hints = []
    for item_hint in world.item_hints:
        if item_hint is None:
            # Joke hint
            patch_data_item_hints.append(None)
            continue
        location = item_hint.location
        player = location.player
        if player == world.player:
            player = None
        else:
            player = world.multiworld.get_player_name(player)
        patch_data_item_hints.append((item_hint.name, location.name, player))
    patch_data["item_hints"] = patch_data_item_hints

    start_inventory = defaultdict(int)
    for item in world.multiworld.precollected_items[world.player]:
        start_inventory[item.name] += 1
    patch_data["start_inventory"] = dict(start_inventory)

    patch.write_file("patch.dat", json.dumps(patch_data).encode("utf-8"))
    return patch
