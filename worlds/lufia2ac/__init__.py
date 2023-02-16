import base64
import itertools
import os
from enum import IntFlag
from typing import Any, ClassVar, Dict, List, Optional, Set, Tuple

from BaseClasses import Entrance, Item, ItemClassification, MultiWorld, Region, Tutorial
from Main import __version__
from Options import AssembleOptions
from worlds.AutoWorld import WebWorld, World
from worlds.generic.Rules import add_rule, set_rule
from .Client import L2ACSNIClient  # noqa: F401
from .Items import ItemData, ItemType, l2ac_item_name_to_id, l2ac_item_table, L2ACItem, start_id as items_start_id
from .Locations import l2ac_location_name_to_id, L2ACLocation
from .Options import Boss, CapsuleStartingForm, CapsuleStartingLevel, DefaultParty, Goal, l2ac_option_definitions, \
    MasterHp, PartyStartingLevel, ShuffleCapsuleMonsters, ShufflePartyMembers
from .Rom import get_base_rom_bytes, get_base_rom_path, L2ACDeltaPatch
from .basepatch import apply_basepatch

CHESTS_PER_SPHERE: int = 5


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

    option_definitions: ClassVar[Dict[str, AssembleOptions]] = l2ac_option_definitions
    item_name_to_id: ClassVar[Dict[str, int]] = l2ac_item_name_to_id
    location_name_to_id: ClassVar[Dict[str, int]] = l2ac_location_name_to_id
    item_name_groups: ClassVar[Dict[str, Set[str]]] = {
        "Blue chest items": {name for name, data in l2ac_item_table.items() if data.type is ItemType.BLUE_CHEST},
        "Capsule monsters": {name for name, data in l2ac_item_table.items() if data.type is ItemType.CAPSULE_MONSTER},
        "Party members": {name for name, data in l2ac_item_table.items() if data.type is ItemType.PARTY_MEMBER},
    }
    data_version: ClassVar[int] = 1
    required_client_version: Tuple[int, int, int] = (0, 3, 6)

    # L2ACWorld specific properties
    rom_name: Optional[bytearray]

    blue_chest_chance: Optional[int]
    blue_chest_count: Optional[int]
    boss: Optional[Boss]
    capsule_cravings_jp_style: Optional[int]
    capsule_starting_form: Optional[CapsuleStartingForm]
    capsule_starting_level: Optional[CapsuleStartingLevel]
    crowded_floor_chance: Optional[int]
    death_link: Optional[int]
    default_capsule: Optional[int]
    default_party: Optional[DefaultParty]
    final_floor: Optional[int]
    gear_variety_after_b9: Optional[int]
    goal: Optional[int]
    healing_floor_chance: Optional[int]
    initial_floor: Optional[int]
    iris_floor_chance: Optional[int]
    iris_treasures_required: Optional[int]
    master_hp: Optional[int]
    party_starting_level: Optional[PartyStartingLevel]
    run_speed: Optional[int]
    shuffle_capsule_monsters: Optional[ShuffleCapsuleMonsters]
    shuffle_party_members: Optional[ShufflePartyMembers]

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

        self.blue_chest_chance = self.multiworld.blue_chest_chance[self.player].value
        self.blue_chest_count = self.multiworld.blue_chest_count[self.player].value
        self.boss = self.multiworld.boss[self.player]
        self.capsule_cravings_jp_style = self.multiworld.capsule_cravings_jp_style[self.player].value
        self.capsule_starting_form = self.multiworld.capsule_starting_form[self.player]
        self.capsule_starting_level = self.multiworld.capsule_starting_level[self.player]
        self.crowded_floor_chance = self.multiworld.crowded_floor_chance[self.player].value
        self.death_link = self.multiworld.death_link[self.player].value
        self.default_capsule = self.multiworld.default_capsule[self.player].value
        self.default_party = self.multiworld.default_party[self.player]
        self.final_floor = self.multiworld.final_floor[self.player].value
        self.gear_variety_after_b9 = self.multiworld.gear_variety_after_b9[self.player].value
        self.goal = self.multiworld.goal[self.player].value
        self.healing_floor_chance = self.multiworld.healing_floor_chance[self.player].value
        self.initial_floor = self.multiworld.initial_floor[self.player].value
        self.iris_floor_chance = self.multiworld.iris_floor_chance[self.player].value
        self.iris_treasures_required = self.multiworld.iris_treasures_required[self.player].value
        self.master_hp = self.multiworld.master_hp[self.player].value
        self.party_starting_level = self.multiworld.party_starting_level[self.player]
        self.run_speed = self.multiworld.run_speed[self.player].value
        self.shuffle_capsule_monsters = self.multiworld.shuffle_capsule_monsters[self.player]
        self.shuffle_party_members = self.multiworld.shuffle_party_members[self.player]

        if self.capsule_starting_level.value == CapsuleStartingLevel.special_range_names["party_starting_level"]:
            self.capsule_starting_level.value = self.party_starting_level.value
        if self.initial_floor >= self.final_floor:
            self.initial_floor = self.final_floor - 1
        if self.master_hp == MasterHp.special_range_names["scale"]:
            self.master_hp = MasterHp.scale(self.final_floor)
        if self.shuffle_party_members:
            self.default_party.value = DefaultParty.default

    def create_regions(self) -> None:
        menu = Region("Menu", self.player, self.multiworld)
        menu.exits.append(Entrance(self.player, "AncientDungeonEntrance", menu))
        self.multiworld.regions.append(menu)

        ancient_dungeon = Region("AncientDungeon", self.player, self.multiworld, "Ancient Dungeon")
        ancient_dungeon.exits.append(Entrance(self.player, "FinalFloorEntrance", ancient_dungeon))
        item_count: int = self.blue_chest_count
        if self.shuffle_capsule_monsters:
            item_count += len(self.item_name_groups["Capsule monsters"])
        if self.shuffle_party_members:
            item_count += len(self.item_name_groups["Party members"])
        for location_name, location_id in itertools.islice(l2ac_location_name_to_id.items(), item_count):
            ancient_dungeon.locations.append(L2ACLocation(self.player, location_name, location_id, ancient_dungeon))
        prog_chest_access = L2ACItem("Progressive chest access", ItemClassification.progression, None, self.player)
        for i in range(CHESTS_PER_SPHERE, item_count, CHESTS_PER_SPHERE):
            chest_access = \
                L2ACLocation(self.player, f"Chest access {i + 1}-{i + CHESTS_PER_SPHERE}", None, ancient_dungeon)
            chest_access.place_locked_item(prog_chest_access)
            ancient_dungeon.locations.append(chest_access)
        treasures = L2ACLocation(self.player, "Iris Treasures", None, ancient_dungeon)
        treasures.place_locked_item(L2ACItem("Treasures collected", ItemClassification.progression, None, self.player))
        ancient_dungeon.locations.append(treasures)
        self.multiworld.regions.append(ancient_dungeon)

        final_floor = Region("FinalFloor", self.player, self.multiworld, "Ancient Cave Final Floor")
        ff_reached = L2ACLocation(self.player, "Final Floor reached", None, final_floor)
        ff_reached.place_locked_item(L2ACItem("Final Floor access", ItemClassification.progression, None, self.player))
        final_floor.locations.append(ff_reached)
        boss = L2ACLocation(self.player, "Boss", None, final_floor)
        boss.place_locked_item(L2ACItem("Boss victory", ItemClassification.progression, None, self.player))
        final_floor.locations.append(boss)
        self.multiworld.regions.append(final_floor)

        self.multiworld.get_entrance("AncientDungeonEntrance", self.player) \
            .connect(self.multiworld.get_region("AncientDungeon", self.player))
        self.multiworld.get_entrance("FinalFloorEntrance", self.player) \
            .connect(self.multiworld.get_region("FinalFloor", self.player))

    def create_items(self) -> None:
        item_pool: List[str] = \
            self.multiworld.random.choices(sorted(self.item_name_groups["Blue chest items"]), k=self.blue_chest_count)
        if self.shuffle_capsule_monsters:
            item_pool += self.item_name_groups["Capsule monsters"]
            self.blue_chest_count += len(self.item_name_groups["Capsule monsters"])
        if self.shuffle_party_members:
            item_pool += self.item_name_groups["Party members"]
            self.blue_chest_count += len(self.item_name_groups["Party members"])
        for item_name in item_pool:
            item_data: ItemData = l2ac_item_table[item_name]
            item_id: int = items_start_id + item_data.code
            self.multiworld.itempool.append(L2ACItem(item_name, item_data.classification, item_id, self.player))

    def set_rules(self) -> None:
        for i in range(1, self.blue_chest_count):
            if i % CHESTS_PER_SPHERE == 0:
                set_rule(self.multiworld.get_location(f"Blue chest {i + 1}", self.player),
                         lambda state, j=i: state.has("Progressive chest access", self.player, j // CHESTS_PER_SPHERE))
                set_rule(self.multiworld.get_location(f"Chest access {i + 1}-{i + CHESTS_PER_SPHERE}", self.player),
                         lambda state, j=i: state.can_reach(f"Blue chest {j}", "Location", self.player))
            else:
                set_rule(self.multiworld.get_location(f"Blue chest {i + 1}", self.player),
                         lambda state, j=i: state.can_reach(f"Blue chest {j}", "Location", self.player))

        set_rule(self.multiworld.get_entrance("FinalFloorEntrance", self.player),
                 lambda state: state.can_reach(f"Blue chest {self.blue_chest_count}", "Location", self.player))
        set_rule(self.multiworld.get_location("Iris Treasures", self.player),
                 lambda state: state.can_reach(f"Blue chest {self.blue_chest_count}", "Location", self.player))
        set_rule(self.multiworld.get_location("Boss", self.player),
                 lambda state: state.can_reach(f"Blue chest {self.blue_chest_count}", "Location", self.player))
        if self.shuffle_capsule_monsters:
            add_rule(self.multiworld.get_location("Boss", self.player), lambda state: state.has("DARBI", self.player))
        if self.shuffle_party_members:
            add_rule(self.multiworld.get_location("Boss", self.player), lambda state: state.has("Dekar", self.player)
                     and state.has("Guy", self.player) and state.has("Arty", self.player))

        if self.goal == Goal.option_final_floor:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Final Floor access", self.player)
        elif self.goal == Goal.option_iris_treasure_hunt:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Treasures collected", self.player)
        elif self.goal == Goal.option_boss:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Boss victory", self.player)
        elif self.goal == Goal.option_boss_iris_treasure_hunt:
            self.multiworld.completion_condition[self.player] = \
                lambda state: state.has("Boss victory", self.player) and state.has("Treasures collected", self.player)

    def generate_output(self, output_directory: str) -> None:
        rom_path: str = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")

        try:
            rom_bytearray = bytearray(apply_basepatch(get_base_rom_bytes()))
            # start and stop indices are offsets in the ROM file, not LoROM mapped SNES addresses
            rom_bytearray[0x007FC0:0x007FC0 + 21] = self.rom_name
            rom_bytearray[0x014308:0x014308 + 1] = self.capsule_starting_level.value.to_bytes(1, "little")
            rom_bytearray[0x01432F:0x01432F + 1] = self.capsule_starting_form.unlock.to_bytes(1, "little")
            rom_bytearray[0x01433C:0x01433C + 1] = self.capsule_starting_form.value.to_bytes(1, "little")
            rom_bytearray[0x0190D5:0x0190D5 + 1] = self.iris_floor_chance.to_bytes(1, "little")
            rom_bytearray[0x019153:0x019153 + 1] = (0x63 - self.blue_chest_chance).to_bytes(1, "little")
            rom_bytearray[0x019176] = 0x38 if self.gear_variety_after_b9 else 0x18
            rom_bytearray[0x019477:0x019477 + 1] = self.healing_floor_chance.to_bytes(1, "little")
            rom_bytearray[0x0194A2:0x0194A2 + 1] = self.crowded_floor_chance.to_bytes(1, "little")
            rom_bytearray[0x019E82:0x019E82 + 1] = self.final_floor.to_bytes(1, "little")
            rom_bytearray[0x01FC75:0x01FC75 + 1] = self.run_speed.to_bytes(1, "little")
            rom_bytearray[0x01FC81:0x01FC81 + 1] = self.run_speed.to_bytes(1, "little")
            rom_bytearray[0x02B2A1:0x02B2A1 + 5] = self.default_party.roster
            for offset in range(0x02B395, 0x02B452, 0x1B):
                rom_bytearray[offset:offset + 1] = self.party_starting_level.value.to_bytes(1, "little")
            for offset in range(0x02B39A, 0x02B457, 0x1B):
                rom_bytearray[offset:offset + 3] = self.party_starting_level.xp.to_bytes(3, "little")
            rom_bytearray[0x05699E:0x05699E + 147] = self.get_goal_text_bytes()
            rom_bytearray[0x056AA3:0x056AA3 + 24] = self.default_party.event_script
            rom_bytearray[0x072742:0x072742 + 1] = self.boss.value.to_bytes(1, "little")
            rom_bytearray[0x072748:0x072748 + 1] = self.boss.flag.to_bytes(1, "little")
            rom_bytearray[0x09D59B:0x09D59B + 256] = self.get_node_connection_table()
            rom_bytearray[0x0B4F02:0x0B4F02 + 2] = self.master_hp.to_bytes(2, "little")
            rom_bytearray[0x280010:0x280010 + 2] = self.blue_chest_count.to_bytes(2, "little")
            rom_bytearray[0x280012:0x280012 + 3] = self.capsule_starting_level.xp.to_bytes(3, "little")
            rom_bytearray[0x280015:0x280015 + 1] = self.initial_floor.to_bytes(1, "little")
            rom_bytearray[0x280016:0x280016 + 1] = self.default_capsule.to_bytes(1, "little")
            rom_bytearray[0x280017:0x280017 + 1] = self.iris_treasures_required.to_bytes(1, "little")
            rom_bytearray[0x280018:0x280018 + 1] = self.shuffle_party_members.unlock.to_bytes(1, "little")
            rom_bytearray[0x280019:0x280019 + 1] = self.shuffle_capsule_monsters.unlock.to_bytes(1, "little")
            rom_bytearray[0x280030:0x280030 + 1] = self.goal.to_bytes(1, "little")
            rom_bytearray[0x28003D:0x28003D + 1] = self.death_link.to_bytes(1, "little")
            rom_bytearray[0x281200:0x281200 + 470] = self.get_capsule_cravings_table()

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
        item_data: ItemData = l2ac_item_table.get(name)
        return L2ACItem(name, item_data.classification, items_start_id + item_data.code, self.player)

    def get_capsule_cravings_table(self) -> bytes:
        rom: bytes = get_base_rom_bytes()

        if self.capsule_cravings_jp_style:
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

    def get_goal_text_bytes(self) -> bytes:
        goal_text: List[str] = []
        iris: str = f"{self.iris_treasures_required} Iris treasure{'s' if self.iris_treasures_required > 1 else ''}"
        if self.goal == Goal.option_boss:
            goal_text = ["You have to defeat", f"the boss on B{self.final_floor}."]
        elif self.goal == Goal.option_iris_treasure_hunt:
            goal_text = ["You have to find", f"{iris}."]
        elif self.goal == Goal.option_boss_iris_treasure_hunt:
            goal_text = ["You have to retrieve", f"{iris} and", f"defeat the boss on B{self.final_floor}."]
        elif self.goal == Goal.option_final_floor:
            goal_text = [f"You need to get to B{self.final_floor}."]
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
