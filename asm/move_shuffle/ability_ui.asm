.gba


hook 0x8084B10, 0x8084B20, InitAbilityIcons  ; SelectMmapInit
hook_manual 0x8085C62, 0x8085C6C, DrawAbilityIcons  ; SelectMmapOamCreate


.autoregion
.align 2


InitAbilityIcons:
        push {lr}

    ; DMA in the tiles
        ldr r1, =REG_DMA3SAD
        ldr r0, =AbilityIconTilesTop
        str r0, [r1]
        ldr r0, =0x6010000 + tile_coord_4b(0, 4)
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(16 * sizeof_tile / 2)
        str r0, [r1, #8]
        ldr r0, [r1, #8]
        ldr r0, =AbilityIconTilesBottom
        str r0, [r1]
        ldr r0, =0x6010000 + tile_coord_4b(0, 5)
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(16 * sizeof_tile / 2)
        str r0, [r1, #8]
        ldr r0, [r1, #8]

    ; DMA in the palettes
        ldr r0, =PassageTreasurePalettes
        str r0, [r1]
        ldr r0, =ObjectPalette4
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(16 * 5)
        str r0, [r1, #8]
        ldr r0, [r1, #8]
        ldr r0, =ExtraAbilityPalettes
        str r0, [r1]
        ldr r0, =ObjectPalette9
        str r0, [r1, #4]
        ldr r0, =dma_enable | dma_halfwords(16 * 2)
        str r0, [r1, #8]
        ldr r0, [r1, #8]

    ; Displaced code
        call_using r0, MmapHekigaChange
        call_using r0, MmapBestScoreSet
        call_using r0, Select_Fade_Init
        ldr r0, =REG_BG0VOFS
        strh r4, [r0]

        pop {pc}

    .pool


ExtraAbilityPalettes:
    ; Garlic
    .halfword 0x42C0, 0x0000, 0x4169, 0x560E, 0x72F5, 0x7FFF, 0x7FFF, 0x02FD
    .halfword 0x1FFF, 0x001F, 0x7B6B, 0x0000, 0x6BDF, 0x3FBF, 0x22FA, 0x0DAF
    ; Bumbleprod helmet
    .halfword 0x42C0, 0x0000, 0x4169, 0x560E, 0x72F5, 0x7FFF, 0x7FFF, 0x02FD
    .halfword 0x1FFF, 0x001F, 0x7B6B, 0x0000, 0x0000, 0x0000, 0x05DE, 0x24C5


DrawAbilityIcons:
    .macro @@check_obj_count
        cmp r4, #0x80
        bgt @@Return
    .endmacro

    .macro @@add_object
        strh r0, [r7]
        strh r1, [r7, #2]
        strh r2, [r7, #4]
        add r4, #1
        add r7, #8
    .endmacro

        ldr r5, =WarioAbilities
        ldr r6, =ucCntObj  ; r6 = pointer to object count
        ldr r7, =OamBuf
        ldrb r4, [r6]  ; r4 = object count
        lsl r0, r4, #3
        add r7, r0  ; r7 = pointer to current OAM buffer entry
        ldr r0, =attr0_square | attr0_4bpp | attr0_y(0)
        ldr r1, =attr1_size(1) | attr1_x(8 * 8)
        ldrb r5, [r5]  ; r5 = Wario's abilities


    ; Super ground pound
        @@check_obj_count
        get_bit r2, r5, MoveBit_GroundPoundSuper
        cmp r2, #0
        beq @@GroundPound
        ldr r2, =attr2_palette(0x4) | attr2_priority(0) | attr2_id(0x08C)
        @@add_object
        b @@Swim

    @@GroundPound:
        get_bit r2, r5, MoveBit_GroundPound
        cmp r2, #0
        beq @@Swim
        ldr r2, =attr2_palette(0x4) | attr2_priority(0) | attr2_id(0x080)
        @@add_object

    @@Swim:
        @@check_obj_count
        add r1, #attr1_x(16)
        get_bit r2, r5, MoveBit_Swim
        cmp r2, #0
        beq @@HeadSmash
        ldr r2, =attr2_palette(0x8) | attr2_priority(0) | attr2_id(0x082)
        @@add_object

    @@HeadSmash:
        @@check_obj_count
        add r1, #attr1_x(16)
        get_bit r2, r5, MoveBit_HeadSmash
        cmp r2, #0
        beq @@HeavyGrab
        ldr r2, =attr2_palette(0xA) | attr2_priority(0) | attr2_id(0x084)
        @@add_object

    @@HeavyGrab:
        @@check_obj_count
        add r1, #attr1_x(16)
        get_bit r2, r5, MoveBit_GrabHeavy
        cmp r2, #0
        beq @@Grab
        ldr r2, =attr2_palette(0x6) | attr2_priority(0) | attr2_id(0x08E)
        @@add_object
        b @@DashAttack

    @@Grab:
        get_bit r2, r5, MoveBit_Grab
        cmp r2, #0
        beq @@DashAttack
        ldr r2, =attr2_palette(0x8) | attr2_priority(0) | attr2_id(0x086)
        @@add_object

    @@DashAttack:
        get_bit r2, r5, MoveBit_DashAttack
        add r1, #attr1_x(16)
        cmp r2, #0
        beq @@EnemyJump
        ldr r2, =attr2_palette(0x9) | attr2_priority(0) | attr2_id(0x088)
        @@add_object

    @@EnemyJump:
        get_bit r2, r5, MoveBit_EnemyJump
        add r1, #attr1_x(16)
        cmp r2, #0
        beq @@Return
        ldr r2, =attr2_palette(0x5) | attr2_priority(0) | attr2_id(0x08A)
        @@add_object

    @@Return:
        strb r4, [r6]

        mov r9, r4
        mov r10, r5
        pop {r4, r5, r6, r7}
        pop {r0}
        bx r0

    .pool


.endautoregion
