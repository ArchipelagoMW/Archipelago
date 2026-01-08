from pathlib import Path
import random
try:  # Literal 3.8
    from typing import Literal, Optional, Type
except ImportError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
import time

try:  # container type annotations 3.9
    from .connection_data import SunkenNestL, area_doors, misc_doors, vanilla_areas
except TypeError:
    input("requires Python 3.9 or higher... press enter to quit")
    exit(1)
from .daphne_gate import get_daphne_gate, get_air_lock_bytes
from .fillForward import fill_major_minor
from .fillInterface import FillAlgorithm
from .game import CypherItems, Game, GameOptions
from .goal import generate_goals, goal_spoiler, write_goals
from .hints import choose_hint_location, get_hint_spoiler_text, write_hint_to_rom
from .item_data import Item, Items
from .item_marker import ItemMarkersOption, make_item_markers, write_item_markers
from .loadout import Loadout
from .location_data import Location, new_locations, spacePortLocs
from .logic_presets import casual, expert, medium
from . import logic_updater
from . import fillMedium
from . import fillMajorMinor
from . import fillAssumed
from . import fillSpeedrun
from . import areaRando
from .new_terrain_writer import TerrainWriter
from .open_escape import patch_open_escape
from .romWriter import RomWriter, RomWriterType
from .solver import hard_required_locations, required_tricks, solve, spoil_play_through
from .spaceport_door_data import shrink_spaceport, spaceport_doors
from .terrain_patch import Space
from .terrain_patch_data import hall_of_the_elders, subterranean, vulnar_caves_access_open_escape
from .trick import Trick
from .trick_data import Tricks

ORIGINAL_ROM_NAME = "Subversion12.sfc"


def plmidFromHiddenness(itemArray: Item, hiddenness: str) -> bytes:
    if hiddenness == "open":
        plmid = itemArray.visible
    elif hiddenness == "chozo":
        plmid = itemArray.chozo
    else:
        plmid = itemArray.hidden
    return plmid


def write_location(romWriter: RomWriter, location: Location) -> None:
    """
    provide a location with an ['item'] value, such as Missile, Super, etc
    write all rom locations associated with the item location
    """
    item = location["item"]
    assert item, f"{location['fullitemname']} didn't get an item"
    # TODO: support locations with no items?
    plmid = plmidFromHiddenness(item, location['hiddenness'])
    for address in location['locids']:
        romWriter.writeItem(address, plmid, item.ammo_qty)
    for address in location['alternateroomlocids']:
        if location['alternateroomdifferenthiddenness'] == "":
            # most of the alt rooms go here, having the same item hiddenness
            # as the corresponding "pre-item-move" item had
            plmid_altroom = plmid
        else:
            plmid_altroom = plmidFromHiddenness(item, location['alternateroomdifferenthiddenness'])
        romWriter.writeItem(address, plmid_altroom, item.ammo_qty)


fillers: dict[str, Type[FillAlgorithm]] = {
    "M": fillMedium.FillMedium,
    "MM": fillMajorMinor.FillMajorMinor,
    "S": fillSpeedrun.FillSpeedrun,
    "AF": fillAssumed.FillAssumed,
}


def verify_cypher_not_required(seedComplete: bool, game: Game) -> bool:
    saved_animate = game.all_locations["Shrine Of The Animate Spark"]["item"]
    saved_enervation = game.all_locations["Enervation Chamber"]["item"]
    game.all_locations["Shrine Of The Animate Spark"]["item"] = None
    game.all_locations["Enervation Chamber"]["item"] = None
    completable, _, _ = solve(game)
    game.all_locations["Shrine Of The Animate Spark"]["item"] = saved_animate
    game.all_locations["Enervation Chamber"]["item"] = saved_enervation
    if not completable:
        print("cypher requirement missing")
    return seedComplete and completable


