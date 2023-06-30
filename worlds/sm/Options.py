import typing
from Options import Choice, Range, OptionDict, OptionList, OptionSet, Option, Toggle, DefaultOnToggle
from .variaRandomizer.utils.objectives import _goals

class StartItemsRemovesFromPool(Toggle):
    """Remove items in starting inventory from pool."""
    display_name = "StartItems Removes From Item Pool"

class Preset(Choice):
    """Choose one of the presets or specify "varia_custom" to use varia_custom_preset option or specify "custom" to use
    custom_preset option."""
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
    """Choose where you want to start the game."""
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

class RemoteItems(Toggle):
    """Indicates you get items sent from your own world. This allows coop play of a world."""
    display_name = "Remote Items"  

class MaxDifficulty(Choice):
    """Depending on the perceived difficulties of the techniques, bosses, hell runs etc. from the preset, it will
    prevent the Randomizer from placing an item in a location too difficult to reach with the current items."""
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
    """Influences where the Morphing Ball with be placed."""
    display_name = "Morph Placement"
    option_early = 0
    option_normal = 1
    default = 0

class StrictMinors(Toggle):
    """Instead of using the Minors proportions as probabilities, enforce a strict distribution to match the proportions
    as closely as possible."""
    display_name = "Strict Minors"

class MissileQty(Range):
    """The higher the number the higher the probability of choosing missles when placing a minor."""
    display_name = "Missile Quantity"
    range_start = 10
    range_end = 90
    default = 30

class SuperQty(Range):
    """The higher the number the higher the probability of choosing super missles when placing a minor."""
    display_name = "Super Quantity"
    range_start = 10
    range_end = 90
    default = 20

class PowerBombQty(Range):
    """The higher the number the higher the probability of choosing power bombs when placing a minor."""
    display_name = "Power Bomb Quantity"
    range_start = 10
    range_end = 90
    default = 10

class MinorQty(Range):
    """From 7%, minimum number of minors required to finish the game, to 100%."""
    display_name = "Minor Quantity"
    range_start = 7
    range_end = 100
    default = 100

class EnergyQty(Choice):
    """Choose how many Energy/Reserve Tanks will be available, from 0-1 in ultra sparse, 4-6 in sparse, 8-12 in medium
    and 18 in vanilla."""
    display_name = "Energy Quantity"
    option_ultra_sparse = 0
    option_sparse = 1
    option_medium = 2
    option_vanilla = 3
    default = 3

class AreaRandomization(Choice):
    """Randomize areas together using bidirectional access portals."""
    display_name = "Area Randomization"
    option_off = 0
    option_light = 1
    option_full = 2
    alias_true = 2
    default = 0

class AreaLayout(Toggle):
    """Some layout tweaks to make your life easier in areas randomizer."""
    display_name = "Area Layout"

class DoorsColorsRando(Toggle):
    """Randomize the color of Red/Green/Yellow doors. Add four new type of doors which require Ice/Wave/Spazer/Plasma
    beams to open them."""
    display_name = "Doors Colors Rando"

class AllowGreyDoors(Toggle):
    """When randomizing the color of Red/Green/Yellow doors, some doors can be randomized to Grey. Grey doors will never
    open, you will have to go around them."""
    display_name = "Allow Grey Doors"

class BossRandomization(Toggle):
    """Randomize Golden 4 bosses access doors using bidirectional access portals."""
    display_name = "Boss Randomization"

class FunCombat(Toggle):
    """Forces removal of Plasma Beam and Screw Attack if the preset and settings allow it. In addition, can randomly
    remove Spazer and Wave Beam from the Combat set. If used, might force 'minimal' accessibility."""
    display_name = "Fun Combat"

class FunMovement(Toggle):
    """Forces removal of Space Jump if the preset allows it. In addition, can randomly remove High Jump, Grappling Beam,
    Spring Ball, Speed Booster, and Bombs from the Movement set. If used, might force 'minimal' accessibility."""
    display_name = "Fun Movement"

class FunSuits(Toggle):
    """If the preset and seed layout allow it, will force removal of at least one of Varia Suit and/or Gravity Suit. If
    used, might force 'minimal' accessibility."""
    display_name = "Fun Suits"

class LayoutPatches(DefaultOnToggle):
    """Include the anti-softlock layout patches. Disable at your own softlocking risk!"""
    display_name = "Layout Patches"

class VariaTweaks(Toggle):
    """Include minor tweaks for the game to behave 'as it should' in a randomizer context"""
    display_name = "Varia Tweaks"

class NerfedCharge(Toggle):
    """Samus begins with a starter Charge Beam that does one third of charged shot damage that can damage bosses. Pseudo
    Screws also do one third damage. Special Beam Attacks do normal damage but cost 3 Power Bombs instead of 1. Once the
    Charge Beam item has been collected, it does full damage and special attacks are back to normal."""
    display_name = "Nerfed Charge"

