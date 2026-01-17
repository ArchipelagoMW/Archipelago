from collections.abc import Mapping, Sequence
from dataclasses import dataclass
import math
from random import Random
import random

from typing_extensions import override

from Options import DefaultOnToggle, PerGameCommonOptions, Range, Choice, FreeText, Removed


class CharacterCount(Range):
    """Sets the number of characters needed to access the final battle"""
    display_name = "Characters Required"
    range_start = 0
    range_end = 14
    default = 8


class EsperCount(Range):
    """Sets the number of Espers needed to access the final battle"""
    display_name = "Espers Required"
    range_start = 0
    range_end = 27
    default = 12


class DragonCount(Range):
    """Sets the number of dragons needed to access the final battle"""
    display_name = "Dragons Required"
    range_start = 0
    range_end = 8
    default = 4


class BossCount(Range):
    """Sets the number of bosses required to access the final battle"""
    display_name = "Bosses Required"
    range_start = 0
    range_end = 40
    default = 16


class StartingCharacterCount(Range):
    """Sets the number of starting characters"""
    display_name = "Starting Character Count"
    range_start = 1
    range_end = 4
    default = 2


class StartingCharacter1(Choice):
    """Starting Character 1"""
    display_name = "Starting Character 1"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_random_with_no_gogo_or_umaro = 14
    default = 14

    @override
    @classmethod
    def from_any(cls, data: object) -> Choice:
        """
        random doesn't allow gogo or umaro in slot 1
        because if it did allow it, we wouldn't have a good way
        to prevent random making possible unbeatable seeds
        """
        # TODO: if core gives us the source of the option
        # so we know whether Gogo/Umaro was chosen from "random"
        # then we can remove this restriction
        # TODO: return type is `Self` after it's fixed in base class
        if data == "random":
            return super().from_any(random.randrange(1, 12))
        return super().from_any(data)


class StartingCharacter2(Choice):
    """Starting Character 2. Only used if Starting Character Count is 2+"""
    display_name = "Starting Character 2"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 15


class StartingCharacter3(Choice):
    """Starting Character 3. Only used if Starting Character Count is 3+"""
    display_name = "Starting Character 3"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 14


class StartingCharacter4(Choice):
    """Starting Character 4. Only used if Starting Character Count is 4"""
    display_name = "Starting Character 4"
    option_terra = 0
    option_locke = 1
    option_edgar = 2
    option_sabin = 3
    option_celes = 4
    option_shadow = 5
    option_cyan = 6
    option_gau = 7
    option_setzer = 8
    option_mog = 9
    option_strago = 10
    option_relm = 11
    option_gogo = 12
    option_umaro = 13
    option_none = 14
    option_random_with_no_gogo_or_umaro = 15
    default = 14


class StartAverageLevel(DefaultOnToggle):
    """ Recruited characters start at the average character level """
    display_name = "Start Average Level"

    def flags(self) -> list[str]:
        return ["-sal"] if self.value else []


class RandomizedStats(Choice):
    """Modify character base stats, as a range of percentages applied to their vanilla stats.
    Options include vanilla (100%), Light (85-125%), Moderate (50-150%), Boosted (100-175%) and Wild (0-200%)"""
    display_name = "Randomized Stats"
    option_vanilla = 0
    option_light = 1
    option_moderate = 2
    option_boosted = 3
    option_wild = 4
    default = 1


class RandomizedCommands(Choice):
    """Randomize everyone's unique commands. Random Vanilla will pull only from the base list of commands.
    Random Most will include Relic-modified commands, and Random All includes temporary character commands
    like Shock"""
    display_name = "Randomized Commands"
    option_vanilla = 0
    option_random_vanilla = 1
    option_random_most = 2
    option_random_all = 3
    default = 2


class BattleRewardMultiplier(Choice):
    """Multiplies the rewards (EXP, MP, GP) from enemies."""
    display_name = "Battle Reward Multiplier"
    option_vanilla = 0
    option_double = 1
    option_triple = 2
    option_quadruple = 3
    option_quintuple = 4
    default = 2


