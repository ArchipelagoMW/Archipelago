import random
import logging
import os
import threading

from BaseClasses import Item, CollectionState
from .SubClasses import ALttPItem
from ..AutoWorld import World
from .Options import alttp_options
from .Items import as_dict_item_table, item_name_groups, item_table
from .Regions import lookup_name_to_id, create_regions, mark_light_world_regions
from .Rules import set_rules
from .ItemPool import generate_itempool
from .Shops import create_shops
from .Dungeons import create_dungeons
from .Rom import LocalRom, patch_rom, patch_race_rom, patch_enemizer, apply_rom_settings, get_hash_string
import Patch

from .InvertedRegions import create_inverted_regions, mark_dark_world_regions
from .EntranceShuffle import link_entrances, link_inverted_entrances, plando_connect

lttp_logger = logging.getLogger("A Link to the Past")

class ALTTPWorld(World):
    game: str = "A Link to the Past"
    options = alttp_options
    topology_present = True
    item_name_groups = item_name_groups
    item_names = frozenset(item_table)
    location_names = frozenset(lookup_name_to_id)
    hint_blacklist = {"Triforce"}

    item_name_to_id = {name: data.item_code for name, data in item_table.items() if type(data.item_code) == int}
    location_name_to_id = lookup_name_to_id

    data_version = 7
    remote_items: bool = False

    set_rules = set_rules

    create_items = generate_itempool

    def create_regions(self):
        self.rom_name_available_event = threading.Event()

        player = self.player
        world = self.world
        if world.open_pyramid[player] == 'goal':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'}
        elif world.open_pyramid[player] == 'auto':
            world.open_pyramid[player] = world.goal[player] in {'crystals', 'ganontriforcehunt',
                                                                'localganontriforcehunt', 'ganonpedestal'} and \
                                         (world.shuffle[player] in {'vanilla', 'dungeonssimple', 'dungeonsfull',
                                                                    'dungeonscrossed'} or not world.shuffle_ganon)
        else:
            world.open_pyramid[player] = {'on': True, 'off': False, 'yes': True, 'no': False}.get(
                world.open_pyramid[player], 'auto')

        world.triforce_pieces_available[player] = max(world.triforce_pieces_available[player],
                                                      world.triforce_pieces_required[player])

        if world.mode[player] != 'inverted':
            create_regions(world, player)
        else:
            create_inverted_regions(world, player)
        create_shops(world, player)
        create_dungeons(world, player)


        if world.logic[player] not in ["noglitches", "minorglitches"] and world.shuffle[player] in \
                {"vanilla", "dungeonssimple", "dungeonsfull", "simple", "restricted", "full"}:
            world.fix_fake_world[player] = False

        # seeded entrance shuffle
        old_random = world.random
        world.random = random.Random(world.er_seeds[player])

        if world.mode[player] != 'inverted':
            link_entrances(world, player)
            mark_light_world_regions(world, player)
        else:
            link_inverted_entrances(world, player)
            mark_dark_world_regions(world, player)

        world.random = old_random
        plando_connect(world, player)

    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.name.startswith('Progressive '):
            if 'Sword' in item.name:
                if state.has('Golden Sword', item.player):
                    pass
                elif state.has('Tempered Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 4:
                    state.prog_items['Golden Sword', item.player] += 1
                    return True
                elif state.has('Master Sword', item.player) and self.world.difficulty_requirements[
                    item.player].progressive_sword_limit >= 3:
                    state.prog_items['Tempered Sword', item.player] += 1
                    return True
                elif state.has('Fighter Sword', item.player) and self.world.difficulty_requirements[item.player].progressive_sword_limit >= 2:
                    state.prog_items['Master Sword', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_sword_limit >= 1:
                    state.prog_items['Fighter Sword', item.player] += 1
                    return True
            elif 'Glove' in item.name:
                if state.has('Titans Mitts', item.player):
                    pass
                elif state.has('Power Glove', item.player):
                    state.prog_items['Titans Mitts', item.player] += 1
                    return True
                else:
                    state.prog_items['Power Glove', item.player] += 1
                    return True
            elif 'Shield' in item.name:
                if state.has('Mirror Shield', item.player):
                    pass
                elif state.has('Red Shield', item.player) and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 3:
                    state.prog_items['Mirror Shield', item.player] += 1
                    return True
                elif state.has('Blue Shield', item.player)  and self.world.difficulty_requirements[item.player].progressive_shield_limit >= 2:
                    state.prog_items['Red Shield', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_shield_limit >= 1:
                    state.prog_items['Blue Shield', item.player] += 1
                    return True
            elif 'Bow' in item.name:
                if state.has('Silver', item.player):
                    pass
                elif state.has('Bow', item.player) and self.world.difficulty_requirements[item.player].progressive_bow_limit >= 2:
                    state.prog_items['Silver Bow', item.player] += 1
                    return True
                elif self.world.difficulty_requirements[item.player].progressive_bow_limit >= 1:
                    state.prog_items['Bow', item.player] += 1
                    return True
        elif item.advancement or item.smallkey or item.bigkey:
            state.prog_items[item.name, item.player] += 1
            return True
        return False

    def pre_fill(self):
        from Fill import fill_restrictive, FillError
        attempts = 5
        world = self.world
        player = self.player
        all_state = world.get_all_state(keys=True)
        crystals = [self.create_item(name) for name in ['Red Pendant', 'Blue Pendant', 'Green Pendant', 'Crystal 1', 'Crystal 2', 'Crystal 3', 'Crystal 4', 'Crystal 7', 'Crystal 5', 'Crystal 6']]
        crystal_locations = [world.get_location('Turtle Rock - Prize', player),
                             world.get_location('Eastern Palace - Prize', player),
                             world.get_location('Desert Palace - Prize', player),
                             world.get_location('Tower of Hera - Prize', player),
                             world.get_location('Palace of Darkness - Prize', player),
                             world.get_location('Thieves\' Town - Prize', player),
                             world.get_location('Skull Woods - Prize', player),
                             world.get_location('Swamp Palace - Prize', player),
                             world.get_location('Ice Palace - Prize', player),
                             world.get_location('Misery Mire - Prize', player)]
        placed_prizes = {loc.item.name for loc in crystal_locations if loc.item}
        unplaced_prizes = [crystal for crystal in crystals if crystal.name not in placed_prizes]
        empty_crystal_locations = [loc for loc in crystal_locations if not loc.item]
        for attempt in range(attempts):
            try:
                prizepool = unplaced_prizes.copy()
                prize_locs = empty_crystal_locations.copy()
                world.random.shuffle(prize_locs)
                fill_restrictive(world, all_state, prize_locs, prizepool, True, lock=True)
            except FillError as e:
                lttp_logger.exception("Failed to place dungeon prizes (%s). Will retry %s more times", e,
                                                attempts - attempt)
                for location in empty_crystal_locations:
                    location.item = None
                continue
            break
        else:
            raise FillError('Unable to place dungeon prizes')

    @classmethod
    def stage_pre_fill(cls, world):
        from .Dungeons import fill_dungeons_restrictive
        fill_dungeons_restrictive(world)

    def generate_output(self, output_directory: str):
        world = self.world
        player = self.player

        use_enemizer = (world.boss_shuffle[player] != 'none' or world.enemy_shuffle[player]
                        or world.enemy_health[player] != 'default' or world.enemy_damage[player] != 'default'
                        or world.shufflepots[player] or world.bush_shuffle[player]
                        or world.killable_thieves[player])

        rom = LocalRom(world.alttp_rom)

        patch_rom(world, rom, player, use_enemizer)

        if use_enemizer:
            patch_enemizer(world, player, rom, world.enemizer, output_directory)

        if world.is_race:
            patch_race_rom(rom, world, player)

        world.spoiler.hashes[player] = get_hash_string(rom.hash)

        palettes_options = {
            'dungeon': world.uw_palettes[player],
            'overworld': world.ow_palettes[player],
            'hud': world.hud_palettes[player],
            'sword': world.sword_palettes[player],
            'shield': world.shield_palettes[player],
            'link': world.link_palettes[player]
        }
        palettes_options = {key: option.current_key for key, option in palettes_options.items()}

        apply_rom_settings(rom, world.heartbeep[player].current_key,
                           world.heartcolor[player].current_key,
                           world.quickswap[player],
                           world.menuspeed[player].current_key,
                           world.music[player],
                           world.sprite[player],
                           palettes_options, world, player, True,
                           reduceflashing=world.reduceflashing[player] or world.is_race,
                           triforcehud=world.triforcehud[player].current_key)

        outfilepname = f'_P{player}'
        outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
            if world.player_name[player] != 'Player%d' % player else ''

        rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
        rom.write_to_file(rompath, hide_enemizer=True)
        Patch.create_patch_file(rompath, player=player, player_name=world.player_name[player])
        os.unlink(rompath)
        self.rom_name = rom.name
        self.rom_name_available_event.set()

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        new_name = base64.b64encode(bytes(self.rom_name)).decode()
        payload = multidata["connect_names"][self.world.player_name[self.player]]
        multidata["connect_names"][new_name] = payload
        del (multidata["connect_names"][self.world.player_name[self.player]])

    def get_required_client_version(self) -> tuple:
        return max((0, 1, 4), super(ALTTPWorld, self).get_required_client_version())

    def create_item(self, name: str) -> Item:
        return ALttPItem(name, self.player, **as_dict_item_table[name])


