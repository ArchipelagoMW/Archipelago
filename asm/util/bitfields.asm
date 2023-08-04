.gba

; DMA control
; [enable] [irq] [timing] <chunk> [repeat] [src dst] <transfers>
; number of transfers
.expfunc dma_transfers(n), n & 0xFFFF
; destination adjustment
dma_dst_inc    equ 0
dma_dst_dec    equ 1 << 0x15
dma_dst_fixed  equ 2 << 0x15
dma_dst_reload equ 3 << 0x15
; source adjustment
dma_src_inc   equ 0
dma_src_dec   equ 1 << 0x17
dma_src_fixed equ 2 << 0x17
; repeat
dma_repeat equ 1 << 0x19
; chunk size
dma_16 equ 0
dma_32 equ 1 << 0x1A
; timing mode
dma_now        equ 0
dma_at_vblank  equ 1 << 0x1C
dma_at_hblank  equ 2 << 0x1C
dma_at_refresh equ 3 << 0x1C
; interrupt request
dma_irq equ 1 << 0x1E
; enable
dma_enable equ 1 << 0x1F

; convenience
.expfunc dma_halfwords(n), dma_16 | dma_transfers(n)
.expfunc dma_words(n), dma_32 | dma_transfers(n)


; Backgrounds
; <size> [wrap] <sbb> <color> [mosaic] <cbb> <priority>
; priority
.expfunc bg_priority(prio), (prio & 3)
; character base block
.expfunc bg_cbb(cbb), (cbb & 3) << 2
; mosaic flag
bg_mosaic equ 1 << 6
; color mode
bg_4bpp equ 0
bg_8bpp equ 1 << 7
; screen base block
.expfunc bg_sbb(sbb), (sbb & 0x1F) << 8
; affine wrapping
bg_wrap equ 1 << 0xD
; size
.expfunc bg_size(sz), (sz & 3) << 0xE
bg_reg_32x32 equ bg_size(0)
bg_reg_64x32 equ bg_size(1)
bg_reg_32x64 equ bg_size(2)
bg_reg_64x64 equ bg_size(3)
bg_aff_16x16 equ bg_size(0)
bg_aff_32x32 equ bg_size(1)
bg_aff_64x64 equ bg_size(2)
bg_aff_128x128 equ bg_size(3)


; OAM

; Attribute 0 - <shape> <bit depth> [mosaic] [gfx] [obj] <y>
; y coordinate
.expfunc attr0_y(y), y & 0xFF
; object mode
attr0_aff  equ 1 << 8
attr0_hide equ 2 << 8
attr0_dbl  equ 3 << 8
; gfx mode
attr0_blend  equ 1 << 0xA
attr0_window equ 2 << 0xA
; mosaic
attr0_mosaic equ 1 << 0xC
; bit depth
attr0_4bpp equ 0
attr0_8bpp equ 1 << 0xD
; shape
attr0_square equ 0
attr0_wide   equ 1 << 0xE
attr0_tall   equ 2 << 0xE

; Attribute 1 - <size> [vf] [hf] <x>
; x coordinate
.expfunc attr1_x(x), x & 0x1FF
; flip
attr1_hf equ 1 << 0xC
attr1_vf equ 1 << 0xD
; size
.expfunc attr1_size(size), (size & 3) << 0xE

; Attribute 2 - <palette> <priority> <id> 
.expfunc attr2_id(id), id & 0x3FF
.expfunc attr2_priority(prio), (prio & 3) << 0xA
.expfunc attr2_palette(pal), (pal & 0xF) << 0xC
