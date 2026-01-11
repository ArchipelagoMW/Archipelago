import collections
import csv
import datetime
import random
import time

from ....randomizer.data.bosses import StarLocation
from ....randomizer.data.keys import get_default_key_item_locations
from ....randomizer.data.items import Item
from ....randomizer.logic.flags import CATEGORIES
from ....randomizer.logic.main import GameWorld, Settings, VERSION

# Flag string for all flags at max level.
ALL_FLAGS = []
for category in CATEGORIES:
    for flag in category.flags:
        # Solo flag that begins with a dash.
        if flag.value.startswith('-'):
            ALL_FLAGS.append(flag.value)
        # Flag that may have a subsection of choices and/or options.
        else:
            chars = []

            if flag.choices:
                chars.append(flag.choices[-1].value[1:])

            for option in flag.options:
                chars.append(option.value[1:])

            # If flag begins with @, it doesn't do anything on its own.  Must have some option enabled.
            if flag.value.startswith('@'):
                if chars:
                    ALL_FLAGS.append(flag.value[1:] + ''.join(chars))
            else:
                ALL_FLAGS.append(flag.value[:1] + ''.join(chars))

ALL_FLAGS = ' '.join(ALL_FLAGS)


class Command():
    help = 'Generate a statistical sampling of seeds to compare randomization spreads.'

    def add_arguments(self, parser):
        """Add optional arguments.

        Args:
            parser (argparse.ArgumentParser): Parser

        """
        parser.add_argument('-s', '--samples', dest='samples', default=10000, type=int,
                            help='Number of samples to generate.  Default: %(default)s')

        parser.add_argument('-o', '--output', dest='output_file', default='sample',
                            help='Output file name prefix.  Default: %(default)s')

        parser.add_argument('-m', '--mode', dest='mode', default='open', choices=['linear', 'open'],
                            help='Mode to use for samples.  Default: %(default)s')

        parser.add_argument('-f', '--flags', dest='flags', default=ALL_FLAGS,
                            help='Flags string (from website).  If not provided, all flags will be used.')

    def handle(self, *args, **options):
        sysrand = random.SystemRandom()
        start = time.time()

        print("Generating {} samples of version {}, {} mode, flags {!r}".format(
            options['samples'], VERSION, options['mode'], options['flags']))

        stars_file = '{}_stars.csv'.format(options['output_file'])
        print("Star Locations: {}".format(stars_file))
        star_stats = {}

        key_items_file = '{}_key_items.csv'.format(options['output_file'])
        print("Key Item Locations: {}".format(key_items_file))
        key_item_stats = {}

        settings = Settings(options['mode'], flag_string=options['flags'])

        for i in range(options['samples']):
            # Generate random full standard seed.
            seed = sysrand.getrandbits(32)
            world = GameWorld(seed, settings)
            try:
                world.randomize()
            except Exception:
                elapsed = int(round(time.time() - start))
                print("Generated {} samples, elapsed time {}".format(
                    i, datetime.timedelta(seconds=elapsed)))
                print("ERROR generating seed {}".format(world.seed))
                raise

            # Record star piece shuffle stats.
            for location in [l for l in world.boss_locations if isinstance(l, StarLocation)]:
                star_stats.setdefault(location.name, 0)
                if location.has_star:
                    star_stats[location.name] += 1

            # Record key item stats.
            for location in world.key_locations:
                if isinstance(location.item, Item):
                    item_name = location.item.name
                else:
                    item_name = location.item.__name__
                key_item_stats.setdefault(item_name, collections.defaultdict(int))
                key_item_stats[item_name][location.name] += 1

            # Print running count of how many seeds we generated every 10 seeds, and on the last one.
            num_gen = i + 1
            if num_gen % 10 == 0 or num_gen == options['samples']:
                elapsed = int(round(time.time() - start))
                print("Generated {} samples, elapsed time {}".format(
                    num_gen, datetime.timedelta(seconds=elapsed)), ending='\r')

        # Blank line for newline.
        print('')

        # Write star piece shuffle stats.
        with open(stars_file, 'w') as f:
            writer = csv.writer(f)
            header = ['Boss', 'Has Star']
            writer.writerow(header)

            keys = list(star_stats.keys())
            keys.sort()
            for boss in keys:
                row = [boss, '{:.2f}%'.format(star_stats[boss] / options['samples'] * 100)]
                writer.writerow(row)

        # Write key item shuffle stats.
        with open(key_items_file, 'w') as f:
            writer = csv.writer(f)
            locations = get_default_key_item_locations(GameWorld(0, settings))
            header = ['Item'] + [l.name for l in locations]
            writer.writerow(header)

            keys = list(key_item_stats.keys())
            keys.sort()
            for item in keys:
                counts = key_item_stats[item]
                row = [item] + ['{:.2f}%'.format(counts[l.name] / options['samples'] * 100) for l in locations]
                writer.writerow(row)
