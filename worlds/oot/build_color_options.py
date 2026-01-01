# Quick script to build top-level color and sfx options for pickling

from Colors import *
import Sounds as sfx


def assemble_color_option(f, internal_name: str, func, display_name: str, default_option: str, outer=False):
    color_options = func()
    if outer:
        color_options.append("Match Inner")
    format_color = lambda color: color.replace(' ', '_').lower()
    color_to_id = {format_color(color): index for index, color in enumerate(color_options)}

    docstring = 'Choose a color. "random_choice" selects a random option. "completely_random" generates a random hex code.'
    if outer:
        docstring += ' "match_inner" copies the inner color for this option.'

    f.write(f"class {internal_name}(Choice):\n")
    f.write(f"    \"\"\"{docstring}\"\"\"\n")
    f.write(f"    display_name = \"{display_name}\"\n")
    for color, id in color_to_id.items():
        f.write(f"    option_{color} = {id}\n")
    f.write(f"    default = {color_options.index(default_option)}")
    f.write(f"\n\n\n")


def assemble_sfx_option(f, internal_name: str, sound_hook: sfx.SoundHooks, display_name: str):
    options = sfx.get_setting_choices(sound_hook).keys()
    sfx_to_id = {sound.replace('-', '_'): index for index, sound in enumerate(options)}
    docstring = 'Choose a sound effect. "random_choice" selects a random option. "random_ear_safe" selects a random safe option. "completely_random" selects any random sound.'

    f.write(f"class {internal_name}(Choice):\n")
    f.write(f"    \"\"\"{docstring}\"\"\"\n")
    f.write(f"    display_name = \"{display_name}\"\n")
    for sound, id in sfx_to_id.items():
        f.write(f"    option_{sound} = {id}\n")
    f.write(f"\n\n\n")


with open('ColorSFXOptions.py', 'w') as f:

    f.write("# Auto-generated color and sound-effect options from Colors.py and Sounds.py \n")
    f.write("from Options import Choice\n\n\n")

    assemble_color_option(f, "kokiri_color", get_tunic_color_options, "Kokiri Tunic", "Kokiri Green")
    assemble_color_option(f, "goron_color", get_tunic_color_options, "Goron Tunic", "Goron Red")
    assemble_color_option(f, "zora_color", get_tunic_color_options, "Zora Tunic", "Zora Blue")
    assemble_color_option(f, "silver_gauntlets_color", get_gauntlet_color_options, "Silver Gauntlets Color", "Silver")
    assemble_color_option(f, "golden_gauntlets_color", get_gauntlet_color_options, "Golden Gauntlets Color", "Gold")
    assemble_color_option(f, "mirror_shield_frame_color", get_shield_frame_color_options, "Mirror Shield Frame Color", "Red")
    assemble_color_option(f, "navi_color_default_inner", get_navi_color_options, "Navi Idle Inner", "White")
    assemble_color_option(f, "navi_color_default_outer", get_navi_color_options, "Navi Idle Outer", "Match Inner", outer=True)
    assemble_color_option(f, "navi_color_enemy_inner", get_navi_color_options, "Navi Targeting Enemy Inner", "Yellow")
    assemble_color_option(f, "navi_color_enemy_outer", get_navi_color_options, "Navi Targeting Enemy Outer", "Match Inner", outer=True)
    assemble_color_option(f, "navi_color_npc_inner", get_navi_color_options, "Navi Targeting NPC Inner", "Light Blue")
    assemble_color_option(f, "navi_color_npc_outer", get_navi_color_options, "Navi Targeting NPC Outer", "Match Inner", outer=True)
    assemble_color_option(f, "navi_color_prop_inner", get_navi_color_options, "Navi Targeting Prop Inner", "Green")
    assemble_color_option(f, "navi_color_prop_outer", get_navi_color_options, "Navi Targeting Prop Outer", "Match Inner", outer=True)
    assemble_color_option(f, "sword_trail_color_inner", get_sword_trail_color_options, "Sword Trail Inner", "White")
    assemble_color_option(f, "sword_trail_color_outer", get_sword_trail_color_options, "Sword Trail Outer", "Match Inner", outer=True)
    assemble_color_option(f, "bombchu_trail_color_inner", get_bombchu_trail_color_options, "Bombchu Trail Inner", "Red")
    assemble_color_option(f, "bombchu_trail_color_outer", get_bombchu_trail_color_options, "Bombchu Trail Outer", "Match Inner", outer=True)
    assemble_color_option(f, "boomerang_trail_color_inner", get_boomerang_trail_color_options, "Boomerang Trail Inner", "Yellow")
    assemble_color_option(f, "boomerang_trail_color_outer", get_boomerang_trail_color_options, "Boomerang Trail Outer", "Match Inner", outer=True)
    assemble_color_option(f, "heart_color", get_heart_color_options, "Heart Color", "Red")
    assemble_color_option(f, "magic_color", get_magic_color_options, "Magic Color", "Green")
    assemble_color_option(f, "a_button_color", get_a_button_color_options, "A Button Color", "N64 Blue")
    assemble_color_option(f, "b_button_color", get_b_button_color_options, "B Button Color", "N64 Green")
    assemble_color_option(f, "c_button_color", get_c_button_color_options, "C Button Color", "Yellow")
    assemble_color_option(f, "start_button_color", get_start_button_color_options, "Start Button Color", "N64 Red")

    assemble_sfx_option(f, "sfx_navi_overworld", sfx.SoundHooks.NAVI_OVERWORLD, "Navi Overworld")
    assemble_sfx_option(f, "sfx_navi_enemy", sfx.SoundHooks.NAVI_ENEMY, "Navi Enemy")
    assemble_sfx_option(f, "sfx_low_hp", sfx.SoundHooks.HP_LOW, "Low HP")
    assemble_sfx_option(f, "sfx_menu_cursor", sfx.SoundHooks.MENU_CURSOR, "Menu Cursor")
    assemble_sfx_option(f, "sfx_menu_select", sfx.SoundHooks.MENU_SELECT, "Menu Select")
    assemble_sfx_option(f, "sfx_nightfall", sfx.SoundHooks.NIGHTFALL, "Nightfall")
    assemble_sfx_option(f, "sfx_horse_neigh", sfx.SoundHooks.HORSE_NEIGH, "Horse")
    assemble_sfx_option(f, "sfx_hover_boots", sfx.SoundHooks.BOOTS_HOVER, "Hover Boots")

print('all done')
