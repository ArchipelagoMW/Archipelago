"""Apply Patch data to the ROM."""

import asyncio
import base64
import io
import json
import random
import zipfile
import time
import string
from datetime import datetime as Datetime
from datetime import timezone
import js
from randomizer.Enums.Models import Model, ModelNames, HeadResizeImmune
from randomizer.Enums.Settings import RandomModels, BigHeadMode
from randomizer.Lists.Songs import ExcludedSongsSelector
from randomizer.Patching.Cosmetics.TextRando import writeCrownNames
from randomizer.Patching.Cosmetics.Holiday import applyHolidayMode
from randomizer.Patching.Cosmetics.EnemyColors import writeMiscCosmeticChanges
from randomizer.Patching.CosmeticColors import (
    apply_cosmetic_colors,
    overwrite_object_colors,
    darkenDPad,
    darkenPauseBubble,
)
from randomizer.Patching.Hash import get_hash_images
from randomizer.Patching.MusicRando import randomize_music
from randomizer.Patching.Patcher import ROM
from randomizer.Patching.Library.Generic import recalculatePointerJSON, camelCaseToWords, getHoliday, Holidays
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, writeText
from randomizer.Patching.ASMPatcher import patchAssemblyCosmetic, disableDynamicReverb, fixLankyIncompatibility

# from randomizer.Spoiler import Spoiler
from randomizer.Settings import Settings, ExcludedSongs, DPadDisplays, KongModels
from ui.progress_bar import ProgressBar

from version import version as rando_version


class BooleanProperties:
    """Class to store data relating to boolean properties."""

    def __init__(self, check, offset, target=1):
        """Initialize with given data."""
        self.check = check
        self.offset = offset
        self.target = target


