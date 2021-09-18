!IBranchItem = #$887C
!ISetItem = #$8899
!ILoadSpecialGraphics = #$8764
!ISetGoto = #$8A24
!ISetPreInstructionCode = #$86C1
!IDrawCustom1 = #$E04F
!IDrawCustom2 = #$E067
!IGoto = #$8724
!IKill = #$86BC
!IPlayTrackNow = #$8BDD
!IJSR = #$8A2E
!ISetCounter8 = #$874E
!IGotoDecrement = #$873F
!IGotoIfDoorSet = #$8A72
!ISleep = #$86B4
!IVisibleItem = #i_visible_item
!IChozoItem = #i_chozo_item
!IHiddenItem = #i_hidden_item
!ILoadCustomGraphics = #i_load_custom_graphics
!IPickup = #i_live_pickup
!IStartDrawLoop = #i_start_draw_loop
!IStartHiddenDrawLoop = #i_start_hidden_draw_loop

!ITEM_RAM = $7E09A2

; SM Item Patches
pushpc

;org $8095f7
;    jsl nmi_read_messages : nop

; Add custom PLM that can asynchronously load in items
org $84f870                               ; lordlou: had to move this from original place ($84efe0) since it conflicts with VariaRandomizer's beam_doors_plms patch
    dw i_visible_item_setup, v_item       ;f870
    dw i_visible_item_setup, c_item       ;f874
    dw i_hidden_item_setup,  h_item       ;f878

v_item:
    dw !IVisibleItem
c_item:
    dw !IChozoItem
h_item:
    dw !IHiddenItem

; Graphics pointers for items (by item index)
sm_item_graphics:
    dw $0008 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Energy Tank
    dw $000A : db $00, $00, $00, $00, $00, $00, $00, $00    ; Missile
    dw $000C : db $00, $00, $00, $00, $00, $00, $00, $00    ; Super Missile
    dw $000E : db $00, $00, $00, $00, $00, $00, $00, $00    ; Power Bomb

    dw $8000 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Bombs
    dw $8B00 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Charge
    dw $8C00 : db $00, $03, $00, $00, $00, $03, $00, $00    ; Ice Beam
    dw $8400 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Hi-Jump
    dw $8A00 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Speed booster
    dw $8D00 : db $00, $02, $00, $00, $00, $02, $00, $00    ; Wave beam
    dw $8F00 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Spazer
    dw $8200 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Spring ball
    dw $8300 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Varia suit
    dw $8100 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Gravity suit
    dw $8900 : db $01, $01, $00, $00, $03, $03, $00, $00    ; X-ray scope
    dw $8E00 : db $00, $01, $00, $00, $00, $01, $00, $00    ; Plasma beam
    dw $8800 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Grapple beam
    dw $8600 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Space jump
    dw $8500 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Screw attack
    dw $8700 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Morph ball
    dw $9000 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Reserve tank
    dw $8700 : db $00, $00, $00, $00, $00, $00, $00, $00    ; Multiworld item: Morph ball

sm_item_table:
    ; pickup, qty,   msg,   type,  ext2,  ext3,  loop,  hloop
    dw $8968, $0064, $0000, $0000, $0000, $0000, $E0A5, #p_etank_hloop      ; E-Tank
    dw $89A9, $0005, $0000, $0001, $0000, $0000, $E0CA, #p_missile_hloop    ; Missiles
    dw $89D2, $0005, $0000, $0002, $0000, $0000, $E0EF, #p_super_hloop      ; Super Missiles
    dw $89FB, $0005, $0000, $0003, $0000, $0000, $E114, #p_pb_hloop         ; Power Bombs
        
    dw $88F3, $1000, $0013, $0004, $0000, $0000, $0000, $0000      ; Bombs
    dw $88B0, $1000, $000E, $0005, $0000, $0000, $0000, $0000      ; Charge beam
    dw $88B0, $0002, $000F, $0005, $0000, $0000, $0000, $0000      ; Ice beam
    dw $88F3, $0100, $000B, $0004, $0000, $0000, $0000, $0000      ; Hi-jump
    dw $88F3, $2000, $000D, $0004, $0000, $0000, $0000, $0000      ; Speed booster
    dw $88B0, $0001, $0010, $0005, $0000, $0000, $0000, $0000      ; Wave beam
    dw $88B0, $0004, $0011, $0005, $0000, $0000, $0000, $0000      ; Spazer
    dw $88F3, $0002, $0008, $0004, $0000, $0000, $0000, $0000      ; Spring ball
    dw $88F3, $0001, $0007, $0004, $0000, $0000, $0000, $0000      ; Varia suit
    dw $88F3, $0020, $001A, $0004, $0000, $0000, $0000, $0000      ; Gravity suit
    dw $8941, $8000, $0000, $0004, $0000, $0000, $0000, $0000      ; X-ray scope
    dw $88B0, $0008, $0012, $0005, $0000, $0000, $0000, $0000      ; Plasma
    dw $891A, $4000, $0000, $0004, $0000, $0000, $0000, $0000      ; Grapple
    dw $88F3, $0200, $000C, $0004, $0000, $0000, $0000, $0000      ; Space jump
    dw $88F3, $0008, $000A, $0004, $0000, $0000, $0000, $0000      ; Screw attack
    dw $88F3, $0004, $0009, $0004, $0000, $0000, $0000, $0000      ; Morph ball
    dw $8986, $0064, $0000, $0006, $0000, $0000, $0000, $0000      ; Reserve tank
    dw $88F3, $0004, $0009, $0004, $0000, $0000, $0000, $0000      ; Multiworld item: Morph ball

