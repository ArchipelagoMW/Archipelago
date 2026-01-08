# We deliberately do not import [random] directly to ensure that all random
# functions go through the multiworld rng seed.
from random import Random
from collections import defaultdict
from dataclasses import dataclass
from enum import IntEnum
import operator
import itertools
import functools
import logging

from typing import Any, Union, Optional, Callable, Iterable, Tuple

from .util import fetch_json, write_short_le, read_short_le, read_word_le, write_word_le

# XXX: most python lsps can't handle `from .constants import *`, so we have to
# specify these manually...
from .constants import (
    ROM_BASE_ADDRESS,
    CHAPTER_UNIT_SIZE,
    INVENTORY_INDEX,
    INVENTORY_SIZE,
    COORDS_INDEX,
    REDA_COUNT_INDEX,
    REDA_PTR_INDEX,
    CHARACTER_TABLE_BASE,
    CHARACTER_SIZE,
    CHARACTER_WRANK_OFFSET,
    CHARACTER_STATS_OFFSET,
    CHARACTER_GROWTHS_OFFSET,
    CHAR_ABILITY_4_OFFSET,
    JOB_TABLE_BASE,
    JOB_SIZE,
    JOB_STATS_OFFSET,
    JOB_CAPS_OFFSET,
    STATS_COUNT,
    EIRIKA,
    EIRIKA_LORD,
    EIRIKA_LOCK,
    EPHRAIM,
    EPHRAIM_LORD,
    EPHRAIM_LOCK,
    EIRIKA_RAPIER_OFFSET,
    ROSS_CH2_HP_OFFSET,
    MOVEMENT_COST_TABLE_BASE,
    MOVEMENT_COST_ENTRY_SIZE,
    MOVEMENT_COST_ENTRY_COUNT,
    MOVEMENT_COST_SENTINEL,
    IMPORTANT_TERRAIN_TYPES,
    ITEM_TABLE_BASE,
    ITEM_SIZE,
    ITEM_ABILITY_1_INDEX,
    UNBREAKABLE_FLAG,
    LOCKPICK,
    CHEST_KEY_5,
    HOLY_WEAPON_IDS,
    MOUNTED_AID_CANTO_MASK,
    MOUNTED_MONSTERS,
    JOB_ABILITY_1_INDEX,
    CH15_AUTO_STEEL_SWORD,
    CH15_AUTO_STEEL_LANCE,
    AI1_INDEX,
    INTERNAL_RANDO_CLASS_WEIGHTS_OFFS,
    INTERNAL_RANDO_CLASS_WEIGHT_ENTRY_SIZE,
    INTERNAL_RANDO_CLASS_WEIGHTS_COUNT,
    INTERNAL_RANDO_CLASS_WEIGHT_NUM_CLASSES,
    INTERNAL_RANDO_WEAPONS_OFFS,
    INTERNAL_RANDO_WEAPONS_ENTRY_SIZE,
    INTERNAL_RANDO_WEAPONS_MAX_CLASSES,
    INTERNAL_RANDO_WEAPON_TABLE_ROWS,
    FEMALE_JOBS,
    SONG_TABLE_BASE,
    SONG_SIZE,
)

DEBUG = False


# CR cam: Maybe these should go into [constants]?

WEAPON_DATA = "data/weapondata.json"
JOB_DATA = "data/jobdata.json"
SONG_DATA = "data/songdata.json"
CHARACTERS = "data/characters.json"
CHAPTER_UNIT_BLOCKS = "data/chapter_unit_blocks.json"
INTERNAL_RANDO_VALID_DISTRIBS = "data/internal_rando_distribs.json"


def encode_unit_coords(x: int, y: int) -> int:
    return y << 6 | x


def int_if_possible(x: str) -> Union[int, str]:
    try:
        return int(x)
    except ValueError:
        return x


class UnitBlock:
    name: str
    base: int
    count: int

    # Currently, the names of blocks in `chapter_unit_blocks.json` are mostly
    # automatically generated from chapter event disassembly and are tagged
    # with any relevant information about the block.
    logic: defaultdict[Union[int, str], dict[str, Any]]

    def __init__(
        self, name: str, base: int, count: int, logic: dict[str, dict[str, Any]]
    ):
        self.name = name
        self.base = base
        self.count = count
        self.logic = defaultdict(
            dict, {int_if_possible(k): v for k, v in logic.items()}
        )


class GrowthRandoKind(IntEnum):
    NONE = 0
    REDISTRIBUTE = 1
    DELTA = 2
    FULL = 3


class MusicRandoKind(IntEnum):
    VANILLA = 0
    CONTEXT = 1
    CHAOS = 2


