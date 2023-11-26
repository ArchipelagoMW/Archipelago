import typing

from Options import Range, Choice, Toggle, DefaultOnToggle, AssembleOptions, DeathLink, ProgressionBalancing


# typing boilerplate
class FlagsProtocol(typing.Protocol):
    value: int
    default: int
    flags: typing.List[str]


class FlagProtocol(typing.Protocol):
    value: int
    default: int
    flag: str


# meta options
class EvermizerFlags:
    flags: typing.List[str]

    def to_flag(self: FlagsProtocol) -> str:
        return self.flags[self.value]


class EvermizerFlag:
    flag: str

    def to_flag(self: FlagProtocol) -> str:
        return self.flag if self.value != self.default else ''


class OffOnFullChoice(Choice):
    option_off = 0
    option_on = 1
    option_full = 2
    alias_chaos = 2


class OffOnLogicChoice(Choice):
    option_off = 0
    option_on = 1
    option_logic = 2


# actual options
class Difficulty(EvermizerFlags, Choice):
    """Changes relative spell cost and stuff"""
    display_name = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_mystery = 3  # 'random' is reserved
    alias_chaos = 3
    default = 1
    flags = ['e', 'n', 'h', 'x']


class EnergyCore(EvermizerFlags, Choice):
    """How to obtain the Energy Core"""
    display_name = "Energy Core"
    option_vanilla = 0
    option_shuffle = 1
    option_fragments = 2
    default = 1
    flags = ['z', '', 'Z']


class RequiredFragments(Range):
    """Required fragment count for Energy Core = Fragments"""
    display_name = "Required Fragments"
    range_start = 1
    range_end = 99
    default = 10


class AvailableFragments(Range):
    """Placed fragment count for Energy Core = Fragments"""
    display_name = "Available Fragments"
    range_start = 1
    range_end = 99
    default = 11


class MoneyModifier(Range):
    """Money multiplier in %"""
    display_name = "Money Modifier"
    range_start = 1
    range_end = 2500
    default = 200


class ExpModifier(Range):
    """EXP multiplier for Weapons, Characters and Spells in %"""
    display_name = "Exp Modifier"
    range_start = 1
    range_end = 2500
    default = 200


class SequenceBreaks(EvermizerFlags, OffOnLogicChoice):
    """Disable, enable some sequence breaks or put them in logic"""
    display_name = "Sequence Breaks"
    default = 0
    flags = ['', 'j', 'J']


class OutOfBounds(EvermizerFlags, OffOnLogicChoice):
    """Disable, enable the out-of-bounds glitch or put it in logic"""
    display_name = "Out Of Bounds"
    default = 0
    flags = ['', 'u', 'U']


class FixCheats(EvermizerFlag, DefaultOnToggle):
    """Fix cheats left in by the devs (not desert skip)"""
    display_name = "Fix Cheats"
    flag = '2'


class FixInfiniteAmmo(EvermizerFlag, Toggle):
    """Fix infinite ammo glitch"""
    display_name = "Fix Infinite Ammo"
    flag = '5'


class FixAtlasGlitch(EvermizerFlag, Toggle):
    """Fix atlas underflowing stats"""
    display_name = "Fix Atlas Glitch"
    flag = '6'


class FixWingsGlitch(EvermizerFlag, Toggle):
    """Fix wings making you invincible in some areas"""
    display_name = "Fix Wings Glitch"
    flag = '7'


class ShorterDialogs(EvermizerFlag, DefaultOnToggle):
    """Cuts some dialogs"""
    display_name = "Shorter Dialogs"
    flag = '9'


class ShortBossRush(EvermizerFlag, DefaultOnToggle):
    """Start boss rush at Metal Magmar, cut enemy HP in half"""
    display_name = "Short Boss Rush"
    flag = 'f'


class Ingredienizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles, Full randomizes spell ingredients"""
    display_name = "Ingredienizer"
    default = 1
    flags = ['i', '', 'I']


class Sniffamizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles, Full randomizes drops in sniff locations"""
    display_name = "Sniffamizer"
    default = 1
    flags = ['s', '', 'S']


class Callbeadamizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles call bead characters, Full shuffles individual spells"""
    display_name = "Callbeadamizer"
    default = 1
    flags = ['c', '', 'C']


class Musicmizer(EvermizerFlag, Toggle):
    """Randomize music for some rooms"""
    display_name = "Musicmizer"
    flag = 'm'


class Doggomizer(EvermizerFlags, OffOnFullChoice):
    """On shuffles dog per act, Full randomizes dog per screen, Pupdunk gives you Everpupper everywhere"""
    display_name = "Doggomizer"
    option_pupdunk = 3
    default = 0
    flags = ['', 'd', 'D', 'p']


class TurdoMode(EvermizerFlag, Toggle):
    """Replace offensive spells by Turd Balls with varying strength and make weapons weak"""
    display_name = "Turdo Mode"
    flag = 't'


class TrapCount(Range):
    """Replace some filler items with traps"""
    display_name = "Trap Count"
    range_start = 0
    range_end = 100
    default = 0


# more meta options
class ItemChanceMeta(AssembleOptions):
    def __new__(mcs, name, bases, attrs):
        if 'item_name' in attrs:
            attrs["display_name"] = f"{attrs['item_name']} Chance"
        attrs["range_start"] = 0
        attrs["range_end"] = 100

        return super(ItemChanceMeta, mcs).__new__(mcs, name, bases, attrs)


class TrapChance(Range, metaclass=ItemChanceMeta):
    item_name: str
    default = 20


# more actual options
class TrapChanceQuake(TrapChance):
    """Sets the chance/ratio of quake traps"""
    item_name = "Quake Trap"


class TrapChancePoison(TrapChance):
    """Sets the chance/ratio of poison effect traps"""
    item_name = "Poison Trap"


class TrapChanceConfound(TrapChance):
    """Sets the chance/ratio of confound effect traps"""
    item_name = "Confound Trap"


class TrapChanceHUD(TrapChance):
    """Sets the chance/ratio of HUD visibility traps"""
    item_name = "HUD Trap"


class TrapChanceOHKO(TrapChance):
    """Sets the chance/ratio of OHKO (1HP left) traps"""
    item_name = "OHKO Trap"


class SoEProgressionBalancing(ProgressionBalancing):
    default = 30
    __doc__ = ProgressionBalancing.__doc__.replace(f"default {ProgressionBalancing.default}", f"default {default}") \
        if ProgressionBalancing.__doc__ else None
    special_range_names = {**ProgressionBalancing.special_range_names, "normal": default}


soe_options: typing.Dict[str, AssembleOptions] = {
    "difficulty":            Difficulty,
    "energy_core":           EnergyCore,
    "required_fragments":    RequiredFragments,
    "available_fragments":   AvailableFragments,
    "money_modifier":        MoneyModifier,
    "exp_modifier":          ExpModifier,
    "sequence_breaks":       SequenceBreaks,
    "out_of_bounds":         OutOfBounds,
    "fix_cheats":            FixCheats,
    "fix_infinite_ammo":     FixInfiniteAmmo,
    "fix_atlas_glitch":      FixAtlasGlitch,
    "fix_wings_glitch":      FixWingsGlitch,
    "shorter_dialogs":       ShorterDialogs,
    "short_boss_rush":       ShortBossRush,
    "ingredienizer":         Ingredienizer,
    "sniffamizer":           Sniffamizer,
    "callbeadamizer":        Callbeadamizer,
    "musicmizer":            Musicmizer,
    "doggomizer":            Doggomizer,
    "turdo_mode":            TurdoMode,
    "death_link":            DeathLink,
    "trap_count":            TrapCount,
    "trap_chance_quake":     TrapChanceQuake,
    "trap_chance_poison":    TrapChancePoison,
    "trap_chance_confound":  TrapChanceConfound,
    "trap_chance_hud":       TrapChanceHUD,
    "trap_chance_ohko":      TrapChanceOHKO,
    "progression_balancing": SoEProgressionBalancing,
}