class RandomizedBosses(Choice):
    """Modifies boss encounters. Shuffled mixes up the vanilla bosses (so you'll still have one of each). Random
    will roll each slot independently, making it likely a boss will show up multiple times or not at all."""
    display_name = "Randomized Bosses"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    default = 1


class RandomEncounters(Choice):
    """Modifies random encounters. The Wild setting mixes bosses into the pool of encounters"""
    display_name = "Random Encounters"
    option_vanilla = 0
    option_randomized = 1
    option_wild = 2
    default = 1


class EsperSpells(Choice):
    """Modifies the spells taught by Espers. Shuffle mixes around the vanilla learnsets, while
    Random rolls new options for every Esper. Random Tiered weights powerful spells to be less common."""
    display_name = "Esper Spells"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    option_random_tiered = 3
    default = 1


class EsperBonuses(Choice):
    """Modifies level up bonuses from Espers. Shuffle mixes around the vanilla bonuses, while Random
    rolls new options for every Esper"""
    display_name = "Esper Bonuses"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    default = 1


class EsperEquipability(Choice):
    """Modifies who can equip each esper. Random rolls a set of characters for each Esper, while Balanced
    Random attempts to give every character the same number of Espers to equip"""
    display_name = "Esper Equipability"
    option_vanilla = 0
    option_randomized = 1
    option_balanced_random = 2
    default = 0


class NaturalMagic(Choice):
    """Modifies which two characters learn Magic via level up, and what they learn"""
    display_name = "Natural Magic"
    option_vanilla = 0
    option_random_characters = 1
    option_random_spells = 2
    option_both = 3
    default = 3


class StartingGP(Range):
    """Starting supply of GP"""
    display_name = "Starting GP"
    range_start = 0
    range_end = 50000
    default = 30000


class RandomizedShops(Choice):
    """Modifies shop inventories. Random can result in anything, while Random Tiered weights more powerful items
    to be less common"""
    display_name = "Randomized Shops"
    option_vanilla = 0
    option_randomized = 1
    option_random_tiered = 2
    default = 2


class SpellcastingItems(Choice):
    """Controls if Rods, Super Balls, and elemental Shields are allowed in shops. Limited removes Shields and
    makes rods and Super Balls very expensive"""
    display_name = "Spellcasting Items"
    option_vanilla = 0
    option_limited = 1
    option_none = 2
    default = 1


class Equipment(Choice):
    """Modifies who can use what equipment. Shuffled mixes each character's equipability with another's,
    while Balanced Random ensures every item is usable by seven characters."""
    display_name = "Equipment"
    option_vanilla = 0
    option_shuffled = 1
    option_randomized = 2
    option_balanced_random = 3
    default = 1


class AllowStrongestItems(DefaultOnToggle):
    """Controls if EXP Eggs, Illuminas, and Paladin Shields can appear in the game."""
    display_name = "Allow Strongest Items"


class RandomizeZozoClock(Removed):
    """ This option has been removed. You can use `ZozoClockChestExclude` instead. """
    display_name = "Randomize Zozo Clock"

    def __init__(self, value: str):
        if value:
            raise RuntimeError("`RandomizeZozoClock` removed in WC 1.4.2, please update your options file. "
                               "If you would like to make sure you don't have to do the clock puzzle, "
                               "you can use `ZozoClockChestExclude`")
        super().__init__("")


class ZozoClockChestExclude(DefaultOnToggle):
    """Whether to exclude the Zozo Clock Puzzle Chest from progression."""
    display_name = "Exclude Zozo Clock Puzzle Chest"


class Treasuresanity(Choice):
    """Mixes all treasure chests and the like into the location pool. Not recommended for beginners.
    Additional Gating prevents having to double dip dungeons where you don't have the character needed to clear"""
    display_name = "Treasuresanity"
    option_off = 0
    option_on = 1
    option_on_with_additional_gating = 2