class GravityBehaviour(Choice):
    """Modify the heat damage and enemy damage reduction qualities of the Gravity and Varia Suits."""
    display_name = "Gravity Behaviour"
    option_Vanilla = 0
    option_Balanced = 1
    option_Progressive = 2
    default = 1

class ElevatorsSpeed(DefaultOnToggle):
    """Accelerate elevators transitions."""
    display_name = "Elevators speed"

class DoorsSpeed(DefaultOnToggle):
    """Accelerate doors transitions."""
    display_name = "Doors speed"

class SpinJumpRestart(Toggle):
    """Allows Samus to start spinning in mid air after jumping or falling."""
    display_name = "Spin Jump Restart"

class SpeedKeep(Toggle):
    """Let Samus keeps her momentum when landing from a fall or from jumping."""
    display_name = "Momentum conservation (a.k.a. Speedkeep)"

class InfiniteSpaceJump(Toggle):
    """Space jumps can be done quicker and at any time in air, water or lava, even after falling long distances."""
    display_name = "Infinite Space Jump"

class RefillBeforeSave(Toggle):
    """Refill energy and ammo when saving."""
    display_name = "Refill Before Save"

class Hud(Toggle):
    """Displays the current area name and the number of remaining items of selected item split in the HUD for the
    current area."""
    display_name = "Hud"

class Animals(Toggle):
    """
    Replace saving the animals in the escape sequence by a random surprise.
    Note: This setting is not available when Escape Randomization is enabled, as it is replaced by Animals Challenges
    (see Escape Randomization help for more information).
    """
    display_name = "Animals"

class NoMusic(Toggle):
    """Disable the background music."""
    display_name = "No Music"

class RandomMusic(Toggle):
    """Randomize the background music."""
    display_name = "Random Music"

class CustomPreset(OptionDict):
    """
    see https://randommetroidsolver.pythonanywhere.com/presets for detailed info on each preset settings
    knows: each skill (know) has a pair [can use, perceived difficulty using one of 1, 5, 10, 25, 50 or 100 each one
           matching a max_difficulty]
    settings: hard rooms, hellruns and bosses settings
    controller: predefined controller mapping and moon walk setting
    """
    display_name = "Custom Preset"
    default = {  "knows": {},
                 "settings": {},
                 "controller": {}
              }

class VariaCustomPreset(OptionList):
    """use an entry from the preset list on https://randommetroidsolver.pythonanywhere.com/presets"""
    display_name = "Varia Custom Preset"  
    default = {}


class EscapeRando(Toggle):
    """
    When leaving Tourian, get teleported to the exit of a random Map station (between Brinstar/Maridia/Norfair/Wrecked Ship).
    You then have to find your way to the ship in the remaining time. Allotted time depends on area layout, but not on skill settings and is pretty generous.
    
    During the escape sequence:
    - All doors are opened
    - Maridia tube is opened
    - The Hyper Beam can destroy Bomb , Power Bomb  and Super Missile  blocks and open blue/green gates from both sides
    - All mini bosses are defeated
    - All minor enemies are removed to allow you to move faster and remove lag

    During regular game only Crateria Map station door can be opened and activating the station will act as if all map stations were activated at once.

    Animals Challenges:
    You can use the extra available time to:
    - find the animals that are hidden behind a (now blue) map station door
    - go to the vanilla animals door to cycle through the 4 available escapes, and complete as many escapes as you can

    Pick your challenge, or try to do both, but watch your timer!
    """
    display_name = "Randomize the escape sequence"

class RemoveEscapeEnemies(Toggle):
    """Remove enemies during escape sequence, disable it to blast through enemies with your Hyper Beam and cause lag."""
    display_name = "Remove enemies during escape"   

class Tourian(Choice):
    """
    Choose endgame Tourian behaviour:
    Vanilla: regular vanilla Tourian
    Fast: speed up Tourian to skip Metroids, Zebetites, and all cutscenes (including Mother Brain 3 fight). Golden Four statues are replaced by an invincible Gadora until all objectives are completed.
    Disabled: skip Tourian entirely, ie. escape sequence is triggered as soon as all objectives are completed.
    """
    display_name = "Endgame behavior with Tourian"
    option_Vanilla = 0
    option_Fast = 1
    option_Disabled = 2
    default = 0  

class CustomObjective(Toggle):
    """
    Use randomized custom objectives. You can choose which objectives are available for the randomizer to choose from. If enabled, the randomizer 
    will choose "Custom objective count" objectives from "Custom objective list". Otherwise, only objective is used. Default is disabled.
    """
    display_name = "Custom objectives"

class CustomObjectiveCount(Range):
    """
    By default you need to complete 4 objectives from the list to access Tourian. You can choose between 1 and 5. This setting is ignored if
    ""Custom objectives"" is set to false.
    """
    display_name = "Custom objective count"
    range_start = 1
    range_end = 5
    default = 4

