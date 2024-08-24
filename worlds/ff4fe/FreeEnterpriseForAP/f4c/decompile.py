import os
import argparse

from . import ff4bin
from . import consts
from . import hints

from .decompile_events import decompile_events
from .decompile_text import decompile_text
from .decompile_triggers import decompile_triggers
from .decompile_event_calls import decompile_event_calls
from .decompile_npcs import decompile_npcs, decompile_map_placements
from .decompile_ai import decompile_ai
from .decompile_ai_scripts import decompile_ai_scripts
from .decompile_map_infos import decompile_map_infos
from .decompile_map_grids import decompile_map_grids
from .decompile_tilesets import decompile_tilesets
from .decompile_shops import decompile_shops
from .decompile_actors import decompile_actors
from .decompile_drop_tables import decompile_drop_tables
from .decompile_monsters import decompile_monsters, decompile_monster_stats
from .decompile_formations import decompile_formations
from .decompile_spells import decompile_spells
from .decompile_spell_sets import decompile_spell_sets

parser = argparse.ArgumentParser()
parser.add_argument('rom')
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('--events', action='store_true')
parser.add_argument('--text', action='store_true')
parser.add_argument('--triggers', action='store_true')
parser.add_argument('--eventcalls', action='store_true')
parser.add_argument('--npcs', action='store_true')
parser.add_argument('--ai', action='store_true')
parser.add_argument('--maps', action='store_true')
parser.add_argument('--tilesets', action='store_true')
parser.add_argument('--shops', action='store_true')
parser.add_argument('--actors', action='store_true')
parser.add_argument('--drops', action='store_true')
parser.add_argument('--monsters', action='store_true')
parser.add_argument('--formations', action='store_true')
parser.add_argument('--spells', action='store_true')
parser.add_argument('--spellsets', action='store_true')

parser.add_argument('-i', '--ignorechecksum', action='store_true')
parser.add_argument('-o', '--output')
args = parser.parse_args()

rom = ff4bin.Rom(args.rom, ignore_checksum=args.ignorechecksum)

consts.load_file(os.path.join(os.path.dirname(__file__), 'default.consts'))
hints.load_file(os.path.join(os.path.dirname(__file__), 'default.hints'))

output_prefix = args.output
if not output_prefix:
    output_prefix = os.path.splitext(args.rom)[0] + '.decomp'

if args.all or args.events:
    filename = output_prefix + '.events.f4c'
    print("Exporting events to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_events(rom))

if args.all or args.text:
    filename = output_prefix + '.text.f4t'
    print("Exporting text to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_text(rom))

if args.all or args.triggers:
    filename = output_prefix + '.triggers.f4c'
    print("Exporting triggers to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_triggers(rom))

if args.all or args.eventcalls:
    filename = output_prefix + '.eventcalls.f4c'
    print("Exporting event calls to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_event_calls(rom))

if args.all or args.npcs:
    filename = output_prefix + '.npcs.f4c'
    print("Exporting NPCs to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_npcs(rom))

    filename = output_prefix + '.placements.f4c'
    print("Exporting NPC placements to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_map_placements(rom))

if args.all or args.ai:
    filename = output_prefix + '.ai.f4c'
    print("Exporting AI to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_ai(rom))

    filename = output_prefix + '.aiscripts.f4c'
    print("Exporting AI scripts to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_ai_scripts(rom))

if args.all or args.maps:
    filename = output_prefix + '.mapinfo.f4c'
    print("Exporting map info to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_map_infos(rom))

    filename = output_prefix + '.mapgrids.f4c'
    print("Exporting map grids to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_map_grids(rom))

if args.all or args.shops:
    filename = output_prefix + '.shops.f4c'
    print("Exporting shops to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_shops(rom))

if args.all or args.tilesets:
    filename = output_prefix + '.tilesets.f4c'
    print("Exporting tilesets to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_tilesets(rom))

if args.all or args.actors:
    filename = output_prefix + '.actors.f4c'
    print("Exporting actors to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_actors(rom))

if args.all or args.drops:
    filename = output_prefix + '.drops.f4c'
    print("Exporting drops to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_drop_tables(rom))

if args.all or args.monsters:
    filename = output_prefix + '.monsters.f4c'
    print("Exporting monsters to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_monsters(rom))

    filename = output_prefix + '.monsterstats.f4c'
    print("Exporting monster stats to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_monster_stats(rom))

if args.all or args.formations:
    filename = output_prefix + '.formations.f4c'
    print("Exporting formations to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_formations(rom))

if args.all or args.spells:
    filename = output_prefix + '.spells.f4c'
    print("Exporting spells to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_spells(rom))

if args.all or args.spellsets:
    filename = output_prefix + '.spellsets.f4c'
    print("Exporting spell sets to {}".format(filename))
    with open(filename, 'w') as outfile:
        outfile.write(decompile_spell_sets(rom))
