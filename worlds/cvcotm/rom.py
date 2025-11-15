
import Utils
import logging
import json

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from typing import Dict, Optional, Collection, TYPE_CHECKING

import hashlib
import os
import pkgutil

from .data import patches
from .locations import cvcotm_location_info
from .cvcotm_text import cvcotm_string_to_bytearray
from .options import CompletionGoal, IronMaidenBehavior, RequiredSkirmishes
from .lz10 import decompress
from settings import get_settings

if TYPE_CHECKING:
    from . import CVCotMWorld

CVCOTM_CT_US_HASH = "50a1089600603a94e15ecf287f8d5a1f"  # Original GBA cartridge ROM
CVCOTM_AC_US_HASH = "87a1bd6577b6702f97a60fc55772ad74"  # Castlevania Advance Collection ROM
# CVCOTM_VC_US_HASH = "2cc38305f62b337281663bad8c901cf9"  # Wii U Virtual Console ROM

# The Wii U VC version is not currently supported. See the Game Page for more info.

ARCHIPELAGO_IDENTIFIER_START = 0x7FFF00
ARCHIPELAGO_IDENTIFIER = "ARCHIPELAG03"
AUTH_NUMBER_START = 0x7FFF10
QUEUED_TEXT_STRING_START = 0x7CEB00
MULTIWORLD_TEXTBOX_POINTERS_START = 0x671C10

BATTLE_ARENA_SONG_IDS = [0x01, 0x03, 0x12, 0x06, 0x08, 0x09, 0x07, 0x0A, 0x0B,
                         0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0x11, 0x13, 0x14]


