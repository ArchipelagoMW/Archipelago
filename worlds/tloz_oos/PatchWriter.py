import yaml

from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
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
        "version": VERSION,
        "seed": world.multiworld.seed,
        "options": world.options.as_dict(
            *[option_name for option_name in OracleOfSeasonsOptions.type_hints
              if hasattr(OracleOfSeasonsOptions.type_hints[option_name], "include_in_patch")]),
        "samasa_gate_sequence": ' '.join([str(x) for x in world.samasa_gate_code]),
        "lost_woods_item_sequence": world.lost_woods_item_sequence,
        "lost_woods_main_sequence": world.lost_woods_main_sequence,
        "default_seasons": world.default_seasons,
        "old_man_rupee_values": world.old_man_rupee_values,
        "dungeon_entrances": {a.replace(" entrance", ""): b.replace("enter ", "")
                              for a, b in world.dungeon_entrances.items()},
        "locations": {},
        "subrosia_portals": world.portal_connections,
        "shop_prices": world.shop_prices,
        "subrosia_seaside_location": world.random.randint(0, 3)
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
                "progression": (loc.item.classification & ItemClassification.progression) != 0
            }

    patch.write_file("patch.dat", yaml.dump(patch_data).encode('utf-8'))
    return patch
