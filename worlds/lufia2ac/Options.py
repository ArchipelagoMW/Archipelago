from __future__ import annotations

import random
from itertools import chain, combinations
from typing import Any, cast, Dict, List, Optional, Set, Tuple

from Options import AssembleOptions, Choice, DeathLink, Option, Range, SpecialRange, TextChoice, Toggle


class AssembleCustomizableChoices(AssembleOptions):
    def __new__(mcs, name: str, bases: Tuple[type, ...], attrs: Dict[str, Any]) -> AssembleCustomizableChoices:
        cls: AssembleOptions = super().__new__(mcs, name, bases, attrs)

        if "extra_options" in attrs:
            cls.name_lookup.update(enumerate(attrs["extra_options"], start=max(cls.name_lookup) + 1))
        return cast(AssembleCustomizableChoices, cls)


class RandomGroupsChoice(Choice, metaclass=AssembleCustomizableChoices):
    extra_options: Optional[Set[str]]
    random_groups: Dict[str, List[str]]

    @classmethod
    def get_option_name(cls, value: int) -> str:
        if value in cls.options.values():
            return next(k for k, v in cls.options.items() if v == value)
        else:
            return super().get_option_name(value)

    @classmethod
    def from_text(cls, text: str) -> Choice:
        key: str = text.lower()
        if key == "random":
            text = random.choice([o for o in cls.options if o not in cls.random_groups])
        elif key in cls.random_groups:
            text = random.choice(cls.random_groups[key])
        return super().from_text(text)


class LevelMixin:
    xp_coefficients: List[int] = sorted([191, 65, 50, 32, 18, 14, 6, 3, 3, 2, 2, 2, 2] * 8, reverse=True)

    @classmethod
    def _to_xp(cls, level: int, *, capsule: bool) -> int:
        if level == 1:
            return 0
        if level == 99:
            return 9999999

        increment: int = 20 << 8
        total: int = increment
        for lv in range(2, level):
            increment += (increment * cls.xp_coefficients[lv]) >> 8
            total += increment
            if capsule:
                total &= 0xFFFFFF00
        return (total >> 8) - 10


class BlueChestChance(Range):
    """The chance of a chest being a blue chest.

    It is given in units of 1/256, i.e., a value of 25 corresponds to 25/256 ~ 9.77%.
    If you increase the blue chest chance, then the chance of finding consumables is decreased in return.
    The chance of finding red chest equipment or spells is unaffected.
    Supported values: 5 – 75
    Default value: 25 (five times as much as in an unmodified game)
    """

    display_name = "Blue chest chance"
    range_start = 5
    range_end = 75
    default = 25


class BlueChestCount(Range):
    """The number of blue chest items that will be in your item pool.

    The number of blue chests in your world that count as multiworld location checks will be equal this amount plus one
    more for each party member or capsule monster if you have shuffle_party_members/shuffle_capsule_monsters enabled.
    (You will still encounter blue chests in your world after all the multiworld location checks have been exhausted,
    but these chests will then generate items for yourself only.)
    Supported values: 10 – 75
    Default value: 25
    """

    display_name = "Blue chest count"
    range_start = 10
    range_end = 75
    default = 25