def generate(options: GameOptions) -> Game:
    """ if generation fails, game.hint_data will be None """
    # hudFlicker=""
    # while hudFlicker != "Y" and hudFlicker != "N" :
    #     hudFlicker= input("Enter Y to patch HUD flicker on emulator, or N to decline:")
    #     hudFlicker = hudFlicker.title()
    seeeed = random.randint(1000000, 9999999)
    random.seed(seeeed)
    # you must include Subversion 1.2 in your roms folder with this name^

    all_locations = new_locations()

    seedComplete = False
    randomizeAttempts = 0
    start_time = time.perf_counter()
    game = Game(options,
                all_locations,
                vanilla_areas(),
                seeeed)
    while not seedComplete:
        if game.options.daphne_gate:
            daphne_blocks = get_daphne_gate(game.options)
            game.daphne_blocks = daphne_blocks

        if game.options.area_rando:  # area rando
            force_normal_early = (
                (
                    Tricks.movement_moderate not in game.options.logic or
                    Tricks.wave_gate_glitch not in game.options.logic
                ) and game.options.fill_choice == "MM"
            )
            game.door_pairs = areaRando.RandomizeAreas(force_normal_early)
            # print(Connections) #test

        if game.options.objective_rando > 0:
            game.goals = generate_goals(game.options)

        if time.perf_counter() - start_time > 70:
            print(f"Giving up after {randomizeAttempts} attempts. Help?")
            return game
        randomizeAttempts += 1
        print("Starting randomization attempt:", randomizeAttempts)
        game.item_placement_spoiler = f"Starting randomization attempt: {randomizeAttempts}\n"
        # now start randomizing
        if options.fill_choice in {"D", "B", "MM"}:
            if options.fill_choice == "MM" and randomizeAttempts > 15:
                seedComplete = fill_major_minor(game)
            else:
                seedComplete = assumed_fill(game)
        else:
            seedComplete = forward_fill(game)

        if game.options.cypher_items == CypherItems.NotRequired:
            seedComplete = verify_cypher_not_required(seedComplete, game)

    # make this optional?
    # If someone doesn't want hints, they can just not look at the log.
    # That doesn't work for competitive play,
    # but we can handle that if people start playing this competitively and want no hints.
    choose_hint_location(game)

    game.item_markers = make_item_markers(game.options.item_markers, game.all_locations.values())

    return game


def resolve_one_up_if_needed(rel_dir: Path, file_check: Optional[str] = None) -> Path:
    """
    looks for `rel_dir` either in the current working directory or in the parent (..)

    If `file_check` is given, it will also require that file to be in that directory.

    returns the relative directory found

    raises `FileNotFoundError` if not found
    """
    if rel_dir.exists() and (
        file_check is None or rel_dir.joinpath(file_check).exists()
    ):
        return rel_dir

    up_one = Path("..").joinpath(rel_dir)
    if up_one.exists() and (
        file_check is None or up_one.joinpath(file_check).exists()
    ):
        return up_one

    raise FileNotFoundError(f"can't find: {rel_dir if file_check is None else rel_dir.joinpath(file_check)}")


def write_rom(game: Game, romWriter: Optional[RomWriter] = None) -> str:
    logicChoice: Literal["E", "U", "C", "Q"] = "Q"
    if game.options.logic == casual:
        logicChoice = "C"
    elif game.options.logic == medium:
        logicChoice = "U"
    elif game.options.logic == expert:
        logicChoice = "E"

    areaA = ""
    if game.options.area_rando:
        areaA = "A"

    rom_name = f"Sub{logicChoice}{game.options.fill_choice}{areaA}{game.seed}.sfc"

    if romWriter is None:
        roms_path = resolve_one_up_if_needed(Path("roms"), ORIGINAL_ROM_NAME)
        rom1_path = roms_path.joinpath(rom_name)
        rom_clean_path = roms_path.joinpath(ORIGINAL_ROM_NAME)
        romWriter = RomWriter.fromFilePaths(orig_rom_path=rom_clean_path)
    else:
        # remove .sfc extension
        romWriter.setBaseFilename(rom_name[:-4])
        rom1_path = None

    write_locations(game, romWriter)
    apply_rom_patches(game, romWriter)

    romWriter.finalizeRom(rom1_path)

    print("Done!")
    print(f"Filename is {rom_name}")

    return rom_name


