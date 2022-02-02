import typing
from Options import Choice, Range, OptionDict, OptionList, Option, Toggle, DefaultOnToggle

class StartItemsRemovesFromPool(Toggle):
    display_name = "StartItems Removes From Item Pool"

class Preset(Choice):
    """choose one of the preset or specify "varia_custom" to use varia_custom_preset option or specify "custom" to use custom_preset option"""
    display_name = "Preset"
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
    option_varia_custom = 11
    default = 2

class StartLocation(Choice):
    display_name = "Start Location"
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

class DeathLink(Choice):
    """When DeathLink is enabled and someone dies, you will die. With survive reserve tanks can save you."""
    display_name = "Death Link"
    option_disable = 0
    option_enable = 1
    option_enable_survive = 3
    alias_false = 0
    alias_true = 1
    default = 0

class MaxDifficulty(Choice):
    display_name = "Maximum Difficulty"
    option_easy = 0
    option_medium = 1
    option_hard = 2
    option_harder = 3
    option_hardcore = 4
    option_mania = 5
    option_infinity = 6
    default = 4

class MorphPlacement(Choice):
    display_name = "Morph Placement"
    option_early = 0
    option_normal = 1
    default = 0

class StrictMinors(Toggle):
    display_name = "Strict Minors"

class MissileQty(Range):
    display_name = "Missile Quantity"
    range_start = 10
    range_end = 90
    default = 30

class SuperQty(Range):
    display_name = "Super Quantity"
    range_start = 10
    range_end = 90
    default = 20

class PowerBombQty(Range):
    display_name = "Power Bomb Quantity"
    range_start = 10
    range_end = 90
    default = 10

class MinorQty(Range):
    display_name = "Minor Quantity"
    range_start = 7
    range_end = 100
    default = 100

class EnergyQty(Choice):
    display_name = "Energy Quantity"
    option_ultra_sparse = 0
    option_sparse = 1
    option_medium = 2
    option_vanilla = 3
    default = 3

class AreaRandomization(Choice):
    display_name = "Area Randomization"
    option_off = 0
    option_light = 1
    option_on = 2
    alias_false = 0
    alias_true = 2
    default = 0

class AreaLayout(Toggle):
    display_name = "Area Layout"

class DoorsColorsRando(Toggle):
    display_name = "Doors Colors Rando"

class AllowGreyDoors(Toggle):
    display_name = "Allow Grey Doors"

class BossRandomization(Toggle):
    display_name = "Boss Randomization"

class FunCombat(Toggle):
    """if used, might force 'items' accessibility"""
    display_name = "Fun Combat"

class FunMovement(Toggle):
    """if used, might force 'items' accessibility"""
    display_name = "Fun Movement"

class FunSuits(Toggle):
    """if used, might force 'items' accessibility"""
    display_name = "Fun Suits"

class LayoutPatches(DefaultOnToggle):
    display_name = "Layout Patches"

class VariaTweaks(Toggle):
    display_name = "Varia Tweaks"

class NerfedCharge(Toggle):
    display_name = "Nerfed Charge"

class GravityBehaviour(Choice):
    display_name = "Gravity Behaviour"
    option_Vanilla = 0
    option_Balanced = 1
    option_Progressive = 2
    default = 1

class ElevatorsDoorsSpeed(DefaultOnToggle):
    display_name = "Elevators doors speed"

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
    """
    see https://randommetroidsolver.pythonanywhere.com/presets for detailed info on each preset settings
    knows: each skill (know) has a pair [can use, perceived difficulty using one of 1, 5, 10, 25, 50 or 100 each one matching a max_difficulty]
    settings: hard rooms, hellruns and bosses settings
    controller: predefined controller mapping and moon walk setting
    """
    displayname = "Custom Preset"
    default = {  "knows": {},
                 "settings": {},
                 "controller": {}
              }

class VariaCustomPreset(OptionList):
    """use an entry from the preset list on https://randommetroidsolver.pythonanywhere.com/presets"""
    displayname = "Varia Custom Preset"  
    default = {}


sm_options: typing.Dict[str, type(Option)] = {
    "start_inventory_removes_from_pool": StartItemsRemovesFromPool,
    "preset": Preset,
    "start_location": StartLocation,
    "death_link": DeathLink,
    #"majors_split": "Full",
    #"scav_num_locs": "10",
    #"scav_randomized": "off",
    #"scav_escape": "off",
    "max_difficulty": MaxDifficulty,
    #"progression_speed": "medium",
    #"progression_difficulty": "normal",
    "morph_placement": MorphPlacement,
    #"suits_restriction": SuitsRestriction,
    #"hide_items": "off",
    "strict_minors": StrictMinors,
    "missile_qty": MissileQty,
    "super_qty": SuperQty,
    "power_bomb_qty": PowerBombQty,
    "minor_qty": MinorQty,
    "energy_qty": EnergyQty,
    "area_randomization": AreaRandomization,
    "area_layout": AreaLayout,
    "doors_colors_rando": DoorsColorsRando,
    "allow_grey_doors": AllowGreyDoors,
    "boss_randomization": BossRandomization,
    #"minimizer": "off",
    #"minimizer_qty": "45",
    #"minimizer_tourian": "off",
    #"escape_rando": "off",
    #"remove_escape_enemies": "off",
    "fun_combat": FunCombat,
    "fun_movement": FunMovement,
    "fun_suits": FunSuits,
    "layout_patches": LayoutPatches,
    "varia_tweaks": VariaTweaks,
    "nerfed_charge": NerfedCharge,
    "gravity_behaviour": GravityBehaviour,
    #"item_sounds": "on",
    "elevators_doors_speed": ElevatorsDoorsSpeed,
    "spin_jump_restart": SpinJumpRestart,
    #"rando_speed": "off",
    "infinite_space_jump": InfiniteSpaceJump,
    "refill_before_save": RefillBeforeSave,
    "hud": Hud,
    "animals": Animals,
    "no_music": NoMusic,
    "random_music": RandomMusic,
    "custom_preset": CustomPreset,
    "varia_custom_preset": VariaCustomPreset
    }