class Boss(RandomGroupsChoice):
    """Which boss to fight on the final floor.

    Supported values:
    lizard_man, big_catfish, regal_goblin, follower_x2, camu, tarantula, pierre, daniele, gades_a, mummy_x4, troll_x3,
    gades_b, idura_a, lion_x2, idura_b, idura_c, rogue_flower, soldier_x4, gargoyle_x4, venge_ghost, white_dragon_x3,
    fire_dragon, ghost_ship, tank, gades_c, amon, erim, daos, egg_dragon, master
    random-low — select a random regular boss, from lizard_man to troll_x3
    random-middle — select a random regular boss, from idura_a to gargoyle_x4
    random-high — select a random regular boss, from venge_ghost to tank
    random-sinistral — select a random Sinistral boss
    Default value: master (same as in an unmodified game)
    """

    display_name = "Boss"
    option_lizard_man = 0x01
    option_big_catfish = 0x02
    # 0x03 = Goblin + Skeleton; regular monsters
    # 0x04 = Goblin; regular monster
    option_regal_goblin = 0x05
    option_follower_x2 = 0x06
    option_camu = 0x07
    option_tarantula = 0x08
    option_pierre = 0x09
    option_daniele = 0x0A
    option_gades_a = 0x0B
    option_mummy_x4 = 0x0C
    option_troll_x3 = 0x0D
    option_gades_b = 0x0E
    option_idura_a = 0x0F
    # 0x10 = Pierre; Maxim + Tia only
    # 0x11 = Daniele; Guy + Selan only
    option_lion_x2 = 0x12
    option_idura_b = 0x13
    option_idura_c = 0x14
    option_rogue_flower = 0x15
    option_soldier_x4 = 0x16
    option_gargoyle_x4 = 0x17
    option_venge_ghost = 0x18
    option_white_dragon_x3 = 0x19
    option_fire_dragon = 0x1A
    option_ghost_ship = 0x1B
    # 0x1C = Soldier x4; same as 0x16
    # 0x1D = Soldier x4; same as 0x16
    option_tank = 0x1E
    option_gades_c = 0x1F
    option_amon = 0x20
    # 0x21 = Gades; same as 0x1F
    # 0x22 = Amon; same as 0x20
    option_erim = 0x23
    option_daos = 0x24
    option_egg_dragon = 0x25
    option_master = 0x26
    default = option_master

    random_groups = {
        "random-low": ["lizard_man", "big_catfish", "regal_goblin", "follower_x2", "camu", "tarantula", "pierre",
                       "daniele", "mummy_x4", "troll_x3"],
        "random-middle": ["idura_a", "lion_x2", "idura_b", "idura_c", "rogue_flower", "soldier_x4", "gargoyle_x4"],
        "random-high": ["venge_ghost", "white_dragon_x3", "fire_dragon", "ghost_ship", "tank"],
        "random-sinistral": ["gades_c", "amon", "erim", "daos"],
    }
    extra_options = frozenset(random_groups)

    @property
    def flag(self) -> int:
        return 0xFE if self.value == Boss.option_master else 0xFF


class CapsuleCravingsJPStyle(Toggle):
    """Make capsule monster cravings behave as in the Japanese version.

    In the US version, the data that determines which items a capsule monster can request is a mess.
    It allows only for a very limited selection of items to be requested, and the quality of the selected item is almost
    always either too low or too high (compared to the capsule monsters current quality preference). This means that,
    if fed, the requested item will either be rejected by the capsule monster or lead to an unreasonable increase of the
    quality preference, making further feeding more difficult.
    This setting provides a fix for the bug described above.
    If enabled, the capsule monster feeding behavior will be changed to behave analogous to the JP (and EU) version.
    This means that requests become more varied, while the requested item will be guaranteed to be of the same quality
    as the capsule monsters current preference. Thus, it can no longer happen that the capsule monster dislikes eating
    the very item it just requested.
    Supported values: false, true
    Default value: false (same as in an unmodified game)
    """

    display_name = "Capsule cravings JP style"


class CapsuleStartingForm(SpecialRange):
    """The starting form of your capsule monsters.

    Supported values: 1 – 4, m
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Capsule monster starting form"
    range_start = 1
    range_end = 5
    default = 1
    special_range_cutoff = 1
    special_range_names = {
        "default": 1,
        "m": 5,
    }

    @property
    def unlock(self) -> int:
        if self.value == self.special_range_names["m"]:
            return 0x0B
        else:
            return self.value - 1


class CapsuleStartingLevel(LevelMixin, SpecialRange):
    """The starting level of your capsule monsters.

    Can be set to the special value party_starting_level to make it the same value as the party_starting_level option.
    Supported values: 1 – 99, party_starting_level
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Capsule monster starting level"
    range_start = 0
    range_end = 99
    default = 1
    special_range_cutoff = 1
    special_range_names = {
        "default": 1,
        "party_starting_level": 0,
    }

    @property
    def xp(self) -> int:
        return self._to_xp(self.value, capsule=True)


class CrowdedFloorChance(Range):
    """The chance of a floor being a crowded floor.

    It is given in units of 1/256, i.e., a value of 16 corresponds to 16/256 = 6.25%.
    A crowded floor is a floor where most of the chests are grouped in one room together with many enemies.
    Supported values: 0 – 255
    Default value: 16 (same as in an unmodified game)
    """

    display_name = "Crowded floor chance"
    range_start = 0
    range_end = 255
    default = 16


class DefaultCapsule(Choice):
    """Preselect the active capsule monster.

    (Only has an effect if shuffle_capsule_monsters is set to false.)
    Supported values: jelze, flash, gusto, zeppy, darbi, sully, blaze
    Default value: jelze
    """

    display_name = "Default capsule monster"
    option_jelze = 0x00
    option_flash = 0x01
    option_gusto = 0x02
    option_zeppy = 0x03
    option_darbi = 0x04
    option_sully = 0x05
    option_blaze = 0x06
    default = option_jelze