class Flagstring(FreeText):
    """Enables custom flagstring. For advanced users only: will override most other options"""
    display_name = "Flagstring"
    default = "False"

    _cache: dict[str, Mapping[str, str]] | None = None
    """ `{full_flagstring_value: {flag: value}}` """

    def _parse(self) -> dict[str, str]:
        parsed: dict[str, str] = {}
        space_split = self.value.split(" ")
        i = 0
        while i < len(space_split):
            if space_split[i].startswith("-"):
                if len(space_split[i]) < 2:
                    raise ValueError(f"invalid {self.display_name} at symbol {i}")
                key = space_split[i]
                values: list[str] = []
                i += 1
                while i < len(space_split) and not space_split[i].startswith("-"):
                    values.append(space_split[i])
                    i += 1
                value = " ".join(values)
                parsed[key] = value
            else:
                i += 1
        return parsed

    def _set(self, flags: Mapping[str, str]) -> None:
        """ inverse of `_parse` """
        items: list[str] = []
        for k, v in flags.items():
            if not k.startswith("-"):
                raise ValueError(f"{k=} should start with '-'")
            items.append(k)
            if len(v):
                items.append(v)
        self.value = " ".join(items)
        assert self._get_from_cache() == flags, flags

    def _get_from_cache(self) -> Mapping[str, str]:
        if self._cache is None:
            self._cache = {}

        parsed = self._cache.get(self.value)
        if parsed is None:
            parsed = self._parse()
            self._cache[self.value] = parsed
        return parsed

    def has_flag(self, key: str) -> bool:
        parsed = self._get_from_cache()
        return key in parsed

    def get_flag(self, key: str) -> str:
        """ `key` including "-" prefix """
        parsed = self._get_from_cache()
        return parsed[key]

    def replace_flag(self, old_key: str, new_key: str, new_value: str) -> None:
        """
        - keys should include the "-" prefix
        - `new_value` should should be empty string for keys without values
        """
        if not new_key.startswith("-"):
            raise ValueError(f"{new_key=} should start with '-'")
        parsed = self._get_from_cache()
        if old_key not in parsed.keys():
            raise KeyError(old_key)
        # to preserve order, new dict instead of pop and insert new key
        new_flags = {
            (k if k != old_key else new_key): (v if k != old_key else new_value)
            for k, v in parsed.items()
        }
        self._set(new_flags)


@dataclass
class FF6WCOptions(PerGameCommonOptions):
    CharacterCount: CharacterCount
    EsperCount: EsperCount
    DragonCount: DragonCount
    BossCount: BossCount
    StartingCharacterCount: StartingCharacterCount
    StartingCharacter1: StartingCharacter1
    StartingCharacter2: StartingCharacter2
    StartingCharacter3: StartingCharacter3
    StartingCharacter4: StartingCharacter4
    StartAverageLevel: StartAverageLevel
    RandomizedStats: RandomizedStats
    RandomizedCommands: RandomizedCommands
    BattleRewardMultiplier: BattleRewardMultiplier
    RandomizedBosses: RandomizedBosses
    RandomEncounters: RandomEncounters
    EsperSpells: EsperSpells
    EsperBonuses: EsperBonuses
    EsperEquipability: EsperEquipability
    NaturalMagic: NaturalMagic
    StartingGP: StartingGP
    RandomizedShops: RandomizedShops
    SpellcastingItems: SpellcastingItems
    Equipment: Equipment
    AllowStrongestItems: AllowStrongestItems
    RandomizeZozoClock: RandomizeZozoClock  # TODO: some time after this option raises an exception, remove this
    ZozoClockChestExclude: ZozoClockChestExclude
    Treasuresanity: Treasuresanity
    Flagstring: Flagstring

    def no_paladin_shields(self) -> bool:
        return (not self.AllowStrongestItems.value) or self.Flagstring.has_flag("-nfps")

    def no_exp_eggs(self) -> bool:
        return (not self.AllowStrongestItems.value) or self.Flagstring.has_flag("-nee")

    def no_illuminas(self) -> bool:
        return (not self.AllowStrongestItems.value) or self.Flagstring.has_flag("-nil")

    def no_shoes(self) -> bool:
        # We default to noshoes if no flagstring is given
        # TODO: SSOT with generate_items_string
        return ("-" not in self.Flagstring.value) or self.Flagstring.has_flag("-noshoes")

    def no_moogle_charm(self) -> bool:
        # We default to nmc if no flagstring is given
        # TODO: SSOT with generate_items_string
        return ("-" not in self.Flagstring.value) or self.Flagstring.has_flag("-nmc")