class WeaponKind(IntEnum):
    SWORD = 0x00
    LANCE = 0x01
    AXE = 0x02
    BOW = 0x03
    STAFF = 0x04
    ANIMA = 0x05
    LIGHT = 0x06
    DARK = 0x07
    ITEM = 0x09
    MONSTER_WEAPON = 0x0B
    RING = 0x0C
    DRAGONSTONE = 0x11

    @classmethod
    def get_valid_names(cls) -> list[str]:
        return [
            "Sword",
            "Lance",
            "Axe",
            "Bow",
            "Staff",
            "Anima",
            "Light",
            "Dark",
            "Item",
            "Monster Weapon",
            "Ring",
            "Dragonstone",
        ]

    @classmethod
    def of_str(cls, s: str) -> "WeaponKind":
        match s:
            case "Sword":
                return WeaponKind.SWORD
            case "Lance":
                return WeaponKind.LANCE
            case "Axe":
                return WeaponKind.AXE
            case "Bow":
                return WeaponKind.BOW
            case "Staff":
                return WeaponKind.STAFF
            case "Anima":
                return WeaponKind.ANIMA
            case "Light":
                return WeaponKind.LIGHT
            case "Dark":
                return WeaponKind.DARK
            case "Item":
                return WeaponKind.ITEM
            case "Monster Weapon":
                return WeaponKind.MONSTER_WEAPON
            case "Ring":
                return WeaponKind.RING
            case "Dragonstone":
                return WeaponKind.DRAGONSTONE
        raise ValueError

    def damaging(self) -> bool:
        match self:
            case WeaponKind.SWORD:
                return True
            case WeaponKind.LANCE:
                return True
            case WeaponKind.AXE:
                return True
            case WeaponKind.BOW:
                return True
            case WeaponKind.STAFF:
                return False
            case WeaponKind.ANIMA:
                return True
            case WeaponKind.LIGHT:
                return True
            case WeaponKind.DARK:
                return True
            case WeaponKind.ITEM:
                return False
            case WeaponKind.MONSTER_WEAPON:
                return True
            case WeaponKind.RING:
                return False
            case WeaponKind.DRAGONSTONE:
                return True
        raise ValueError


class WeaponRank(IntEnum):
    E = 0x1
    D = 0x1F
    C = 0x47
    B = 0x79
    A = 0xB5
    S = 0xFB

    @classmethod
    def of_str(cls, s: str) -> "WeaponRank":
        match s:
            case "E":
                return WeaponRank.E
            case "D":
                return WeaponRank.D
            case "C":
                return WeaponRank.C
            case "B":
                return WeaponRank.B
            case "A":
                return WeaponRank.A
            case "S":
                return WeaponRank.S
        raise ValueError


@dataclass
class WeaponData:
    id: int
    name: str
    rank: WeaponRank
    kind: WeaponKind
    locks: set[str]

    @classmethod
    def of_object(cls, obj: dict[str, Any]):
        return WeaponData(
            id=obj["id"],
            name=obj["name"],
            rank=WeaponRank.of_str(obj["rank"]),
            kind=WeaponKind.of_str(obj["kind"]),
            locks=obj.get("locks", set()),
        )


@dataclass
class JobData:
    id: int
    name: str
    is_promoted: bool
    usable_weapons: set[WeaponKind]
    tags: set[str]

    @classmethod
    def of_object(cls, obj: dict[str, Any]):
        return JobData(
            id=obj["id"],
            name=obj["name"],
            is_promoted=obj["is_promoted"],
            usable_weapons=set(
                WeaponKind.of_str(kind) for kind in obj["usable_weapons"]
            ),
            tags=set(obj["tags"]),
        )

    def __hash__(self):
        return self.id

    def __eq__(self, other):
        if not isinstance(other, JobData):
            return False
        return self.id == other.id


class CharacterStore:
    names_by_id: dict[int, str]
    ids_by_name: dict[str, list[int]]
    character_jobs: dict[str, JobData]
    character_tags: dict[str, set[str]]

    def __init__(self, char_data: dict[str, dict[str, Any]]):
        self.names_by_id = {}
        self.character_tags = dict()
        self.ids_by_name = dict()

        for name, data in char_data.items():
            for i in data["ids"]:
                assert isinstance(i, int)
                self.names_by_id[i] = name

            # CR cam: figure out how to convince mypy that `data["tags"]` is
            # actually a list of strings
            self.character_tags[name] = set(data["tags"])
            self.ids_by_name[name] = data["ids"]

        self.character_jobs = {}

    def lookup_ids(self, char_name: str) -> Optional[list[int]]:
        if char_name not in self.ids_by_name:
            return None
        return self.ids_by_name[char_name]

    def lookup_name(self, char_id: int) -> Optional[str]:
        if char_id not in self.names_by_id:
            return None
        return self.names_by_id[char_id]

    def tags(self, char: Union[int, str]) -> Optional[set[str]]:
        if isinstance(char, int):
            if char not in self.names_by_id:
                return None
            name = self.names_by_id[char]
        else:
            name = char
        return self.character_tags[name]

    def __setitem__(self, char: Union[int, str], job: JobData) -> None:
        if isinstance(char, int):
            if char not in self.names_by_id:
                return
            name = self.names_by_id[char]
        else:
            name = char
        self.character_jobs[name] = job

    def __getitem__(self, char: Union[int, str]):
        name = char if isinstance(char, str) else self.names_by_id[char]
        return self.character_jobs[name]

    def __contains__(self, char: Union[int, str]) -> bool:
        if isinstance(char, int):
            if char not in self.names_by_id:
                return False
            name = self.names_by_id[char]
        else:
            name = char

        return name in self.character_jobs


