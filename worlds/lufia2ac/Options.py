from __future__ import annotations

import functools
import numbers
import random
from dataclasses import dataclass
from itertools import accumulate, chain, combinations
from typing import Any, cast, Dict, Iterator, List, Mapping, Optional, Set, Tuple, Type, TYPE_CHECKING, Union

from Options import AssembleOptions, Choice, DeathLink, ItemDict, NamedRange, OptionDict, PerGameCommonOptions, Range, \
    TextChoice, Toggle
from .Enemies import enemy_name_to_sprite
from .Items import ItemType, l2ac_item_table

if TYPE_CHECKING:
    from BaseClasses import PlandoOptions
    from worlds.AutoWorld import World


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


class EnemyChoice(TextChoice):
    _valid_sprites: Dict[str, int] = {enemy_name.lower(): sprite for enemy_name, sprite in enemy_name_to_sprite.items()}

    def verify(self, world: Type[World], player_name: str, plando_options: PlandoOptions) -> None:
        if isinstance(self.value, int):
            return
        if str(self.value).lower() in self._valid_sprites:
            return
        raise ValueError(f"Could not find option '{self.value}' for '{self.__class__.__name__}', known options are:\n"
                         f"{', '.join(self.options)}, {', '.join(enemy_name_to_sprite)}.")

    @property
    def sprite(self) -> Optional[int]:
        return self._valid_sprites.get(str(self.value).lower())


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
    If you increase the blue chest chance, then the red chest chance is decreased in return.
    Supported values: 5 – 75
    Default value: 25 (five times as much as in an unmodified game)
    """

    display_name = "Blue chest chance"
    range_start = 5
    range_end = 75
    default = 25

    @property
    def chest_type_thresholds(self) -> bytes:
        ratio: float = (256 - self.value) / (256 - 5)
        # unmodified chances are: consumable (mostly non-restorative) = 36/256, consumable (restorative) = 58/256,
        # blue chest = 5/256, spell = 30/256, gear = 45/256 (and the remaining part, weapon = 82/256)
        chest_type_chances: List[float] = [36 * ratio, 58 * ratio, float(self.value), 30 * ratio, 45 * ratio]
        return bytes(round(threshold) for threshold in reversed(tuple(accumulate(chest_type_chances))))


class BlueChestCount(Range):
    """The number of blue chest items that will be in your item pool.

    The number of blue chests in your world that count as multiworld location checks will be equal this amount plus one
    more for each party member or capsule monster if you have shuffle_party_members/shuffle_capsule_monsters enabled.
    (You will still encounter blue chests in your world after all the multiworld location checks have been exhausted,
    but these chests will then generate items for yourself only.)
    Supported values: 10 – 100
    Default value: 25
    """

    display_name = "Blue chest count"
    range_start = 10
    range_end = 100
    default = 25
    overall_max = range_end + 7 + 6  # Have to account for capsule monster and party member items


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

    _sprite: Dict[int, int] = {
        option_lizard_man: 0x9E,
        option_big_catfish: 0xC5,
        option_regal_goblin: 0x9D,
        option_follower_x2: 0x76,
        option_camu: 0x75,
        option_tarantula: 0xC6,
        option_pierre: 0x77,
        option_daniele: 0x78,
        option_gades_a: 0x7A,
        option_mummy_x4: 0xA8,
        option_troll_x3: 0xA9,
        option_gades_b: 0x7A,
        option_idura_a: 0x74,
        option_lion_x2: 0xB7,
        option_idura_b: 0x74,
        option_idura_c: 0x74,
        option_rogue_flower: 0x96,
        option_soldier_x4: 0x18,
        option_gargoyle_x4: 0xC4,
        option_venge_ghost: 0xD0,
        option_white_dragon_x3: 0xC3,
        option_fire_dragon: 0xC0,
        option_ghost_ship: 0xC8,
        option_tank: 0xC7,
        option_gades_c: 0x7A,
        option_amon: 0x79,
        option_erim: 0x38,
        option_daos: 0x7B,
        option_egg_dragon: 0xC0,
        option_master: 0x94,
    }

    random_groups = {
        "random-low": ["lizard_man", "big_catfish", "regal_goblin", "follower_x2", "camu", "tarantula", "pierre",
                       "daniele", "mummy_x4", "troll_x3"],
        "random-middle": ["idura_a", "lion_x2", "idura_b", "idura_c", "rogue_flower", "soldier_x4", "gargoyle_x4"],
        "random-high": ["venge_ghost", "white_dragon_x3", "fire_dragon", "ghost_ship", "tank"],
        "random-sinistral": ["gades_c", "amon", "erim", "daos"],
    }
    extra_options = set(random_groups)

    @property
    def flag(self) -> int:
        return 0xFE if self.value == Boss.option_master else 0xFF

    @property
    def music(self) -> int:
        return 0x1B if self.value in {Boss.option_master, Boss.option_gades_a, Boss.option_gades_b, Boss.option_gades_c,
                                      Boss.option_amon, Boss.option_erim, Boss.option_daos} else 0x19

    @property
    def sprite(self) -> int:
        return Boss._sprite[self.value]


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


class CapsuleStartingForm(NamedRange):
    """The starting form of your capsule monsters.

    Supported values: 1 – 4, m
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Capsule monster starting form"
    range_start = 1
    range_end = 5
    default = 1
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