def verify_flagstring(flags: Sequence[str]) -> None:
    """ raises exception (`ValueError`) if flagstring is invalid """
    from .WorldsCollide.args.arguments import Arguments
    from . import FF6WCWorld
    assert not isinstance(flags, str)
    if "-i" not in flags:
        flags = ["-i", "x"] + list(flags)
    with FF6WCWorld.wc_ready:
        Arguments(flags)


def generate_flagstring(options: FF6WCOptions, starting_characters: list[str]) -> list[str]:
    if (options.Flagstring.value).capitalize() != 'False':
        flags = options.Flagstring.value.split(" ")
    else:
        flags = [
            *generate_settings_string(),
            *generate_objectives_string(options),
            *generate_party_string(options, starting_characters),
            *generate_commands_string(options),
            *generate_battle_string(options),
            *generate_magic_string(options),
            *generate_items_string(options),
            *generate_gameplay_string(options),
            *generate_graphics_string(),
            *generate_accessibility_string(),
            *generate_fixes_string()
        ]
        flags = [_ for _ in flags if len(_) > 0]
    verify_flagstring(flags)
    return flags


def generate_settings_string() -> list[str]:
    # Character gating is always on, and we want the spoiler log
    return ["-cg", "-sl"]


def generate_objectives_string(options: FF6WCOptions) -> list[str]:
    character_count = options.CharacterCount
    esper_count = options.EsperCount
    dragon_count = options.DragonCount
    boss_count = options.BossCount

    # fb = final battle unlock
    fb_character_string = f".2.{character_count}.{character_count}" if character_count > 0 else ""
    fb_esper_string = f".4.{esper_count}.{esper_count}" if esper_count > 0 else ""
    fb_dragon_string = f".6.{dragon_count}.{dragon_count}" if dragon_count > 0 else ""
    fb_boss_string = f".8.{boss_count}.{boss_count}" if boss_count > 0 else ""
    conditions = 0
    if character_count > 0:
        conditions += 1
    if esper_count > 0:
        conditions += 1
    if dragon_count > 0:
        conditions += 1
    if boss_count > 0:
        conditions += 1
    fb_base = f"2.{conditions}.{conditions}"
    fb_string = ["-oa", fb_base + fb_character_string + fb_esper_string + fb_dragon_string + fb_boss_string]

    character_count = min(14, character_count + 3)
    esper_count = min(27, esper_count + 3)
    dragon_count = min(8, dragon_count + 3)
    boss_count = min(40, boss_count + 3)
    conditions = math.ceil(conditions / 2)
    # kts = kefka's tower skip
    kts_character_string = f".2.{character_count}.{character_count}" if character_count > 0 else ""
    kts_esper_string = f".4.{esper_count}.{esper_count}" if esper_count > 0 else ""
    kts_dragon_string = f".6.{dragon_count}.{dragon_count}" if dragon_count > 0 else ""
    kts_boss_string = f".8.{boss_count}.{boss_count}" if boss_count > 0 else ""
    kts_base = f"3.{conditions}.{conditions}"
    kts_string = ["-ob", kts_base + kts_character_string + kts_esper_string + kts_dragon_string + kts_boss_string]

    swdtech_learn = ["-oc", "30.8.8.1.1.11.8"]
    magitek_upgrade = ["-od", "59.1.1.11.31"]

    return [*fb_string, *kts_string, *swdtech_learn, *magitek_upgrade]


