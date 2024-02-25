import binascii
import importlib.util
import importlib.machinery
import os
import pkgutil
from collections import defaultdict

from .romTables import ROMWithTables
from . import assembler
from . import mapgen
from . import patches
from .patches import overworld as _
from .patches import dungeon as _
from .patches import entrances as _
from .patches import enemies as _
from .patches import titleScreen as _
from .patches import aesthetics as _
from .patches import music as _
from .patches import core as _
from .patches import phone as _
from .patches import photographer as _
from .patches import owl as _
from .patches import bank3e as _
from .patches import bank3f as _
from .patches import inventory as _
from .patches import witch as _
from .patches import tarin as _
from .patches import fishingMinigame as _
from .patches import softlock as _
from .patches import maptweaks as _
from .patches import chest as _
from .patches import bomb as _
from .patches import rooster as _
from .patches import shop as _
from .patches import trendy as _
from .patches import goal as _
from .patches import hardMode as _
from .patches import weapons as _
from .patches import health as _
from .patches import heartPiece as _
from .patches import droppedKey as _
from .patches import goldenLeaf as _
from .patches import songs as _
from .patches import bowwow as _
from .patches import desert as _
from .patches import reduceRNG as _
from .patches import madBatter as _
from .patches import tunicFairy as _
from .patches import seashell as _
from .patches import instrument as _
from .patches import endscreen as _
from .patches import save as _
from .patches import bingo as _
from .patches import multiworld as _
from .patches import tradeSequence as _
from . import hints

from .patches import bank34
from .utils import formatText
from ..Options import TrendyGame, Palette
from .roomEditor import RoomEditor, Object
from .patches.aesthetics import rgb_to_bin, bin_to_rgb

from .locations.keyLocation import KeyLocation

from BaseClasses import ItemClassification
from ..Locations import LinksAwakeningLocation
from ..Options import TrendyGame, Palette, MusicChangeCondition