i_visible_item:
    lda #$0006
    jsr i_load_rando_item
    rts

i_chozo_item:
    lda #$0008
    jsr i_load_rando_item
    rts

i_hidden_item:
    lda #$000A
    jsr i_load_rando_item
    rts

p_etank_hloop:
    dw $0004, $a2df
    dw $0004, $a2e5
    dw !IGotoDecrement, p_etank_hloop
    dw !IJSR, $e020
    dw !IGoto, p_hidden_item_loop2

p_missile_hloop:
    dw $0004, $A2EB
    dw $0004, $A2F1
    dw !IGotoDecrement, p_missile_hloop
    dw !IJSR, $e020
    dw !IGoto, p_hidden_item_loop2

p_super_hloop:
    dw $0004, $A2F7
    dw $0004, $A2FD
    dw !IGotoDecrement, p_super_hloop
    dw !IJSR, $e020
    dw !IGoto, p_hidden_item_loop2

p_pb_hloop:
    dw $0004, $A303
    dw $0004, $A309
    dw !IGotoDecrement, p_pb_hloop
    dw !IJSR, $e020
    dw !IGoto, p_hidden_item_loop2

p_visible_item:
    dw !ILoadCustomGraphics
    dw !IBranchItem, .end
    dw !ISetGoto, .trigger
    dw !ISetPreInstructionCode, $df89
    dw !IStartDrawLoop
    .loop
    dw !IDrawCustom1
    dw !IDrawCustom2
    dw !IGoto, .loop
    .trigger
    dw !ISetItem
    dw SOUNDFX : db !Click
    dw !IPickup
    .end
    dw !IGoto, $dfa9

p_chozo_item:
    dw !ILoadCustomGraphics
    dw !IBranchItem, .end
    dw !IJSR, $dfaf
    dw !IJSR, $dfc7
    dw !ISetGoto, .trigger
    dw !ISetPreInstructionCode, $df89
    dw !ISetCounter8 : db $16
    dw !IStartDrawLoop
    .loop
    dw !IDrawCustom1
    dw !IDrawCustom2
    dw !IGoto, .loop
    .trigger
    dw !ISetItem
    dw SOUNDFX : db !Click
    dw !IPickup
    .end
    dw $0001, $a2b5
    dw !IKill   

p_hidden_item:
    dw !ILoadCustomGraphics
    .loop2
    dw !IJSR, $e007
    dw !IBranchItem, .end
    dw !ISetGoto, .trigger
    dw !ISetPreInstructionCode, $df89
    dw !ISetCounter8 : db $16
    dw !IStartHiddenDrawLoop
    .loop
    dw !IDrawCustom1
    dw !IDrawCustom2
    dw !IGotoDecrement, .loop
    dw !IJSR, $e020
    dw !IGoto, .loop2
    .trigger
    dw !ISetItem
    dw SOUNDFX : db !Click
    dw !IPickup
    .end
    dw !IJSR, $e032
    dw !IGoto, .loop2

