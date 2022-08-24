from typing import Dict, List, Set, Tuple, TextIO

from BaseClasses import Item, MultiWorld, ItemClassification
from .items import item_table, filler_items
from .locations import get_locations
from ..AutoWorld import World, WebWorld
from .regions import create_regions
from .logic import PokemonLogic
from .options import pokemon_rb_options
from .rom_addresses import rom_addresses
from .text import encode_text
from Patch import APDeltaPatch, read_rom
from .poke_data import pokemons, types, type_chart
import Utils
import os
import hashlib
import bsdiff4


class PokemonRedBlueWorld(World):
    """Pokemon"""
    game = "Pokemon Red - Blue"
    options = pokemon_rb_options
    remote_items = False
    data_version = 0
    topology_present = False

    item_name_to_id = {name: data.id for name, data in item_table.items()}
    location_name_to_id = {location.name: location.address for location in get_locations()}
    item_name_groups = {}

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.fly_map = None
        self.fly_map_code = None
        self.extra_badges = {}
        self.type_chart = None

    def generate_basic(self):
        if self.world.badges_needed_for_hm_moves[self.player].value >= 2:
            badges_to_add = ["Soul Badge", "Volcano Badge", "Earth Badge"]
            if self.world.badges_needed_for_hm_moves[self.player].value == 3:
                for _ in range(0, 2):
                    badges_to_add.append(self.world.random.choice(["Boulder Badge", "Cascade Badge", "Thunder Badge",
                                                                   "Rainbow Badge", "Marsh Badge",   "Soul Badge",
                                                                   "Volcano Badge", "Earth Badge"]))
            hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
            self.world.random.shuffle(hm_moves)
            self.extra_badges = {}
            for badge in badges_to_add:
                self.extra_badges[hm_moves.pop()] = badge


    def create_items(self) -> None:
        locations = get_locations(self.player)
        item_pool = []
        badgelocs = []
        badges = []
        for location in locations:
            if "Hidden" in location.name and not self.world.randomize_hidden_items[self.player].value:
                continue
            item = self.create_item(location.original_item)
            if location.event:
                self.world.get_location(location.name, self.player).place_locked_item(item)
            elif "Badge" in item.name and not self.world.badgesanity[self.player]:
                badgelocs.append(self.world.get_location(location.name, self.player))
                badges.append(item)
            else:
                item_pool.append(item)

        self.world.random.shuffle(item_pool)
        if self.world.extra_key_items[self.player].value:
            for item_name in ["Plant Key", "Mansion Key", "Hideout Key", "Safari Pass"]:
                item = self.create_item(item_name)
                for i, old_item in enumerate(item_pool):
                    if old_item.classification == ItemClassification.filler:
                        item_pool[i] = item
                        break
        self.world.random.shuffle(item_pool)
        place_pc_item = True
        if self.world.old_man[self.player].value == 1:
            place_pc_item = [True, False][self.world.random.randint(0, 1)]
        if place_pc_item:
            for i, item in enumerate(item_pool):
                if "Badge" not in item.name:
                    self.world.get_location("Pallet Town - Player's PC", self.player).place_locked_item(item_pool.pop(i))
                    break
        if self.world.old_man[self.player].value == 1:
            if not place_pc_item:
                loc = self.world.get_location("Pallet Town - Player's PC", self.player)
            else:
                loc = self.world.get_location("Viridian City - Pokemart Quest", self.player)
            for i, item in enumerate(item_pool):
                if item.name == "Oak's Parcel":
                    loc.place_locked_item(item_pool.pop(i))

        self.world.itempool += item_pool

        if not self.world.badgesanity[self.player].value:
            state = self.world.get_all_state(False)
            self.world.random.shuffle(badges)
            from Fill import fill_restrictive
            fill_restrictive(self.world, state, badgelocs, badges, True, True)

    def create_regions(self):
        if self.world.free_fly_location[self.player].value:
            fly_map_code = self.world.random.randint(5, 9)
            if fly_map_code == 9:
                fly_map_code = 10
            if fly_map_code == 5:
                fly_map_code = 4
        else:
            fly_map_code = 0
        self.fly_map = ["Pallet Town", "Viridian City", "Pewter City", "Cerulean City", "Lavender Town",
                        "Vermilion City", "Celadon City", "Fuchsia City", "Cinnabar Island", "Indigo Plateau",
                        "Saffron City"][fly_map_code]
        self.fly_map_code = fly_map_code
        create_regions(self.world, self.player)
        self.world.completion_condition[self.player] = lambda state, player=self.player: state.has("Become Champion", player=player)

    def create_item(self, name: str) -> Item:
        return PokemonRBItem(name, self.player)

    def generate_output(self, output_directory: str):

        random = self.world.slot_seeds[self.player]
        game_version = self.world.game_version[self.player].current_key
        data = bytearray(get_base_rom_bytes(game_version))

        for location in self.world.get_locations():
            if location.player != self.player or location.address is None:
                continue
            if location.item.player == self.player:
                if location.rom_address:
                    data[location.rom_address] = self.item_name_to_id[location.item.name] - 172000000

            else:
                data[location.rom_address] = 0x2C  # AP Item
        data[rom_addresses['Fly_Location']] = self.fly_map_code

        # if self.world.goal[self.player].value:
        #     data[rom_addresses['Options']] |= 1
        if self.world.extra_key_items[self.player].value:
            data[rom_addresses['Options']] |= 4
        if self.world.blind_trainers[self.player].value > 0:
            data[rom_addresses['Option_Trainer_Encounters']] = 1
            if self.world.blind_trainers[self.player].value == 2:
                data[rom_addresses['Option_Trainer_Encounters'] + 2] = 0xC0  # ret nz
        data[rom_addresses['Option_Cerulean_Cave_Condition']] = self.world.cerulean_cave_goal[self.player].value
        data[rom_addresses['Option_Encounter_Minimum_Steps']] = self.world.minimum_steps_between_encounters[self.player].value
        data[rom_addresses['Option_Badge_Goal']] = self.world.badge_goal[self.player].value - 2
        data[rom_addresses['Option_Viridian_Gym_Badges']] = self.world.badge_goal[self.player].value - 1
        data[rom_addresses['Option_EXP_Modifier']] = self.world.exp_modifier[self.player].value
        if self.world.extra_strength_boulders[self.player].value:
            for i in range(0, 3):
                data[rom_addresses['Option_Boulders'] + (i * 3)] = 0x15
        if self.world.old_man[self.player].value == 2:
            data[rom_addresses['Option_Old_Man']] = 0x11
            data[rom_addresses['Option_Old_Man_Lying']] = 0x15
        hm_moves = ["Cut", "Fly", "Surf", "Strength", "Flash"]
        if self.world.badges_needed_for_hm_moves[self.player].value == 0:
            for hm_move in hm_moves:
                write_bytes(data, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                            rom_addresses["HM_" + hm_move + "_Badge_a"])
        elif self.extra_badges:
            written_badges = set()
            for hm_move, badge in self.extra_badges.items():
                data[rom_addresses["HM_" + hm_move + "_Badge_b"]] = {"Boulder Badge": 0x47, "Cascade Badge": 0x4F,
                     "Thunder Badge": 0x57, "Rainbow Badge": 0x5F, "Soul Badge": 0x67, "Marsh Badge": 0x6F,
                     "Volcano Badge": 0x77, "Earth Badge": 0x7F}[badge]
                move_text = hm_move
                if badge not in ["Marsh Badge", "Volcano Badge", "Earth Badge"]:
                    move_text = ", " + move_text
                write_bytes(data, encode_text(move_text.upper()), rom_addresses["Badge_Text_" + badge.replace(" ", "_")])
                written_badges.update(badge)
            for badge in ["Marsh Badge", "Volcano Badge", "Earth Badge"]:
                if badge not in written_badges:
                    write_bytes(data, encode_text("Nothing"), rom_addresses["Badge_Text_" + badge.replace(" ", "_")])

        chart = type_chart.deepcopy()
        if self.world.randomize_type_matchup_attacking_types[self.player].value == 1:
            attacking_types = []
            for matchup in chart:
                attacking_types.append(matchup[0])
            self.world.random.shuffle(attacking_types)
            for (matchup, attacking_type) in zip(chart, attacking_types):
                matchup[0] = attacking_type
        elif self.world.randomize_type_matchup_attacking_types[self.player].value == 2:
            for matchup in chart:
                matchup[0] = self.world.random.choice(list(types.keys()))
        if self.world.randomize_type_matchup_defending_types[self.player].value == 1:
            defending_types = []
            for matchup in chart:
                defending_types.append(matchup[1])
            self.world.random.shuffle(defending_types)
            for (matchup, defending_type) in zip(chart, defending_types):
                matchup[1] = defending_type
        elif self.world.randomize_type_matchup_defending_types[self.player].value == 2:
            for matchup in chart:
                matchup[1] = self.world.random.choice(list(types.keys()))
        type_loc = rom_addresses["Type_Chart"]
        for matchup in chart:
            data[type_loc] = types[matchup[0]]
            data[type_loc + 1] = types[matchup[1]]
            data[type_loc + 2] = matchup[2]
            type_loc += 3
        self.type_chart = chart





        mons = list(pokemons.values())
        random.shuffle(mons)
        data[rom_addresses['Title_Mon_First']] = mons.pop()
        for mon in range(0, 16):
            data[rom_addresses['Title_Mons'] + mon] = mons.pop()
        write_bytes(data, self.world.seed_name.encode(), 0xFFDC)
        write_bytes(data, encode_text(self.world.seed_name, 20, True), rom_addresses['Title_Seed'])
        write_bytes(data, self.world.player_name[self.player].encode(), 0xFFF0)
        slot_name = self.world.player_name[self.player]
        slot_name.replace("@", " ")
        slot_name.replace("<", " ")
        slot_name.replace(">", " ")
        write_bytes(data, encode_text(slot_name, 16, True, True), rom_addresses['Title_Slot_Name'])
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.world.get_file_safe_player_name(self.player).replace(' ', '_')}" \
            if self.world.player_name[self.player] != 'Player%d' % self.player else ''
        rompath = os.path.join(output_directory, f'AP_{self.world.seed_name}{outfilepname}.gb')
        with open(rompath, 'wb') as outfile:
            outfile.write(data)
        if self.world.game_version[self.player].current_key == "red":
            patch = RedDeltaPatch(os.path.splitext(rompath)[0] + RedDeltaPatch.patch_file_ending, player=self.player,
                                  player_name=self.world.player_name[self.player], patched_path=rompath)
        else:
            patch = BlueDeltaPatch(os.path.splitext(rompath)[0] + BlueDeltaPatch.patch_file_ending, player=self.player,
                                   player_name=self.world.player_name[self.player], patched_path=rompath)
        patch.write()
        os.unlink(rompath)

    def write_spoiler_header(self, spoiler_handle: TextIO):
        if self.world.free_fly_location[self.player].value:
            spoiler_handle.write('Fly unlocks:                     %s\n' % self.fly_map)
        if self.extra_badges:
            for hm_move, badge in self.extra_badges.items():
                spoiler_handle.write(hm_move + " enabled by: " + (" " * 20)[:20 - len(hm_move)] + badge + "\n")

    def write_spoiler(self, spoiler_handle):
        if self.world.randomize_type_matchup_attacking_types[self.player].value or \
                self.world.randomize_type_matchup_defending_types[self.player].value:
            spoiler_handle.write("\n\nType matchups:\n\n")
            for matchup in self.type_chart:
                spoiler_handle.write(f"{matchup[0]} deals {matchup[2] * 10}% damage to {matchup[1]}\n")

