import json
import typing
from Options import Choice, OptionSet, PerGameCommonOptions, Range, OptionDict, OptionList, Option, StartInventoryPool, Toggle, DefaultOnToggle
from dataclasses import dataclass
from . import map_rando_app_data

from schema import Schema

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

class CommonMap(Toggle):
    """
    If On, the common multiworld seed will be used to choose the map. This overrides the "random_seed" of "other_settings" from "map_rando_options".
    All Map Rando worlds having this On will use the same map.
    """
    display_name = "Common Map"

class CommonDoorColors(Toggle):
    """
    If On, the common multiworld seed will be used to choose the doors randomization. This overrides the "random_seed" of "other_settings" from "map_rando_options".
    All Map Rando worlds having this On will use the same map This setting is ignored if "common_map" is Off.
    """
    display_name = "Common Door Colors"

class EtankColorRed(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank red intensity"
    range_start = 0
    range_end = 255
    default = 222

class EtankColorGreen(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank green intensity"
    range_start = 0
    range_end = 255
    default = 56

class EtankColorBlue(Range):
    """
    Use this to make Energy Tanks appear with a different color in the HUD.

    This option has minor side effects on the colors of certain items.
    """
    display_name = "Etank blue intensity"
    range_start = 0
    range_end = 255
    default = 148

class ItemDotChange(Choice):
    """
    This option affects what happens to item dots on the map after item collection:
    - Fade: Item dots fade to a darker color but remain visible.
    - Disappear: Item dots disappear entirely.
    """ 
    display_name = "Item dot change"
    option_Fade = 0
    option_Disappear = 1
    default = 0

class TransitionLetters(Choice):
    """
    This option affects how transitions between areas are marked on the map:
    - Arrows: An arrow is used, showing the direction of the transition.
    - Letters: A letter is used, the first letter of the name of the neighboring area.
    """ 
    option_Arrows = 0
    option_Letters = 1
    display_name = "Transition letters"
    default = 1

class RoomTheme(Choice):
    """
    This setting controls the palettes for rooms (affecting foregrounds and backgrounds):
    - Vanilla: Rooms use the palette from the original game.
    - AreaPalettes: Rooms use a palette based on the area in which they appear in the randomized map. This adds variety and can help the 
                    randomized areas to feel more coherent.
    - AreaTiling: Rooms graphics are redrawn to follow a consistent theme for each area. This provides the highest level of variety
                    and cohesiveness in room appearance.
    """ 
    display_name = "Room theming"
    option_Vanilla = 0
    option_AreaPalettes = 1
    option_AreaTiling = 2
    default = 0

class DoorColors(Choice):
    """
    This setting controls the color of ammo doors, the ones unlocked by Missiles, Supers, and Power Bombs.

    - Vanilla: Doors have the colors that they do in the vanilla game.
    - Alternate: Different door colors are used, which may be easier to distinguish for color-blind players. This is based on a color scheme by Vibrant Colors.
    """ 
    display_name = "Door colors"
    option_Vanilla = 0
    option_Alternate = 1
    default = 0

class Music(Choice):
    """
    This setting can be used to disable game music, while still playing sound effects. The same music tracks will load (though not play), 
    in order to keep room load timings consistent.

    MSU-1 support is built into the randomizer; on applicable platforms this can be used to customize the music, still with no effect on room load timings.
    """ 
    display_name = "Door colors"
    option_Area = 0
    option_Disabled = 1
    default = 0

class ScreenShaking(Choice):
    """
    This setting affects the graphical appearance of screen shaking, e.g., during the escape sequence, bosses, and in rooms where lava or acid rises.
    - Vanilla: Screen shaking happens as in the vanilla game (which has up to 3-pixel displacements).
    - Reduced: Screen shaking is capped to 1-pixel displacements.
    - Disabled: Screen shaking is disabled.
    """ 
    display_name = "Screen shaking"
    option_Vanilla = 0
    option_Reduced = 1
    option_Disabled = 2
    default = 0

class ScreenFlashing(Choice):
    """
    This setting affects the graphical appearance of screen flashing, including lightning, escape sequence effects, boss damage, and the initial flash
    of Power Bomb explosions.
    - Vanilla: Screen flashing happens as in the vanilla game.
    - Reduced: Most large, sudden flashes are reduced to have a milder change in brightness, while still being noticeable. Caution is recommended for 
                those with serious sensitivities to such effects, as the effectiveness of these changes is not guaranteed and may vary by individual.

    The full-screen flashing after Mother Brain phase 1 is an exception, being always removed regardless of which option is selected.   
    """ 
    display_name = "Screen shaking"
    option_Vanilla = 0
    option_Reduced = 1
    default = 1

class DisableBeeping(Choice):
    """
    This setting affects the low-energy beeping which alerts the player when Samus is at 30 energy or less.
    - Vanilla: The low-energy beeping behaves as in the vanilla game.
    - Disabled: The low-energy beeping is disabled.
    """ 
    display_name = "Low-energy beeping"
    option_Vanilla = 0
    option_Disabled = 1
    default = 0

class RoomPalettes(Choice):
    """
    This setting controls the palettes for rooms (affecting foregrounds and backgrounds):
    - Vanilla: Rooms use the palette from the original game.
    - Area_Themed: Rooms use a palette based on the area in which they appear in the randomized map. This adds variety and can help the 
                    randomized areas to feel more coherent.
    """ 
    display_name = "Room palettes"
    option_Vanilla = 0
    option_Area_Themed = 1
    default = 0

class TileTheme(Choice):
    """
    This setting controls how the rooms in the game will be drawn. This affects only the graphical appearance of the rooms.
    - If None is selected, then rooms are tiled as they are in the vanilla game.
    - If Area_Themed is selceted, then rooms are tiled according to their area on the map.
    - If Scrambled is selected, then each room is tiled using a random theme.
    - If an individual theme is selected (e.g. Outer Crateria), then all the rooms are tiled using that theme.
    - If Practice Outlines is selected, then rooms are tiled using green outlines to mark the room collision; special blocks are shown in their true form; 
        and a background grid helps with measuring positions and distances.
    - If Invisible is selected, then rooms are tiled using blank, transparent foreground, making the game difficult to navigate. 
        Doors will still be visible, as will vanilla backgrounds and sprites.
    """ 
    display_name = "Tile theme"
    option_None = 0
    option_Area_Themed = 1
    option_Scrambled = 2
    option_Outer_Crateria = 3
    option_Inner_Crateria = 4
    option_Blue_Brinstar = 5
    option_Green_Brinstar = 6
    option_Pink_Brinstar = 7
    option_Red_Brinstar = 8
    option_Upper_Norfair = 9
    option_Lower_Norfair = 10
    option_Wrecked_Ship = 11
    option_West_Maridia = 12
    option_Yellow_Maridia = 13
    option_Mecha_Tourian = 14
    option_Metroid_Habitat = 15
    option_Outline = 16
    option_Invisible = 17
    default = 0

class ReserveHudStyle(Choice):
    """
    The setting affects how reserve tanks are displayed on the HUD.
    - Vanilla: A reserve tank indicator is shown on the HUD only if reserve mode is AUTO, and its color indicates whether reserves have any energy or not.
    - Revamped: Each reserve tank is indicated with a bar showing how full it is. If reserve mode is AUTO, then the AUTO text also appears, 
                and its color indicates whether reserves have any energy or not.
    """
    display_name = "Reserve tank HUD style"
    option_Vanilla = 0
    option_Revamped = 1
    default = 0

class ScrewAttackAnimation(Choice):
    """
    This setting determines how the Screw Attack animation appears:
    - Vanilla: The Screw Attack animation is always based on the Space Jump animation regardless of whether or not Space Jump is equipped.
    - Split: Screw Attack without Space Jump equipped is based on the spin-jump animation. Screw Attack with Space Jump equipped is based 
            on the Space Jump animation.
    """ 
    display_name = "Screw Attack animation"
    option_Vanilla = 0
    option_Split = 1
    default = 0

class RoomNames(DefaultOnToggle):
    """
    If enabled, then the name of the current room is shown at the bottom of the pause menu map screen.
    """ 
    display_name = "Room names"

class ControllerButton(Choice):
    #option_Default = 0
    #option_Left = 1
    #option_Right = 2
    #option_Up = 3
    #option_Down = 4
    option_X = 5
    option_Y = 6
    option_A = 7
    option_B = 8
    option_L = 9
    option_R = 10
    option_Select = 11
    option_Start = 12

    free_controller_button_per_player = {}
    current_player_id = 0

    def verify(self, world, player_name: str, plando_options) -> None:
        # player_name isnt resolved yet here so this is required to handle having many times the same player name with {number}
        player_name_id = player_name + f"{ControllerButton.current_player_id / 8}"
        if (player_name_id not in ControllerButton.free_controller_button_per_player.keys()):
            ControllerButton.free_controller_button_per_player[player_name_id] = [
                                                                                ControllerButton.option_X,
                                                                                ControllerButton.option_Y,
                                                                                ControllerButton.option_A,
                                                                                ControllerButton.option_B,
                                                                                ControllerButton.option_L,
                                                                                ControllerButton.option_R,
                                                                                ControllerButton.option_Select,
                                                                                ControllerButton.option_Start
                                                                            ]
        if self.value in ControllerButton.free_controller_button_per_player[player_name_id]:
            ControllerButton.free_controller_button_per_player[player_name_id].remove(self.value)
            ControllerButton.current_player_id += 1
            return
        raise Exception(f"Controller button '{self.value}' is already used. Possible buttons are: \
                        {ControllerButton.free_controller_button_per_player[player_name_id]}")

class Shot(ControllerButton):
    """
    Shot button
    """
    display_name = "Shot button"
    default = 5

class Jump(ControllerButton):
    """
    Jump button
    """
    display_name = "Jump button"
    default = 7

class Dash(ControllerButton):
    """
    Dash button
    """
    display_name = "Dash button"
    default = 8

class ItemSelect(ControllerButton):
    """
    ItemSelect button
    """
    display_name = "ItemSelect button"
    default = 11

class ItemCancel(ControllerButton):
    """
    ItemCancel button
    """
    display_name = "ItemCancel button"
    default = 6

class AngleUp(ControllerButton):
    """
    AngleUp button
    """
    display_name = "AngleUp button"
    default = 10

class AngleDown(ControllerButton):
    """
    AngleDown button
    """
    display_name = "AngleDown button"
    default = 9

class QuickReloadButtons(OptionSet):
    """
    Press the combination simultaneously to quick reload from the last save. Repeat to cycle through previous saves.
    """
    display_name = "QuickReload button combination"
    default = {"L", "R", "Select", "Start"}
    valid_keys = {"X", "Y", "A", "B", "L", "R", "Select", "Start", "Up", "Down", "Left", "Right"}

class SpinLockButtons(OptionSet):
    """
    Press the combination simultaneously to activate Spin Lock, temporarily preventing up/down inputs from breaking spin. Pressing shot will cancel this mode.
    """
    display_name = "SpinLock button combination"
    default = {"L", "R", "Up", "X"}
    valid_keys = {"X", "Y", "A", "B", "L", "R", "Select", "Start", "Up", "Down", "Left", "Right"}

class Moonwalk(Toggle):
    """
    Moonwalk
    """
    display_name = "Moonwalk"
    default = 0  

class MapRandoOptions(OptionDict):
    """
    Map Rando Settings as defined by maprando.com.
    If you dont need to change deeper settings, you can either:
     - use the lighter minimal version (see the default)
     - add a "name" field at the topmost level, beside "version", and name it as one of the existing Map Rando builtin complete Settings Preset (ie, "Community Race Season 3 (Save the animals)")
    Otherwise, you can use your preferred Map Rando Settings Presets on maprando.com, export its JSON and directly embed it under here like so:

    map_rando_options: {
      "version": 119,
      "name": my_custom_preset,
        ...
    }
    
    In all cases, using one of the existing "preset" name (ie, "Basic") of a settings category (ie, "skill_assumption_settings") will make the
    randomizer ignore all its children settings and use corresponding existing preset from Map Rando.

    If "random_seed" is null, the seed from this world will be used instead of a random one to keep determinism in AP.
    """
    display_name = "Map Rando Options"
    value: dict[str, dict[str, typing.Any]]
    default =   {
                    "version": 119,
                    "skill_assumption_settings": {
                        "preset": "Basic"
                    },
                    "item_progression_settings": {
                        "preset": "Normal"
                    },
                    "quality_of_life_settings": {
                        "preset": "Default"
                    },
                    "objective_settings": {
                        "preset": "Bosses"
                    },
                    "map_layout": "Standard",
                    "doors_mode": "Ammo",
                    "start_location_settings": {
                        "mode": "Ship"
                    },
                    "save_animals": "No",
                    "other_settings": {
                        "wall_jump": "Vanilla",
                        "etank_refill": "Vanilla",
                        "area_assignment": "Standard",
                        "door_locks_size": "Large",
                        "maps_revealed": "No",
                        "map_station_reveal": "Full",
                        "energy_free_shinesparks": False,
                        "ultra_low_qol": False,
                        "race_mode": False,
                        "random_seed": None
                    }
                }
    
    def verify(self, world, player_name: str, plando_options) -> None:
        if not world.validate_settings(json.dumps(self.value)):
            raise Exception("MapRandoOptions failed to validate.")

@dataclass
class SMMROptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    remote_items: RemoteItems
    death_link: DeathLink
    common_map: CommonMap
    common_door_colors: CommonDoorColors
    etank_color_red: EtankColorRed
    etank_color_green: EtankColorGreen
    etank_color_blue: EtankColorBlue
    item_dot_change: ItemDotChange
    transition_letters: TransitionLetters
    room_theme: RoomTheme
    door_colors: DoorColors
    music: Music
    screen_shaking: ScreenShaking
    screen_flashing: ScreenFlashing
    disable_beeping: DisableBeeping
    room_palettes: RoomPalettes
    tile_theme: TileTheme
    reserve_hud_style: ReserveHudStyle
    screw_attack_animation: ScrewAttackAnimation
    room_names: RoomNames
    shot: Shot
    jump: Jump
    dash: Dash
    item_select: ItemSelect
    item_cancel: ItemCancel
    angle_up: AngleUp
    angle_down: AngleDown
    spin_lock_buttons: SpinLockButtons
    quick_reload_buttons: QuickReloadButtons
    moonwalk: Moonwalk
    map_rando_options: MapRandoOptions