class DefaultParty(RandomGroupsChoice, TextChoice):
    """Preselect the party lineup.

    (Only has an effect if shuffle_party_members is set to false.)
    Supported values:
    Can be set to any valid combination of up to 4 party member initials, e.g.:
    M — Maxim
    DGMA — Dekar, Guy, Maxim, and Arty
    MSTL — Maxim, Selan, Tia, and Lexis
    random-2p — a random 2-person party
    random-3p — a random 3-person party
    random-4p — a random 4-person party
    Default value: M
    """

    display_name = "Default party lineup"
    default = "M"

    random_groups = {
        "random-2p": ["M" + "".join(p) for p in combinations("ADGLST", 1)],
        "random-3p": ["M" + "".join(p) for p in combinations("ADGLST", 2)],
        "random-4p": ["M" + "".join(p) for p in combinations("ADGLST", 3)],
    }
    vars().update({f"option_{party}": party for party in (*random_groups, "M", *chain(*random_groups.values()))})
    _valid_sorted_parties: List[List[str]] = [sorted(party) for party in ("M", *chain(*random_groups.values()))]
    _members_to_bytes: bytes = bytes.maketrans(b"MSGATDL", bytes(range(7)))

    def verify(self, *args, **kwargs) -> None:
        if str(self.value).lower() in self.random_groups:
            return
        if sorted(str(self.value).upper()) in self._valid_sorted_parties:
            return
        raise ValueError(f"Could not find option '{self.value}' for '{self.__class__.__name__}', known options are:\n"
                         f"{', '.join(self.random_groups)}, {', '.join(('M', *chain(*self.random_groups.values())))} "
                         "as well as all permutations of these.")

    @staticmethod
    def _flip(i: int) -> int:
        return {4: 5, 5: 4}.get(i, i)

    @property
    def event_script(self) -> bytes:
        return bytes((*(b for i in bytes(self) if i != 0 for b in (0x2B, i, 0x2E, i + 0x65, 0x1A, self._flip(i) + 1)),
                      0x1E, 0x0B, len(self) - 1, 0x1C, 0x86, 0x03, *(0x00,) * (6 * (4 - len(self)))))

    @property
    def roster(self) -> bytes:
        return bytes((len(self), *bytes(self), *(0xFF,) * (4 - len(self))))

    def __bytes__(self) -> bytes:
        return str(self.value).upper().encode("ASCII").translate(self._members_to_bytes)

    def __len__(self) -> int:
        return len(str(self.value))


class FinalFloor(Range):
    """The final floor, where the boss resides.

    Supported values: 2 – 99
    Default value: 99 (same as in an unmodified game)
    """

    display_name = "Final floor"
    range_start = 2
    range_end = 99
    default = 99


class GearVarietyAfterB9(Toggle):
    """Fixes a bug that prevents various gear from appearing after B9.

    Due to an overflow bug in the game, the distribution of red chest gear is impaired after B9.
    Starting with B10, the number of items available from red chests is severely limited, meaning that red chests will
    no longer contain any shields, headgear, rings, or jewels (and the selection of body armor is reduced as well).
    This setting provides a fix for the bug described above.
    If enabled, red chests beyond B9 will continue to produce shields, headgear, rings, and jewels as intended,
    while the odds of finding body armor in red chests are decreased as a result.
    The distributions of red chest weapons, spells, and consumables as well as blue chests are unaffected.
    Supported values: false, true
    Default value: false (same as in an unmodified game)
    """

    display_name = "Increase gear variety after B9"


class Goal(Choice):
    """The objective you have to fulfill in order to complete the game.

    Supported values:
    boss — defeat the boss on the final floor
    iris_treasure_hunt — gather the required number of Iris treasures and leave the cave
    boss_iris_treasure_hunt — complete both the "boss" and the "iris_treasure_hunt" objective (in any order)
    final_floor — merely reach the final floor
    Default value: boss
    """

    display_name = "Goal"
    option_boss = 0x01
    option_iris_treasure_hunt = 0x02
    option_boss_iris_treasure_hunt = 0x03
    option_final_floor = 0x04
    default = option_boss


class HealingFloorChance(Range):
    """The chance of a floor having a healing tile hidden under a bush.

    It is given in units of 1/256, i.e., a value of 16 corresponds to 16/256 = 6.25%.
    Supported values: 0 – 255
    Default value: 16 (same as in an unmodified game)
    """

    display_name = "Healing tile floor chance"
    range_start = 0
    range_end = 255
    default = 16


