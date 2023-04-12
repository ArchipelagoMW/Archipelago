.gba

input equ "../../Wario Land 4 (UE) [!].gba"
output equ "data/basepatch.gba"

unusedram equ 0x03006280
unusedrom equ 0x0878F97C


; Variables
.definelabel PassageID, 0x3000002
.definelabel InPassageLevelID, 0x3000003
.definelabel CurrentRoomId, 0x3000024
.definelabel ucFlashLoop, 0x3000044
.definelabel ucTimeUp, 0x3000047
.definelabel EntityLeftOverStateList, 0x3000564
.definelabel CurrentEnemyData, 0x3000A24
.definelabel LevelStatusTable, 0x3000A68
.definelabel Scbuf_ucStatus, 0x3000BE0
.definelabel HasJewelPiece1, 0x3000C07
.definelabel HasJewelPiece2, 0x3000C08
.definelabel HasJewelPiece3, 0x3000C09
.definelabel HasJewelPiece4, 0x3000C0A
.definelabel HasCD, 0x3000C0B
.definelabel HasKeyzer, 0x3000C0C
.definelabel sGameSeq, 0x3000C3C
.definelabel GlobalTimer, 0x3000C41
.definelabel KeyPressContinuous, 0x3001844
.definelabel KeyPressPrevious, 0x3001846
.definelabel usTrg_KeyPress1Frame, 0x3001848
.definelabel Wario_ucReact, 0x3001898
.definelabel Wario_ucMiss, 0x300189C
.definelabel WarioHeart, 0x3001910
.definelabel usWarStopFlg, 0x30019F6

; This is the upper halfword of entry passage level 3.
; This level doesn't actually exist, so we can sneak this bit of extra save data
; in there.
.definelabel ReceivedItemCount, LevelStatusTable + 14  ; halfword

; Extends the existing box system to include full health boxes
.definelabel HasFullHealthItem, unusedram + 0  ; byte

; Items can be received one at a time w/o issue
.definelabel IncomingItemID, unusedram + 1  ; byte
.definelabel IncomingItemSender, unusedram + 2  ; byte

; The jewel piece or CD that you've most recently received or grabbed from a box
.definelabel LastCollectedItemID, unusedram + 3  ; byte

.definelabel DeathlinkEnabled, unusedram + 8  ; byte

.definelabel QueuedJunk, unusedram + 16  ; bytes
    .definelabel QueuedFullHealthItem, QueuedJunk + 0
    .definelabel QueuedFormTraps, QueuedJunk + 1
    .definelabel QueuedHearts, QueuedJunk + 2
    .definelabel QueuedLightningTraps, QueuedJunk + 3

.definelabel Jewel1BoxContents, unusedram + 24
.definelabel Jewel2BoxContents, unusedram + 26
.definelabel Jewel3BoxContents, unusedram + 28
.definelabel Jewel4BoxContents, unusedram + 30
.definelabel CDBoxContents, unusedram + 32
.definelabel HealthBoxContents, unusedram + 34


; Functions
.definelabel MainGameLoop, 0x80001CC
.definelabel m4aSongNumStart, 0x8001DA4
.definelabel WarioHitMain, 0x801009c
.definelabel EnemyChildSet, 0x801E328
.definelabel ChangeWarioReact_Fire, 0x801EA3C
.definelabel ChangeWarioReact_Fat, 0x801EA64
.definelabel ChangeWarioReact_Puffy, 0x801EADC
.definelabel ChangeWarioReact_Spring, 0x801EB04
.definelabel ChangeWarioReact_Frozen, 0x801EB54
.definelabel KillChildWhenParentDies, 0x80268DC
.definelabel EntityAI_Q_K5_Hip_COM_takarabako, 0x80292BC
.definelabel EntityAI_INITIAL_takara_kakera, 0x802932C
.definelabel TOptObjSet, 0x80766E8
.definelabel WarioCoinSet, 0x80768B8
.definelabel WarioVoiceSet, 0x8088620
.definelabel MiniRandomCreate, 0x8089B80
.definelabel modsi3, 0x8094ED0
.definelabel WarioChng_React, 0x82DECA0