i_start_draw_loop:
    phy : phx
    lda $1dc7, x              ; Load PLM room argument
    asl #3 : tax
    lda.l rando_item_table+$2, x ; Load item id
    asl #4
    clc : adc #$000C
    tax
    lda sm_item_table, x      ; Load next loop point if available
    beq .custom_item
    plx : ply
    tay
    rts

.custom_item
    plx
    ply
    rts

i_start_hidden_draw_loop:
    phy : phx
    lda $1dc7, x              ; Load PLM room argument
    asl #3 : tax
    lda.l rando_item_table+$2, x ; Load item id
    asl #4
    clc : adc #$000E
    tax
    lda sm_item_table, x      ; Load next loop point if available
    beq .custom_item
    plx : ply
    tay
    rts

.custom_item
    plx
    ply
    rts

i_load_custom_graphics:
    phy : phx : phx
    lda $1dc7, x              ; Load PLM room argument
    asl #3 : tax
    lda.l rando_item_table+$2, x ; Load item id
    plx

    %a8()
    sta $4202
    lda #$0A
    sta $4203
    nop : nop : %ai16()
    lda $4216               ; Multiply it by 0x0A
    clc
    adc #sm_item_graphics
    tay                     ; Add it to the graphics table and transfer into Y
    lda $0000, y
    cmp #$8000
    bcc .no_custom    
    jsr $8764               ; Jump to original PLM graphics loading routine
    plx
    ply
    rts

.no_custom
    tay
    lda $0000, y
    sta.l $7edf0c, x
    plx
    ply
    rts

i_visible_item_setup:
    phy : phx
    lda $1dc7, y                    ; Load PLM room argument (contains location index of item)
    asl #3                          ; Multiply by 8 for table width
    tax
    lda.l rando_item_table+$2, x       ; Load item id from item table
    %a8()
    sta $4202
    lda #$0A
    sta $4203
    nop : nop : %ai16()
    lda $4216                       ; Multiply it by 0x0A
    tax

    lda sm_item_graphics, x
    cmp #$8000
    bcc .no_custom
    plx : ply
    jmp $ee64

.no_custom
    plx : ply
    tyx
    sta.l $7edf0c, x
    jmp $ee64

i_hidden_item_setup:
    phy : phx
    lda $1dc7, y                    ; Load PLM room argument (contains location index of item)
    asl #3                          ; Multiply by 8 for table width
    tax
    lda.l rando_item_table+$2, x       ; Load item id from item table
    %a8()
    sta $4202
    lda #$0A
    sta $4203
    nop : nop : %ai16()
    lda $4216                       ; Multiply it by 0x0A
    tax

    lda sm_item_graphics, x
    cmp #$8000
    bcc .no_custom
    plx : ply
    jmp $ee8e
    
.no_custom
    plx : ply
    tyx
    sta.l $7edf0c, x
    jmp $ee8e


i_load_rando_item:
    cmp #$0006 : bne +
    ldy #p_visible_item
    bra .end
+   cmp #$0008 : bne +    
    ldy #p_chozo_item
    bra .end
+   ldy #p_hidden_item

.end
    rts

; Pick up SM item
i_live_pickup:
    phx : phy : php
    lda $1dc7, x              ; Load PLM room argument
    asl #3 : tax
    
    ; lda.l rando_item_table, x ; Load item type
    ; beq .own_item

.multiworld_item                    ; This is someone elses item, send message
    phx
    lda.l rando_item_table+$4, x    ; Load item owner into Y
    tay
    lda.l rando_item_table+$2, x    ; Load original item id into X
    tax
    pla                             ; Multiworld item table id in A
    phx : phy : pha
    jsl mw_write_message            ; Send message
    plx
    lda.l rando_item_table, x ; Load item type
    beq .own_item
    ply : plx
    jsl mw_display_item_sent     ; Display custom message box
    bra .end

.own_item
    ply : pla
    lda.l rando_item_table+$2, x ; Load item id
    jsr receive_sm_item
    bra .end

.end
    plp : ply : plx
    rts


; Item index to receive in A
receive_sm_item:
    asl : asl : asl : asl
    phx
    clc
    adc #sm_item_table ; A contains pointer to pickup routine from item table
    tax
    tay
    iny : iny          ; Y points to data to be used in item pickup routine
    jsr ($0000,x)
    plx
    rts

mw_call_receive:
    phx : phy
    jsr SETFX
    lda #$0037
    jsl $809049
    ply : plx
    jsr ($0000,x)
    rtl

pullpc