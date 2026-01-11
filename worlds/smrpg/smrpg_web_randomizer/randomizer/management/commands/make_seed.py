import json
import os
import random
import __main__
from pkgutil import get_data

from .generatesample import ALL_FLAGS

from ....randomizer.logic.main import GameWorld, Settings


class Command():
    help = 'Generate a statistical sampling of seeds to compare randomization spreads.'

    def add_arguments(self, parser):
        """Add optional arguments.

        Args:
            parser (argparse.ArgumentParser): Parser

        """

        parser.add_argument('-r', '--rom', dest='rom', required=True,
                            help='Path to a Mario RPG rom')

        parser.add_argument('-s', '--seed', dest='seed', type=int, default=0,
                            help='Seed')

        parser.add_argument('-o', '--output', dest='output_file', default='sample',
                            help='Output file name prefix')

        parser.add_argument('-m', '--mode', dest='mode', default='open', choices=['linear', 'open'],
                            help='Mode to use for rom.  Default: %(default)s')

        parser.add_argument('-f', '--flags', dest='flags', default=ALL_FLAGS,
                            help='Flags string (from website). If not provided, all flags will be used.')

    def handle(self, *args, **options):
        settings = Settings(options['mode'], flag_string=options['flags'])
        seed = options['seed']

        # If seed is not provided, generate a 32 bit seed integer using the CSPRNG.
        if not seed:
            r = random.SystemRandom()
            seed = r.getrandbits(32)
            del r

        world = GameWorld(seed, settings)
        ap_data = self.build_ap_data(options["ap_data"], world)
        world.randomize(ap_data)

        patch = world.build_patch()

        rom = bytearray(open(options['rom'], 'rb').read())
        base_patch = json.loads(get_data(__name__, "open_mode.json"))
        for ele in base_patch:
            key = list(ele)[0]
            bytes = ele[key]
            addr = int(key)
            for byte in bytes:
                rom[addr] = byte
                addr += 1

        for addr in patch.addresses:
            bytes = patch.get_data(addr)
            for byte in bytes:
                rom[addr] = byte
                addr += 1

        rom[0x7FC0:0x7FD4] = options["rom_name"]

        checksum = sum(rom) & 0xFFFF
        rom[0x7FDC] = (checksum ^ 0xFFFF) & 0xFF
        rom[0x7FDD] = (checksum ^ 0xFFFF) >> 8
        rom[0x7FDE] = checksum & 0xFF
        rom[0x7FDF] = checksum >> 8

        open(options['output_file'], 'wb').write(rom)
        spoiler_fname = options['output_file'] + '.spoiler'
        json.dump(world.spoiler, open(spoiler_fname, 'w'))

    def build_ap_data(self, ap_data, world):
        from ...data.items import get_default_items, RecoveryMushroom, Flower, YouMissed, \
            Coins5, Coins8, Coins10, Coins50, Coins100, Coins150, FrogCoin, InvincibilityStar, Mushroom2
        from ...data.keys import get_default_key_item_locations
        from ...data.chests import get_default_chests
        from ...data.bosses import get_default_boss_locations
        items = {item.name: item for item in get_default_items(world)}
        boxes = [*get_default_chests(world)]
        keys = [*get_default_key_item_locations(world)]
        bosses = [*get_default_boss_locations(world)]
        chests = [*boxes, *keys, *bosses]
        new_ap_data = dict()
        for chest in chests:
            chest.item = None
            if chest.name in ap_data.keys():
                item_name = ap_data[chest.name]
                if "Coins" in item_name:
                    if item_name == "FiveCoins":
                        new_ap_data[chest.name] = Coins5(world)
                    if item_name == "EightCoins":
                        new_ap_data[chest.name] = Coins8(world)
                    if item_name == "TenCoins":
                        new_ap_data[chest.name] = Coins10(world)
                    if item_name == "FiftyCoins":
                        new_ap_data[chest.name] = Coins50(world)
                    if item_name == "OneHundredCoins":
                        new_ap_data[chest.name] = Coins100(world)
                    if item_name == "OneHundredFiftyCoins":
                        new_ap_data[chest.name] = Coins150(world)
                elif item_name == "FrogCoin":
                    new_ap_data[chest.name] = FrogCoin(world)
                elif item_name == "RecoveryMushroom":
                    new_ap_data[chest.name] = RecoveryMushroom(world)
                elif item_name == "YouMissed!":
                    new_ap_data[chest.name] = YouMissed(world)
                elif item_name == "InvincibilityStar":
                    new_ap_data[chest.name] = InvincibilityStar(world)
                elif item_name == "ArchipelagoItem":
                    if chest in boxes:
                        if chest.item_allowed(Flower(world)):
                            new_ap_data[chest.name] = Flower(world)
                        else:
                            new_ap_data[chest.name] = Mushroom2(world)
                    else:
                        new_ap_data[chest.name] = Mushroom2(world)
                elif item_name == "Flower":
                    new_ap_data[chest.name] = Flower(world)
                elif item_name in items.keys():
                    item = items[item_name]
                    new_ap_data[chest.name] = item
                elif item_name == "Defeated!" or item_name == "StarPiece":
                    item = item_name
                    new_ap_data[chest.name] = item
                else:
                    print(item_name)
                    raise RuntimeError()
            elif chest.name + "(Boss)" in ap_data.keys():
                item_name = ap_data[chest.name + "(Boss)"]
                if item_name == "Defeated!" or item_name == "StarPiece":
                    item = item_name
                    new_ap_data[chest.name + "(Boss)"] = item
        return new_ap_data
