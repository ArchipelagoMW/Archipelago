.gba

input equ "Wario Land 4 (UE) [!].gba"
output equ "worlds/wl4/data/basepatch.gba"

unusedram equ 0x03006280
unusedrom equ 0x0878F97C


; Variables
.definelabel CurrentRoomId, 0x3000024
.definelabel EntityLeftOverStateList, 0x3000564
.definelabel LevelStatusTable, 0x03000A68
.definelabel HasKeyzer, 0x03000C0C

.definelabel HasFullHealthItem, unusedram + 0

; Functions
.definelabel EnemyChildSet, 0x801E328
.definelabel EntityAI_Q_K5_Hip_COM_takarabako, 0x80292BC

; ROM data
.definelabel zako_takara_box_Anm_11, 0x83B5004


.open input,output,0x08000000

; Allocate space at ROM end
.org unusedrom
.region 0x0E010000-.
.endregion

.include "worlds/wl4/asm/full_health_shuffle.asm"

.close