# Function to generate a final rom, this patches the rom with all required patches
def generateRom(args, settings, ap_settings, auth, seed_name, logic, rnd=None, multiworld=None, player_name=None, player_names=[], player_id = 0):
    rom_patches = []

    rom = ROMWithTables(args.input_filename, rom_patches)
    rom.player_names = player_names
    pymods = []
    if args.pymod:
        for pymod in args.pymod:
            spec = importlib.util.spec_from_loader(pymod, importlib.machinery.SourceFileLoader(pymod, pymod))
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            pymods.append(module)
    for pymod in pymods:
        pymod.prePatch(rom)

    if settings.gfxmod:
        patches.aesthetics.gfxMod(rom, os.path.join("data", "sprites", "ladx", settings.gfxmod))

    item_list = [item for item in logic.iteminfo_list if not isinstance(item, KeyLocation)]

    assembler.resetConsts()
    assembler.const("INV_SIZE", 16)
    assembler.const("wHasFlippers", 0xDB3E)
    assembler.const("wHasMedicine", 0xDB3F)
    assembler.const("wTradeSequenceItem", 0xDB40)  # we use it to store flags of which trade items we have
    assembler.const("wTradeSequenceItem2", 0xDB7F)  # Normally used to store that we have exchanged the trade item, we use it to store flags of which trade items we have
    assembler.const("wSeashellsCount", 0xDB41)
    assembler.const("wGoldenLeaves", 0xDB42)  # New memory location where to store the golden leaf counter
    assembler.const("wCollectedTunics", 0xDB6D)  # Memory location where to store which tunic options are available
    assembler.const("wCustomMessage", 0xC0A0)

    # We store the link info in unused color dungeon flags, so it gets preserved in the savegame.
    assembler.const("wLinkSyncSequenceNumber", 0xDDF6)
    assembler.const("wLinkStatusBits", 0xDDF7)
    assembler.const("wLinkGiveItem", 0xDDF8)
    assembler.const("wLinkGiveItemFrom", 0xDDF9)
    assembler.const("wLinkSendItemRoomHigh", 0xDDFA)
    assembler.const("wLinkSendItemRoomLow", 0xDDFB)
    assembler.const("wLinkSendItemTarget", 0xDDFC)
    assembler.const("wLinkSendItemItem", 0xDDFD)

    assembler.const("wZolSpawnCount", 0xDE10)
    assembler.const("wCuccoSpawnCount", 0xDE11)
    assembler.const("wDropBombSpawnCount", 0xDE12)
    assembler.const("wLinkSpawnDelay", 0xDE13)

    #assembler.const("HARDWARE_LINK", 1)
    assembler.const("HARD_MODE", 1 if settings.hardmode != "none" else 0)

    patches.core.cleanup(rom)
    patches.save.singleSaveSlot(rom)
    patches.phone.patchPhone(rom)
    patches.photographer.fixPhotographer(rom)
    patches.core.bugfixWrittingWrongRoomStatus(rom)
    patches.core.bugfixBossroomTopPush(rom)
    patches.core.bugfixPowderBagSprite(rom)
    patches.core.fixEggDeathClearingItems(rom)
    patches.core.disablePhotoPrint(rom)
    patches.core.easyColorDungeonAccess(rom)
    patches.owl.removeOwlEvents(rom)
    patches.enemies.fixArmosKnightAsMiniboss(rom)
    patches.bank3e.addBank3E(rom, auth, player_id, player_names)
    patches.bank3f.addBank3F(rom)
    patches.bank34.addBank34(rom, item_list)
    patches.core.removeGhost(rom)
    patches.core.fixMarinFollower(rom)
    patches.core.fixWrongWarp(rom)
    patches.core.alwaysAllowSecretBook(rom)
    patches.core.injectMainLoop(rom)

    from ..Options import ShuffleSmallKeys, ShuffleNightmareKeys

    if ap_settings["shuffle_small_keys"] != ShuffleSmallKeys.option_original_dungeon or  ap_settings["shuffle_nightmare_keys"] != ShuffleNightmareKeys.option_original_dungeon:
        patches.inventory.advancedInventorySubscreen(rom)
    patches.inventory.moreSlots(rom)
    if settings.witch:
        patches.witch.updateWitch(rom)
    patches.softlock.fixAll(rom)
    patches.maptweaks.tweakMap(rom)
    patches.chest.fixChests(rom)
    patches.shop.fixShop(rom)
    patches.rooster.patchRooster(rom)
    patches.trendy.fixTrendy(rom)
    patches.droppedKey.fixDroppedKey(rom)
    patches.madBatter.upgradeMadBatter(rom)
    patches.tunicFairy.upgradeTunicFairy(rom)
    patches.tarin.updateTarin(rom)
    patches.fishingMinigame.updateFinishingMinigame(rom)
    patches.health.upgradeHealthContainers(rom)
    if settings.owlstatues in ("dungeon", "both"):
        patches.owl.upgradeDungeonOwlStatues(rom)
    if settings.owlstatues in ("overworld", "both"):
        patches.owl.upgradeOverworldOwlStatues(rom)
    patches.goldenLeaf.fixGoldenLeaf(rom)
    patches.heartPiece.fixHeartPiece(rom)
    patches.seashell.fixSeashell(rom)
    patches.instrument.fixInstruments(rom)
    patches.seashell.upgradeMansion(rom)
    patches.songs.upgradeMarin(rom)
    patches.songs.upgradeManbo(rom)
    patches.songs.upgradeMamu(rom)
    if settings.tradequest:
        patches.tradeSequence.patchTradeSequence(rom, settings.boomerang)
    else:
        # Monkey bridge patch, always have the bridge there.
        rom.patch(0x00, 0x333D, assembler.ASM("bit 4, e\njr Z, $05"), b"", fill_nop=True)
    patches.bowwow.fixBowwow(rom, everywhere=settings.bowwow != 'normal')
    if settings.bowwow != 'normal':
        patches.bowwow.bowwowMapPatches(rom)
    patches.desert.desertAccess(rom)
    if settings.overworld == 'dungeondive':
        patches.overworld.patchOverworldTilesets(rom)
        patches.overworld.createDungeonOnlyOverworld(rom)
    elif settings.overworld == 'nodungeons':
        patches.dungeon.patchNoDungeons(rom)
    elif settings.overworld == 'random':
        patches.overworld.patchOverworldTilesets(rom)
        mapgen.store_map(rom, logic.world.map)
    #if settings.dungeon_items == 'keysy':
    #    patches.dungeon.removeKeyDoors(rom)
    # patches.reduceRNG.slowdownThreeOfAKind(rom)
    patches.reduceRNG.fixHorseHeads(rom)
    patches.bomb.onlyDropBombsWhenHaveBombs(rom)
    if ap_settings['music_change_condition'] == MusicChangeCondition.option_always:
        patches.aesthetics.noSwordMusic(rom)
    patches.aesthetics.reduceMessageLengths(rom, rnd)
    patches.aesthetics.allowColorDungeonSpritesEverywhere(rom)
    if settings.music == 'random':
        patches.music.randomizeMusic(rom, rnd)
    elif settings.music == 'off':
        patches.music.noMusic(rom)
    if settings.noflash:
        patches.aesthetics.removeFlashingLights(rom)
    if settings.hardmode == "oracle":
        patches.hardMode.oracleMode(rom)
    elif settings.hardmode == "hero":
        patches.hardMode.heroMode(rom)
    elif settings.hardmode == "ohko":
        patches.hardMode.oneHitKO(rom)
    if settings.superweapons:
        patches.weapons.patchSuperWeapons(rom)
    if settings.textmode == 'fast':
        patches.aesthetics.fastText(rom)
    if settings.textmode == 'none':
        patches.aesthetics.fastText(rom)
        patches.aesthetics.noText(rom)
    if not settings.nagmessages:
        patches.aesthetics.removeNagMessages(rom)
    if settings.lowhpbeep == 'slow':
        patches.aesthetics.slowLowHPBeep(rom)
    if settings.lowhpbeep == 'none':
        patches.aesthetics.removeLowHPBeep(rom)
    if 0 <= int(settings.linkspalette):
        patches.aesthetics.forceLinksPalette(rom, int(settings.linkspalette))
    if args.romdebugmode:
        # The default rom has this build in, just need to set a flag and we get this save.
        rom.patch(0, 0x0003, "00", "01")

    # Patch the sword check on the shopkeeper turning around.
    if settings.steal == 'never':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0000")
    elif settings.steal == 'always':
        rom.patch(4, 0x36F9, "FA4EDB", "3E0100")

    if settings.hpmode == 'inverted':
        patches.health.setStartHealth(rom, 9)
    elif settings.hpmode == '1':
        patches.health.setStartHealth(rom, 1)

    patches.inventory.songSelectAfterOcarinaSelect(rom)
    if settings.quickswap == 'a':
        patches.core.quickswap(rom, 1)
    elif settings.quickswap == 'b':
        patches.core.quickswap(rom, 0)

    world_setup = logic.world_setup

    JUNK_HINT = 0.33
    RANDOM_HINT= 0.66
    # USEFUL_HINT = 1.0
    # TODO: filter events, filter unshuffled keys
    all_items = multiworld.get_items()
    our_items = [item for item in all_items if item.player == player_id and item.location and item.code is not None and item.location.show_in_spoiler]
    our_useful_items = [item for item in our_items if ItemClassification.progression in item.classification]

    def gen_hint():
        chance = rnd.uniform(0, 1)
        if chance < JUNK_HINT:
            return None
        elif chance < RANDOM_HINT:
            location = rnd.choice(our_items).location
        else: # USEFUL_HINT
            location = rnd.choice(our_useful_items).location

        if location.item.player == player_id:
            name = "Your"
        else:
            name = f"{multiworld.player_name[location.item.player]}'s"

        if isinstance(location, LinksAwakeningLocation):
            location_name = location.ladxr_item.metadata.name
        else:
            location_name = location.name

        hint = f"{name} {location.item} is at {location_name}"
        if location.player != player_id:
            hint += f" in {multiworld.player_name[location.player]}'s world"

        # Cap hint size at 85
        # Realistically we could go bigger but let's be safe instead
        hint = hint[:85]

        return hint

    hints.addHints(rom, rnd, gen_hint)

    if world_setup.goal == "raft":
        patches.goal.setRaftGoal(rom)
    elif world_setup.goal in ("bingo", "bingo-full"):
        patches.bingo.setBingoGoal(rom, world_setup.bingo_goals, world_setup.goal)
    elif world_setup.goal == "seashells":
        patches.goal.setSeashellGoal(rom, 20)
    else:
        patches.goal.setRequiredInstrumentCount(rom, world_setup.goal)

    # Patch the generated logic into the rom
    patches.chest.setMultiChest(rom, world_setup.multichest)
    if settings.overworld not in {"dungeondive", "random"}:
        patches.entrances.changeEntrances(rom, world_setup.entrance_mapping)
    for spot in item_list:
        if spot.item and spot.item.startswith("*"):
            spot.item = spot.item[1:]
        mw = None
        if spot.item_owner != spot.location_owner:
            mw = spot.item_owner
            if mw > 100:
                # There are only 101 player name slots (99 + "The Server" + "another world"), so don't use more than that
                mw = 100
        spot.patch(rom, spot.item, multiworld=mw)
    patches.enemies.changeBosses(rom, world_setup.boss_mapping)
    patches.enemies.changeMiniBosses(rom, world_setup.miniboss_mapping)

    if not args.romdebugmode:
        patches.core.addFrameCounter(rom, len(item_list))

    patches.core.warpHome(rom)  # Needs to be done after setting the start location.
    patches.titleScreen.setRomInfo(rom, auth, seed_name, settings, player_name, player_id)
    if ap_settings["ap_title_screen"]:
        patches.titleScreen.setTitleGraphics(rom)
    patches.endscreen.updateEndScreen(rom)
    patches.aesthetics.updateSpriteData(rom)
    if args.doubletrouble:
        patches.enemies.doubleTrouble(rom)

    if ap_settings["text_shuffle"]:
        buckets = defaultdict(list)
        # For each ROM bank, shuffle text within the bank
        for n, data in enumerate(rom.texts._PointerTable__data):
            # Don't muck up which text boxes are questions and which are statements
            if type(data) != int and data and data != b'\xFF':
                buckets[(rom.texts._PointerTable__banks[n], data[len(data) - 1] == 0xfe)].append((n, data))
        for bucket in buckets.values():
            # For each bucket, make a copy and shuffle
            shuffled = bucket.copy()
            rnd.shuffle(shuffled)
            # Then put new text in
            for bucket_idx, (orig_idx, data) in enumerate(bucket):
                rom.texts[shuffled[bucket_idx][0]] = data
    

    if ap_settings["trendy_game"] != TrendyGame.option_normal:

        # TODO: if 0 or 4, 5, remove inaccurate conveyor tiles


        room_editor = RoomEditor(rom, 0x2A0)

        if ap_settings["trendy_game"] == TrendyGame.option_easy:
            # Set physics flag on all objects
            for i in range(0, 6):
                rom.banks[0x4][0x6F1E + i -0x4000] = 0x4
        else:
            # All levels
            # Set physics flag on yoshi
            rom.banks[0x4][0x6F21-0x4000] = 0x3
            # Add new conveyor to "push" yoshi (it's only a visual)
            room_editor.objects.append(Object(5, 3, 0xD0))

            if int(ap_settings["trendy_game"]) >= TrendyGame.option_harder:
                """
                Data_004_76A0::
                    db   $FC, $00, $04, $00, $00

                Data_004_76A5::
                    db   $00, $04, $00, $FC, $00
                """
                speeds = {
                    TrendyGame.option_harder: (3, 8),
                    TrendyGame.option_hardest: (3, 8),
                    TrendyGame.option_impossible: (3, 16),
                }
                def speed():
                    return rnd.randint(*speeds[ap_settings["trendy_game"]])
                rom.banks[0x4][0x76A0-0x4000] = 0xFF - speed()
                rom.banks[0x4][0x76A2-0x4000] = speed()
                rom.banks[0x4][0x76A6-0x4000] = speed()
                rom.banks[0x4][0x76A8-0x4000] = 0xFF - speed()
                if int(ap_settings["trendy_game"]) >= TrendyGame.option_hardest:
                    rom.banks[0x4][0x76A1-0x4000] = 0xFF - speed()
                    rom.banks[0x4][0x76A3-0x4000] = speed()
                    rom.banks[0x4][0x76A5-0x4000] = speed()
                    rom.banks[0x4][0x76A7-0x4000] = 0xFF - speed()

            room_editor.store(rom)
            # This doesn't work, you can set random conveyors, but they aren't used
            # for x in range(3, 9):
            #     for y in range(1, 5):
            #         room_editor.objects.append(Object(x, y, 0xCF + rnd.randint(0, 3)))

    # Attempt at imitating gb palette, fails
    if False:
        gb_colors = [
            [0x0f, 0x38, 0x0f],
            [0x30, 0x62, 0x30],
            [0x8b, 0xac, 0x0f],
            [0x9b, 0xbc, 0x0f],
        ]
        for color in gb_colors:
            for channel in range(3):
                color[channel] = color[channel] * 31 // 0xbc

    if ap_settings["warp_improvements"]:
        patches.core.addWarpImprovements(rom, ap_settings["additional_warp_points"])

    palette = ap_settings["palette"]
    if palette != Palette.option_normal:
        ranges = {
            # Object palettes
            # Overworld palettes
            # Dungeon palettes
            # Interior palettes
            "code/palettes.asm 1": (0x21, 0x1518, 0x34A0),
            # Intro/outro(?)
            # File select
            # S+Q
            # Map
            "code/palettes.asm 2": (0x21, 0x3536, 0x3FFE),
            # Used for transitioning in and out of forest
            "backgrounds/palettes.asm": (0x24, 0x3478, 0x3578),
            # Haven't yet found menu palette
        }

        for name, (bank, start, end) in ranges.items():
            def clamp(x, min, max):
                if x < min:
                    return min
                if x > max:
                    return max
                return x

            for address in range(start, end, 2):
                packed = (rom.banks[bank][address + 1] << 8) | rom.banks[bank][address]
                r,g,b = bin_to_rgb(packed)

                # 1 bit
                if palette == Palette.option_1bit:
                    r &= 0b10000
                    g &= 0b10000
                    b &= 0b10000
                # 2 bit
                elif palette == Palette.option_1bit:
                    r &= 0b11000
                    g &= 0b11000
                    b &= 0b11000
                # Invert
                elif palette == Palette.option_inverted:
                    r = 31 - r
                    g = 31 - g
                    b = 31 - b
                # Pink
                elif palette == Palette.option_pink:
                    r = r // 2
                    r += 16
                    r = int(r)
                    r = clamp(r, 0, 0x1F)
                    b = b // 2
                    b += 16
                    b = int(b)
                    b = clamp(b, 0, 0x1F)
                elif palette == Palette.option_greyscale:
                    # gray=int(0.299*r+0.587*g+0.114*b)
                    gray = (r + g + b) // 3
                    r = g = b = gray

                packed = rgb_to_bin(r, g, b)
                rom.banks[bank][address] = packed & 0xFF
                rom.banks[bank][address + 1] = packed >> 8

    SEED_LOCATION = 0x0134
    # Patch over the title
    assert(len(auth) == 12)
    rom.patch(0x00, SEED_LOCATION, None, binascii.hexlify(auth))

    for pymod in pymods:
        pymod.postPatch(rom)

    return rom