class CapsuleStartingLevel(LevelMixin, NamedRange):
    """The starting level of your capsule monsters.

    Can be set to the special value party_starting_level to make it the same value as the party_starting_level option.
    Supported values: 1 – 99, party_starting_level
    Default value: 1 (same as in an unmodified game)
    """

    display_name = "Capsule monster starting level"
    range_start = 1
    range_end = 99
    default = 1
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


class CustomItemPool(ItemDict, Mapping[str, int]):
    """Customize your multiworld item pool.

    Using this option you can place any cave item in your multiworld item pool. (By default, the pool is filled with
    blue chest items.) Here you can add any valid item from the Lufia II Ancient Cave section of the datapackage
    (see https://archipelago.gg/datapackage). The value of this option has to be a mapping of item name to count,
    e.g., to add two Deadly rods and one Dekar Blade: {Deadly rod: 2, Dekar blade: 1}
    The maximum total amount of custom items you can place is limited by the chosen blue_chest_count; any remaining,
    non-customized space in the pool will be occupied by random blue chest items.
    """

    display_name = "Custom item pool"
    value: Dict[str, int]

    @property
    def count(self) -> int:
        return sum(self.values())

    def __getitem__(self, key: str) -> int:
        return self.value.__getitem__(key)

    def __iter__(self) -> Iterator[str]:
        return self.value.__iter__()

    def __len__(self) -> int:
        return self.value.__len__()


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
    default: Union[str, int] = "M"
    value: Union[str, int]

    random_groups = {
        "random-2p": ["M" + "".join(p) for p in combinations("ADGLST", 1)],
        "random-3p": ["M" + "".join(p) for p in combinations("ADGLST", 2)],
        "random-4p": ["M" + "".join(p) for p in combinations("ADGLST", 3)],
    }
    vars().update({f"option_{party}": party for party in (*random_groups, "M", *chain(*random_groups.values()))})
    _valid_sorted_parties: List[List[str]] = [sorted(party) for party in ("M", *chain(*random_groups.values()))]
    _members_to_bytes: bytes = bytes.maketrans(b"MSGATDL", bytes(range(7)))

    def verify(self, world: Type[World], player_name: str, plando_options: PlandoOptions) -> None:
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


class EnemyFloorNumbers(Choice):
    """Change which enemy types are encountered at which floor numbers.

    Supported values:
    vanilla
        Ninja, e.g., is allowed to appear on the 3 floors B44-B46
    shuffle — The existing enemy types are redistributed among nearby floors. Shifts by up to 6 floors are possible.
        Ninja, e.g., will be allowed to appear on exactly 3 consecutive floors somewhere from B38-B40 to B50-B52
    randomize — For each floor, new enemy types are chosen randomly from the set usually possible on floors [-6, +6].
        Ninja, e.g., is among the various possible selections for any enemy slot affecting the floors from B38 to B52
    Default value: vanilla (same as in an unmodified game)
    """

    display_name = "Enemy floor numbers"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    default = option_vanilla


