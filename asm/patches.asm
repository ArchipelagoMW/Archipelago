.gba

input equ "Wario Land 4 (UE) [!].gba"
output equ "worlds/wl4/data/basepatch.gba"

unusedram equ 0x03006280
unusedrom equ 0x0878F97C


; Variables
.definelabel PassageID, 0x3000002
.definelabel InPassageLevelID, 0x3000003
.definelabel CurrentRoomId, 0x3000024
.definelabel EntityLeftOverStateList, 0x3000564
.definelabel CurrentEnemyData, 0x3000A24
.definelabel LevelStatusTable, 0x03000A68
.definelabel HasJewelPiece1, 0x3000C07
.definelabel HasJewelPiece2, 0x3000C08
.definelabel HasJewelPiece3, 0x3000C09
.definelabel HasJewelPiece4, 0x3000C0A
.definelabel HasCD, 0x3000C0B
.definelabel HasKeyzer, 0x3000C0C
.definelabel Wario_ucReact, 0x3001898
.definelabel WarioHeart, 0x3001910

; Extends the existing box system to include full health boxes
.definelabel HasFullHealthItem, unusedram + 0  ; byte

; Items can be received one at a time w/o issue
.definelabel IncomingItemID, unusedram + 1  ; byte

.definelabel ReceivedItemCount, unusedram + 2  ; halfword
.definelabel DeathlinkEnabled, unusedram + 4  ; byte

.definelabel QueuedFullHealthItems, unusedram + 10  ; byte
.definelabel QueuedDamageTraps, unusedram + 11  ; byte
.definelabel QueuedFormTraps, unusedram + 12  ; byte

; Functions
.definelabel m4aSongNumStart, 0x8001DA4
.definelabel EnemyChildSet, 0x801E328
.definelabel KillChildWhenParentDies, 0x80268DC
.definelabel EntityAI_Q_K5_Hip_COM_takarabako, 0x80292BC
.definelabel EntityAI_INITIAL_takara_kakera, 0x802932C
.definelabel TOptObjSet, 0x80766E8

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
.region 0x0E010000-.

; Player's name, up to 16 characters
Player_Name: .fill 16, 0

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

; Retrieve the item ID at the location specified in r0 in this level.
; Return the encoded ID in r0
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

    ; r0 = locationID = (boxtype * 6 + passageID) * 4 + levelID
    ldr r0, =InPassageLevelID
    ldrb r0, [r0]
    add r0, r1, r0

    ; r0 = item ID
    ldr r1, =ItemLocationTable
    add r2, r1, r0
    ldrb r0, [r2]

    mov pc, lr

.endregion

.include "worlds/wl4/asm/check_locations.asm"
.include "worlds/wl4/asm/randomize_boxes.asm"
.include "worlds/wl4/asm/full_health_shuffle.asm"

.close
