import typing
from Options import Option, Range, Choice, Toggle, DefaultOnToggle


class EvermizerFlags:
    flags: typing.List[str]

    def to_flag(self) -> str:
        return self.flags[self.value]


class EvermizerFlag:
    flag: str

    def to_flag(self) -> str:
        return self.flag if self.value != self.default else ''


class OffOnFullChoice(Choice):
    option_off = 0
    option_on = 1
    option_full = 2
    alias_chaos = 2
    alias_false = 0
    alias_true = 1


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


class FixSequence(EvermizerFlag, DefaultOnToggle):
    """Fix some sequence breaks"""
    display_name = "Fix Sequence"
    flag = '1'


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


soe_options: typing.Dict[str, type(Option)] = {
    "difficulty":           Difficulty,
    "money_modifier":       MoneyModifier,
    "exp_modifier":         ExpModifier,
    "fix_sequence":         FixSequence,
    "fix_cheats":           FixCheats,
    "fix_infinite_ammo":    FixInfiniteAmmo,
    "fix_atlas_glitch":     FixAtlasGlitch,
    "fix_wings_glitch":     FixWingsGlitch,
    "shorter_dialogs":      ShorterDialogs,
    "short_boss_rush":      ShortBossRush,
    "ingredienizer":        Ingredienizer,
    "sniffamizer":          Sniffamizer,
    "callbeadamizer":       Callbeadamizer,
    "musicmizer":           Musicmizer,
    "doggomizer":           Doggomizer,
    "turdo_mode":           TurdoMode,
}
