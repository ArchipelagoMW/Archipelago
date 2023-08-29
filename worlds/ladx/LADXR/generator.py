import binascii
import importlib.util
import importlib.machinery
import os
import pkgutil

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
from .patches.aesthetics import rgb_to_bin, bin_to_rgb

from .locations.keyLocation import KeyLocation

from BaseClasses import ItemClassification
from ..Locations import LinksAwakeningLocation
from ..Options import TrendyGame, Palette, MusicChangeCondition

def patch_vwf(rom, assembler):
    def get_asm(name):
        return pkgutil.get_data(__name__, os.path.join("patches/vwf", name)).decode().replace("\r", "")
    
    assembler.const("CURR_CHAR_GFX"		,0xD608)
    assembler.const("CURR_CHAR"			,0xD638)
    assembler.const("CURR_CHAR_SIZE"		,0xD63A)
    assembler.const("IS_TILE_READY"		,0xD63B)
    assembler.const("IS_CHAR_READY"		,0xD63C)
    assembler.const("CURR_CHAR_BUFFER"	,0xD640)
    assembler.const("TILE_BUFFER"			,0xD650)
    assembler.const("wDialogBoxPosIndex"	,0xD668)
    assembler.const("wDialogBoxPosIndexHi" ,0xD669)
    assembler.const("PIXELS_TO_SUBTRACT"	,0xD66A)
    assembler.const("PIXELS_TO_ADD"		,0xD66B)
    assembler.const("wDialogCharacterIndex" ,0xC170)
    assembler.const("wDialogState" ,0xC19F)
    assembler.const("wDrawCommand.destinationHigh" , 0xD601)
    assembler.const("wDrawCommand.destinationLow" ,0xD602)
    assembler.const("wDialogNextCharPosition" ,0xC171)
    assembler.const("rSelectROMBank" , 0x2100)
    assembler.const("CodepointToTileMap" , 0x4641)

    vfw_main = 0x4000 - 332
    assembler.const("variableWidthFontThunk" , vfw_main + 0x4000)
    
    rom.patch(0x1C, vfw_main, old="00" * 332, new=assembler.ASM(get_asm("vwf.asm"), vfw_main + 0x4000))

    widthtable_size = len(assembler.ASM(get_asm("vwf_widthtable.asm"), 0x1000)) // 2

    vfw_widthtable = 0x4000 - widthtable_size
    symbols = {}
    rom.patch(0x36, vfw_widthtable, old="00" * widthtable_size, new=assembler.ASM(get_asm("vwf_widthtable.asm"), vfw_widthtable + 0x4000, symbols))
    assembler.const("saveLetterWidths", symbols["SAVELETTERWIDTHS"])
    # TODO: we may want to make sure we patch late
    font = pkgutil.get_data(__name__, "patches/vwf/font.vwf.2bpp")
    import binascii
    font = binascii.hexlify(font)
    rom.patch(0x0F, 0x1000, old=None, new=font)
    
    # wDialogCharacterIndexHi -> wDialogBoxPosIndexHi
    rom.patch(0x00, 0x2335, '64C1', '69D6') 
    # wDialogCharacterIndex -> wDialogBoxPosIndex
    rom.patch(0x00, 0x2339, '70C1', '68D6')
    rom.patch(0x00, 0x2517, '70C1', '68D6')
    rom.patch(0x00, 0x252F, '70C1', '68D6')
    rom.patch(0x1C, 0x09F2, '70C1', '68D6')
    # " " -> "/0"
    rom.patch(0x00, 0x2607, '20', '00')


    rom.patch(0x00, 0x260B, old=assembler.ASM("""
    ld   a, $1C                                   ; $260B: $3E $1C
    ld   [rSelectROMBank], a                      ; $260D: $EA $00 $21
    ld   hl, CodepointToTileMap                   ; $2610: $21 $41 $46
    add  hl, de                                   ; $2613: $19
    ld   e, [hl]                                  ; $2614: $5E
    ld   d, $00                                   ; $2615: $16 $00
    sla  e                                        ; $2617: $CB $23
                                                        """),
    new=assembler.ASM("""
    ld   a, $36
    ld   [rSelectROMBank], a
    call saveLetterWidths
    ;ld   a, $1C                                   ; $260B: $3E $1C
    ;ld   [rSelectROMBank], a                      ; $260D: $EA $00 $21
    
                          """), fill_nop=True)
    rom.patch(0x00, 0x2646, assembler.ASM("""
        xor  a 
        pop hl
        and  a
        """),
        assembler.ASM("""jp variableWidthFontThunk"""))
    # wDialogCharacterIndex -> wDialogBoxPosIndex
    rom.patch(0x00, 0x2696, '70C1', '68D6')

    rom.patch(0x1C, 0x0641, old=assembler.ASM("""
    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $7e, $3d, $41, 0  , $8a, $8b, $44, $40, $45, $46, $8c, $8d, $3a, $3f, $3b, 0

    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $42, $43, $8e, 0  , $8f, $3c

    db  0  , 0  , $01, $02, $03, $04, $05, $06, $07, $08, $09, $0a, $0b, $0c, $0d, $0e

    db  $0f, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, 0  , 0  , 0  , $40, 0

    db  0  , $1a, $1b, $1c, $1d, $1e, $1f, $20, $21, $22, $23, $24, $25, $26, $27, $28

    db  $29, $2a, $2b, $2c, $2d, $2e, $2f, $30, $31, $32, $3e, 0  , 0  , 0  , 0  , 0

    db  $47, $48, $49, $4a, $4b, $4c, $4d, $4e, $4f, $50, $51, $52, $53, $59, $5a, $5b

    db  $5c, $5d, $59, $5a, $5b, $5c, $5d, $32, $6f, $6d, $6e, 0  , 0  , 0  , 0  , 0

    db  $3d, $3c, $3f, $7e, $39, $3a, $3b, $7a, $7b, 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $9b, $9c, $9d, $9e, $9f, $38

    db  0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0

    db  $80, $81, $82, $83, $84, $85, $86, $87, $88, $89, $8a, $8b, $8c, $8d, $8e, $8f

    db  $88, $90, $91, $92, $93, $94, $95, $89, $96, $97, $98, $99, $9a, $87, $86, 0

    db  $34, $35, $36, $37, 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , 0  , $7e, 0  , 0
                                              """), new=assembler.ASM("""
    db  $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e

    db  $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e
;  $20        !    "    #    $    %    &    '    (    )    *    +    ,    -           
    db  $7e, $3d, $41, $16, $8a, $8b, $44, $40, $45, $46, $8c, $8d, $3a, $3f, $39, $7e
;  $30   0    1    2    3    4    5    6    7    8    9    :    ;    <    =    >    ?
    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $42, $43, $8e, 0  , $8f, $3c
;  $40   @    A    B    C    D    E    F    G    H    I    J    K    L    M    N    O
    db  0  , 0  , $01, $02, $03, $04, $05, $06, $07, $08, $09, $0a, $0b, $0c, $0d, $0e
;  $50   P    Q    R    S    T    U    V    W    X    Y    Z   ...   \    ]    ^    _
    db  $0f, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $6F, 0  , 0  , $40, 0
;  $60   `    a    b    c    d    e    f    g    h    i    j    k    l    m    n    o
    db  0  , $1a, $1b, $1c, $1d, $1e, $1f, $20, $21, $22, $23, $24, $25, $26, $27, $28
;  $70   p    q    r    s    t    u    v    w    x    y    z    --   |    }    ~
    db  $29, $2a, $2b, $2c, $2d, $2e, $2f, $30, $31, $32, $3e, $4e, 0  , 0  , 0  , 0
;  $80   Á    É    Í    Ó    Ú    Ü    Ñ    --   Ç    á    é    í    ó    ú    ü    ñ
    db  $47, $48, $49, $4a, $4b, $4c, $4d, $4e, $4f, $50, $51, $52, $53, $54, $55, $56
;  $90   à    è    ì    ò    ù    ä    ë    ï    ö   ...   ¡    ¿    "    '    .
    db  $57, $58, $59, $5A, $5B, $5C, $5D, $5E, $5F, $6f, $6e, $6d, $6c, $6b, $6a, 0
;  $A0   !    ?    -  BLANK  .    ,    .2   "     
    db  $3d, $3c, $3f, $7e, $39, $3a, $3b, $7a, $7b, 0  , 0  , 0  , 0  , 0  , 0  , 0
;  $B0   0    1    2    3    4    5    6    7    8    9    â    ê    î    ô    û
    db  $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $9b, $9c, $9d, $9e, $9f, $38
;  $C0   0    1    2    3    4    5    6    7    8    9  
    db  $60, $61, $62, $63, $64, $65, $66, $67, $68, $69, 0  , 0  , 0  , 0  , 0  , 0
;  $D0   A2  B2   C2   D2   E2   F2   DPAD LTTR YOSH HIBS FOOT (X)  SKUL LINK MARN TARN
    db  $80, $81, $82, $83, $84, $85, $86, $87, $88, $89, $8a, $8b, $8c, $8d, $8e, $8f
;  $E0  YOSH BOW  CAN  BANA STCK BEEH PINE BROM HOOK BRA  SCAL GLAS      LTTR DPAD
    db  $88, $90, $91, $92, $93, $94, $95, $89, $96, $97, $98, $99, $9a, $87, $86, 0
;  $F0   UP  DOWN LEFT RIGHT                                            BLANK
    db  $34, $35, $36, $37, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e, $7e
                                                        """))

    # TODO: fix tilemap



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

    patch_vwf(rom, assembler)
    
    if ap_settings["trendy_game"] != TrendyGame.option_normal:

        # TODO: if 0 or 4, 5, remove inaccurate conveyor tiles

        from .roomEditor import RoomEditor, Object
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