class BlueDeltaPatch(APDeltaPatch):
    patch_file_ending = ".apblue"
    hash = "50927e843568814f7ed45ec4f944bd8b"
    game_version = "blue"
    game = "Pokemon Red - Blue"
    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(cls.game_version, cls.hash)


class RedDeltaPatch(APDeltaPatch):
    patch_file_ending = ".apred"
    hash = "3d45c1ee9abd5738df46d2bdda8b57dc"
    game_version = "red"
    game = "Pokemon Red - Blue"
    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes(cls.game_version, cls.hash)


def write_bytes(data, byte_array, address):
    for byte in byte_array:
        data[address] = byte
        address += 1


def get_base_rom_bytes(game_version: str, hash: str="") -> bytes:
    file_name = get_base_rom_path(game_version)
    base_rom_bytes = bytes(read_rom(open(file_name, "rb")))
    if hash:
        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if hash != basemd5.hexdigest():
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        #get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    with open(Utils.local_path('data', f'basepatch_{game_version}.bsdiff4'), 'rb') as stream:
        base_patch = bytes(stream.read())
    base_rom_bytes = bsdiff4.patch(base_rom_bytes, base_patch)
    return base_rom_bytes


def get_base_rom_path(game_version: str) -> str:
    options = Utils.get_options()
    file_name = options["pkrb_options"][f"{game_version}_rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.local_path(file_name)
    return file_name


class PokemonRBItem(Item):
    game = "Pokemon Red - Blue"
    type = "idk"
    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(PokemonRBItem, self).__init__(
            name,
            item_data.classification,
            item_data.id, player
        )