def generate_party_string(options: FF6WCOptions, starting_characters: list[str]) -> list[str]:
    character_count = options.StartingCharacterCount.value

    if character_count < 4:
        starting_characters.extend(["", "", ""])

    character_one = starting_characters[0]
    character_two = starting_characters[1] if character_count >= 2 else ""
    character_three = starting_characters[2] if character_count >= 3 else ""
    character_four = starting_characters[3] if character_count == 4 else ""

    character_one = "-sc1=" + str.lower(character_one)
    character_two = "-sc2=" + str.lower(character_two) if character_count >= 2 else ""
    character_three = "-sc3=" + str.lower(character_three) if character_count >= 3 else ""
    character_four = "-sc4=" + str.lower(character_four) if character_count == 4 else ""

    sal = options.StartAverageLevel.flags()

    stat_min = 100
    stat_max = 100
    if options.RandomizedStats == 1:  # Light
        stat_min = 85
        stat_max = 125
    elif options.RandomizedStats == 2:  # Moderate
        stat_min = 50
        stat_max = 150
    elif options.RandomizedStats == 3:  # Boosted
        stat_min = 100
        stat_max = 175
    elif options.RandomizedStats == 4:  # Wild
        stat_min = 0
        stat_max = 200

    stat_string = ["-csrp", f"{stat_min}", f"{stat_max}"]

    equipable_umaro = "-eu"

    return [character_one, character_two, character_three, character_four, *sal, *stat_string, equipable_umaro]


def generate_commands_string(options: FF6WCOptions) -> list[str]:
    command_strings = []
    if options.RandomizedCommands.value == RandomizedCommands.option_vanilla:
        command_strings = ["-com=03050708091011121315191629"]
    if options.RandomizedCommands.value == RandomizedCommands.option_random_vanilla:
        command_strings = ["-com=03050708091011121315191629", "-scc"]
    if options.RandomizedCommands.value >= 2:  # Random Most/Random All
        forbid_commands_strings = (
            ["-rec1=28", "-rec2=27", "-rec3=26"] if options.RandomizedCommands.value == 3 else ""
        )
        command_strings = ["-com=98989898989898989898989898", *forbid_commands_strings]

    steal_command_strings = ["-sch", "-fc"]  # Higher Steal Chance, Fix Capture Bugs
    swdtech_command_strings = ["-fst", "-sel"]  # Fast SwdTech, Everyone Learns
    tools_command_strings = ["-sto=1"]  # One starting Tool
    blitz_command_strings = ["-brl", "-bel"]  # Bum Rush Last, Everyone Learns
    # Start with 3-5 Lores, +/- 25% MP cost, Everyone Learns
    lore_command_strings = ["-slr", "3", "5", "-lmprp", "75", "125", "-lel"]
    sketch_command_strings = ["-scis"]  # Improved Sketch/Control
    # Start with one Dance, Shuffle Abilities, Display Abilities, No Stumble, Everyone Learns
    dance_command_strings = ["-sdr", "1", "1", "-das", "-dda", "-dns", "-del"]
    rage_command_strings = ["-srr", "10", "20", "-rnl"]  # Start with 10-20 Rages, No Leap
    other_command_string = ["-stra"]  # SwdTech/Runic All

    return [*command_strings, *steal_command_strings, *swdtech_command_strings, *tools_command_strings,
            *blitz_command_strings, *lore_command_strings, *sketch_command_strings, *dance_command_strings,
            *rage_command_strings, *other_command_string]