# CR cam: Eirika and Ephraim should be able to use their respective weapons if
# they get randomized into the right class.
def weapon_usable(weapon: WeaponData, job: JobData, logic: dict[str, Any]) -> bool:
    if weapon.kind not in job.usable_weapons:
        return False

    if any(lock not in job.tags for lock in weapon.locks):
        return False

    if "must_fight" in logic and weapon.kind in [
        WeaponKind.ITEM,
        WeaponKind.STAFF,
        WeaponKind.RING,
    ]:
        return False

    return True


# CR cam: ensure that all the progression weapons are usable
# CR-soon cam: This class does way too much. We should refactor this so things
# like `apply_5x_buffs` can happen external to this class.
class FE8Randomizer:
    unit_blocks: dict[str, list[UnitBlock]]
    weapons_by_id: dict[int, WeaponData]
    weapons_by_name: dict[str, WeaponData]
    weapons_by_rank: dict[WeaponRank, list[WeaponData]]
    character_store: CharacterStore
    jobs_by_id: dict[int, JobData]
    valid_distribs_by_row: dict[int, list[int]]
    promoted_jobs: list[JobData]
    unpromoted_jobs: list[JobData]
    songs: dict[str, dict[int, str]]

    random: Random
    rom: bytearray
    config: dict[str, Any]

    def __init__(self, rom: bytearray, random: Random, config: dict[str, Any]):
        self.random = random
        self.rom = rom
        unit_blocks = fetch_json(CHAPTER_UNIT_BLOCKS)
        self.config = config

        self.unit_blocks = {
            name: [UnitBlock(**block) for block in blocks]
            for name, blocks in unit_blocks.items()
        }

        valid_distribs_by_row = fetch_json(INTERNAL_RANDO_VALID_DISTRIBS)
        self.valid_distribs_by_row = {
            int(k): v for k, v in valid_distribs_by_row.items()
        }

        item_data = fetch_json(WEAPON_DATA, object_hook=WeaponData.of_object)

        job_data = fetch_json(
            JOB_DATA,
            object_hook=JobData.of_object,
        )

        # TODO: handle these properly
        job_data = [job for job in job_data if job.usable_weapons]

        self.character_store = CharacterStore(fetch_json(CHARACTERS))

        self.weapons_by_id = {item.id: item for item in item_data}
        self.weapons_by_name = {item.name: item for item in item_data}
        self.jobs_by_id = {job.id: job for job in job_data}

        self.promoted_jobs = [
            job for job in job_data if job.is_promoted and "no_rando" not in job.tags
        ]
        self.unpromoted_jobs = [
            job
            for job in job_data
            if not job.is_promoted and "no_rando" not in job.tags
        ]

        self.weapons_by_rank = defaultdict(list)

        for weap in self.weapons_by_id.values():
            self.weapons_by_rank[weap.rank].append(weap)

        # Dark has no E-ranked weapons by default.
        self.weapons_by_rank[WeaponRank.E].append(self.weapons_by_name["Flux"])

        # cam: Should we allow Lyon to become a monster?

        self.weapons_by_rank[WeaponRank.D].append(self.weapons_by_name["Fiery Fang"])
        self.weapons_by_rank[WeaponRank.C].append(self.weapons_by_name["Fiery Fang"])
        self.weapons_by_rank[WeaponRank.A].append(self.weapons_by_name["Hellfang"])
        self.weapons_by_rank[WeaponRank.S].append(self.weapons_by_name["Hellfang"])

        self.weapons_by_rank[WeaponRank.A].append(self.weapons_by_name["Fetid Claw"])
        self.weapons_by_rank[WeaponRank.S].append(self.weapons_by_name["Fetid Claw"])

        # CR-soon cam:
        # Darr: Dragon zombies experience the same problem. I've disabled them for now;
        # they only have one weapon and E-rank Wretched Air does not sound fun.
        #
        # Cam: What we need to do is prevent units from randomizing into Dracozombies
        # unless they have an A rank weapon. There are a few easy ways to hack that
        # in, but I'm going to punt on it for now because that's a bunch of design
        # decisions we can make later.

        songdata = fetch_json(SONG_DATA)
        self.songs = defaultdict(dict)
        for song in songdata:
            self.songs[song["category"]][int(song["id"], 16)] = song["name"]

    def job_valid(self, job: JobData, char: int, logic: dict[str, Any]) -> bool:
        # get list of tags that make the job invalid (notags)
        # the "no_" prefix adds the tag to the invalid tag list
        # "no_flying" makes any job with "flying" tag invalid
        notags = set()
        # config option for disabling player unit monsters
        if "player" in logic and logic["player"] and not self.config["player_monster"]:
            notags.add("monster")
        for x in logic:
            if x.startswith("no_") and logic[x]:
                notags.add(x.removeprefix("no_"))
        # job is invalid if it has any of the tags in notags
        if notags and notags & job.tags:
            return False

        # CR-soon cam: see above
        if job.name in ("Dracozombie", "Revenant", "Entombed"):
            return False

        if "must_fly" in logic and logic["must_fly"] and "flying" not in job.tags:
            # demand that valid job has the "flying" tag
            return False

        if "must_fight" in logic and logic["must_fight"]:
            if "cannot_fight" in job.tags:
                return False
            if all(not wtype.damaging() for wtype in job.usable_weapons):
                return False

        return True

    def select_new_item(self, job: JobData, item_id: int, logic: dict[str, Any]) -> int:
        if item_id == LOCKPICK:
            if "Lockpick" in job.tags:
                return LOCKPICK
            else:
                return CHEST_KEY_5

        if item_id not in self.weapons_by_id:
            return item_id
        weapon_attrs = self.weapons_by_id[item_id]

        choices = [
            weap
            for weap in self.weapons_by_rank[weapon_attrs.rank]
            if weapon_usable(weap, job, logic)
        ]

        if not choices:
            import json

            logging.warning("LOGIC ERROR: no viable weapons, defaulting to E rank")
            logging.warning(f"  job: {job.name}")
            logging.warning(f"  rank: {weapon_attrs.rank}")
            logging.warning(f"  logic: {json.dumps(logic, indent=2)}")

            choices = [
                weap
                for weap in self.weapons_by_rank[WeaponRank.E]
                if weapon_usable(weap, job, dict())
            ]

            if not choices:
                logging.warning(
                    "LOGIC ERROR (2): still no viable weapons, defaulting to iron sword"
                )
                choices = [self.weapons_by_name["Iron Sword"]]

        return self.random.choice(choices).id

    def select_new_inventory(
        self, job: JobData, items: bytes, logic: dict[str, Any]
    ) -> list[int]:
        return [self.select_new_item(job, item_id, logic) for item_id in items]

    def rewrite_coords(self, offset: int, x: int, y: int):
        old_coords = read_short_le(self.rom, offset)
        flags = old_coords & 0b1111000000000000
        new_coords = encode_unit_coords(x, y)
        write_short_le(self.rom, offset, new_coords | flags)

    def apply_nudges(self, data_offset: int, nudges: dict[str, list[int]]) -> None:
        if "start" in nudges:
            x, y = nudges["start"]
            start_offs = data_offset + COORDS_INDEX
            self.rewrite_coords(start_offs, x, y)

        reda_count = self.rom[data_offset + REDA_COUNT_INDEX]
        redas_addr = read_word_le(self.rom, data_offset + REDA_PTR_INDEX)
        redas_offs = redas_addr - ROM_BASE_ADDRESS

        for i in range(reda_count):
            if str(i) in nudges:
                x, y = nudges[str(i)]
                reda_offs = redas_offs + 8 * i
                self.rewrite_coords(reda_offs, x, y)

    def select_new_job(
        self,
        job: JobData,
        unpromoted_pool: Iterable[JobData],
        promoted_pool: Iterable[JobData],
        job_valid: Callable[[JobData], bool],
    ) -> JobData:
        new_job_pool = promoted_pool if job.is_promoted else unpromoted_pool
        choices = [job for job in new_job_pool if job_valid(job)]
        if not choices:
            logging.warning("LOGIC ERROR: no valid jobs")
            logging.warning(f"  original job: {job.name}")
            return job
        return self.random.choice(choices)

    def randomize_chapter_unit(self, data_offset: int, logic: dict[str, Any]) -> None:
        # We *could* read the full struct, but we only need a few individual
        # bytes, so we may as well extract them ad-hoc.
        unit = self.rom[data_offset : data_offset + CHAPTER_UNIT_SIZE]
        job_id = unit[1]

        # If the unit's class is is not a "standard" class that can be given to
        # players, it's probably some NPC or enemy that shouldn't be touched.
        if job_id not in self.jobs_by_id:
            return

        # CR cam: this is dracozombie. prevents randomizing existing dracozombies.
        if job_id == 101:
            return

        job = self.jobs_by_id[job_id]
        char = unit[0]

        # add character tags to logic
        ctags = self.character_store.tags(char)
        if not ctags:
            ctags = set()
        for t in ctags:
            if t not in logic:
                logic[t] = True

        no_store = "no_store" in logic and logic["no_store"]

        # config option for disabling player unit randomization
        if not self.config["player_rando"] and "player" in logic and logic["player"]:
            if char not in self.character_store and not no_store:
                self.character_store[char] = job
            return

        # Affiliation = bits 1,2; unit is player if they're unset
        is_player = not bool(unit[3] & 0b0110)
        # Autolevel is LSB
        autolevel = unit[3] & 1
        inventory = unit[INVENTORY_INDEX : INVENTORY_INDEX + INVENTORY_SIZE]

        if char in self.character_store:
            new_job = self.character_store[char]
        else:
            new_job = self.select_new_job(
                job,
                unpromoted_pool=self.unpromoted_jobs,
                promoted_pool=self.promoted_jobs,
                job_valid=lambda job: self.job_valid(job, char, logic),
            )

            if not no_store:
                self.character_store[char] = new_job

        new_inventory = self.select_new_inventory(new_job, inventory, logic)

        self.rom[data_offset + 1] = new_job.id
        for i, item_id in enumerate(new_inventory):
            self.rom[data_offset + INVENTORY_INDEX + i] = item_id

        if (
            "ai1_mod" in logic
            and self.rom[data_offset + AI1_INDEX] == logic["ai1_mod"]["from"]
        ):
            self.rom[data_offset + AI1_INDEX] = logic["ai1_mod"]["to"]

        # If an NPC isn't autoleveled, it's probably a boss or important NPC of
        # some kind, so we should force its weapon levels in the character
        # table.
        if not is_player and not autolevel and char in self.character_store:
            for item_id in new_inventory:
                if item_id not in self.weapons_by_id:
                    continue
                boss_data_offs = CHARACTER_TABLE_BASE + char * CHARACTER_SIZE
                weapon = self.weapons_by_id[item_id]
                boss_wrank_offs = boss_data_offs + CHARACTER_WRANK_OFFSET + weapon.kind
                rank = self.rom[boss_wrank_offs]
                self.rom[boss_wrank_offs] = max(rank, weapon.rank)

    def randomize_block(self, block: UnitBlock):
        for k, v in list(block.logic.items()):
            if isinstance(k, int):
                continue

            assert isinstance(k, str)

            if isinstance(v, dict) and "at_least" in v:
                affected = self.random.sample(range(block.count), v["at_least"])
            else:
                affected = list(range(block.count))

            for i in affected:
                block.logic[i][k] = v

        for i in range(block.count):
            offset = block.base + i * CHAPTER_UNIT_SIZE
            logic = block.logic[i]

            if "nudges" in logic:
                self.apply_nudges(offset, logic["nudges"])
            if "ignore" in logic and logic["ignore"]:
                continue
            # If this unit is tagged as a monster, its class gets selected by
            # the in-game randomizer, meaning we don't have to touch it.
            if "monster" in logic and logic["monster"]:
                continue
            self.randomize_chapter_unit(offset, logic)

    # Randomize the classes and possible invtories for the game's internal
    # randomizer (used for skirmishes, tower/ruins, and the two random Wights
    # with Lyon for some reason).
    def randomize_monster_gen(self) -> None:
        class JobSet:
            promoted: set[JobData]
            unpromoted: set[JobData]

            def __init__(self):
                self.promoted = set()
                self.unpromoted = set()

            def add(self, job: JobData) -> None:
                (self.promoted if job.is_promoted else self.unpromoted).add(job)

            def __len__(self):
                return len(self.promoted) + len(self.unpromoted)

            def pools(self) -> Tuple[set[JobData], set[JobData]]:
                return self.unpromoted, self.promoted

            def iter(self):
                for j in self.unpromoted:
                    yield j
                for j in self.promoted:
                    yield j

        def job_valid_for_internal_rando(job: JobData) -> bool:
            # We disable mages because there aren't any entries for them in the
            # base weapon tables. Eventually we'll add them back in, but for
            # now we can just disable them.
            # CR-soon cam: Add these back in
            if any(
                map(
                    job.name.startswith,
                    (
                        # catches both regular Mages and "Mage Knight"
                        "Mage",
                        "Sage",
                        "Shaman",
                        "Druid",
                        "Priest",
                        "Cleric",
                        "Monk",
                        "Bishop",
                        "Troubadour",
                        "Valkyrie",
                        "Summoner",
                        "Necromancer",
                        "Pupil",
                        "Journeyman",
                        "Recruit",
                        "Dracozombie",
                    ),
                )
            ):
                return False

            return True

        # CR-soon cam: do this better
        weapon_tables = {
            (
                WeaponKind.of_str(ty) if ty in WeaponKind.get_valid_names() else ty,
                level,
            ): i
            for i, (ty, level) in enumerate(INTERNAL_RANDO_WEAPON_TABLE_ROWS)
        }
        jobset = JobSet()

        for i in range(INTERNAL_RANDO_CLASS_WEIGHTS_COUNT):
            offs = (
                INTERNAL_RANDO_CLASS_WEIGHTS_OFFS
                + i * INTERNAL_RANDO_CLASS_WEIGHT_ENTRY_SIZE
            )
            for j in range(INTERNAL_RANDO_CLASS_WEIGHT_NUM_CLASSES):
                job_id = self.rom[offs + j]
                if not job_id or job_id >= 255:
                    break
                job = self.jobs_by_id[job_id]
                if job.name == "Dracozombie":
                    continue
                unpromoted_pool, promoted_pool = (
                    jobset.pools()
                    # We _could_ repoint this and not need to check, but eh
                    if len(jobset) >= INTERNAL_RANDO_WEAPONS_MAX_CLASSES
                    else (self.unpromoted_jobs, self.promoted_jobs)
                )
                new_job = self.select_new_job(
                    job,
                    unpromoted_pool=unpromoted_pool,
                    promoted_pool=promoted_pool,
                    job_valid=job_valid_for_internal_rando,
                )
                self.rom[offs + j] = new_job.id
                jobset.add(new_job)

        # CR-someday cam: There is a lot of hardcoding going on here. It would
        # be nice to move some of the special-casing here to the data files.
        for i, job in enumerate(jobset.iter()):
            offs = INTERNAL_RANDO_WEAPONS_OFFS + i * INTERNAL_RANDO_WEAPONS_ENTRY_SIZE
            row1: Tuple[int, int, int, int, int]
            row1weights: Tuple[int, int, int, int, int]
            row1distrib: Tuple[int, int, int, int, int]
            if "Claw" in job.tags:
                pwr, distrib = {
                    "Revenant": (0, 1),
                    "Entombed": (1, 3),
                    "Bael": (2, 26),
                    "Elder Bael": (3, 27),
                }[job.name]
                idx = weapon_tables[("Claw", pwr)]
                row1 = (idx, 0, 0, 0, 0)
                row1weights = (100, 0, 0, 0, 0)
                row1distrib = (distrib, 0, 0, 0, 0)
            elif "Fang" in job.tags:
                pwr = 1 if job.is_promoted else 0
                idx = weapon_tables[("Fang", pwr)]
                row1 = (idx, 0, 0, 0, 0)
                row1weights = (
                    (25, 75, 0, 0, 0) if job.is_promoted else (75, 25, 0, 0, 0)
                )
                row1distrib = (13, 0, 0, 0, 0)
            elif "MonsterDark" in job.tags:
                match job.name:
                    case "Mogall":
                        idx = weapon_tables[("MonsterDark", 0)]
                        distrib_idx = 45
                    case "Arch Mogall":
                        idx = weapon_tables[("MonsterDark", 1)]
                        distrib_idx = 47
                    case "Gorgon":
                        idx = weapon_tables[("MonsterDark", 3)]
                        distrib_idx = 49
                    case other:
                        raise ValueError(
                            f"BUG: unhandled class {other} tagged as `MonsterDark`"
                        )
                row1 = (idx, 0, 0, 0, 0)
                row1weights = (100, 0, 0, 0, 0)
                row1distrib = (distrib_idx, 0, 0, 0, 0)
            elif len(job.usable_weapons) > 1:
                lo_pwr, mid_pwr, hi_pwr = (2, 3, 4) if job.is_promoted else (0, 1, 2)
                lo_kind1, lo_kind2 = self.random.sample(list(job.usable_weapons), k=2)
                lo_idx1 = weapon_tables[(lo_kind1, lo_pwr)]
                lo_idx2 = weapon_tables[(lo_kind2, lo_pwr)]
                hi_kind1, hi_kind2 = self.random.sample(list(job.usable_weapons), k=2)
                hi_idx1 = weapon_tables[(hi_kind1, hi_pwr)]
                hi_idx2 = weapon_tables[(hi_kind2, hi_pwr)]
                mid_kind = self.random.choice((lo_kind1, lo_kind2, hi_kind1, hi_kind2))
                mid_idx = weapon_tables[(mid_kind, mid_pwr)]
                row1 = (lo_idx1, hi_idx1, mid_idx, lo_idx2, hi_idx2)
                row1weights = (23, 15, 25, 22, 15)
                # doens't typecheck
                # row1distrib = tuple(
                #    self.random.choice(self.valid_distribs_by_row[row]) for row in row1
                # )
                row1distrib = (
                    self.random.choice(self.valid_distribs_by_row[row1[0]]),
                    self.random.choice(self.valid_distribs_by_row[row1[1]]),
                    self.random.choice(self.valid_distribs_by_row[row1[2]]),
                    self.random.choice(self.valid_distribs_by_row[row1[3]]),
                    self.random.choice(self.valid_distribs_by_row[row1[4]]),
                )
            else:
                kind = list(job.usable_weapons)[0]
                lo_pwr, mid_pwr, hi_pwr = (2, 3, 4) if job.is_promoted else (0, 1, 2)
                lo_idx = weapon_tables[(kind, lo_pwr)]
                mid_idx = weapon_tables[(kind, mid_pwr)]
                hi_idx = weapon_tables[(kind, hi_pwr)]
                row1 = (lo_idx, mid_idx, hi_idx, 0, 0)
                row1weights = (30, 35, 35, 0, 0)
                row1distrib = (
                    self.random.choice(self.valid_distribs_by_row[row1[0]]),
                    self.random.choice(self.valid_distribs_by_row[row1[1]]),
                    self.random.choice(self.valid_distribs_by_row[row1[2]]),
                    0,
                    0,
                )

            self.rom[offs] = job.id
            self.rom[offs + 1 : offs + 6] = bytes(row1)
            self.rom[offs + 11 : offs + 16] = bytes(row1weights)
            self.rom[offs + 21 : offs + 26] = bytes(row1distrib)

    def make_monsters_mounted(self) -> None:
        for job in MOUNTED_MONSTERS:
            entry = JOB_TABLE_BASE + job * JOB_SIZE
            self.rom[entry + JOB_ABILITY_1_INDEX] |= MOUNTED_AID_CANTO_MASK

    def fix_movement_costs(self) -> None:
        """
        Units that spawn over water or mountains can get stuck, causing crashes
        or softlocking if their new class cannot walk on those tiles. To resolve
        this, the basepatch includes a fix allowing units to walk on certain
        terrain types (marked by the sentinel value) if they are otherwise stuck.
        """
        for i in range(MOVEMENT_COST_ENTRY_COUNT):
            entry = MOVEMENT_COST_TABLE_BASE + i * MOVEMENT_COST_ENTRY_SIZE
            for terrain_type in IMPORTANT_TERRAIN_TYPES:
                if self.rom[entry + terrain_type] == 255:
                    self.rom[entry + terrain_type] = MOVEMENT_COST_SENTINEL

    def normalize_genders(self) -> None:
        for fjob, mjob in FEMALE_JOBS:
            fjob_entry = JOB_TABLE_BASE + fjob * JOB_SIZE
            mjob_entry = JOB_TABLE_BASE + mjob * JOB_SIZE

            fjob_stats_base = fjob_entry + JOB_STATS_OFFSET
            mjob_stats_base = mjob_entry + JOB_STATS_OFFSET

            fjob_caps_base = fjob_entry + JOB_CAPS_OFFSET
            mjob_caps_base = mjob_entry + JOB_CAPS_OFFSET

            for i in range(STATS_COUNT + 1):
                self.rom[fjob_stats_base + i] = self.rom[mjob_stats_base + i]
                self.rom[fjob_caps_base + i] = self.rom[mjob_caps_base + i]

    def tweak_lords(self) -> None:
        for char, job, lock_mask in [
            (EIRIKA, EIRIKA_LORD, EIRIKA_LOCK),
            (EPHRAIM, EPHRAIM_LORD, EPHRAIM_LOCK),
        ]:
            # Move some of the lord base stats from the lord classes to the lords
            character_entry = CHARACTER_TABLE_BASE + char * CHARACTER_SIZE
            stats_base = character_entry + CHARACTER_STATS_OFFSET

            lord_entry = JOB_TABLE_BASE + job * JOB_SIZE
            job_stats_base = lord_entry + JOB_STATS_OFFSET

            for i in range(STATS_COUNT):
                roll = self.random.randint(0, 4)
                old_base = self.rom[job_stats_base + i]
                new_personal_base = min(roll, old_base)
                self.rom[stats_base + i] += new_personal_base
                self.rom[job_stats_base + i] -= new_personal_base

            ability_4_base = character_entry + CHAR_ABILITY_4_OFFSET
            self.rom[ability_4_base] |= lock_mask

    def fix_cutscenes(self) -> None:
        # Eirika's Rapier is given in a cutscene at the start of the chapter,
        # rather than being in her inventory
        eirika_job = self.character_store["Eirika"]
        if any(wkind != WeaponKind.STAFF for wkind in eirika_job.usable_weapons):
            new_rapier = self.select_new_item(
                eirika_job, self.weapons_by_name["Steel Blade"].id, {}
            )
        else:
            new_rapier = self.random.choice(
                [
                    self.weapons_by_name["Heal"],
                    self.weapons_by_name["Mend"],
                    self.weapons_by_name["Recover"],
                ]
            ).id
        self.rom[EIRIKA_RAPIER_OFFSET] = new_rapier

        # While we force Vanessa to fly to give Ross a fighting chance, it's
        # very possible that she won't be able to lift him. To make it more
        # reasonable to save him, we _also_ set his starting HP.
        self.rom[ROSS_CH2_HP_OFFSET] = 15

        # Eirika and Ephraim get automatic steels on rejoining in Ch15, which
        # need to be adjusted.
        ch15_auto_steel_sword = self.select_new_item(
            eirika_job, self.weapons_by_name["Steel Sword"].id, {}
        )
        ephraim_job = self.character_store["Ephraim"]
        ch15_auto_steel_lance = self.select_new_item(
            ephraim_job, self.weapons_by_name["Steel Lance"].id, {}
        )

        self.rom[CH15_AUTO_STEEL_SWORD] = ch15_auto_steel_sword
        self.rom[CH15_AUTO_STEEL_LANCE] = ch15_auto_steel_lance

    # TODO: logic
    #   - Flying Duessel vs enemy archers in Ephraim 10 may be unbeatable
    def apply_base_changes(self) -> None:
        for chapter_name, chapter in self.unit_blocks.items():
            for block in chapter:
                try:
                    self.randomize_block(block)
                except (ValueError, IndexError) as e:
                    logging.error("crash dump:")
                    logging.error(f"  block_data: {chapter_name}, {block.name}")
                    logging.error(f"  {e}")
                    raise

        self.fix_movement_costs()
        self.fix_cutscenes()
        self.tweak_lords()
        self.make_monsters_mounted()

    def apply_5x_buffs(self) -> None:
        for char in ["Ephraim", "Forde", "Kyle"]:
            ids = self.character_store.lookup_ids(char)
            if ids is None:
                logging.error(f"Error: apply_5x_buffs: Unable to lookup ids for {char}")
                continue
            for char_id in ids:
                char_base = CHARACTER_TABLE_BASE + CHARACTER_SIZE * char_id
                stats_base = char_base + CHARACTER_STATS_OFFSET
                for i in range(STATS_COUNT):
                    self.rom[stats_base + i] += 2

    def apply_infinite_holy_weapons(self) -> None:
        for weapon_id in HOLY_WEAPON_IDS:
            weapon_base = ITEM_TABLE_BASE + weapon_id * ITEM_SIZE
            ability_1_base = weapon_base + ITEM_ABILITY_1_INDEX
            self.rom[ability_1_base] |= UNBREAKABLE_FLAG

    def redistribute_growths(self, total: int) -> list[int]:
        cuts = sorted(self.random.sample(range(1, total), STATS_COUNT))
        result = []
        overflow = 0
        for st, end in zip([0]+cuts, cuts+[total]):
            growth = end-st
            if growth > 255:
                result.append(255)
                overflow += growth-255
            else:
                result.append(growth)
        while overflow > 0:
            available_indices = [i for i, g in enumerate(result) if g < 255]
            if not available_indices:
                break
            i = self.random.choice(available_indices)
            result[i] += overflow
            overflow = 0
            if result[i] > 255:
                overflow = result[i]-255
                result[i] = 255
        return result

    def randomize_growths(self, kind: GrowthRandoKind, grmin: int, grmax: int) -> None:
        if grmin > grmax:
            grmin, grmax = grmax, grmin

        player_ids: Iterable[int] = itertools.chain.from_iterable(
            ids
            for ids in (
                self.character_store.lookup_ids(char)
                for char in self.character_store.character_tags
                if "player" in self.character_store.character_tags[char]
            )
            if ids is not None
        )

        def roll_delta() -> int:
            delta = self.random.randint(grmin, grmax)
            direction = self.random.choice([-1, 1])
            return delta * direction

        for char_id in player_ids:
            char_base = CHARACTER_TABLE_BASE + CHARACTER_SIZE * char_id
            growths_base = char_base + CHARACTER_GROWTHS_OFFSET
            growths = list(self.rom[growths_base : growths_base + STATS_COUNT + 1])
            new_growths: list[int]
            match kind:
                case GrowthRandoKind.NONE:
                    return
                case GrowthRandoKind.REDISTRIBUTE:
                    total = sum(growths) + roll_delta()
                    new_growths = self.redistribute_growths(total)
                case GrowthRandoKind.DELTA:
                    new_growths = [max(growth + roll_delta(), 0) for growth in growths]
                case GrowthRandoKind.FULL:
                    new_growths = [self.random.randint(grmin, grmax) for _ in growths]

            for i in range(STATS_COUNT + 1):
                self.rom[growths_base + i] = max(min(255, new_growths[i]), 0)

    def generate_swaps(
        self, songs: dict[int, str]
    ) -> list[Tuple[Tuple[int, str], Tuple[int, str]]]:
        ids = list(songs.items())
        return list(zip(ids, self.random.sample(ids, k=len(ids))))

    def randomize_music(self, kind: MusicRandoKind) -> None:
        swaps: list[Tuple[Tuple[int, str], Tuple[int, str]]]
        match kind:
            case MusicRandoKind.VANILLA:
                return
            case MusicRandoKind.CONTEXT:
                swaps = list(
                    itertools.chain.from_iterable(
                        self.generate_swaps(songs)
                        for (_ctx, songs) in self.songs.items()
                    )
                )
            case MusicRandoKind.CHAOS:
                swaps = self.generate_swaps(
                    functools.reduce(operator.or_, self.songs.values())
                )

        logging.debug("Music rando song swaps:")
        ptrs: list[Tuple[int, int]] = []
        for (baseid, basename), (newid, newname) in swaps:
            logging.debug(f"  {basename} ({hex(baseid)}) -> {newname} ({hex(newid)})")
            ptrs.append(
                (baseid, read_word_le(self.rom, SONG_TABLE_BASE + newid * SONG_SIZE))
            )

        for id, ptr in ptrs:
            write_word_le(self.rom, SONG_TABLE_BASE + id * SONG_SIZE, ptr)