class EnemyMovementPatterns(EnemyChoice):
    """Change the movement patterns of enemies.

    Supported values:
    vanilla
    shuffle_by_pattern — The existing movement patterns are redistributed among each other.
        Sprites that usually share a movement pattern will still share movement patterns after shuffling
    randomize_by_pattern — For each movement pattern, a new one is chosen randomly from the set of existing patterns.
        Sprites that usually share a movement pattern will still share movement patterns after randomizing
    shuffle_by_sprite — The existing movement patterns of sprites are redistributed among the enemy sprites.
        Sprites that usually share a movement pattern can end up with different movement patterns after shuffling
    randomize_by_sprite — For each sprite, a new movement is chosen randomly from the set of existing patterns.
        Sprites that usually share a movement pattern can end up with different movement patterns after randomizing
    singularity — All enemy sprites use the same, randomly selected movement pattern
    Alternatively, you can directly specify an enemy name such as "Red Jelly" as the value of this option.
        In that case, the movement pattern usually associated with this sprite will be used by all enemy sprites
    Default value: vanilla (same as in an unmodified game)
    """

    display_name = "Enemy movement patterns"
    option_vanilla = 0
    option_shuffle_by_pattern = 1
    option_randomize_by_pattern = 2
    option_shuffle_by_sprite = 3
    option_randomize_by_sprite = 4
    option_singularity = 5
    default = option_vanilla


class EnemySprites(EnemyChoice):
    """Change the appearance of enemies.

    Supported values:
    vanilla
    shuffle — The existing sprites are redistributed among the enemy types.
        This means that, after shuffling, exactly 1 enemy type will be dressing up as the "Red Jelly" sprite
    randomize — For each enemy type, a new sprite is chosen randomly from the set of existing sprites.
        This means that, after randomizing, any number of enemy types could end up using the "Red Jelly" sprite
    singularity — All enemies use the same, randomly selected sprite
    Alternatively, you can directly specify an enemy name such as "Red Jelly" as the value of this option.
        In this case, the sprite usually associated with that enemy will be used by all enemies
    Default value: vanilla (same as in an unmodified game)
    """

    display_name = "Enemy sprites"
    option_vanilla = 0
    option_shuffle = 1
    option_randomize = 2
    option_singularity = 3
    default = option_vanilla


