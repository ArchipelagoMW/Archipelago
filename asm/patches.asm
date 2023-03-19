.gba

input equ "Wario Land 4 (UE) [!].gba"
output equ "worlds/wl4/data/basepatch.gba"

unusedram equ 0x03006280
unusedrom equ 0x0878F97C


; Variables
CurrentRoomId equ 0x3000024
EntityLeftOverStateList equ 0x3000564
LevelStatusTable equ 0x03000A68
HasKeyzer equ 0x03000C0C

HasFullHealthItem equ unusedram + 0

; Functions
EnemyChildSet equ 0x801E328
EntityAI_Q_K5_Hip_COM_takarabako equ 0x80292BC

; ROM data
zako_takara_box_Anm_11 equ 0x83B5004


.open input,output,0x08000000

; Allocate space at ROM end
.org unusedrom
.region 0x0E010000-.
.endregion

.include "worlds/wl4/asm/full_health_shuffle.asm"

.close
