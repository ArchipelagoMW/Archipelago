import typing
from Options import Choice, Range, OptionDict, Option, Toggle, DefaultOnToggle

class Preset(Choice):
    displayname = "Preset"
    option_newbie = 0
    option_casual = 1
    option_regular = 2
    option_veteran = 3
    option_expert = 4
    option_master = 5
    option_samus = 6
    option_Season_Races = 7
    option_SMRAT2021 = 8
    option_solution = 9
    option_custom = 10
    default = 2

class StartLocation(Choice):
    displayname = "Start Location"
    option_Ceres = 0
    option_Landing_Site = 1
    option_Gauntlet_Top = 2
    option_Green_Brinstar_Elevator = 3
    option_Big_Pink = 4
    option_Etecoons_Supers = 5
    option_Wrecked_Ship_Main = 6
    option_Firefleas_Top = 7
    option_Business_Center = 8
    option_Bubble_Mountain = 9
    option_Mama_Turtle = 10
    option_Watering_Hole = 11
    option_Aqueduct = 12
    option_Red_Brinstar_Elevator = 13
    option_Golden_Four = 14
    default = 1

class MaxDifficulty(Choice):
    displayname = "Maximum Difficulty"
    option_baby = 0
    option_easy = 1
    option_medium = 2
    option_hard = 3
    option_harder = 4
    option_very_hard = 5
    option_hardcore = 6
    option_mania = 7
    option_god = 8
    option_samus = 9
    option_impossibru = 10
    option_infinity = 11
    default = 6

class SuitsRestriction(DefaultOnToggle):
    displayname = "Suits Restriction"

class StrictMinors(Toggle):
    displayname = "Strict Minors"

class MissileQty(Range):
    displayname = "Missile Quantity"
    range_start = 1
    range_end = 9
    default = 3

class SuperQty(Range):
    displayname = "Super Quantity"
    range_start = 1
    range_end = 9
    default = 2

class PowerBombQty(Range):
    displayname = "Power Bomb Quantity"
    range_start = 1
    range_end = 9
    default = 1

class MinorQty(Range):
    displayname = "Minor Quantity"
    range_start = 7
    range_end = 100
    default = 100

class EnergyQty(Choice):
    displayname = "Energy Quantity"
    option_ultra_sparse = 0
    option_sparse = 1
    option_medium = 2
    option_vanilla = 3
    default = 3

class AreaRandomization(Toggle):
    displayname = "Area Randomization"

class LightAreaRandomization(Toggle):
    displayname = "Light Area Randomization"

class AreaLayout(Toggle):
    displayname = "Area Layout"

class DoorsColorsRando(Toggle):
    displayname = "Doors Colors Rando"

class AllowGreyDoors(Toggle):
    displayname = "Allow Grey Doors"

class BossRandomization(Toggle):
    displayname = "Boss Randomization"

class FunCombat(Toggle):
    displayname = "Fun Combat"

class FunMovement(Toggle):
    displayname = "Fun Movement"

class FunSuits(Toggle):
    displayname = "Fun Suits"

class LayoutPatches(DefaultOnToggle):
    displayname = "Layout Patches"

class VariaTweaks(Toggle):
    displayname = "Varia Tweaks"

class NerfedCharge(Toggle):
    displayname = "Nerfed Charge"

class GravityBehaviour(Choice):
    displayname = "Gravity Behaviour"
    option_Vanilla = 0
    option_Balanced = 1
    option_Progressive = 2
    default = 1

class ElevatorsDoorsSpeed(DefaultOnToggle):
    displayname = "Elevators doors speed"

class SpinJumpRestart(Toggle):
    displayname = "Spin Jump Restart"

class InfiniteSpaceJump(Toggle):
    displayname = "Infinite Space Jump"

class RefillBeforeSave(Toggle):
    displayname = "Refill Before Save"

class Hud(Toggle):
    displayname = "Hud"

class Animals(Toggle):
    displayname = "Animals"

class NoMusic(Toggle):
    displayname = "No Music"

class RandomMusic(Toggle):
    displayname = "Random Music"

class CustomPreset(OptionDict):
    displayname = "Custom Preset"
    default = { "knows": {}, "settings": {}, "controller": {} }


sm_options: typing.Dict[str, type(Option)] = {
    "preset": Preset,
    "startLocation": StartLocation,
    #"majorsSplit": "Full",
    #"scavNumLocs": "10",
    #"scavRandomized": "off",
    #"scavEscape": "off",
    "maxDifficulty": MaxDifficulty,
    #"progressionSpeed": "medium",
    #"progressionDifficulty": "normal",
    #"morphPlacement": "early",
    "suitsRestriction": SuitsRestriction,
    #"hideItems": "off",
    "strictMinors": StrictMinors,
    "missileQty": MissileQty,
    "superQty": SuperQty,
    "powerBombQty": PowerBombQty,
    "minorQty": MinorQty,
    "energyQty": EnergyQty,
    "areaRandomization": AreaRandomization,
    "lightAreaRandomization": LightAreaRandomization,
    "areaLayout": AreaLayout,
    "doorsColorsRando": DoorsColorsRando,
    "allowGreyDoors": AllowGreyDoors,
    "bossRandomization": BossRandomization,
    #"minimizer": "off",
    #"minimizerQty": "45",
    #"minimizerTourian": "off",
    #"escapeRando": "off",
    #"removeEscapeEnemies": "off",
    "funCombat": FunCombat,
    "funMovement": FunMovement,
    "funSuits": FunSuits,
    "layoutPatches": LayoutPatches,
    "variaTweaks": VariaTweaks,
    "nerfedCharge": NerfedCharge,
    "gravityBehaviour": GravityBehaviour,
    #"itemsounds": "on",
    "elevators_doors_speed": ElevatorsDoorsSpeed,
    "spinjumprestart": SpinJumpRestart,
    #"rando_speed": "off",
    "Infinite_Space_Jump": InfiniteSpaceJump,
    "refill_before_save": RefillBeforeSave,
    "hud": Hud,
    "animals": Animals,
    "No_Music": NoMusic,
    "random_music": RandomMusic,
    "customPreset": CustomPreset
    }