class ExpModifier(Range):
    """Percentage modifier for EXP gained from enemies.

    Supported values: 100 – 500
    Default value: 100 (same as in an unmodified game)
    """

    display_name = "EXP modifier"
    range_start = 100
    range_end = 500
    default = 100

    def __call__(self, exp: bytes) -> bytes:
        try:
            return (int.from_bytes(exp, "little") * self.value // 100).to_bytes(2, "little")
        except OverflowError:
            return b"\xFF\xFF"


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


class GoldModifier(Range):
    """Percentage modifier for gold gained from enemies.

    Supported values: 25 – 400
    Default value: 100 (same as in an unmodified game)
    """

    display_name = "Gold modifier"
    range_start = 25
    range_end = 400
    default = 100

    def __call__(self, gold: bytes) -> bytes:
        try:
            return (int.from_bytes(gold, "little") * self.value // 100).to_bytes(2, "little")
        except OverflowError:
            return b"\xFF\xFF"


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


class InactiveExpGain(Choice):
    """The rate at which characters not currently in the active party gain EXP.

    Supported values: disabled, half, full
    Default value: disabled (same as in an unmodified game)
    """

    display_name = "Inactive character EXP gain"
    option_disabled = 0
    option_half = 50
    option_full = 100
    default = option_disabled


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


class MasterHp(Range):
    """The number of hit points of the Master

    (Only has an effect if boss is set to master.)
    Supported values: 1 – 9980
    Default value: 9980 (same as in an unmodified game)
    """

    display_name = "Master HP"
    range_start = 1
    range_end = 9980
    default = 9980


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


class ShopInterval(NamedRange):
    """Place shops after a certain number of floors.

    E.g., if you set this to 5, then you will be given the opportunity to shop after completing B5, B10, B15, etc.,
    whereas if you set it to 1, then there will be a shop after every single completed floor.
    Shops will offer a random selection of wares; on deeper floors, more expensive items might appear.
    You can customize the stock that can appear in shops using the shop_inventory option.
    You can control how much gold you will be obtaining from enemies using the gold_multiplier option.
    Supported values: disabled, 1 – 10
    Default value: disabled (same as in an unmodified game)
    """

    display_name = "Shop interval"
    range_start = 1
    range_end = 10
    default = 0
    special_range_names = {
        "disabled": 0,
    }


class ShopInventory(OptionDict):
    """Determine the item types that can appear in shops.

    The value of this option should be a mapping of item categories (or individual items) to weights (non-negative
    integers), which are used as relative probabilities when it comes to including these things in shops. (The actual
    contents of the generated shops are selected randomly and are subject to additional constraints such as more
    expensive things being allowed only on later floors.)
    Supported keys:
    non_restorative — a selection of mostly non-restorative red chest consumables
    restorative — all HP- or MP-restoring red chest consumables
    blue_chest — all blue chest items
    spell — all red chest spells
    gear — all red chest armors, shields, headgear, rings, and rocks (this respects the gear_variety_after_b9 option,
        meaning that you will not encounter any shields, headgear, rings, or rocks in shops from B10 onward unless you
        also enabled that option)
    weapon — all red chest weapons
    Additionally, you can also add extra weights for any specific cave item. If you want your shops to have a
    higher than normal chance of selling a Dekar blade, you can, e.g., add "Dekar blade: 5".
    You can even forego the predefined categories entirely and design a custom shop pool from scratch by providing
    separate weights for each item you want to include.
    (Spells, however, cannot be weighted individually and are only available as part of the "spell" category.)
    Default value: {spell: 30, gear: 45, weapon: 82}
    """

    display_name = "Shop inventory"
    _special_keys = {"non_restorative", "restorative", "blue_chest", "spell", "gear", "weapon"}
    valid_keys = _special_keys | {item for item, data in l2ac_item_table.items()
                                  if data.type in {ItemType.BLUE_CHEST, ItemType.ENEMY_DROP, ItemType.ENTRANCE_CHEST,
                                                   ItemType.RED_CHEST, ItemType.RED_CHEST_PATCH}}
    default: Dict[str, int] = {
        "spell": 30,
        "gear": 45,
        "weapon": 82,
    }
    value: Dict[str, int]

    def verify(self, world: Type[World], player_name: str, plando_options: PlandoOptions) -> None:
        super().verify(world, player_name, plando_options)
        for item, weight in self.value.items():
            if not isinstance(weight, numbers.Integral) or weight < 0:
                raise Exception(f"Weight for item \"{item}\" from option {self} must be a non-negative integer, "
                                f"but was \"{weight}\".")

    @property
    def total(self) -> int:
        return sum(self.value.values())

    @property
    def non_restorative(self) -> int:
        return self.value.get("non_restorative", 0)

    @property
    def restorative(self) -> int:
        return self.value.get("restorative", 0)

    @property
    def blue_chest(self) -> int:
        return self.value.get("blue_chest", 0)

    @property
    def spell(self) -> int:
        return self.value.get("spell", 0)

    @property
    def gear(self) -> int:
        return self.value.get("gear", 0)

    @property
    def weapon(self) -> int:
        return self.value.get("weapon", 0)

    @functools.cached_property
    def custom(self) -> Dict[int, int]:
        return {l2ac_item_table[item].code & 0x01FF: weight for item, weight in self.value.items()
                if item not in self._special_keys}


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
        multiworld; when one of these items is found, the corresponding party member is unlocked for you to use.
        While cave diving, you can add or remove unlocked party members by using the character items from the inventory
    Default value: false (same as in an unmodified game)
    """

    display_name = "Shuffle party members"

    @property
    def unlock(self) -> int:
        return 0b00000000 if self.value else 0b11111100


@dataclass
class L2ACOptions(PerGameCommonOptions):
    blue_chest_chance: BlueChestChance
    blue_chest_count: BlueChestCount
    boss: Boss
    capsule_cravings_jp_style: CapsuleCravingsJPStyle
    capsule_starting_form: CapsuleStartingForm
    capsule_starting_level: CapsuleStartingLevel
    crowded_floor_chance: CrowdedFloorChance
    custom_item_pool: CustomItemPool
    death_link: DeathLink
    default_capsule: DefaultCapsule
    default_party: DefaultParty
    enemy_floor_numbers: EnemyFloorNumbers
    enemy_movement_patterns: EnemyMovementPatterns
    enemy_sprites: EnemySprites
    exp_modifier: ExpModifier
    final_floor: FinalFloor
    gear_variety_after_b9: GearVarietyAfterB9
    goal: Goal
    gold_modifier: GoldModifier
    healing_floor_chance: HealingFloorChance
    inactive_exp_gain: InactiveExpGain
    initial_floor: InitialFloor
    iris_floor_chance: IrisFloorChance
    iris_treasures_required: IrisTreasuresRequired
    master_hp: MasterHp
    party_starting_level: PartyStartingLevel
    run_speed: RunSpeed
    shop_interval: ShopInterval
    shop_inventory: ShopInventory
    shuffle_capsule_monsters: ShuffleCapsuleMonsters
    shuffle_party_members: ShufflePartyMembers
