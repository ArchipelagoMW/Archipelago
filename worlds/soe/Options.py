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
    displayname = "Difficulty"
    option_easy = 0
    option_normal = 1
    option_hard = 2
    option_mystery = 3  # 'random' is reserved
    alias_chaos = 3
    default = 1
    flags = ['e', 'n', 'h', 'x']


class MoneyModifier(Range):
    """Money multiplier in %"""
    displayname = "Money Modifier"
    range_start = 1
    range_end = 2500
    default = 200


class ExpModifier(Range):
    """EXP multiplier for Weapons, Characters and Spells in %"""
    displayname = "Exp Modifier"
    range_start = 1
    range_end = 2500
    default = 200


class FixSequence(EvermizerFlag, DefaultOnToggle):
    """Fix some sequence breaks"""
    displayname = "Fix Sequence"
    flag = '1'


class FixCheats(EvermizerFlag, DefaultOnToggle):
    """Fix cheats left in by the devs (not desert skip)"""
    displayname = "Fix Cheats"
    flag = '2'


class FixInfiniteAmmo(EvermizerFlag, Toggle):
    """Fix infinite ammo glitch"""
    displayname = "Fix Infinite Ammo"
    flag = '5'


class FixAtlasGlitch(EvermizerFlag, Toggle):
    """Fix atlas underflowing stats"""
    displayname = "Fix Atlas Glitch"
    flag = '6'


class FixWingsGlitch(EvermizerFlag, Toggle):
    """Fix wings making you invincible in some areas"""
    displayname = "Fix Wings Glitch"
    flag = '7'


class ShorterDialogs(EvermizerFlag, DefaultOnToggle):
    """Cuts some dialogs"""
    displayname = "Shorter Dialogs"
    flag = '9'


class ShortBossRush(EvermizerFlag, DefaultOnToggle):
    """Start boss rush at Metal Magmar, cut enemy HP in half"""
    displayname = "Short Boss Rush"
    flag = 'f'


class Ingredienizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles, Full randomizes spell ingredients"""
    displayname = "Ingredienizer"
    default = 1
    flags = ['i', '', 'I']


class Sniffamizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles, Full randomizes drops in sniff locations"""
    displayname = "Sniffamizer"
    default = 1
    flags = ['s', '', 'S']


class Callbeadamizer(EvermizerFlags, OffOnFullChoice):
    """On Shuffles call bead characters, Full shuffles individual spells"""
    displayname = "Callbeadamizer"
    default = 1
    flags = ['c', '', 'C']


class Musicmizer(EvermizerFlag, Toggle):
    """Randomize music for some rooms"""
    displayname = "Musicmizer"
    flag = 'm'


class Doggomizer(EvermizerFlags, OffOnFullChoice):
    """On shuffles dog per act, Full randomizes dog per screen, Pupdunk gives you Everpupper everywhere"""
    displayname = "Doggomizer"
    option_pupdunk = 3
    default = 0
    flags = ['', 'd', 'D', 'p']


class TurdoMode(EvermizerFlag, Toggle):
    """Replace offensive spells by Turd Balls with varying strength and make weapons weak"""
    displayname = "Turdo Mode"
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