def generate_battle_string(options: FF6WCOptions) -> list[str]:
    reward_value = options.BattleRewardMultiplier + 1
    rewards_strings = [f"-xpm={reward_value}", f"-mpm={reward_value}", f"-gpm={reward_value}", "-be", "-nxppd"]

    boss_string = ""
    if options.RandomizedBosses == 1:
        boss_string = "-bbs"
    elif options.RandomizedBosses == 2:
        boss_string = "-bbr"

    statue_string = "-stloc=mix"  # Mix statues into the general pool

    dragon_string = "-drloc=shuffle"  # Shuffle dragons amongst each other

    # Scaling factor of 2, abilities scale keeping elements, max level scale is 40, dragons get scaled
    scaling_string = ["-lsc=2", "-hmc=2", "-xgc=2", "-ase=2", "-msl=40", "-sed"]

    return [*rewards_strings, boss_string, statue_string, dragon_string, *scaling_string]


def generate_magic_string(options: FF6WCOptions) -> list[str]:
    spell_strings = ["-mmprp", "75", "125"]  # Spell cost +/- 25%

    esper_spells_strings = [""]
    if options.EsperSpells == 1:
        esper_spells_strings = ["-ess"]  # Shuffle Esper spells
    elif options.EsperSpells == 2:
        esper_spells_strings = ["-esr", "1", "5"]  # Fully randomize Esper spells
    elif options.EsperSpells == 3:
        esper_spells_strings = ["-esrt"]  # Randomize Esper spells with tiered weighting

    esper_bonuses_string = ""
    if options.EsperBonuses == 1:  # Shuffled bonuses
        esper_bonuses_string = "-ebs"
    elif options.EsperBonuses == 2:  # Random bonuses
        esper_bonuses_string = "-ebr=70"

    esper_equipability_string = ""
    if options.EsperEquipability == 1:  # Random equipability
        esper_equipability_string = ["-eer", "1", "12"]
    elif options.EsperEquipability == 2:  # Balanced random equipability
        esper_equipability_string = ["-eebr", "6"]

    multi_summon_string = "-ems"

    natural_magic_strings = ["-nmmi"]  # Show who has Natural Magic
    if options.NaturalMagic == 1 or options.NaturalMagic == 3:  # Random characters
        natural_magic_strings.extend(["-nm1=random", "-nm2=random"])
    if options.NaturalMagic == 2 or options.NaturalMagic == 3:  # Random learnsets
        natural_magic_strings.extend(["-rns1", "-rns2", "-rnl1", "-rnl2"])

    return [*spell_strings, *esper_spells_strings, esper_bonuses_string, *esper_equipability_string,
            multi_summon_string, *natural_magic_strings]


def generate_items_string(options: FF6WCOptions) -> list[str]:
    starting_gp_string = f"-gp={options.StartingGP}"
    # Three Moogle Charms, a Warp Stone, and five Fenix Downs
    starting_items_strings = ["-smc=3", "-sws=1", "-sfd=5"]

    # 75-125% shop prices, five Dried Meat shops, no priceless items
    shops_strings = ["-sprp", "75", "125", "-sdm", "5", "-npi"]
    if options.RandomizedShops.value == RandomizedShops.option_randomized:
        # 20 is the default value on the worlds collide website
        shops_strings.extend(["-sisr", "20"])
    elif options.RandomizedShops.value == RandomizedShops.option_random_tiered:
        shops_strings.extend(["-sirt"])

    if options.SpellcastingItems.value == SpellcastingItems.option_limited:
        spellcasting_items_string = ["-sebr", "-sesb", "-snes"]
    elif options.SpellcastingItems.value == SpellcastingItems.option_none:
        spellcasting_items_string = ["-snbr", "-snsb", "-snes"]
    else:  # vanilla
        spellcasting_items_string = []

    # Moogle Charms equipable by all, no Moogle Charms in item pool, no Sprint Shoes in pool
    # Stronger Atma Weapon, 8-32 battles to uncurse Cursed Shield
    equipability_strings = ["-mca", "-nmc", "-noshoes", "-saw", "-csb", "8", "32"]
    if not options.AllowStrongestItems.value:
        equipability_strings.extend(["-nee", "-nil", "-nfps"])
    if options.Equipment.value == Equipment.option_shuffled:
        equipability_strings.extend(["-iesr=0", "-iersr=0"])
    elif options.Equipment.value == Equipment.option_randomized:
        equipability_strings.extend(["-ier", "1", "14", "-ierr", "1", "14"])
    elif options.Equipment.value == Equipment.option_balanced_random:
        equipability_strings.extend(["-iebr=6", "-ierbr=6"])

    chest_randomization = ["-ccsr", "20"]  # Default shuffle + 20% random. Only applies if Treasuresanity = off

    return [starting_gp_string, *starting_items_strings, *shops_strings,
            *spellcasting_items_string, *equipability_strings, *chest_randomization]


