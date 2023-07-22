import base64
import itertools
import os
from enum import IntFlag
from typing import Any, ClassVar, Dict, get_type_hints, Iterator, List, Set, Tuple

import settings
from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial
from Options import AssembleOptions
from Utils import __version__
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule
from .Client import L2ACSNIClient  # noqa: F401
from .Items import ItemData, ItemType, l2ac_item_name_to_id, l2ac_item_table, L2ACItem, start_id as items_start_id
from .Locations import l2ac_location_name_to_id, L2ACLocation
from .Options import CapsuleStartingLevel, DefaultParty, EnemyFloorNumbers, EnemyMovementPatterns, EnemySprites, \
    ExpModifier, Goal, L2ACOptions
from .Rom import get_base_rom_bytes, get_base_rom_path, L2ACDeltaPatch
from .Utils import constrained_choices, constrained_shuffle
from .basepatch import apply_basepatch

CHESTS_PER_SPHERE: int = 5


class L2ACSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the US rom"""
        description = "Lufia II ROM File"
        copy_to = "Lufia II - Rise of the Sinistrals (USA).sfc"
        md5s = [L2ACDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class L2ACWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Lufia II Ancient Cave for MultiWorld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["word_fcuk"]
    )]
    theme = "dirt"


class L2ACWorld(World):
    """
    The Ancient Cave is a roguelike dungeon crawling game built into
    the RGP Lufia II. Face 99 floors of ever harder to beat monsters,
    random items and find new companions on the way to face the Royal
    Jelly in the end. Can you beat it?
    """
    game: ClassVar[str] = "Lufia II Ancient Cave"
    web: ClassVar[WebWorld] = L2ACWeb()

    option_definitions: ClassVar[Dict[str, AssembleOptions]] = get_type_hints(L2ACOptions)
    settings: ClassVar[L2ACSettings]
    item_name_to_id: ClassVar[Dict[str, int]] = l2ac_item_name_to_id
    location_name_to_id: ClassVar[Dict[str, int]] = l2ac_location_name_to_id
    item_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Blue chest items": {name for name, data in l2ac_item_table.items() if data.type is ItemType.BLUE_CHEST},
        "Capsule monsters": {name for name, data in l2ac_item_table.items() if data.type is ItemType.CAPSULE_MONSTER},
        "Iris treasures": {name for name, data in l2ac_item_table.items() if data.type is ItemType.IRIS_TREASURE},
        "Party members": {name for name, data in l2ac_item_table.items() if data.type is ItemType.PARTY_MEMBER},
    }
    data_version: ClassVar[int] = 2
    required_client_version: Tuple[int, int, int] = (0, 4, 2)

    # L2ACWorld specific properties
    rom_name: bytearray
    o: L2ACOptions

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld) -> None:
        rom_file: str = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(f"Could not find base ROM for {cls.game}: {rom_file}")

        # # uncomment this section to recreate the basepatch
        # # (you will need to provide "asar.py" as well as an Asar library in the basepatch directory)
        # from .basepatch import create_basepatch
        # create_basepatch()

    def generate_early(self) -> None:
        self.rom_name = \
            bytearray(f"L2AC{__version__.replace('.', '')[:3]}_{self.player}_{self.multiworld.seed}", "utf8")[:21]
        self.rom_name.extend([0] * (21 - len(self.rom_name)))

        self.o = L2ACOptions(**{opt: getattr(self.multiworld, opt)[self.player] for opt in self.option_definitions})

        if self.o.blue_chest_count < self.o.custom_item_pool.count:
            raise ValueError(f"Number of items in custom_item_pool ({self.o.custom_item_pool.count}) is "
                             f"greater than blue_chest_count ({self.o.blue_chest_count}).")
        if self.o.capsule_starting_level == CapsuleStartingLevel.special_range_names["party_starting_level"]:
            self.o.capsule_starting_level.value = int(self.o.party_starting_level)
        if self.o.initial_floor >= self.o.final_floor:
            self.o.initial_floor.value = self.o.final_floor - 1
        if self.o.shuffle_party_members:
            self.o.default_party.value = DefaultParty.default

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu)

        ancient_dungeon = Region("AncientDungeon", self.player, self.multiworld, "Ancient Dungeon")
        item_count: int = int(self.o.blue_chest_count)
        if self.o.shuffle_capsule_monsters:
            item_count += len(self.item_name_groups["Capsule monsters"])
        if self.o.shuffle_party_members:
            item_count += len(self.item_name_groups["Party members"])
        for location_name, location_id in itertools.islice(l2ac_location_name_to_id.items(), item_count):
            ancient_dungeon.locations.append(L2ACLocation(self.player, location_name, location_id, ancient_dungeon))
        for i in range(CHESTS_PER_SPHERE, item_count, CHESTS_PER_SPHERE):
            chest_access = \
                L2ACLocation(self.player, f"Chest access {i + 1}-{i + CHESTS_PER_SPHERE}", None, ancient_dungeon)
            chest_access.place_locked_item(
                L2ACItem("Progressive chest access", ItemClassification.progression, None, self.player))
            ancient_dungeon.locations.append(chest_access)
        for iris in self.item_name_groups["Iris treasures"]:
            treasure_name: str = f"Iris treasure {self.item_name_to_id[iris] - self.item_name_to_id['Iris sword'] + 1}"
            iris_treasure: Location = \
                L2ACLocation(self.player, treasure_name, self.location_name_to_id[treasure_name], ancient_dungeon)
            iris_treasure.place_locked_item(self.create_item(iris))
            ancient_dungeon.locations.append(iris_treasure)
        self.multiworld.regions.append(ancient_dungeon)

        final_floor = Region("FinalFloor", self.player, self.multiworld, "Ancient Cave Final Floor")
        ff_reached = L2ACLocation(self.player, "Final Floor reached", None, final_floor)
        ff_reached.place_locked_item(L2ACItem("Final Floor access", ItemClassification.progression, None, self.player))
        final_floor.locations.append(ff_reached)
        boss: Location = L2ACLocation(self.player, "Boss", self.location_name_to_id["Boss"], final_floor)
        boss.place_locked_item(self.create_item("Ancient key"))
        final_floor.locations.append(boss)
        self.multiworld.regions.append(final_floor)

        menu.connect(ancient_dungeon, "AncientDungeonEntrance")
        ancient_dungeon.connect(final_floor, "FinalFloorEntrance")

    def create_items(self) -> None:
        item_pool: List[str] = self.random.choices(sorted(self.item_name_groups["Blue chest items"]),
                                                   k=self.o.blue_chest_count - self.o.custom_item_pool.count)
        item_pool += [item_name for item_name, count in self.o.custom_item_pool.items() for _ in range(count)]

        if self.o.shuffle_capsule_monsters:
            item_pool += self.item_name_groups["Capsule monsters"]
            self.o.blue_chest_count.value += len(self.item_name_groups["Capsule monsters"])
        if self.o.shuffle_party_members:
            item_pool += self.item_name_groups["Party members"]
            self.o.blue_chest_count.value += len(self.item_name_groups["Party members"])
        for item_name in item_pool:
            self.multiworld.itempool.append(self.create_item(item_name))

    def set_rules(self) -> None:
        for i in range(1, self.o.blue_chest_count):
            if i % CHESTS_PER_SPHERE == 0:
                set_rule(self.multiworld.get_location(f"Blue chest {i + 1}", self.player),
                         lambda state, j=i: state.has("Progressive chest access", self.player, j // CHESTS_PER_SPHERE))
                set_rule(self.multiworld.get_location(f"Chest access {i + 1}-{i + CHESTS_PER_SPHERE}", self.player),
                         lambda state, j=i: state.can_reach(f"Blue chest {j}", "Location", self.player))
            else:
                set_rule(self.multiworld.get_location(f"Blue chest {i + 1}", self.player),
                         lambda state, j=i: state.can_reach(f"Blue chest {j}", "Location", self.player))

        set_rule(self.multiworld.get_entrance("FinalFloorEntrance", self.player),
                 lambda state: state.can_reach(f"Blue chest {self.o.blue_chest_count}", "Location", self.player))
        for i in range(9):
            set_rule(self.multiworld.get_location(f"Iris treasure {i + 1}", self.player),
                     lambda state: state.can_reach(f"Blue chest {self.o.blue_chest_count}", "Location", self.player))
        set_rule(self.multiworld.get_location("Boss", self.player),
                 lambda state: state.can_reach(f"Blue chest {self.o.blue_chest_count}", "Location", self.player))
        if self.o.shuffle_capsule_monsters:
            add_rule(self.multiworld.get_location("Boss", self.player), lambda state: state.has("DARBI", self.player))
        if self.o.shuffle_party_members:
            add_rule(self.multiworld.get_location("Boss", self.player), lambda state: state.has("Dekar", self.player)
                     and state.has("Guy", self.player) and state.has("Arty", self.player))

        if self.o.goal == Goal.option_final_floor:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Final Floor access", self.player)
        elif self.o.goal == Goal.option_iris_treasure_hunt:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has_group("Iris treasures", self.player, int(self.o.iris_treasures_required))
        elif self.o.goal == Goal.option_boss:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Ancient key", self.player)
        elif self.o.goal == Goal.option_boss_iris_treasure_hunt:
            self.multiworld.completion_condition[self.player] = \
                lambda state: (state.has("Ancient key", self.player) and
                               state.has_group("Iris treasures", self.player, int(self.o.iris_treasures_required)))

    def generate_output(self, output_directory: str) -> None:
        rom_path: str = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")

        try:
            rom_bytearray = bytearray(apply_basepatch(get_base_rom_bytes()))
            # start and stop indices are offsets in the ROM file, not LoROM mapped SNES addresses
            rom_bytearray[0x007FC0:0x007FC0 + 21] = self.rom_name
            rom_bytearray[0x014308:0x014308 + 1] = self.o.capsule_starting_level.value.to_bytes(1, "little")
            rom_bytearray[0x01432F:0x01432F + 1] = self.o.capsule_starting_form.unlock.to_bytes(1, "little")
            rom_bytearray[0x01433C:0x01433C + 1] = self.o.capsule_starting_form.value.to_bytes(1, "little")
            rom_bytearray[0x0190D5:0x0190D5 + 1] = self.o.iris_floor_chance.value.to_bytes(1, "little")
            rom_bytearray[0x019147:0x019157 + 1:4] = self.o.blue_chest_chance.chest_type_thresholds
            rom_bytearray[0x019176] = 0x38 if self.o.gear_variety_after_b9 else 0x18
            rom_bytearray[0x019477:0x019477 + 1] = self.o.healing_floor_chance.value.to_bytes(1, "little")
            rom_bytearray[0x0194A2:0x0194A2 + 1] = self.o.crowded_floor_chance.value.to_bytes(1, "little")
            rom_bytearray[0x019E82:0x019E82 + 1] = self.o.final_floor.value.to_bytes(1, "little")
            rom_bytearray[0x01FC75:0x01FC75 + 1] = self.o.run_speed.value.to_bytes(1, "little")
            rom_bytearray[0x01FC81:0x01FC81 + 1] = self.o.run_speed.value.to_bytes(1, "little")
            rom_bytearray[0x02B2A1:0x02B2A1 + 5] = self.o.default_party.roster
            for offset in range(0x02B395, 0x02B452, 0x1B):
                rom_bytearray[offset:offset + 1] = self.o.party_starting_level.value.to_bytes(1, "little")
            for offset in range(0x02B39A, 0x02B457, 0x1B):
                rom_bytearray[offset:offset + 3] = self.o.party_starting_level.xp.to_bytes(3, "little")
            rom_bytearray[0x03AE49:0x03AE49 + 1] = self.o.boss.sprite.to_bytes(1, "little")
            rom_bytearray[0x05699E:0x05699E + 147] = self.get_goal_text_bytes()
            rom_bytearray[0x056AA3:0x056AA3 + 24] = self.o.default_party.event_script
            rom_bytearray[0x072740:0x072740 + 1] = self.o.boss.music.to_bytes(1, "little")
            rom_bytearray[0x072742:0x072742 + 1] = self.o.boss.value.to_bytes(1, "little")
            rom_bytearray[0x072748:0x072748 + 1] = self.o.boss.flag.to_bytes(1, "little")
            rom_bytearray[0x09D59B:0x09D59B + 256] = self.get_node_connection_table()
            rom_bytearray[0x0B05C0:0x0B05C0 + 18843] = self.get_enemy_stats()
            rom_bytearray[0x0B4F02:0x0B4F02 + 2] = self.o.master_hp.value.to_bytes(2, "little")
            rom_bytearray[0x280010:0x280010 + 2] = self.o.blue_chest_count.value.to_bytes(2, "little")
            rom_bytearray[0x280012:0x280012 + 3] = self.o.capsule_starting_level.xp.to_bytes(3, "little")
            rom_bytearray[0x280015:0x280015 + 1] = self.o.initial_floor.value.to_bytes(1, "little")
            rom_bytearray[0x280016:0x280016 + 1] = self.o.default_capsule.value.to_bytes(1, "little")
            rom_bytearray[0x280017:0x280017 + 1] = self.o.iris_treasures_required.value.to_bytes(1, "little")
            rom_bytearray[0x280018:0x280018 + 1] = self.o.shuffle_party_members.unlock.to_bytes(1, "little")
            rom_bytearray[0x280019:0x280019 + 1] = self.o.shuffle_capsule_monsters.unlock.to_bytes(1, "little")
            rom_bytearray[0x280030:0x280030 + 1] = self.o.goal.value.to_bytes(1, "little")
            rom_bytearray[0x28003D:0x28003D + 1] = self.o.death_link.value.to_bytes(1, "little")
            rom_bytearray[0x281200:0x281200 + 470] = self.get_capsule_cravings_table()

            (rom_bytearray[0x08A1D4:0x08A1D4 + 128],
             rom_bytearray[0x0A595C:0x0A595C + 200],
             rom_bytearray[0x0A5DF6:0x0A5DF6 + 192],
             rom_bytearray[0x27F6B5:0x27F6B5 + 113]) = self.get_enemy_floors_sprites_and_movement_patterns()

            with open(rom_path, "wb") as f:
                f.write(rom_bytearray)
        except Exception as e:
            raise e
        else:
            patch = L2ACDeltaPatch(os.path.splitext(rom_path)[0] + L2ACDeltaPatch.patch_file_ending,
                                   player=self.player, player_name=self.multiworld.player_name[self.player],
                                   patched_path=rom_path)
            patch.write()
        finally:
            if os.path.exists(rom_path):
                os.unlink(rom_path)

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        b64_name: str = base64.b64encode(bytes(self.rom_name)).decode()
        multidata["connect_names"][b64_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    # end of ordered Main.py calls

    def create_item(self, name: str) -> Item:
        item_data: ItemData = l2ac_item_table[name]
        return L2ACItem(name, item_data.classification, items_start_id + item_data.code, self.player)

    def get_filler_item_name(self) -> str:
        return ["Potion", "Hi-Magic", "Miracle", "Hi-Potion", "Potion", "Ex-Potion", "Regain", "Ex-Magic", "Hi-Magic"][
            (self.random.randrange(9) + self.random.randrange(9)) // 2]

    # end of overridden AutoWorld.py methods

    def get_capsule_cravings_table(self) -> bytes:
        rom: bytes = get_base_rom_bytes()

        if self.o.capsule_cravings_jp_style:
            number_of_items: int = 467
            items_offset: int = 0x0B4F69
            value_thresholds: List[int] = \
                [200, 500, 600, 800, 1000, 2000, 3000, 4000, 5000, 6000, 8000, 12000, 20000, 25000, 29000, 32000, 33000]
            tier_list: List[List[int]] = [list() for _ in value_thresholds[:-1]]

            for item_id in range(number_of_items):
                pointer: int = int.from_bytes(rom[items_offset + 2 * item_id:items_offset + 2 * item_id + 2], "little")
                if rom[items_offset + pointer] & 0x20 == 0 and rom[items_offset + pointer + 1] & 0x40 == 0:
                    value: int = int.from_bytes(rom[items_offset + pointer + 5:items_offset + pointer + 7], "little")
                    for t in range(len(tier_list)):
                        if value_thresholds[t] <= value < value_thresholds[t + 1]:
                            tier_list[t].append(item_id)
                            break
            tier_sizes: List[int] = [len(tier) for tier in tier_list]

            cravings_table: bytes = b"".join(i.to_bytes(2, "little") for i in itertools.chain(
                *zip(itertools.accumulate((2 * tier_size for tier_size in tier_sizes), initial=0x40), tier_sizes),
                (item_id for tier in tier_list for item_id in tier)))
            assert len(cravings_table) == 470, cravings_table
            return cravings_table
        else:
            return rom[0x0AFF16:0x0AFF16 + 470]

    def get_enemy_floors_sprites_and_movement_patterns(self) -> Tuple[bytes, bytes, bytes, bytes]:
        rom: bytes = get_base_rom_bytes()

        if self.o.enemy_floor_numbers == EnemyFloorNumbers.default \
                and self.o.enemy_sprites == EnemySprites.default \
                and self.o.enemy_movement_patterns == EnemyMovementPatterns.default:
            return rom[0x08A1D4:0x08A1D4 + 128], rom[0x0A595C:0x0A595C + 200], \
                rom[0x0A5DF6:0x0A5DF6 + 192], rom[0x27F6B5:0x27F6B5 + 113]

        formations: bytes = rom[0x0A595C:0x0A595C + 200]
        sprites: bytes = rom[0x0A5DF6:0x0A5DF6 + 192]
        indices: bytes = rom[0x27F6B5:0x27F6B5 + 113]
        pointers: List[bytes] = [rom[0x08A1D4 + 2 * index:0x08A1D4 + 2 * index + 2] for index in range(64)]

        used_formations: List[int] = list(formations)
        formation_set: Set[int] = set(used_formations)
        used_sprites: List[int] = [sprite for formation, sprite in enumerate(sprites) if formation in formation_set]
        sprite_set: Set[int] = set(used_sprites)
        used_indices: List[int] = [index for sprite, index in enumerate(indices, 128) if sprite in sprite_set]
        index_set: Set[int] = set(used_indices)
        used_pointers: List[bytes] = [pointer for index, pointer in enumerate(pointers) if index in index_set]

        d: int = 2 * 6
        if self.o.enemy_floor_numbers == EnemyFloorNumbers.option_shuffle:
            constrained_shuffle(used_formations, d, random=self.random)
        elif self.o.enemy_floor_numbers == EnemyFloorNumbers.option_randomize:
            used_formations = constrained_choices(used_formations, d, k=len(used_formations), random=self.random)

        if self.o.enemy_sprites == EnemySprites.option_shuffle:
            self.random.shuffle(used_sprites)
        elif self.o.enemy_sprites == EnemySprites.option_randomize:
            used_sprites = self.random.choices(tuple(dict.fromkeys(used_sprites)), k=len(used_sprites))
        elif self.o.enemy_sprites == EnemySprites.option_singularity:
            used_sprites = [self.random.choice(tuple(dict.fromkeys(used_sprites)))] * len(used_sprites)
        elif self.o.enemy_sprites.sprite:
            used_sprites = [self.o.enemy_sprites.sprite] * len(used_sprites)

        if self.o.enemy_movement_patterns == EnemyMovementPatterns.option_shuffle_by_pattern:
            self.random.shuffle(used_pointers)
        elif self.o.enemy_movement_patterns == EnemyMovementPatterns.option_randomize_by_pattern:
            used_pointers = self.random.choices(tuple(dict.fromkeys(used_pointers)), k=len(used_pointers))
        elif self.o.enemy_movement_patterns == EnemyMovementPatterns.option_shuffle_by_sprite:
            self.random.shuffle(used_indices)
        elif self.o.enemy_movement_patterns == EnemyMovementPatterns.option_randomize_by_sprite:
            used_indices = self.random.choices(tuple(dict.fromkeys(used_indices)), k=len(used_indices))
        elif self.o.enemy_movement_patterns == EnemyMovementPatterns.option_singularity:
            used_indices = [self.random.choice(tuple(dict.fromkeys(used_indices)))] * len(used_indices)
        elif self.o.enemy_movement_patterns.sprite:
            used_indices = [indices[self.o.enemy_movement_patterns.sprite - 128]] * len(used_indices)

        sprite_iter: Iterator[int] = iter(used_sprites)
        index_iter: Iterator[int] = iter(used_indices)
        pointer_iter: Iterator[bytes] = iter(used_pointers)
        formations = bytes(used_formations)
        sprites = bytes(next(sprite_iter) if form in formation_set else sprite for form, sprite in enumerate(sprites))
        indices = bytes(next(index_iter) if sprite in sprite_set else idx for sprite, idx in enumerate(indices, 128))
        pointers = [next(pointer_iter) if idx in index_set else pointer for idx, pointer in enumerate(pointers)]
        return b"".join(pointers), formations, sprites, indices

    def get_enemy_stats(self) -> bytes:
        rom: bytes = get_base_rom_bytes()

        if self.o.exp_modifier == ExpModifier.default:
            return rom[0x0B05C0:0x0B05C0 + 18843]

        number_of_enemies: int = 224
        enemy_stats = bytearray(rom[0x0B05C0:0x0B05C0 + 18843])

        for enemy_id in range(number_of_enemies):
            pointer: int = int.from_bytes(enemy_stats[2 * enemy_id:2 * enemy_id + 2], "little")
            enemy_stats[pointer + 29:pointer + 31] = self.o.exp_modifier(enemy_stats[pointer + 29:pointer + 31])
        return enemy_stats

    def get_goal_text_bytes(self) -> bytes:
        goal_text: List[str] = []
        iris: str = f"{self.o.iris_treasures_required} Iris treasure{'s' if self.o.iris_treasures_required > 1 else ''}"
        if self.o.goal == Goal.option_boss:
            goal_text = ["You have to defeat", f"the boss on B{self.o.final_floor}."]
        elif self.o.goal == Goal.option_iris_treasure_hunt:
            goal_text = ["You have to find", f"{iris}."]
        elif self.o.goal == Goal.option_boss_iris_treasure_hunt:
            goal_text = ["You have to retrieve", f"{iris} and", f"defeat the boss on B{self.o.final_floor}."]
        elif self.o.goal == Goal.option_final_floor:
            goal_text = [f"You need to get to B{self.o.final_floor}."]
        assert len(goal_text) <= 4 and all(len(line) <= 28 for line in goal_text), goal_text
        goal_text_bytes = bytes((0x08, *b"\x03".join(line.encode("ascii") for line in goal_text), 0x00))
        return goal_text_bytes + b"\x00" * (147 - len(goal_text_bytes))

    @staticmethod
    def get_node_connection_table() -> bytes:
        class Connect(IntFlag):
            TOP_LEFT = 0b00000001
            LEFT = 0b00000010
            BOTTOM_LEFT = 0b00000100
            TOP = 0b00001000
            BOTTOM = 0b00010000
            TOP_RIGHT = 0b00100000
            RIGHT = 0b01000000
            BOTTOM_RIGHT = 0b10000000

        rom: bytes = get_base_rom_bytes()

        return bytes(rom[0x09D59B + ((n & ~Connect.TOP_LEFT if not n & (Connect.TOP | Connect.LEFT) else n) &
                                     (n & ~Connect.TOP_RIGHT if not n & (Connect.TOP | Connect.RIGHT) else n) &
                                     (n & ~Connect.BOTTOM_LEFT if not n & (Connect.BOTTOM | Connect.LEFT) else n) &
                                     (n & ~Connect.BOTTOM_RIGHT if not n & (Connect.BOTTOM | Connect.RIGHT) else n))]
                     for n in range(256))
