from collections.abc import Callable
from os import PathLike

from .rom import Rom
from .zm.auto_generated_types import MarsSchemaZM


def patch_zm(
    rom: Rom,
    output_path: str | PathLike[str],
    patch_data: MarsSchemaZM,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized Zero Mission game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        input_path: The path to an unmodified Metroid Zero Mission (U) ROM.
        output_path: The path where the randomized Zero Mission ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
            This function assumes that it satisfies the needed schema. To validate it, use
            validate_patch_data_zm().
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Apply base patch first
    # apply_base_patch(rom)

    # Randomize palettes - palettes are randomized first since the item
    # patcher needs to copy tilesets
    # if "Palettes" in patch_data:
    #     status_update("Randomizing palettes...", -1)
    #     pal_settings = PaletteSettings.from_json(patch_data["Palettes"])
    #     pal_randomizer = PaletteRandomizer(rom, pal_settings)
    #     pal_randomizer.randomize()

    # Load locations and set assignments
    # status_update("Writing item assignments...", -1)
    # loc_settings = LocationSettings.initialize()
    # loc_settings.set_assignments(patch_data["Locations"])
    # item_patcher = ItemPatcher(rom, loc_settings)
    # item_patcher.write_items()

    # Required metroid count
    # set_required_metroid_count(rom, patch_data["RequiredMetroidCount"])

    # Starting location
    # if "StartingLocation" in patch_data:
    #     status_update("Writing starting location...", -1)
    # set_starting_location(rom, patch_data["StartingLocation"])

    # Starting items
    # if "StartingItems" in patch_data:
    #     status_update("Writing starting items...", -1)
    # set_starting_items(rom, patch_data["StartingItems"])

    # Tank increments
    # if "TankIncrements" in patch_data:
    #     status_update("Writing tank increments...", -1)
    # set_tank_increments(rom, patch_data["TankIncrements"])

    # Elevator connections
    # conns = None
    # if "ElevatorConnections" in patch_data:
    #     status_update("Writing elevator connections...", -1)
    #     conns = Connections(rom)
    #     conns.set_elevator_connections(patch_data["ElevatorConnections"])

    # Hints
    # TODO

    # Room Names
    # if room_names := patch_data.get("RoomNames", []):
    #     status_update("Writing room names...", -1)
    #     write_room_names(rom, room_names)

    # Credits
    # if credits_text := patch_data.get("CreditsText", []):
    #     status_update("Writing credits text...", -1)
    #     write_credits(rom, credits_text)

    # Misc patches
    # if patch_data.get("AccessibilityPatches"):
    #     apply_accessibility_patch(rom)

    # if patch_data.get("DisableDemos"):
    #     disable_demos(rom)

    # if patch_data.get("SkipDoorTransitions"):
    #     skip_door_transitions(rom)

    # if patch_data.get("StereoDefault", True):
    #     stereo_default(rom)

    # if patch_data.get("DisableMusic"):
    #     disable_music(rom)

    # if patch_data.get("DisableSoundEffects"):
    #     disable_sound_effects(rom)

    # if patch_data.get("UnexploredMap"):
    #     apply_unexplored_map(rom)

    #     if not patch_data.get("HideDoorsOnMinimap", False):
    #         apply_reveal_unexplored_doors(rom)

    # if patch_data.get("RevealHiddenTiles"):
    #     apply_reveal_hidden_tiles(rom)

    # if "LevelEdits" in patch_data:
    #     apply_level_edits(rom, patch_data["LevelEdits"])

    # Apply base minimap edits
    # apply_base_minimap_edits(rom)

    # Apply JSON minimap edits
    # if "MinimapEdits" in patch_data:
    #     apply_minimap_edits(rom, patch_data["MinimapEdits"])

    # Door locks
    # if door_locks := patch_data.get("DoorLocks", []):
    #     status_update("Writing door locks...", -1)
    #     set_door_locks(rom, door_locks)

    # write_seed_hash(rom, patch_data["SeedHash"])

    # Title-screen text
    # if title_screen_text := patch_data.get("TitleText"):
    #     status_update("Writing title screen text...", -1)
    # write_title_text(rom, title_screen_text)

    rom.save(output_path)
    status_update(f"Output written to {output_path}", -1)