async def patching_response(data, from_patch_gen=False, lanky_from_history=False, gen_history=False):
    """Apply the patch data to the ROM in the BROWSER not the server."""
    # Unzip the data_passed
    loop = asyncio.get_event_loop()
    # Base64 decode the data
    decoded_data = base64.b64decode(data)
    # Create an in-memory byte stream from the zip data
    zip_stream = io.BytesIO(decoded_data)

    # Dictionary to store the extracted variables
    extracted_variables = {}

    # Extract the contents of the zip file
    with zipfile.ZipFile(zip_stream, "r") as zip_file:
        for file_name in zip_file.namelist():
            # Read the contents of each file in the zip
            with zip_file.open(file_name) as file:
                # Convert the file contents back to their original data type
                variable_value = file.read()

                # Store the extracted variable
                variable_name = file_name.split(".")[0]
                extracted_variables[variable_name] = variable_value
    settings = Settings(json.loads(js.serialize_settings(include_plando=True)))
    seed_id = str(extracted_variables["seed_id"].decode("utf-8"))
    spoiler = json.loads(extracted_variables["spoiler_log"])
    if extracted_variables.get("version") is None:
        version = "0.0.0"
    else:
        version = str(extracted_variables["version"].decode("utf-8"))
    try:
        hash_id = str(extracted_variables["seed_number"].decode("utf-8"))
    except Exception:
        hash_id = None
    # Make sure we re-load the seed id for patch file creation
    js.event_response_data = data
    if lanky_from_history:
        js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        loop.run_until_complete(ProgressBar().reset())
        return
    # elif settings.download_patch_file and from_patch_gen is False:
    #     js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
    #     js.load_old_seeds()
    #     js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
    #     loop.run_until_complete(ProgressBar().reset())
    #     return
    elif from_patch_gen is True:
        if (js.document.getElementById("download_patch_file").checked or js.document.getElementById("load_patch_file").checked) and js.document.getElementById(
            "generate_seed"
        ).value != "Download Seed":
            js.save_text_as_file(data, f"dk64r-patch-{seed_id}.lanky")
        # gif_fairy = get_hash_images("browser", "loading-fairy")
        # gif_dead = get_hash_images("browser", "loading-dead")
        # js.document.getElementById("progress-fairy").src = "data:image/jpeg;base64," + gif_fairy[0]
        # js.document.getElementById("progress-dead").src = "data:image/jpeg;base64," + gif_dead[0]
        # Apply the base patch
        await js.apply_patch(data)
        if gen_history is False:
            js.write_seed_history(seed_id, str(data), json.dumps(settings.seed_hash))
            js.load_old_seeds()

    curr_time = Datetime.now(timezone.utc)
    unix = time.mktime(curr_time.timetuple())
    random.seed(int(unix))
    split_version = version.split(".")
    patch_major = split_version[0]
    patch_minor = split_version[1]
    patch_patch = split_version[2]
    split_data = rando_version.split(".")
    major = split_data[0]
    minor = split_data[1]
    patch = split_data[2]

    ROM_COPY = ROM()
    if major != patch_major or minor != patch_minor:
        js.document.getElementById("patch_version_warning").hidden = False
        js.document.getElementById("patch_warning_message").innerHTML = (
            f"This patch was generated with version {patch_major}.{patch_minor}.{patch_patch} of the randomizer, but you are using version {major}.{minor}.{patch}. Cosmetic packs have been disabled for this patch."
        )
        fixLankyIncompatibility(ROM_COPY)
    elif from_patch_gen is True:
        sav = settings.rom_data
        if from_patch_gen:
            recalculatePointerJSON(ROM_COPY)
        js.document.getElementById("patch_version_warning").hidden = True
        ROM_COPY.seek(settings.rom_data + 0x1B8 + 4)
        chunky_model_setting = int.from_bytes(ROM_COPY.readBytes(1), "big")  # 0 is default
        if settings.disco_chunky and chunky_model_setting == 0 and settings.override_cosmetics:
            settings.kong_model_chunky = KongModels.disco_chunky
            ROM_COPY.seek(settings.rom_data + 0x1B8 + 4)
            ROM_COPY.writeMultipleBytes(6, 1)
            chunky_slots = [11, 12]
            disco_slots = [0xD, 0xEC]
            for model_slot in range(2):
                dest_start = getPointerLocation(TableNames.ActorGeometry, chunky_slots[model_slot])
                source_start = getPointerLocation(TableNames.ActorGeometry, disco_slots[model_slot])
                source_end = getPointerLocation(TableNames.ActorGeometry, disco_slots[model_slot] + 1)
                source_size = source_end - source_start
                ROM_COPY.seek(source_start)
                file_bytes = ROM_COPY.readBytes(source_size)
                ROM_COPY.seek(dest_start)
                ROM_COPY.writeBytes(file_bytes)
                # Write uncompressed size
                unc_table = getPointerLocation(TableNames.UncompressedFileSizes, TableNames.ActorGeometry)
                ROM_COPY.seek(unc_table + (disco_slots[model_slot] * 4))
                unc_size = int.from_bytes(ROM_COPY.readBytes(4), "big")
                ROM_COPY.seek(unc_table + (chunky_slots[model_slot] * 4))
                ROM_COPY.writeMultipleBytes(unc_size, 4)
        # Fetch hash images before they're altered by cosmetic changes
        loaded_hash = get_hash_images("browser", "hash")
        apply_cosmetic_colors(settings, ROM_COPY)

        if settings.override_cosmetics:
            overwrite_object_colors(settings, ROM_COPY)
            writeMiscCosmeticChanges(settings, ROM_COPY)
            applyHolidayMode(settings, ROM_COPY)
            darkenPauseBubble(settings, ROM_COPY)
            if settings.misc_cosmetics:
                writeCrownNames(ROM_COPY)

            # Fog
            holiday = getHoliday(settings)
            fog_enabled = [0, 0, 0]  # 0 = Vanilla, 1 = Set to a default (defined by either holiday mode or a custom default), 2 = rando
            default_colors = [
                [0x8A, 0x52, 0x16],  # Aztec
                [0x20, 0xFF, 0xFF],  # Caves
                [0x40, 0x10, 0x10],  # Castle
            ]
            holiday_colors = {
                Holidays.Anniv25: [0xFF, 0xFF, 0x00],
                Holidays.Halloween: [0xFF, 0x00, 0x00],
                Holidays.Christmas: [0x00, 0xFF, 0xFF],
            }
            if holiday in holiday_colors:
                fog_enabled = [1, 1, 1]
                for x in range(3):
                    default_colors[x] = holiday_colors[holiday]
            elif settings.misc_cosmetics:
                fog_enabled = [2, 1, 1]
            for index, enabled_setting in enumerate(fog_enabled):
                if enabled_setting != 0:
                    color = default_colors[index]
                    if enabled_setting == 2:
                        color = []
                        for x in range(3):
                            color.append(random.randint(1, 0xFF))
                    ROM_COPY.seek(sav + 0x088 + (index * 3))
                    for x in color:
                        ROM_COPY.writeMultipleBytes(x, 1)

            # D-Pad Display
            ROM_COPY.seek(sav + 0x139)
            # The DPadDisplays enum is indexed to allow this.
            ROM_COPY.write(int(settings.dpad_display))

            if settings.dpad_display == DPadDisplays.on and settings.dark_mode_textboxes:
                darkenDPad(ROM_COPY)

            if settings.homebrew_header:
                # Write ROM Header to assist some Mupen Emulators with recognizing that this has a 16K EEPROM
                ROM_COPY.seek(0x3C)
                CARTRIDGE_ID = "ED"
                ROM_COPY.writeBytes(CARTRIDGE_ID.encode("ascii"))
                ROM_COPY.seek(0x3F)
                SAVE_TYPE = 2  # 16K EEPROM
                ROM_COPY.writeMultipleBytes(SAVE_TYPE << 4, 1)

            # Colorblind mode
            ROM_COPY.seek(sav + 0x43)
            # The ColorblindMode enum is indexed to allow this.
            ROM_COPY.write(int(settings.colorblind_mode))

            # Big head mode
            ROM_COPY.seek(0x1FEE800)
            setting_size = {
                BigHeadMode.off: 0x00,
                BigHeadMode.big: 0xFF,
                BigHeadMode.small: 0x2F,
                BigHeadMode.random: 0x00,
            }
            applied_sizes = []
            tied_models = {
                0x04: [0x5],  # DK
                0x01: [0x2, 0x3],  # Diddy
                0x06: [0x7, 0x8],  # Lanky
                0x09: [0xA, 0xB],  # Tiny
                0x0C: [0xD, 0xE, 0xF, 0x10],  # Chunky
                0x19: [0x1A],  # Beaver
                0x1D: [0x5E],
            }
            head_sizes = {}
            for x in range(0xED):
                value = setting_size.get(settings.big_head_mode, 0x00)
                if settings.big_head_mode == BigHeadMode.random:
                    value = random.choice([0x00, 0x2F, 0x2F, 0xFF, 0xFF])  # Make abnormal head sizes more likely than a normal head size
                    # Check if model chosen is part of a tied model
                    push_name = True
                    if x == 0 or (x - 1) in HeadResizeImmune:
                        push_name = False
                    for m in tied_models:
                        if x in tied_models[m]:
                            value = applied_sizes[m]
                            push_name = False
                    if push_name:
                        head_size_names = {
                            0x00: "Normal",
                            0x2F: "Small",
                            0xFF: "Big",
                        }
                        head_sizes[ModelNames[x - 1]] = head_size_names.get(value, f"Unknown {hex(value)}")
                applied_sizes.append(value)
                ROM_COPY.write(value)

            # Remaining Menu Settings
            ROM_COPY.seek(sav + 0xC7)
            ROM_COPY.write(int(settings.sound_type))  # Sound Type

            music_volume = 40
            sfx_volume = 40
            if settings.sfx_volume is not None and settings.sfx_volume != "":
                sfx_volume = int(settings.sfx_volume / 2.5)
            if settings.music_volume is not None and settings.music_volume != "":
                music_volume = int(settings.music_volume / 2.5)
            ROM_COPY.seek(sav + 0xC8)
            ROM_COPY.write(sfx_volume)
            ROM_COPY.seek(sav + 0xC9)
            ROM_COPY.write(music_volume)

            boolean_props = [
                BooleanProperties(settings.remove_water_oscillation, 0x10F),  # Remove Water Oscillation
                BooleanProperties(settings.dark_mode_textboxes, 0x44),  # Dark Mode Text bubble
                BooleanProperties(settings.pause_hint_coloring, 0x1E4),  # Pause Hint Coloring
                BooleanProperties(settings.camera_is_follow, 0xCB),  # Free/Follow Cam
                BooleanProperties(settings.camera_is_not_inverted, 0xCC),  # Inverted/Non-Inverted Camera
            ]

            for prop in boolean_props:
                if prop.check:
                    ROM_COPY.seek(sav + prop.offset)
                    ROM_COPY.write(prop.target)

            # Excluded Songs
            if settings.songs_excluded:
                disabled_songs = settings.excluded_songs_selected.copy()
                write_data = [0]
                for item in ExcludedSongsSelector:
                    if (ExcludedSongs[item["value"]] in disabled_songs and item["shift"] >= 0) or len(disabled_songs) == 0:
                        offset = int(item["shift"] >> 3)
                        check = int(item["shift"] % 8)
                        write_data[offset] |= 0x80 >> check
                ROM_COPY.seek(sav + 0x1B7)
                ROM_COPY.writeMultipleBytes(write_data[0], 1)

            patchAssemblyCosmetic(ROM_COPY, settings)
            music_data, music_names = randomize_music(settings, ROM_COPY)
            # Disable dynamic FXMix (reverb)
            # If this impacts non-BGM music in a way that produces unwanted behavior, we'll want to only apply this to BGM
            if settings.music_disable_reverb:
                disableDynamicReverb(ROM_COPY)
            music_text = []
            accepted_characters = [*string.ascii_uppercase] + [" ", "\n", "(", ")", "%", ",", ".", "!", ">", ":", ";", "'", "-"] + [*string.digits]
            for name in music_names:
                output_name = name
                if name is None:
                    output_name = ""
                music_text.append([{"text": ["".join([x for x in [*output_name.upper()] if x in accepted_characters])]}])
            if len(music_names) > 0:
                writeText(ROM_COPY, 46, music_text)
            if settings.show_song_name:
                ROM_COPY.seek(sav + 0x1ED)
                ROM_COPY.write(1)

            spoiler = updateJSONCosmetics(spoiler, settings, music_data, int(unix), head_sizes)

        # Apply Hash
        order = 0
        for count in json.loads(extracted_variables["hash"].decode("utf-8")):
            js.document.getElementById("hashdiv").innerHTML = ""
            # clear the innerHTML of the hash element
            js.document.getElementById("hash" + str(order)).src = "data:image/jpeg;base64," + loaded_hash[count]
            # Clear all the styles of the hash element
            js.document.getElementById("hash" + str(order)).style.transform = "rotate(180deg)"
            order += 1
    # if the hash is not set, just put the text in the spoiler log
    if js.document.getElementById("hash0").src == "":
        # insert a text div into the js.document.getElementById("hashdiv") and set the innerHTML to the No ROM loaded message add the div
        js.document.getElementById("hashdiv").innerHTML = "Shared Link, No Hash Images Loaded."

    if from_patch_gen is True:
        await ProgressBar().update_progress(10, "Seed Generated.")
    js.document.getElementById("nav-settings-tab").style.display = ""
    js.document.getElementById("spoiler_log_block").style.display = ""
    loop.run_until_complete(js.GenerateSpoiler(json.dumps(spoiler)))
    js.document.getElementById("generated_seed_id").innerHTML = seed_id
    # Set the current URL to the seed ID so that it can be shared without reloading the page
    js.window.history.pushState("generated_seed", hash_id, f"/randomizer?seed_id={hash_id}")
    # if generate_spoiler_log is False enable the download_unlocked_spoiler_button button
    if settings.generate_spoilerlog is False and hash_id is not None:
        try:
            js.document.getElementById("download_unlocked_spoiler_button").onclick = lambda x: js.unlock_spoiler_log(hash_id)
            js.document.getElementById("download_unlocked_spoiler_button").hidden = False
            js.document.getElementById("download_spoiler_button").hidden = True
        except Exception:
            js.document.getElementById("download_unlocked_spoiler_button").hidden = True
            js.document.getElementById("download_unlocked_spoiler_button").onclick = None
            js.document.getElementById("download_spoiler_button").hidden = False
    else:
        js.document.getElementById("download_unlocked_spoiler_button").hidden = True
        js.document.getElementById("download_unlocked_spoiler_button").onclick = None
        js.document.getElementById("download_spoiler_button").hidden = False
    if from_patch_gen is True:
        ROM_COPY.fixSecurityValue()
        ROM_COPY.save(f"dk64r-rom-{seed_id}.z64")
        loop.run_until_complete(ProgressBar().reset())
    js.jq("#nav-settings-tab").tab("show")
    js.check_seed_info_tab()