class CustomObjectiveList(OptionSet):
    """
    If ""Custom objectives"" is enabled, "Custom Objective count" will be used to pick an amount of objective from the list.
    This setting is ignored if ""Custom objectives"" is set to false.
    Note: If you leave the list empty no objective is required to access Tourian, ie. it's open.
    Note: See the Tourian parameter to enable fast Tourian or trigger the escape when all objectives are completed.
    Note: Current percentage of collected items is displayed in the inventory pause menu.
    Note: Collect 100% items is excluded by default as it requires you to complete all the objectives.
    Note: In AP, Items% and areas objectives are counted toward location checks, not items collected or received, except for "collect all upgrades"
    
    Format as a comma-separated list of objective names: ["kill three G4", "collect 75% items"] or ["random"] to specify the whole list except
    "collect 100% items" and "nothing". The default is ["random"]. A full list of supported objectives can be found at:
    https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/sm/variaRandomizer/utils/objectives.py
    """
    display_name = "Custom objective list"
    default = ["random"]
    valid_keys = frozenset([name for name in _goals.keys()] + ["random"])
    #valid_keys_casefold = True

class Objective(OptionSet):
    """
    If ""Custom objectives"" is disabled, choose which objectives are required to sink the Golden Four statue and to open access to Tourian.
    You can choose from 0 to 5 objectives. Up to the first 5 objectives from the list will be selected.
    Note: If you leave the list empty no objective is required to access Tourian, ie. it's open.
    Note: See the Tourian parameter to enable fast Tourian or trigger the escape when all objectives are completed.
    Note: Current percentage of collected items is displayed in the inventory pause menu.
    Note: In AP, Items% and areas objectives are counted toward location checks, not items collected or received, except for "collect all upgrades"
    
    Format as a comma-separated list of objective names: ["kill three G4", "collect 75% items"]. The default is ["kill all G4"].
    A full list of supported objectives can be found at:
    https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/sm/variaRandomizer/utils/objectives.py
    """
    display_name = "Objectives"
    default = ["kill all G4"]
    valid_keys = frozenset({name: goal for (name, goal) in _goals.items()})
    #valid_keys_casefold = True

class HideItems(Toggle):
    """
    Hides half of the visible items.
    Items always visible:
    - Energy Tank, Gauntlet
    - Energy Tank, Terminator
    - Morphing Ball
    - Missile (Crateria moat)
    - Missile (green Brinstar below super missile)
    - Missile (above Crocomire)
    - Power Bomb (lower Norfair above fire flea room)
    - Missile (Gravity Suit)
    - Missile (green Maridia shinespark)
    """
    display_name = "Hide half the items"

class RelaxedRoundRobinCF(Toggle):
    """
    Changes Crystal Flashes behavior and requirements as follows:

    You can perform a Crystal Flash with any amount of ammo, but you need at least one Power Bomb to begin the process.
    After consuming 1 ammo, Samus gains 50 energy, and it will try a different ammo type next,  
    cycling through Missiles, Supers, and Power Bombs as available. The cycling is to keep the consumption even between ammo types.
    If one of your ammo types is at 0, it will be skipped.
    The Crystal Flash ends when Samus is out of ammo or a total of 30 ammo has been consumed.
    """
    display_name = "Relaxed round robin Crystal Flash"

sm_options: typing.Dict[str, type(Option)] = {
    "start_inventory_removes_from_pool": StartItemsRemovesFromPool,
    "preset": Preset,
    "start_location": StartLocation,
    "remote_items": RemoteItems,
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
    "hide_items": HideItems,
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
    "escape_rando": EscapeRando,
    "remove_escape_enemies": RemoveEscapeEnemies,
    "fun_combat": FunCombat,
    "fun_movement": FunMovement,
    "fun_suits": FunSuits,
    "layout_patches": LayoutPatches,
    "varia_tweaks": VariaTweaks,
    "nerfed_charge": NerfedCharge,
    "gravity_behaviour": GravityBehaviour,
    #"item_sounds": "on",
    "elevators_speed": ElevatorsSpeed,
    "fast_doors": DoorsSpeed,
    "spin_jump_restart": SpinJumpRestart,
    "rando_speed": SpeedKeep,
    "infinite_space_jump": InfiniteSpaceJump,
    "refill_before_save": RefillBeforeSave,
    "hud": Hud,
    "animals": Animals,
    "no_music": NoMusic,
    "random_music": RandomMusic,
    "custom_preset": CustomPreset,
    "varia_custom_preset": VariaCustomPreset,
    "tourian": Tourian,
    "custom_objective": CustomObjective,
    "custom_objective_list": CustomObjectiveList,
    "custom_objective_count": CustomObjectiveCount,
    "objective": Objective,
    "relaxed_round_robin_cf": RelaxedRoundRobinCF,
    }
