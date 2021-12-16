from enum import Enum
from typing import Dict, List

class GameMode(Enum):
        Normal = 0
        Multiworld = 1

class Z3Logic(Enum):
        Normal = 0
        Nmg = 1
        Owg = 2

class SMLogic(Enum):
        Normal = 0
        Hard = 1

class SwordLocation(Enum):
        Randomized = 0
        Early = 1
        Uncle = 2   

class MorphLocation(Enum):
        Randomized = 0
        Early = 1
        Original = 2

class Goal(Enum):
        DefeatBoth = 0

class KeyShuffle(Enum):
        Null = 0
        Keysanity = 1

class GanonInvincible(Enum):
        Never = 0
        BeforeCrystals = 1
        BeforeAllDungeons = 2
        Always = 3

class Config:
    GameMode: GameMode = GameMode.Normal
    Z3Logic: Z3Logic = Z3Logic.Normal
    SMLogic: SMLogic = SMLogic.Normal
    SwordLocation: SwordLocation= SwordLocation.Randomized
    MorphLocation: MorphLocation = MorphLocation.Randomized
    Goal: Goal = Goal.DefeatBoth
    KeyShuffle: KeyShuffle = KeyShuffle.Null
    Keysanity: bool = KeyShuffle != KeyShuffle.Null
    Race: bool = False
    GanonInvincible: GanonInvincible = GanonInvincible.BeforeCrystals

    def __init__(self, options: Dict[str, str]):
        self.GameMode = self.ParseOption(options, self.GameMode.Normal)
        self.Z3Logic = self.ParseOption(options, self.Z3Logic.Normal)
        self.SMLogic = self.ParseOption(options, self.SMLogic.Normal)
        self.SwordLocation = self.ParseOption(options, self.SwordLocation.Randomized)
        self.MorphLocation = self.ParseOption(options, self.MorphLocation.Randomized)
        self.Goal = self.ParseOption(options, self.Goal.DefeatBoth)
        self.GanonInvincible = self.ParseOption(options, self.GanonInvincible.BeforeCrystals)
        self.KeyShuffle = self.ParseOption(options, self.KeyShuffle.Null)
        self.Race = self.ParseOption(options, "Race", False)

    def ParseOption(options:Dict[str, str], defaultValue:Enum):
        enumKey = defaultValue.__class__.__name__.lower()
        if (enumKey in options):
            return defaultValue.__class__[options[enumKey]]
        return defaultValue

    def ParseOption(options:Dict[str, str], option:str, defaultValue:bool):
        if (option.lower() in options):
            return options[option.lower()]
        return defaultValue

    """ public static RandomizerOption GetRandomizerOption<T>(string description, string defaultOption = "") where T : Enum {
        var enumType = typeof(T);
        var values = Enum.GetValues(enumType).Cast<Enum>();

        return new RandomizerOption {
            Key = enumType.Name.ToLower(),
            Description = description,
            Type = RandomizerOptionType.Dropdown,
            Default = string.IsNullOrEmpty(defaultOption) ? GetDefaultValue<T>().ToLString() : defaultOption,
            Values = values.ToDictionary(k => k.ToLString(), v => v.GetDescription())
        };
    }

    public static RandomizerOption GetRandomizerOption(string name, string description, bool defaultOption = false) {
        return new RandomizerOption {
            Key = name.ToLower(),
            Description = description,
            Type = RandomizerOptionType.Checkbox,
            Default = defaultOption.ToString().ToLower(),
            Values = new Dictionary<string, string>()
        };
    }

    public static TEnum GetDefaultValue<TEnum>() where TEnum : Enum {
        Type t = typeof(TEnum);
        var attributes = (DefaultValueAttribute[])t.GetCustomAttributes(typeof(DefaultValueAttribute), false);
        if ((attributes?.Length ?? 0) > 0) {
            return (TEnum)attributes.First().Value;
        }
        else {
            return default;
        }
    } """