class InitialFloor(Range):
    """The initial floor, where you begin your journey.

    (If this value isn't smaller than the value of final_floor, it will automatically be set to final_floor - 1)
    Supported values: 1 – 98
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Initial floor"
    range_start = 1
    range_end = 98
    default = 1


class IrisFloorChance(Range):
    """The chance of a floor being able to generate an Iris treasure.

    It is given in units of 1/256, i.e., a value of 5 corresponds to 5/256 ~ 1.95%.
    The true chance of a floor holding an Iris treasure you need is usually lower than the chance specified here, e.g.,
    if you have already found 8 of 9 Iris items then the chance of generating the last one is only 1/9 of this value.
    Supported values: 5 – 255
    Default value: 5 (same as in an unmodified game)
    """

    display_name = "Iris treasure floor chance"
    range_start = 5
    range_end = 255
    default = 5


class IrisTreasuresRequired(Range):
    """The number of Iris treasures required to complete the goal.

    This setting only has an effect if the "iris_treasure_hunt" or "boss_iris_treasure_hunt" goal is active.
    Supported values: 1 – 9
    Default value: 9
    """

    display_name = "Iris treasures required"
    range_start = 1
    range_end = 9
    default = 9


class MasterHp(SpecialRange):
    """The number of hit points of the Master

    Supported values:
    1 – 9980,
    scale — scales the HP depending on the value of final_floor
    Default value: 9980 (same as in an unmodified game)
    """

    display_name = "Master HP"
    range_start = 0
    range_end = 9980
    default = 9980
    special_range_cutoff = 1
    special_range_names = {
        "default": 9980,
        "scale": 0,
    }

    @staticmethod
    def scale(final_floor: int) -> int:
        return final_floor * 100 + 80


class PartyStartingLevel(LevelMixin, Range):
    """The starting level of your party members.

    Supported values: 1 – 99
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Party starting level"
    range_start = 1
    range_end = 99
    default = 1

    @property
    def xp(self) -> int:
        return self._to_xp(self.value, capsule=False)


class RunSpeed(Choice):
    """Modifies the game to allow you to move faster than normal when pressing the Y button.

    Supported values: disabled, double, triple, quadruple
    Default value: disabled (same as in an unmodified game)
    """

    display_name = "Run speed"
    option_disabled = 0x08
    option_double = 0x10
    option_triple = 0x16
    option_quadruple = 0x20
    default = option_disabled


class ShuffleCapsuleMonsters(Toggle):
    """Shuffle the capsule monsters into the multiworld.

    Supported values:
    false — all 7 capsule monsters are available in the menu and can be selected right away
    true — you start without capsule monster; 7 new "items" are added to your pool and shuffled into the multiworld;
        when one of these items is found, the corresponding capsule monster is unlocked for you to use
    Default value: false (same as in an unmodified game)
    """

    display_name = "Shuffle capsule monsters"

    @property
    def unlock(self) -> int:
        return 0b00000000 if self.value else 0b01111111


class ShufflePartyMembers(Toggle):
    """Shuffle the party members into the multiworld.

    Supported values:
    false — all 6 optional party members are present in the cafe and can be recruited right away
    true — only Maxim is available from the start; 6 new "items" are added to your pool and shuffled into the
        multiworld; when one of these items is found, the corresponding party member is unlocked for you to use
    Default value: false (same as in an unmodified game)
    """

    display_name = "Shuffle party members"

    @property
    def unlock(self) -> int:
        return 0b00000000 if self.value else 0b11111100


l2ac_option_definitions: Dict[str, type(Option)] = {
    "blue_chest_chance": BlueChestChance,
    "blue_chest_count": BlueChestCount,
    "boss": Boss,
    "capsule_cravings_jp_style": CapsuleCravingsJPStyle,
    "capsule_starting_form": CapsuleStartingForm,
    "capsule_starting_level": CapsuleStartingLevel,
    "crowded_floor_chance": CrowdedFloorChance,
    "death_link": DeathLink,
    "default_capsule": DefaultCapsule,
    "default_party": DefaultParty,
    "final_floor": FinalFloor,
    "gear_variety_after_b9": GearVarietyAfterB9,
    "goal": Goal,
    "healing_floor_chance": HealingFloorChance,
    "initial_floor": InitialFloor,
    "iris_floor_chance": IrisFloorChance,
    "iris_treasures_required": IrisTreasuresRequired,
    "master_hp": MasterHp,
    "party_starting_level": PartyStartingLevel,
    "run_speed": RunSpeed,
    "shuffle_capsule_monsters": ShuffleCapsuleMonsters,
    "shuffle_party_members": ShufflePartyMembers,
}
