.gba

input equ "../../Wario Land 4 (UE) [!].gba"
output equ "data/basepatch.gba"
.open input,output,0x08000000

UnusedRamStart equ 0x03006280
UnusedRomStart equ 0x0878F97C

.include "asm/util/vanilla_labels.asm"
.include "asm/util/randomizer_variables.asm"
.include "asm/util/hook_macros.asm"


; Allocate space at ROM end
.org UnusedRomStart
.region 0x0E000000-.
PlayerName: .fill 16, 0  ; Player's name, up to 16 characters
PlayerID: .byte 0
DeathLinkFlag: .byte 0
.endregion

.include "asm/items/item_table.asm"
.include "asm/items/multiworld.asm"
.include "asm/items/collect_treasure.asm"
.include "asm/items/collect_junk.asm"
.include "asm/boxes/randomize_boxes.asm"
.include "asm/boxes/save_full_health.asm"
.include "asm/routines.asm"
.include "asm/patches.asm"

.close