class RomData:
    def __init__(self, file: bytes, name: Optional[str] = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_byte(self, offset: int, value: int) -> None:
        self.file[offset] = value

    def write_bytes(self, offset: int, values: Collection[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)

    def apply_ips(self, filename: str) -> None:
        # Try loading the IPS file.
        try:
            ips_file = pkgutil.get_data(__name__, "data/ips/" + filename)
        except IOError:
            raise Exception(f"{filename} is not present in the ips folder. If it was removed, please replace it.")

        # Verify that the IPS patch is, indeed, an IPS patch.
        if ips_file[0:5].decode("ascii") != "PATCH":
            logging.error(filename + " does not appear to be an IPS patch...")
            return

        file_pos = 5
        while True:
            # Get the ROM offset bytes of the current record.
            rom_offset = int.from_bytes(ips_file[file_pos:file_pos + 3], "big")

            # If we've hit the "EOF" codeword (aka 0x454F46), stop iterating because we've reached the end of the patch.
            if rom_offset == 0x454F46:
                return

            # Get the size bytes of the current record.
            bytes_size = int.from_bytes(ips_file[file_pos + 3:file_pos + 5], "big")

            if bytes_size != 0:
                # Write the bytes to the ROM.
                self.write_bytes(rom_offset, ips_file[file_pos + 5:file_pos + 5 + bytes_size])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 5 + bytes_size
            else:
                # If the size is 0, we are looking at an RLE record.
                # Get the size of the RLE.
                rle_size = int.from_bytes(ips_file[file_pos + 5:file_pos + 7], "big")

                # Get the byte to be written over and over.
                rle_byte = int.from_bytes(ips_file[file_pos + 7:file_pos + 8], "big")

                # Write the RLE byte to the ROM the RLE size times over.
                self.write_bytes(rom_offset, [rle_byte for _ in range(rle_size)])

                # Increase our position in the IPS patch to the start of the next record.
                file_pos += 8


class CVCotMPatchExtensions(APPatchExtension):
    game = "Castlevania - Circle of the Moon"

    @staticmethod
    def apply_patches(caller: APProcedurePatch, rom: bytes, options_file: str) -> bytes:
        """Applies every patch to mod the game into its rando state, both CotMR's pre-made IPS patches and some
        additional byte writes. Each patch is credited to its author."""

        rom_data = RomData(rom)
        options = json.loads(caller.get_file(options_file).decode("utf-8"))

        # Check to see if the patch was generated on a compatible APWorld version.
        if "compat_identifier" not in options:
            raise Exception("Incompatible patch/APWorld version. Make sure the Circle of the Moon APWorlds of both you "
                            "and the person who generated are matching (and preferably up-to-date).")
        if options["compat_identifier"] != ARCHIPELAGO_IDENTIFIER:
            raise Exception("Incompatible patch/APWorld version. Make sure the Circle of the Moon APWorlds of both you "
                            "and the person who generated are matching (and preferably up-to-date).")

        # This patch allows placing DSS cards on pedestals, prevents them from timing out, and removes them from enemy
        # drop tables. Created by DevAnj originally as a standalone hack known as Card Mode, it has been modified for
        # this randomizer's purposes by stripping out additional things like drop and pedestal item replacements.

        # Further modified by Liquid Cat to make placed cards set their flags upon pickup (instead of relying on whether
        # the card is in the player's inventory when determining to spawn it or not), enable placing dummy DSS Cards to
        # represent other players' Cards in a multiworld setting, and turn specific cards blue to visually indicate
        # their status as valid ice/stone combo cards.
        rom_data.apply_ips("CardUp_v3_Custom2.ips")

        # This patch replaces enemy drops that included DSS cards. Created by DevAnj as part of the Card Up patch but
        # modified for different replacement drops (Lowered rate, Potion instead of Meat, and no Shinning Armor change
        # on Devil).
        rom_data.apply_ips("NoDSSDrops.ips")

        # This patch reveals card combination descriptions instead of showing "???" until the combination is used.
        # Created by DevAnj.
        rom_data.apply_ips("CardCombosRevealed.ips")

        # In lategame, the Trick Candle and Scary Candle load in the Cerberus and Iron Golem boss rooms after defeating
        # Camilla and Twin Dragon Zombies respectively. If the former bosses have not yet been cleared (i.e., we have
        # sequence broken the game and returned to the earlier boss rooms to fight them), the candle enemies will cause
        # the bosses to fail to load and soft lock the game. This patches the candles to appear after the early boss is
        # completed instead.
        # Created by DevAnj.
        rom_data.apply_ips("CandleFix.ips")

        # A Tackle block in Machine Tower will cause a softlock if you access the Machine Tower from the Audience Room
        # using the stone tower route with Kick Boots and not Double. This is a small level edit that moves that block
        # slightly, removing the potential for a softlock.
        # Created by DevAnj.
        rom_data.apply_ips("SoftlockBlockFix.ips")

        # Normally, the MP boosting card combination is useless since it depletes more MP than it gains. This patch
        # makes it consume zero MP.
        # Created by DevAnj.
        rom_data.apply_ips("MPComboFix.ips")

        # Normally, you must clear the game with each mode to unlock subsequent modes, and complete the game at least
        # once to be able to skip the introductory text crawl. This allows all game modes to be selected and the
        # introduction to be skipped even without game/mode completion.
        # Created by DevAnj.
        rom_data.apply_ips("GameClearBypass.ips")

        # This patch adds custom mapping in Underground Gallery and Underground Waterway to avoid softlocking/Kick Boots
        # requirements.
        # Created by DevAnj.
        rom_data.apply_ips("MapEdits.ips")

        # Prevents demos on the main title screen after the first one from being displayed to avoid pedestal item
        # reconnaissance from the menu.
        # Created by Fusecavator.
        rom_data.apply_ips("DemoForceFirst.ips")

        # Used internally in the item randomizer to allow setting drop rate to 10000 (100%) and actually drop the item
        # 100% of the time. Normally, it is hard capped at 50% for common drops and 25% for rare drops.
        # Created by Fusecavator.
        rom_data.apply_ips("AllowAlwaysDrop.ips")

        # Displays the seed on the pause menu. Originally created by Fusecavator and modified by Liquid Cat to display a
        # 20-digit seed (which AP seeds most commonly are).
        rom_data.apply_ips("SeedDisplay20Digits.ips")

        # Write the seed. Upwards of 20 digits can be displayed for the seed number.
        curr_seed_addr = 0x672152
        total_digits = 0
        while options["seed"] and total_digits < 20:
            seed_digit = (options["seed"] % 10) + 0x511C
            rom_data.write_bytes(curr_seed_addr, int.to_bytes(seed_digit, 2, "little"))
            curr_seed_addr -= 2
            total_digits += 1
            options["seed"] //= 10

        # Optional patch created by Fusecavator. Permanent dash effect without double tapping.
        if options["auto_run"]:
            rom_data.apply_ips("PermanentDash.ips")

        # Optional patch created by Fusecavator. Prohibits the DSS glitch. You will not be able to update the active
        # effect unless the card combination switched to is obtained. For example, if you switch to another DSS
        # combination that you have not obtained during DSS startup, you will still have the effect of the original
        # combination you had selected when you started the DSS activation. In addition, you will not be able to
        # increase damage and/or change the element of a summon attack unless you possess the cards you swap to.
        if options["dss_patch"]:
            rom_data.apply_ips("DSSGlitchFix.ips")

        # Optional patch created by DevAnj. Breaks the iron maidens blocking access to the Underground Waterway,
        # Underground Gallery, and the room beyond the Adramelech boss room from the beginning of the game.
        if options["break_iron_maidens"]:
            rom_data.apply_ips("BrokenMaidens.ips")

        # Optional patch created by Fusecavator. Changes game behavior to add instead of set Last Key values, and check
        # for a specific value of Last Keys on the door to the Ceremonial Room, allowing multiple keys to be required to
        # complete the game. Relies on the program to set required key values.
        if options["required_last_keys"] != 1:
            rom_data.apply_ips("MultiLastKey.ips")
            rom_data.write_byte(0x96C1E, options["required_last_keys"])
            rom_data.write_byte(0xDFB4, options["required_last_keys"])
            rom_data.write_byte(0xCB84, options["required_last_keys"])

        # Optional patch created by Fusecavator. Doubles the damage dealt by projectiles fired by ranged familiars.
        if options["buff_ranged_familiars"]:
            rom_data.apply_ips("BuffFamiliars.ips")

        # Optional patch created by Fusecavator. Increases the base damage dealt by some sub-weapons.
        # Changes below (normal multiplier on left/shooter on right):
        # Original:                         Changed:
        # Dagger:            45 / 141 ----> 100 / 141 (Non-Shooter buffed)
        # Dagger crush:      32 / 45  ----> 100 / 141 (Both buffed to match non-crush values)
        # Axe:               89 / 158 ----> 125 / 158 (Non-Shooter somewhat buffed)
        # Axe crush:         89 / 126 ----> 125 / 158 (Both buffed to match non-crush values)
        # Holy water:        63 / 100 ---->  63 / 100 (Unchanged)
        # Holy water crush:  45 / 63  ---->  63 / 100 (Large buff to Shooter, non-Shooter slightly buffed)
        # Cross:            110 / 173 ----> 110 / 173 (Unchanged)
        # Cross crush:      100 / 141 ----> 110 / 173 (Slightly buffed to match non-crush values)
        if options["buff_sub_weapons"]:
            rom_data.apply_ips("BuffSubweapons.ips")

        # Optional patch created by Fusecavator. Increases the Shooter gamemode base strength and strength per level to
        # match Vampire Killer.
        if options["buff_shooter_strength"]:
            rom_data.apply_ips("ShooterStrength.ips")

        # Optional patch created by Fusecavator. Allows using the Pluto + Griffin combination for the speed boost with
        # or without the cards being obtained.
        if options["always_allow_speed_dash"]:
            rom_data.apply_ips("AllowSpeedDash.ips")

        # Optional patch created by fuse. Displays a counter on the HUD showing the number of magic items and cards
        # remaining in the current area. Requires a lookup table generated by the randomizer to function.
        if options["countdown"]:
            rom_data.apply_ips("Countdown.ips")

        # This patch disables the MP drain effect in the Battle Arena.
        # Created by Fusecavator.
        if options["disable_battle_arena_mp_drain"]:
            rom_data.apply_ips("NoMPDrain.ips")

        # Patch created by Fusecavator. Makes various changes to dropped item graphics to avoid garbled Magic Items and
        # allow displaying arbitrary items on pedestals. Modified by Liquid Cat for the purposes of changing the
        # appearances of items regardless of what they really are, as well as allowing additional Magic Items.
        rom_data.apply_ips("DropReworkMultiEdition.ips")
        # Decompress the Magic Item graphics and reinsert them (decompressed) where the patch expects them.
        # Doing it this way is more copyright-safe.
        rom_data.write_bytes(0x678C00, decompress(rom_data.read_bytes(0x630690, 0x605))[0x300:])

        # Everything past here was added by Liquid Cat.

        # Makes the Pluto + Griffin speed increase apply even while in the air, instead of losing it.
        if options["pluto_griffin_air_speed"]:
            rom_data.apply_ips("DSSRunSpeed.ips")

        # Move the item sprite info table.
        rom_data.write_bytes(0x678A00, rom_data.read_bytes(0x630B98, 0x98))
        # Update the ldr numbers pointing to the above item sprite table.
        rom_data.write_bytes(0x95A08, [0x00, 0x8A, 0x67, 0x08])
        rom_data.write_bytes(0x100380, [0x00, 0x8A, 0x67, 0x08])
        # Move the magic item text ID table.
        rom_data.write_bytes(0x6788B0, rom_data.read_bytes(0x100A7E, 0x48))
        # Update the ldr numbers pointing to the above magic item text ID table.
        rom_data.write_bytes(0x95C10, [0xB0, 0x88, 0x67, 0x08])
        rom_data.write_bytes(0x95CE0, [0xB0, 0x88, 0x67, 0x08])
        # Move the magic item pickup function jump table.
        rom_data.write_bytes(0x678B20, rom_data.read_bytes(0x95B80, 0x24))
        # Update the ldr number point to the above jump table.
        rom_data.write_bytes(0x95B7C, [0x20, 0x8B, 0x67, 0x08])
        rom_data.write_byte(0x95B6A, 0x09)  # Raise the magic item function index limit.

        # Make the Maiden Detonator detonate the maidens when picked up.
        rom_data.write_bytes(0x678B44, [0x90, 0x1F, 0x67, 0x08])
        rom_data.write_bytes(0x671F90, patches.maiden_detonator)
        # Add the text for detonating the maidens.
        rom_data.write_bytes(0x671C0C, [0xC0, 0x1F, 0x67, 0x08])
        rom_data.write_bytes(0x671FC0, cvcotm_string_to_bytearray("    「Iron Maidens」 broken◊", "little middle", 0,
                                                                  wrap=False))

        # Put the new text string IDs for all our new items.
        rom_data.write_bytes(0x6788F8, [0xF1, 0x84, 0xF1, 0x84, 0xF1, 0x84, 0xF1, 0x84,
                                        0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        # Have the game get the entry in that table to use by adding the item's parameter.
        rom_data.write_bytes(0x95980, [0x0A, 0x30, 0x00, 0x00, 0x00, 0x00])
        # Add the AP Item sprites and their associated info.
        rom_data.write_bytes(0x679080, patches.extra_item_sprites)
        rom_data.write_bytes(0x678A98, [0xF8, 0xFF, 0xF8, 0xFF, 0xFC, 0x21, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x00, 0x22, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x04, 0x22, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x08, 0x22, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x0C, 0x22, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x10, 0x22, 0x45, 0x00,
                                        0xF8, 0xFF, 0xF8, 0xFF, 0x14, 0x32, 0x45, 0x00])
        # Enable changing the Magic Item appearance separately from what it really is.
        # Change these ldrh's to ldrb's to read only the high or low byte of the object list entry's parameter field.
        rom_data.write_bytes(0x9597A, [0xC1, 0x79])
        rom_data.write_bytes(0x95B64, [0x80, 0x79])
        rom_data.write_bytes(0x95BF0, [0x81, 0x79])
        rom_data.write_bytes(0x95CBE, [0x82, 0x79])
        # Enable changing the Max Up appearance separately from what it really is.
        rom_data.write_bytes(0x5DE98, [0xC1, 0x79])
        rom_data.write_byte(0x5E152, 0x13)
        rom_data.write_byte(0x5E15C, 0x0E)
        rom_data.write_byte(0x5E20A, 0x0B)

        # Set the 0xF0 flag on the iron maiden switch if we're placing an Item on it.
        if options["iron_maiden_behavior"] == IronMaidenBehavior.option_detonator_in_pool:
            rom_data.write_byte(0xD47B4, 0xF0)

        if options["nerf_roc_wing"]:
            # Prevent Roc jumping in midair if the Double is not in the player's inventory.
            rom_data.write_bytes(0x6B8A0, [0x00, 0x4A, 0x97, 0x46, 0x00, 0x9A, 0x67, 0x08])
            rom_data.write_bytes(0x679A00, patches.doubleless_roc_midairs_preventer)

            # Make Roc Wing not jump as high if Kick Boots isn't in the inventory.
            rom_data.write_bytes(0x6B8B4, [0x00, 0x49, 0x8F, 0x46, 0x60, 0x9A, 0x67, 0x08])
            rom_data.write_bytes(0x679A60, patches.kickless_roc_height_shortener)

        # Give the player their Start Inventory upon entering their name on a new file.
        rom_data.write_bytes(0x7F70, [0x00, 0x48, 0x87, 0x46, 0x00, 0x00, 0x69, 0x08])
        rom_data.write_bytes(0x690000, patches.start_inventory_giver)

        # Prevent Max Ups from exceeding 255.
        rom_data.write_bytes(0x5E170, [0x00, 0x4A, 0x97, 0x46, 0x00, 0x00, 0x6A, 0x08])
        rom_data.write_bytes(0x6A0000, patches.max_max_up_checker)

        # Write the textbox messaging system code.
        rom_data.write_bytes(0x7D60, [0x00, 0x48, 0x87, 0x46, 0x20, 0xFF, 0x7F, 0x08])
        rom_data.write_bytes(0x7FFF20, patches.remote_textbox_shower)

        # Write the code that sets the screen transition delay timer.
        rom_data.write_bytes(0x6CE14, [0x00, 0x4A, 0x97, 0x46, 0xC0, 0xFF, 0x7F, 0x08])
        rom_data.write_bytes(0x7FFFC0, patches.transition_textbox_delayer)

        # Write the code that allows any sound to be played with any Magic Item.
        rom_data.write_bytes(0x95BE4, [0x00, 0x4A, 0x97, 0x46, 0x00, 0x98, 0x67, 0x08])
        rom_data.write_bytes(0x679800, patches.magic_item_sfx_customizer)
        # Array of sound IDs for each Magic Item.
        rom_data.write_bytes(0x6797C0, [0xB4, 0x01, 0xB4, 0x01, 0xB4, 0x01, 0xB4, 0x01, 0xB4, 0x01, 0xB4, 0x01,
                                        0xB4, 0x01, 0xB4, 0x01, 0xB4, 0x01, 0x79, 0x00])

        # Write all the data for the missing ASCII text characters.
        for offset, data in patches.missing_char_data.items():
            rom_data.write_bytes(offset, data)

        # Change all the menu item name strings that use the overwritten character IDs to use a different, equivalent
        # space character ID.
        rom_data.write_bytes(0x391A1B, [0xAD, 0xAD, 0xAD, 0xAD, 0xAD, 0xAD])
        rom_data.write_bytes(0x391CB6, [0xAD, 0xAD, 0xAD])
        rom_data.write_bytes(0x391CC1, [0xAD, 0xAD, 0xAD])
        rom_data.write_bytes(0x391CCB, [0xAD, 0xAD, 0xAD, 0xAD])
        rom_data.write_bytes(0x391CD5, [0xAD, 0xAD, 0xAD, 0xAD, 0xAD])
        rom_data.write_byte(0x391CE1, 0xAD)

        # Put the unused bottom-of-screen textbox in the middle of the screen instead.
        # Its background's new y position will be 0x28 instead of 0x50.
        rom_data.write_byte(0xBEDEA, 0x28)
        # Change all the hardcoded checks for the 0x50 position to instead check for 0x28.
        rom_data.write_byte(0xBF398, 0x28)
        rom_data.write_byte(0xBF41C, 0x28)
        rom_data.write_byte(0xBF4CC, 0x28)
        # Change all the hardcoded checks for greater than 0x48 to instead check for 0x28 specifically.
        rom_data.write_byte(0xBF4A4, 0x28)
        rom_data.write_byte(0xBF4A7, 0xD0)
        rom_data.write_byte(0xBF37E, 0x28)
        rom_data.write_byte(0xBF381, 0xD0)
        rom_data.write_byte(0xBF40A, 0x28)
        rom_data.write_byte(0xBF40D, 0xD0)
        # Change the y position of the contents within the textbox from 0xA0 to 0xB4.
        # KCEK didn't program hardcoded checks for these, thankfully!
        rom_data.write_byte(0xBF3BC, 0xB4)

        # Insert the multiworld message pointer at the end of the text pointers.
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START, int.to_bytes(QUEUED_TEXT_STRING_START + 0x8000000,
                                                                             4, "little"))
        # Insert pointers for every item tutorial.
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 4,  [0x8E, 0x3B, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 8,  [0xDF, 0x3B, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 12, [0x35, 0x3C, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 16, [0xC4, 0x3C, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 20, [0x41, 0x3D, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 24, [0x88, 0x3D, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 28, [0xF7, 0x3D, 0x39, 0x08])
        rom_data.write_bytes(MULTIWORLD_TEXTBOX_POINTERS_START + 32, [0x67, 0x3E, 0x39, 0x08])

        # Write the completion goal messages over the menu Dash Boots tutorial and Battle Arena's explanation message.
        if options["completion_goal"] == CompletionGoal.option_dracula:
            dash_tutorial_message = "Your goal is:\n  Dracula◊"
            if options["required_skirmishes"] == RequiredSkirmishes.option_all_bosses_and_arena:
                arena_goal_message = "Your goal is:\n「Dracula」▶" \
                                     "A required 「Last Key」 is waiting for you at the end of the Arena. Good luck!◊"
            else:
                arena_goal_message = "Your goal is:\n「Dracula」▶" \
                                     "You don't have to win the Arena, but you are certainly welcome to try!◊"
        elif options["completion_goal"] == CompletionGoal.option_battle_arena:
            dash_tutorial_message = "Your goal is:\n  Battle Arena◊"
            arena_goal_message = "Your goal is:\n「Battle Arena」▶" \
                                 "Win the Arena, and your goal will send. Good luck!◊"
        else:
            dash_tutorial_message = "Your goal is:\n  Arena and Dracula◊"
            arena_goal_message = "Your goal is:\n「Battle Arena & Dracula」▶" \
                                 "Your goal will send once you've both won the Arena and beaten Dracula. Good luck!◊"

        rom_data.write_bytes(0x393EAE, cvcotm_string_to_bytearray(dash_tutorial_message, "big top", 4,
                                                                  skip_textbox_controllers=True))
        rom_data.write_bytes(0x393A0C, cvcotm_string_to_bytearray(arena_goal_message, "big top", 4))

        # Change the pointer to the Ceremonial Room locked door text.
        rom_data.write_bytes(0x670D94, [0xE0, 0xE9, 0x7C, 0x08])
        # Write the Ceremonial Room door and menu Last Key tutorial messages telling the player's Last Key options.
        door_message = f"Hmmmmmm...\nI need 「{options['required_last_keys']}」/" \
                       f"「{options['available_last_keys']}」 Last Keys.◊"
        key_tutorial_message = f"You need {options['required_last_keys']}/{options['available_last_keys']} keys.◊"
        rom_data.write_bytes(0x7CE9E0, cvcotm_string_to_bytearray(door_message, "big top", 4, 0))
        rom_data.write_bytes(0x394098, cvcotm_string_to_bytearray(key_tutorial_message, "big top", 4,
                                                                  skip_textbox_controllers=True))

        # Nuke all the tutorial-related text if Skip Tutorials is enabled.
        if options["skip_tutorials"]:
            rom_data.write_byte(0x5EB55, 0xE0)  # DSS
            rom_data.write_byte(0x393B8C, 0x00)  # Dash Boots
            rom_data.write_byte(0x393BDD, 0x00)  # Double
            rom_data.write_byte(0x393C33, 0x00)  # Tackle
            rom_data.write_byte(0x393CC2, 0x00)  # Kick Boots
            rom_data.write_byte(0x393D41, 0x00)  # Heavy Ring
            rom_data.write_byte(0x393D86, 0x00)  # Cleansing
            rom_data.write_byte(0x393DF5, 0x00)  # Roc Wing
            rom_data.write_byte(0x393E65, 0x00)  # Last Key

        # Nuke all the cutscene dialogue before the ending if Skip Dialogues is enabled.
        if options["skip_dialogues"]:
            rom_data.write_byte(0x392372, 0x00)
            rom_data.write_bytes(0x3923C9, [0x20, 0x80, 0x00])
            rom_data.write_bytes(0x3924EE, [0x20, 0x81, 0x00])
            rom_data.write_byte(0x392621, 0x00)
            rom_data.write_bytes(0x392650, [0x20, 0x81, 0x00])
            rom_data.write_byte(0x392740, 0x00)
            rom_data.write_byte(0x3933C8, 0x00)
            rom_data.write_byte(0x39346E, 0x00)
            rom_data.write_byte(0x393670, 0x00)
            rom_data.write_bytes(0x393698, [0x20, 0x80, 0x00])
            rom_data.write_byte(0x3936A6, 0x00)
            rom_data.write_byte(0x393741, 0x00)
            rom_data.write_byte(0x392944, 0x00)
            rom_data.write_byte(0x392FFB, 0x00)
            rom_data.write_byte(0x39305D, 0x00)
            rom_data.write_byte(0x393114, 0x00)
            rom_data.write_byte(0x392771, 0x00)
            rom_data.write_byte(0x3928E9, 0x00)
            rom_data.write_byte(0x392A3C, 0x00)
            rom_data.write_byte(0x392A55, 0x00)
            rom_data.write_byte(0x392A8B, 0x00)
            rom_data.write_byte(0x392AA4, 0x00)
            rom_data.write_byte(0x392AF4, 0x00)
            rom_data.write_byte(0x392B3F, 0x00)
            rom_data.write_byte(0x392C4D, 0x00)
            rom_data.write_byte(0x392DEA, 0x00)
            rom_data.write_byte(0x392E65, 0x00)
            rom_data.write_byte(0x392F09, 0x00)
            rom_data.write_byte(0x392FE4, 0x00)

        # Make the Battle Arena play the player's chosen track.
        if options["battle_arena_music"]:
            arena_track_id = BATTLE_ARENA_SONG_IDS[options["battle_arena_music"] - 1]
            rom_data.write_bytes(0xEDEF0, [0xFC, 0xFF, arena_track_id])
            rom_data.write_bytes(0xEFA50, [0xFC, 0xFF, arena_track_id])
            rom_data.write_bytes(0xF24F0, [0xFC, 0xFF, arena_track_id])
            rom_data.write_bytes(0xF3420, [0xF5, 0xFF])
            rom_data.write_bytes(0xF3430, [0xFC, 0xFF, arena_track_id])

        return rom_data.get_bytes()

    @staticmethod
    def fix_item_positions(caller: APProcedurePatch, rom: bytes) -> bytes:
        """After writing all the items into the ROM via token application, translates Magic Items in non-Magic Item
        Locations up by 8 units and the reverse down by 8 units. This is necessary for them to look properly placed,
        as Magic Items are offset differently on the Y axis from the other item types."""
        rom_data = RomData(rom)
        for loc in cvcotm_location_info:
            offset = cvcotm_location_info[loc].offset
            if offset is None:
                continue
            item_type = rom_data.read_byte(offset)

            # Magic Items in non-Magic Item Locations should have their Y position decreased by 8.
            if item_type == 0xE8 and cvcotm_location_info[loc].type not in ["magic item", "boss"]:
                y_pos = int.from_bytes(rom_data.read_bytes(offset-2, 2), "little")
                y_pos -= 8
                rom_data.write_bytes(offset-2, int.to_bytes(y_pos, 2, "little"))

            # Non-Magic Items in Magic Item Locations should have their Y position increased by 8.
            if item_type != 0xE8 and cvcotm_location_info[loc].type in ["magic item", "boss"]:
                y_pos = int.from_bytes(rom_data.read_bytes(offset - 2, 2), "little")
                y_pos += 8
                rom_data.write_bytes(offset - 2, int.to_bytes(y_pos, 2, "little"))

        return rom_data.get_bytes()


class CVCotMProcedurePatch(APProcedurePatch, APTokenMixin):
    # hash = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH, CVCOTM_VC_US_HASH]
    hash = [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]
    patch_file_ending: str = ".apcvcotm"
    result_file_ending: str = ".gba"

    game = "Castlevania - Circle of the Moon"

    procedure = [
        ("apply_patches", ["options.json"]),
        ("apply_tokens", ["token_data.bin"]),
        ("fix_item_positions", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()


def patch_rom(world: "CVCotMWorld", patch: CVCotMProcedurePatch, offset_data: Dict[int, bytes],
              start_with_detonator: bool) -> None:

    # Write all the new item values
    for offset, data in offset_data.items():
        patch.write_token(APTokenTypes.WRITE, offset, data)

    # Write the secondary name the client will use to distinguish a vanilla ROM from an AP one.
    patch.write_token(APTokenTypes.WRITE, ARCHIPELAGO_IDENTIFIER_START, ARCHIPELAGO_IDENTIFIER.encode("utf-8"))
    # Write the slot authentication
    patch.write_token(APTokenTypes.WRITE, AUTH_NUMBER_START, bytes(world.auth))

    patch.write_file("token_data.bin", patch.get_token_binary())

    # Write these slot options to a JSON.
    options_dict = {
        "auto_run": world.options.auto_run.value,
        "dss_patch": world.options.dss_patch.value,
        "break_iron_maidens": start_with_detonator,
        "iron_maiden_behavior": world.options.iron_maiden_behavior.value,
        "required_last_keys": world.required_last_keys,
        "available_last_keys": world.options.available_last_keys.value,
        "required_skirmishes": world.options.required_skirmishes.value,
        "buff_ranged_familiars": world.options.buff_ranged_familiars.value,
        "buff_sub_weapons": world.options.buff_sub_weapons.value,
        "buff_shooter_strength": world.options.buff_shooter_strength.value,
        "always_allow_speed_dash": world.options.always_allow_speed_dash.value,
        "countdown": world.options.countdown.value,
        "disable_battle_arena_mp_drain": world.options.disable_battle_arena_mp_drain.value,
        "completion_goal": world.options.completion_goal.value,
        "skip_dialogues": world.options.skip_dialogues.value,
        "skip_tutorials": world.options.skip_tutorials.value,
        "nerf_roc_wing": world.options.nerf_roc_wing.value,
        "pluto_griffin_air_speed": world.options.pluto_griffin_air_speed.value,
        "battle_arena_music": world.options.battle_arena_music.value,
        "seed": world.multiworld.seed,
        "compat_identifier": ARCHIPELAGO_IDENTIFIER
    }

    patch.write_file("options.json", json.dumps(options_dict).encode('utf-8'))


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(open(file_name, "rb").read())

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        # if basemd5.hexdigest() not in [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH, CVCOTM_VC_US_HASH]:
        if basemd5.hexdigest() not in [CVCOTM_CT_US_HASH, CVCOTM_AC_US_HASH]:
            raise Exception("Supplied Base ROM does not match known MD5s for Castlevania: Circle of the Moon USA."
                            "Get the correct game and version, then dump it.")
        setattr(get_base_rom_bytes, "base_rom_bytes", base_rom_bytes)
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    if not file_name:
        file_name = get_settings()["cvcotm_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
