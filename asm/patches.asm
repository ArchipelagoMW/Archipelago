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
.definelabel LevelStatusTable, 0x03000A68
.definelabel HasJewelPiece1, 0x3000C07
.definelabel HasJewelPiece2, 0x3000C08
.definelabel HasJewelPiece3, 0x3000C09
.definelabel HasJewelPiece4, 0x3000C0A
.definelabel HasCD, 0x3000C0B
.definelabel HasKeyzer, 0x03000C0C

.definelabel HasFullHealthItem, unusedram + 0  ; byte

; Functions
.definelabel EnemyChildSet, 0x801E328
.definelabel EntityAI_Q_K5_Hip_COM_takarabako, 0x80292BC

; ROM data
.definelabel zako_takara_box_Anm_11, 0x83B5004


; Macros
.macro hook, Start, End, HackFunction
.org Start
.region End-.
    ldr r0, =End
    mov lr, r0
    ldr r0, =HackFunction
    mov pc, r0
.pool
.endregion
.endmacro


.open input,output,0x08000000

; Allocate space at ROM end
.org unusedrom
.region 0x0E010000-.

; 24 available level IDs, not all of which are used.
@levels equ 6 * 4

invalid_item equ 0xFF

; Maps locations to the 8-bit IDs of the items they contain.
; After Archipelago patches the ROM, the "invalid" value should only be in
; locations that don't exist
ItemLocationTable:
    Jewel1LocationTable: .fill @levels, invalid_item
    Jewel2LocationTable: .fill @levels, invalid_item
    Jewel3LocationTable: .fill @levels, invalid_item
    Jewel4LocationTable: .fill @levels, invalid_item
    CDLocationTable:     .fill @levels, invalid_item
    HealthLocationTable: .fill @levels, invalid_item

.endregion

.include "worlds/wl4/asm/check_locations.asm"
.include "worlds/wl4/asm/full_health_shuffle.asm"

.close