def FormatSpoiler(value):
    """Format the values passed to the settings table into a more readable format.

    Args:
        value (str) or (bool)
    """
    string = str(value)
    formatted = string.replace("_", " ")
    result = formatted.title()
    return result


def updateJSONCosmetics(spoiler, settings, music_data, cosmetic_seed, head_sizes):
    """Update spoiler JSON with cosmetic settings."""
    humanspoiler = spoiler
    if humanspoiler.get("Settings") is None:
        humanspoiler["Settings"] = {}
    if humanspoiler.get("Cosmetics") is None:
        humanspoiler["Cosmetics"] = {}
    humanspoiler["Settings"]["Cosmetic Seed"] = cosmetic_seed

    random_model_choices = [
        {"name": "Beaver Bother Klaptrap", "setting": settings.bother_klaptrap_model},
        {"name": "Beetle", "setting": settings.beetle_model},
        {"name": "Rabbit", "setting": settings.rabbit_model},
        {"name": "Peril Path Panic Fairy", "setting": settings.panic_fairy_model},
        {"name": "Peril Path Panic Klaptrap", "setting": settings.panic_klaptrap_model},
        {"name": "Turtle", "setting": settings.turtle_model},
        {"name": "Searchlight Seek Klaptrap", "setting": settings.seek_klaptrap_model},
        {"name": "Forest Tomato", "setting": settings.fungi_tomato_model},
        {"name": "Caves Tomato", "setting": settings.caves_tomato_model},
        {"name": "Factory Piano Burper", "setting": settings.piano_burp_model},
        {"name": "Spotlight Fish", "setting": settings.spotlight_fish_model},
        {"name": "Candy (Chunky Phase, End Sequence)", "setting": settings.candy_cutscene_model},
        {"name": "Funky (Chunky Phase, End Sequence)", "setting": settings.funky_cutscene_model},
        {"name": "Funky's Boot (Chunky Phase)", "setting": settings.boot_cutscene_model},
    ]

    if settings.colors != {} or settings.random_models != RandomModels.off or settings.misc_cosmetics:
        humanspoiler["Cosmetics"]["Colors"] = {}
        humanspoiler["Cosmetics"]["Models"] = {}
        humanspoiler["Cosmetics"]["Sprites"] = {}
        for color_item in settings.colors:
            if color_item == "dk":
                humanspoiler["Cosmetics"]["Colors"]["DK Color"] = settings.colors[color_item]
            else:
                humanspoiler["Cosmetics"]["Colors"][f"{color_item.capitalize()} Color"] = settings.colors[color_item]
        for data in random_model_choices:
            if isinstance(data["setting"], Model):
                humanspoiler["Cosmetics"]["Models"][data["name"]] = camelCaseToWords(data["setting"].name)
            else:
                humanspoiler["Cosmetics"]["Models"][data["name"]] = f"Unknown Model {hex(int(data['setting']))}"
    if settings.misc_cosmetics:
        humanspoiler["Cosmetics"]["Sprites"]["Minigame Melon"] = camelCaseToWords(settings.minigame_melon_sprite.name)
    if settings.music_bgm_randomized or settings.bgm_songs_selected:
        humanspoiler["Cosmetics"]["Background Music"] = music_data.get("music_bgm_data")
    if settings.music_majoritems_randomized or settings.majoritems_songs_selected:
        humanspoiler["Cosmetics"]["Major Item Themes"] = music_data.get("music_majoritem_data")
    if settings.music_minoritems_randomized or settings.minoritems_songs_selected:
        humanspoiler["Cosmetics"]["Minor Item Themes"] = music_data.get("music_minoritem_data")
    if settings.music_events_randomized or settings.events_songs_selected:
        humanspoiler["Cosmetics"]["Event Themes"] = music_data.get("music_event_data")
    if settings.big_head_mode == BigHeadMode.random:
        humanspoiler["Cosmetics"]["Head Sizes"] = head_sizes
    humanspoiler["Cosmetics"]["Textures"] = {}
    if settings.custom_transition is not None:
        humanspoiler["Cosmetics"]["Textures"]["Transition"] = settings.custom_transition
    if settings.custom_troff_portal is not None:
        humanspoiler["Cosmetics"]["Textures"]["Troff 'n' Scoff Portal"] = settings.custom_troff_portal
    paintings = {
        "DK Isles Painting": settings.painting_isles,
        "Museum K. Rool Painting": settings.painting_museum_krool,
        "Museum Knight Painting": settings.painting_museum_knight,
        "Museum Swords Painting": settings.painting_museum_swords,
        "Treehouse Dolphin Painting": settings.painting_treehouse_dolphin,
        "Treehouse Candy Painting": settings.painting_treehouse_candy,
    }
    for painting_name in paintings:
        painting_setting = paintings[painting_name]
        if painting_setting is not None:
            humanspoiler["Cosmetics"]["Textures"][painting_name] = painting_setting
    return humanspoiler