def generate_gameplay_string(options: FF6WCOptions) -> list[str]:
    # B Dash, randomized Coliseum rewards and enemies, randomize Auction House minor items
    gameplay_strings = ["-move=bd", "-cor", "-crr", "-crvr", "50", "250", "-crm", "-ari"]
    if not options.AllowStrongestItems.value:
        gameplay_strings.extend(["-cnee", "-cnil"])
    # Zozo Clock is always randomized as of version 1.4.2, so do not need to add this into flagstring anymore
    # if options.RandomizeZozoClock.value:
    #    gameplay_strings.extend(["-rc"])
    return gameplay_strings


def generate_graphics_string() -> list[str]:
    # Lowercase the names.
    return ["-name=Terra.Locke.Cyan.Shadow.Edgar.Sabin.Celes.Strago.Relm.Setzer.Mog.Gau.Gogo.Umaro "]


def generate_accessibility_string() -> list[str]:
    # Remove flashing, add high contrast world map
    return ["-frm", "-wmhc"]


def generate_fixes_string() -> list[str]:
    # Bug fixes, and Magimaster can cast his final spell because I'm a jerk.
    return ["-fedc", "-fe", "-fbs", "-fvd", "-fj", "-dgne", "-wnz", "-cmd"]


def resolve_character_options(options: FF6WCOptions, random: Random) -> list[str]:
    """ returns the starting characters and sets the option values to match the returned characters """

    from . import Rom

    character_count = options.StartingCharacterCount.value
    from_options = [
        (options.StartingCharacter1.current_key).capitalize(),
        (options.StartingCharacter2.current_key).capitalize(),
        (options.StartingCharacter3.current_key).capitalize(),
        (options.StartingCharacter4.current_key).capitalize()
    ]
    to_use = from_options[:character_count]
    assert len(to_use) == character_count, f"{to_use=} {character_count=}"
    specified: list[str] = []
    for ch in to_use:
        specified.append(ch if (ch in Rom.characters and ch not in specified) else "")
    assert len(specified) == character_count, f"{specified=} {character_count=}"
    have_non_gogo_umaro = any(ch in Rom.characters[:12] for ch in specified)
    for i in range(character_count):
        if specified[i] == "":
            # If the player is asking for no Gogo or Umaro
            # or if they don't have any other characters besides Gogo or Umaro
            # then the random choice doesn't allow Gogo or Umaro.
            # Also don't choose from characters already chosen.
            choices = [ch for ch in (
                Rom.characters[:12]
                if (to_use[i] == "Random_with_no_gogo_or_umaro" or not have_non_gogo_umaro)
                else Rom.characters
            ) if ch not in specified]
            choice = random.choice(choices)
            specified[i] = choice
            assert any(ch in Rom.characters[:12] for ch in specified), (
                f"still don't have ngu {specified=} {choices=} {choice=}"
            )
            have_non_gogo_umaro = True
    assert all(ch in Rom.characters for ch in specified), f"{specified=}"
    assert len(specified) == character_count, f"{specified=} {character_count=}"

    options.StartingCharacter1.value = StartingCharacter1.options[specified[0].lower()]
    if character_count > 1:
        options.StartingCharacter2.value = StartingCharacter2.options[specified[1].lower()]
    if character_count > 2:
        options.StartingCharacter3.value = StartingCharacter3.options[specified[2].lower()]
    if character_count > 3:
        options.StartingCharacter4.value = StartingCharacter4.options[specified[3].lower()]

    return specified