def write_locations(game: Game, romWriter: RomWriter) -> None:
    """
    write all items into their locations

    not compatible with multiworld
    """
    for loc in game.all_locations.values():
        write_location(romWriter, loc)


def apply_rom_patches(game: Game, romWriter: RomWriter) -> None:
    """
    - bestiary hint
    - area rando
    - suit animation skip
    - chozo and hidden for Morph PLM
    - skip intro
    - disable demos
    - area rando doors always flashing
    - loading dock always has elevator to space port
    - using mass driver uncrashes space port
    - open escape (no grey doors in escape path)
    - subterranean burrow terrain - anti-softlock
    - randomized wrecked daphne gate
    - lower water in Norak Brook
    - rotate save files
    - start with all maps
    - always show items on map
    - small spaceport
    - escape shortcuts
    - objective rando
    - skip crash space port
    """
    if game.hint_data:
        hint_loc_name, hint_loc_marker = game.hint_data
        write_hint_to_rom(hint_loc_name, hint_loc_marker, romWriter)

    if game.options.area_rando:
        areaRando.write_area_doors(game.door_pairs, romWriter)

    # Suit animation skip patch
    romWriter.writeBytes(0x20717, b"\xea\xea\xea\xea")
    # Flickering hud removal patch
    # if hudFlicker == "Y" :
    #     writeBytes(0x547a, b"\x02")
    #     writeBytes(0x547f, b"\x00")
    # Morph Ball PLM patch (chozo, hidden)
    romWriter.writeBytes(0x268ce, b"\x04")
    romWriter.writeBytes(0x26e02, b"\x04")
    # skip intro (asm edits) TODO turn this into asm and a proper hook
    romWriter.writeBytes(0x16eda, b"\x1f")  # initial game state set by $82:eeda
    romWriter.writeBytes(0x16ee0, b"\x06\x00")  # initial game area = 6 (ceres)
    romWriter.writeBytes(0x16ee3, b"\x9f\x07")  # $079f Area index
    romWriter.writeBytes(0x16ee5, b"\xa9\x05\x00\x8f\x14\xd9\x7e\xea\xea")  # $7e:d914 = 05 Main
    romWriter.writeBytes(0x16eee, b"\xad\x52\x09\x22\x00\x80\x81")  # jsl save game (param in A: save slot)
    romWriter.writeBytes(0x16ed0, b"\x24")  # adjust earlier branch to go +6 bytes later to rts
    romWriter.writeBytes(0x16ed8, b"\x1c")  # adjust earlier branch to go +6 bytes later to rts
    # disable demos (asm opcode edit). because the demos show items
    romWriter.writeBytes(0x59f29, b"\xad")
    # make always flashing doors out of vanilla gray 'animals saved' doors:
    #   edit in function $84:BE30 'gray door pre: go to link instruction if critters escaped',
    #   which is vanilla and probably not used anyway
    #   use by writing 0x18 to the high byte of a gray door plm param, OR'ed with the low bit of the 9-low-bits id part
    romWriter.writeBytes(0x23e33, b"\x38\x38\x38\x38")  # set the carry bit (a lot)

    tw = TerrainWriter(romWriter)

    # loading dock always has elevator to space port
    # state header pointer copied from un-crashed power on state condition
    romWriter.writeBytes(0x7b688, b"\xb0")  # crashed power on state condition - pointer to state header - lo byte
    # new state header pointer created to default state header (un-crashed power off)
    romWriter.writeBytes(0x7b68d, b"\x96")  # crashed power off state condition - pointer to state header - lo byte
    # state headers pointed to by the original state conditions are now unused (b6e4, b6ca)
    # so their level data (without elevator) is now unused
    # (2 sections of data are contiguous - 2115097 size 893 and 2115992 size 902)
    tw.add_space(Space(1797, 2115097))

    # mass driver un-crashes space port
    # door from loading dock into mass driver points to some asm
    location_of_pointer_to_asm = 0x1bb06
    assert (
        romWriter.romWriterType == RomWriterType.ipsblob or
        romWriter.rom_data[location_of_pointer_to_asm:location_of_pointer_to_asm+2] == b"\x4c\xa8"
    )
    # we're going to point it to some different asm
    # in some free space at 7f56d
    # TODO: verify this space is free with multiworld patch
    dest = 0x7f56d
    romWriter.writeBytes(location_of_pointer_to_asm, bytearray([dest & 0xff, (dest // 256) & 0xff]))
    new_code = (
        b"\xa9\x1d\x00"      # lda 001d    (crash spaceport event)
        b"\x22\x12\x82\x80"  # jsl 808212  (unset event)
        b"\x4c\x4c\xa8"      # JMP a84c    (to the original door asm)
    )
    assert (
        romWriter.romWriterType == RomWriterType.ipsblob or
        all(b == 0xff for b in romWriter.rom_data[dest:dest + len(new_code)])
    ), f"data expected to be empty {romWriter.rom_data[dest:dest + len(new_code)]}"
    romWriter.writeBytes(dest, new_code)

    # TODO: verify objective rando log completion matches space port crash requirement (after un-crash)

    # romWriter.apply_IPS('open_escape.ips')  # TODO: MB room lag from explosions and shaking during fight
    patch_open_escape(romWriter)
    tw.write(vulnar_caves_access_open_escape)

    tw.write(subterranean)
    tw.write(hall_of_the_elders)

    if game.options.daphne_gate:
        wrecked, non_default, default = get_air_lock_bytes(game.daphne_blocks)
        tw.write(non_default)
        tw.write(default)
        tw.write(wrecked)

        # harder to go left through speed blocks
        if (game.daphne_blocks.one == "Speed" and not (  # speed on top
            # horizontal shinespark from broken platform before door
            Tricks.short_charge_2 in game.options.logic and
            Tricks.movement_moderate in game.options.logic
        )) or (game.daphne_blocks.two == "Speed" and not (  # speed on bottom
            # mockball over broken platform before door
            Tricks.short_charge_3 in game.options.logic and
            Tricks.mockball_hard in game.options.logic
        )):
            romWriter.connect_doors(misc_doors["WreckedCrewQuartersAccessL"], misc_doors["RockyRidgeR"], one_way=True)

    # lower the water slightly in norak brook, to get up without aqua suit
    # (because it's too easy to go down without thinking about it)
    # This is the lower byte of "Base Y position"
    # in the FX (18ea0) of the State Headers of Norak Brook (8be5)
    romWriter.writeBytes(0x18ea2, b'\xbb')  # changed from a7

    # rotate save files and get all maps
    # (I figured this was an ok combination
    # because the game is automatically saved when you start a new game,
    # so if I get all the maps every time I save, I get all the maps at the beginning.)
    new_save_code = (
        # get all maps
        b'\xa9\xff\xff'      # LDA #$FFFF
        b'\x8d\x89\x07'      # STA $0789    ; have map for current area
        b'\x8F\x08\xD9\x7E'  # STA $7ED908  ; maps for each region
        b'\x8F\x0A\xD9\x7E'  # STA $7ED90A
        b'\x8F\x0C\xD9\x7E'  # STA $7ED90C
        b'\x8F\x0E\xD9\x7E'  # STA $7ED90E

        # rotate save slots
        b'\xad\x52\x09'      # lda $0952  # save slot
        b'\xc9\x02\x00'      # cmp #$0002
        b'\x30\x03'          # bmi 03
        b'\xa9\xff\xff'      # lda #$ffff
        b'\x1a'              # inc
        b'\x8d\x52\x09'      # sta $0952
        b'\x4c\x35\xef'      # jmp $ef35  # the place where 818000 originally jumped to
    )
    unused_space = 0xff60
    assert all(b == 0xff for b in romWriter.rom_data[unused_space: unused_space + len(new_save_code)]), (
        "new code overflow"
    )
    romWriter.writeBytes(
        unused_space,
        new_save_code
    )
    new_save_code_address = unused_space.to_bytes(2, "little")
    romWriter.writeBytes(
        0x8000,                          # save code
        b'\x4c' + new_save_code_address  # jmp that code above  (changed from jmp $ef35)
    )

    # always show items on map
    # changing BCS (branch if carry set 0xb0) to BRA (branch always 0x80)
    # MapColors.asm - .not_collected
    romWriter.writeBytes(0xdd57f, b"\x80")
    # MapColors.asm - .circle
    romWriter.writeBytes(0xdd647, b"\x80")

    if game.options.item_markers == ItemMarkersOption.ThreeTiered:
        patch_3_tier_icons_before_collect(romWriter)
    else:
        # assert_type(game.options.item_markers, Literal[ItemMarkersOption.Simple])
        patch_major_minor_icons_before_collect(romWriter)
    write_item_markers(romWriter, game.item_markers)

    if game.options.small_spaceport:
        romWriter.writeBytes(0x106283, b'\x71\x01')  # zebetite health
        romWriter.writeBytes(0x204b3, b'\x08')  # fake zebetite hits taken
        shrink_spaceport(romWriter)

    if game.options.escape_shortcuts:
        romWriter.connect_doors(spaceport_doors['BridgeL'], spaceport_doors['StationCorridorBR'], one_way=True)
        if not game.options.area_rando:
            romWriter.connect_doors(misc_doors["AuroraUnitWreckageL"], area_doors["CraterR"], one_way=True)

    if game.options.objective_rando > 0:
        romWriter.apply_IPS('objective_rando.ips')
        write_goals(game.goals, romWriter)

    if game.options.skip_crash():
        # Crash GFS Daphne room starts in crashed state
        romWriter.writeBytes(0x07BAA1, b'\x35\xE6')  # also use state (skip test for state 1D)
        # Wrecked Engineering Room uses escape level data to remove PB requirement
        romWriter.writeBytes(0x07E06B, b'\x7D\xCB\xC6')  # change level data pointer


def patch_major_minor_icons_before_collect(romWriter: RomWriter) -> None:
    """
    - show the large filled in circle for an uncollected major item
    - show the large unfilled circle for am uncollected minor item
    - show small dots for all collected items
    """
    # MapColors.asm

    # full map

    # .collected  BRA branch always to small dot
    romWriter.writeBytes(0xdd567, b"\x80")  # BEQ f0 -> BRA 80
    # new code for .not_collected
    romWriter.writeBytes(
        0xdd578,
        b"\x80\x05\xea\xea\xea\xea\xea"  # fill existing space with BRA NOP
        b"\xbd\x06\x00"  # LDA $0006,X          ; minor or major
        b"\xf0\x0b"      # BEQ +                ; if minor, goto after this
        # else major item
        b"\x20\xb9\xd5"  # JSR GetTilemapIndex
        b"\x20\x8c\xd8"  # JSR LoadTile4bpp
        b"\x20\xe0\xd8"  # JSR DrawTilePlus
        b"\x80\x09"      # BRA ++               ; jump over minor
    )

    # mini map

    # .dot (collected)  BRA branch always to small dot
    romWriter.writeBytes(0xdd634, b"\x80")  # BEQ f0 -> BRA 80
    # .circle (not collected)  new code
    romWriter.writeBytes(
        0xdd640,
        b"\x80\x0b\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea"  # fill existing space with BRA NOP
        b"\xbd\x06\x00"  # LDA $0006,X          ; minor or major
        b"\xf0\x05"      # BEQ +                ; if minor, goto after this
        # else major item
        b"\xa9\x00\x08"  # LDA #$0800           ; major big dot
        b"\x80\x03"      # BRA ++               ; jump over minor
    )


def patch_3_tier_icons_before_collect(romWriter: RomWriter) -> None:
    """
    - show the large filled in circle for item classification 1
    - show the large unfilled circle for item classification 0
    - show small dots for item classification 2
    - collected item shows nothing
    """
    # MapColors.asm

    # full map

    # new code for .itemloop - starting at `BEQ .not_collected ; test if collected``
    romWriter.writeBytes(
        0xdd54c,
        b"\x80\x0e\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea\xea"  # fill existing space with BRA NOP

        b"\xf0\x19"          # BEQ .not_collected ; test if collected

        # .collected
        b"\xfa\xda"          # PLX : PHX

        b"\x20\xb9\xd5"      # JSR GetTilemapIndex
        b"\xbf\x00\x40\x7e"	 # LDA $7E4000,X
        b"\x29\xee\x03"      # AND #$03EE
        b"\xc9\x0e\x00"      # CMP #$000E ; blank tiles: 0x000E, 0x000F, 0x001E, 0x001F
        b"\xf0\x2c"          # BEQ .continue

        b"\x20\x8c\xd8"      # JSR LoadTile4bpp
        b"\x20\x0c\xd9"      # JSR DMATile4bpp

        b"\x80\x24"          # BRA .continue

        # .not_collected
        b"\xfa\xda"      # PLX : PHX

        b"\x20\xb9\xd5"  # JSR GetTilemapIndex
        b"\x20\x8c\xd8"  # JSR LoadTile4bpp
        b"\xfa\xda"      # PLX : PHX
        b"\xbd\x06\x00"  # LDA $0006,X          ; minor or major
        b"\xf0\x0f"      # BEQ "0"              ; if "0", goto after all this
        b"\x29\x02\x00"  # AND #$0002
        b"\xd0\x05"      # BNE "2"
        # else "1"
        b"\x20\xe0\xd8"  # JSR DrawTilePlus
        b"\x80\x08"      # BRA ++               ; jump over others
        # ; "2"
        b"\x20\xca\xd8"  # JSR DrawTileDot
        b"\x80\x03"      # BRA ++               ; jump over "0"
        # dd595 ; "0"
        # JSR DrawTileCircle  20 f6 d8
        # ++
        # JSR DMATile4bpp     20 0c d9
        # .continue
    )

    # mini map

    # .dot (collected)  BRA branch always to .blank
    romWriter.writeBytes(0xdd62f, b"\x80")  # BEQ f0 -> BRA 80
    # .circle (not collected)  new code
    romWriter.writeBytes(
        0xdd640,
        b"\xea\xea\xea"  # fill existing space with NOP
        b"\xbd\x06\x00"  # LDA $0006,X          ; 0, 1, 2
        b"\xf0\x0f"      # BEQ "0"              ; if minor, goto after this
        b"\x29\x02\x00"  # AND #$0002
        b"\xd0\x05"      # BNE "2"
        # else "1"
        b"\xa9\x00\x08"  # LDA #$0800           ; major big dot
        b"\x80\x08"      # BRA ++               ; jump over minor
        # "2"
        b"\xa9\x00\x04"  # LDA #$0400           ; small dot
        b"\x80\x03"      # BRA ++               ; jump over minor

        # after this
        # + "0"
        # LDA #$0200  ; uncollected circle
        # ++
        # BRA .return
    )


def get_spoiler(game: Game) -> str:
    """ the text in the spoiler file """

    spoilerSave = game.item_placement_spoiler + '\n'

    # add area transitions to spoiler
    if game.options.area_rando:
        for door1, door2 in game.door_pairs.connections():
            spoilerSave += f"{door1.area_name} {door1.name} << >> {door2.area_name} {door2.name}\n"
        spoilerSave += "\n"
        spoilerSave += " --- possible escape path ---\n"
        path = areaRando.escape_path(game.door_pairs)
        if path is None:
            spoilerSave += "path error\n"
        else:
            for door in path:
                spoilerSave += f"  {door}\n"

    if game.hint_data:
        hint_loc_name, hint_loc_marker = game.hint_data
        spoilerSave += get_hint_spoiler_text(hint_loc_name, hint_loc_marker)

    _completable, play_through, _locs = solve(game)
    solve_lines = spoil_play_through(play_through)

    s = f"RNG Seed: {game.seed}\n\n"
    s += "\n Spoiler \n\n Spoiler \n\n Spoiler \n\n Spoiler \n\n"
    s += spoilerSave
    s += '\n\n'
    for solve_line in solve_lines:
        s += solve_line + '\n'
    s += '\n\n'
    s += required_locations_spoiler(game)
    s += '\n'
    s += daphne_gate_spoiler(game)
    s += '\n'
    s += goal_spoiler(game.goals)
    s += '\n'
    s += required_tricks_spoiler(game)
    s += '\n'
    s += logic_tricks_spoiler(game)
    s += '\n'

    return s


def write_spoiler_file(game: Game, rom_name: str) -> None:
    text = get_spoiler(game)
    spoiler_dir = resolve_one_up_if_needed(Path("spoilers"))
    spoiler_file_name = f"{rom_name}.spoiler.txt"
    spoiler_path = spoiler_dir.joinpath(spoiler_file_name)
    with open(spoiler_path, "w") as spoiler_file:
        spoiler_file.write(text)
    print(f"Spoiler file is {spoiler_path}")


def required_locations_spoiler(game: Game) -> str:
    spoiler_text = "hard required locations:\n"
    req_locs, _ = hard_required_locations(game)
    for loc_name in req_locs:
        item = game.all_locations[loc_name]['item']
        item_name = item.name if item else "Nothing"
        spoiler_text += f"  {loc_name}  --  {item_name}\n"
    return spoiler_text


def daphne_gate_spoiler(game: Game) -> str:
    return f"wrecked daphne gate requires: {game.daphne_blocks.one} or {game.daphne_blocks.two}\n"


def required_tricks_spoiler(game: Game) -> str:
    for_win, for_locs = required_tricks(game)
    spoiler_text = "tricks required to win:\n"
    for trick_name in for_win:
        spoiler_text += f"  {trick_name}\n"
    spoiler_text += "\ntricks required to reach all locations:\n"
    for trick_name in for_locs:
        spoiler_text += f"  {trick_name}\n"
    return spoiler_text


def logic_tricks_spoiler(game: Game) -> str:
    spoiler_text = "tricks allowed in this logic:\n"
    for trick_name, trick in vars(Tricks).items():
        if isinstance(trick, Trick) and trick in game.options.logic:
            spoiler_text += f'    "{trick_name}",\n'
    return spoiler_text


def assumed_fill(game: Game) -> bool:
    for loc in game.all_locations.values():
        loc["item"] = None
    dummy_locations: list[Location] = []
    loadout = Loadout(game)
    fill_algorithm = fillAssumed.FillAssumed(game.door_pairs)

    if game.options.cypher_items == CypherItems.SmallAmmo and game.options.fill_choice != "MM":
        game.all_locations["Shrine Of The Animate Spark"]["item"] = Items.SmallAmmo
        game.all_locations["Enervation Chamber"]["item"] = Items.SmallAmmo
        fill_algorithm.extra_items.remove(Items.SmallAmmo)
        fill_algorithm.extra_items.remove(Items.SmallAmmo)
        game.item_placement_spoiler += f"Shrine Of The Animate Spark - - - {Items.SmallAmmo.name}\n"
        game.item_placement_spoiler += f"Enervation Chamber - - - {Items.SmallAmmo.name}\n"

    if game.options.fill_choice == "MM":  # major/minor
        first, second = Items.Missile, Items.GravityBoots
        if Tricks.wave_gate_glitch in game.options.logic and random.random() < 0.5:
            first, second = second, first
        game.all_locations["Torpedo Bay"]["item"] = first
        game.all_locations["Subterranean Burrow"]["item"] = second
        fill_algorithm.prog_items.remove(first)
        fill_algorithm.prog_items.remove(second)
        game.item_placement_spoiler += f"Torpedo Bay - - - {first.name}\n"
        game.item_placement_spoiler += f"Subterranean Burrow - - - {second.name}\n"

    n_items_to_place = fill_algorithm.count_items_remaining()
    assert n_items_to_place <= len(game.all_locations), \
        f"{n_items_to_place} items to put in {len(game.all_locations)} locations"
    print(f"{fill_algorithm.count_items_remaining()} items to place")
    while fill_algorithm.count_items_remaining():
        placePair = fill_algorithm.choose_placement(dummy_locations, loadout)
        if placePair is None:
            message = ('Item placement was not successful in assumed. '
                       f'{fill_algorithm.count_items_remaining()} items remaining.')
            print(message)
            game.item_placement_spoiler += f'{message}\n'
            break
        placeLocation, placeItem = placePair
        # if placeItem in {Items.Morph, Items.Bombs, Items.Speedball, Items.PowerBomb}:
        #     print(f"DEBUG: placing {placeItem.name} in {placeLocation['fullitemname']}")
        placeLocation["item"] = placeItem
        game.item_placement_spoiler += f"{placeLocation['fullitemname']} - - - {placeItem.name}\n"

        if fill_algorithm.count_items_remaining() == 0:
            # Normally, assumed fill will always make a valid playthrough,
            # but dropping from spaceport can mess that up,
            # so it needs to be checked again.
            completable, _, accessible_locations = solve(game)
            done = completable and len(accessible_locations) == len(game.all_locations)
            if done:
                print("Item placements successful.")
                game.item_placement_spoiler += "Item placements successful.\n"
            return done

    return False


def forward_fill(game: Game) -> bool:
    unusedLocations: list[Location] = []
    unusedLocations.extend(game.all_locations.values())
    availableLocations: list[Location] = []
    # visitedLocations = []
    loadout = Loadout(game)
    loadout.append(SunkenNestL)  # starting area
    # use appropriate fill algorithm for initializing item lists
    fill_algorithm = fillers[game.options.fill_choice](game.door_pairs)
    while len(unusedLocations) != 0 or len(availableLocations) != 0:
        # print("loadout contains:")
        # print(loadout)
        # for a in loadout:
        #     print("-",a[0])
        # update logic by updating unusedLocations
        # using helper function, modular for more logic options later
        # unusedLocations[i]['inlogic'] holds the True or False for logic
        logic_updater.updateLogic(unusedLocations, loadout)

        # update unusedLocations and availableLocations
        for i in reversed(range(len(unusedLocations))):  # iterate in reverse so we can remove freely
            if unusedLocations[i]['inlogic'] is True:
                # print("Found available location at",unusedLocations[i]['fullitemname'])
                availableLocations.append(unusedLocations[i])
                unusedLocations.pop(i)
        # print("Available locations sits at:",len(availableLocations))
        # for al in availableLocations :
        #     print(al[0])
        # print("Unused locations sits at size:",len(unusedLocations))
        # print("unusedLocations:")
        # for u in unusedLocations :
        #     print(u['fullitemname'])

        if availableLocations == [] and unusedLocations != []:
            print(f'Item placement was not successful. {len(unusedLocations)} locations remaining.')
            game.item_placement_spoiler += \
                f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            # for i in loadout:
            #     print(i[0])
            # for u in unusedLocations :
            #     print("--",u['fullitemname'])

            break

        placePair = fill_algorithm.choose_placement(availableLocations, loadout)
        if placePair is None:
            print(f'Item placement was not successful due to majors. {len(unusedLocations)} locations remaining.')
            game.item_placement_spoiler += \
                f'Item placement was not successful. {len(unusedLocations)} locations remaining.\n'
            break
        # it returns your location and item, which are handled here
        placeLocation, placeItem = placePair
        if (placeLocation in unusedLocations):
            unusedLocations.remove(placeLocation)
        placeLocation["item"] = placeItem
        availableLocations.remove(placeLocation)
        fill_algorithm.remove_from_pool(placeItem)
        loadout.append(placeItem)
        if not ((placeLocation['fullitemname'] in spacePortLocs) or (Items.spaceDrop in loadout)):
            loadout.append(Items.spaceDrop)
        game.item_placement_spoiler += f"{placeLocation['fullitemname']} - - - {placeItem.name}\n"
        # print(placeLocation['fullitemname']+placeItem.name)

        if availableLocations == [] and unusedLocations == []:
            print("Item placements successful.")
            game.item_placement_spoiler += "Item placements successful.\n"
            return True
    return False