; ROM data
.definelabel takara_Anm_00, 0x83B4BC8
.definelabel takara_Anm_01, 0x83B4BD8
.definelabel takara_Anm_02, 0x83B4C00
.definelabel takara_Anm_03, 0x83B4C10
.definelabel takara_Anm_04, 0x83B4C20
.definelabel takara_Anm_05, 0x83B4C30
.definelabel zako_takara_box_Anm_02, 0x83B4F34
.definelabel zako_takara_box_Anm_11, 0x83B5004


; Macros

; Replaces a branch with a call to a mod function.
; This is for when the replaced code ends with an unconditional jump so that the
; pool afterward in the original code can also be replaced.
.macro hook_branch, Start, End, ReturnAddress, HackFunction
.org Start
.region End-.
    ldr r0, =ReturnAddress
    mov lr, r0
    ldr r0, =HackFunction
    mov pc, r0
.pool
.endregion
.endmacro

; Replace some code with a call to a mod function.
; This will return execution to the end of the code that was replaced.
.macro hook, Start, End, HackFunction
    hook_branch Start, End, End, HackFunction
.endmacro

; Load a function pointer into a register and call it. Since mod code is at the
; end of the ROM while vanilla code is at the beginning, this is needed for the
; large jumps between modded/vanilla subroutines
.macro call_using, register, Function
    ldr register, =@@Return | 1
    mov lr, register
    ldr register, =Function
    mov pc, register
@@Return:
.endmacro

.open input,output,0x08000000

; Allocate space at ROM end
.org unusedrom
.region 0x0E000000-.

PlayerName: .fill 16, 0  ; Player's name, up to 16 characters
PlayerID: .byte 0

; 24 available level IDs, not all of which are used.
@levels equ 6 * 4

invalid_item equ 0xFF

; Maps locations to the 8-bit IDs of the items they contain.
; After Archipelago patches the ROM, the "invalid" value should only be in
; locations that don't exist
.align 4
ItemLocationTable:
    Jewel1LocationTable: .fill @levels, invalid_item
    Jewel2LocationTable: .fill @levels, invalid_item
    Jewel3LocationTable: .fill @levels, invalid_item
    Jewel4LocationTable: .fill @levels, invalid_item
    CDLocationTable:     .fill @levels, invalid_item
    HealthLocationTable: .fill @levels, invalid_item

; Maps locations to the 8-bit player ID of the item's owner.
.align 4
ItemDestinationTable:
    Jewel1DestinationTable: .fill @levels, -1
    Jewel2DestinationTable: .fill @levels, -1
    Jewel3DestinationTable: .fill @levels, -1
    Jewel4DestinationTable: .fill @levels, -1
    CDDestinationTable:     .fill @levels, -1
    HealthDestinationTable: .fill @levels, -1

DeathLinkFlag: .byte 0

.align 2
; Retrieve the item and player ID at the location specified in r0 in this level.
; Return the encoded ID in r0 and the player ID in r1
GetItemAtLocation:
    ; r1 = boxtype * 6
    lsl r1, r0, #1
    add r1, r1, r0
    lsl r1, r1, #1
    
    ; r1 = (boxtype * 6 + passageID) * 4
    ldr r0, =PassageID
    ldrb r0, [r0]
    add r1, r1, r0
    lsl r1, r1, #2

    ; r3 = locationID = (boxtype * 6 + passageID) * 4 + levelID
    ldr r0, =InPassageLevelID
    ldrb r0, [r0]
    add r3, r1, r0

    ; r0 = item ID
    ldr r1, =ItemLocationTable
    add r2, r1, r3
    ldrb r0, [r2]

    ; r1 = player ID
    ldr r1, =ItemDestinationTable
    add r2, r1, r3
    ldrb r1, [r2]

    mov pc, lr

.endregion

.include "asm/check_locations.asm"
.include "asm/junk_effects.asm"
.include "asm/randomize_boxes.asm"
.include "asm/save_full_health.asm"
.include "asm/item_queue.asm"
.include "asm/pre_game_loop.asm"
.include "asm/collection_indicator.asm"

.close
