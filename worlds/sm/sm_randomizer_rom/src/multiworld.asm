; SM Multiworld support
;

; New multiworld communication stuff
!SRAM_MW_ITEMS_RECV = $702000
!SRAM_MW_ITEMS_RECV_RPTR = $702600
!SRAM_MW_ITEMS_RECV_WPTR = $702602
!SRAM_MW_ITEMS_RECV_SPTR = $702604  ; This gets updated on game save and reloaded into RPTR on game load

!SRAM_MW_ITEMS_SENT_RPTR = $702680
!SRAM_MW_ITEMS_SENT_WPTR = $702682
!SRAM_MW_ITEMS_SENT = $702700       ; [worldId, itemId, itemIndex] (need unique item index to prevent duping)

!SRAM_MW_INITIALIZED = $7026fe

!Big = #$825A
!Small = #$8289
!EmptySmall = #$8436
!Shot = #$83C5
!Dash = #$83CC
!EmptyBig = #message_EmptyBig
!PlaceholderBig = #message_PlaceholderBig

mw_init:
    pha : phx : phy : php
    %ai16()

    ; If already initialized, don't do it again
    lda.l !SRAM_MW_INITIALIZED
    cmp #$cafe
    beq .end

    lda #$0000
    ldx #$0000

-
    sta.l !SRAM_MW_ITEMS_RECV, x
    sta.l !SRAM_MW_ITEMS_RECV+$0400, x
    sta.l !SRAM_MW_ITEMS_RECV+$0800, x
    sta.l !SRAM_MW_ITEMS_RECV+$0C00, x
    inx : inx
    cpx #$0400
    bne -

    lda #$cafe
    sta.l !SRAM_MW_INITIALIZED
    
.end
    plp : ply : plx : pla
    rtl

; Write multiworld item message
; A = item index, X = item id, Y = world id (all 16-bit)
mw_write_message:
    pha : phx
    lda.l !SRAM_MW_ITEMS_SENT_WPTR
    asl #3 : tax
    tya
    sta.l !SRAM_MW_ITEMS_SENT, x
    pla
    sta.l !SRAM_MW_ITEMS_SENT+$2, x
    pla
    sta.l !SRAM_MW_ITEMS_SENT+$4, x

    lda.l !SRAM_MW_ITEMS_SENT_WPTR
    inc a
    sta.l !SRAM_MW_ITEMS_SENT_WPTR
    rtl

mw_save_sram:
    pha : php
    %ai16()
    lda.l !SRAM_MW_ITEMS_RECV_RPTR
    sta.l !SRAM_MW_ITEMS_RECV_SPTR
    plp : pla
    rtl

mw_load_sram:
    pha : php
    %ai16()
    lda.l !SRAM_MW_ITEMS_RECV_SPTR
    sta.l !SRAM_MW_ITEMS_RECV_RPTR
    plp : pla
    rtl

; Display message that we picked up someone elses item
; X = item id, Y = player id
mw_display_item_sent:
    stx $c1
    sty $c3
    ;lda #$0168       ; With fanfare skip, no need to queue room track
    ;jsl $82e118      ; Queue room track after item fanfare
    lda #$001d
    jsl $858080
    rtl

mw_receive_item:
    pha : phx
    cmp #$0016
    beq .end                      ; skip receiving if its a Nothing item
    cmp #$0017
    beq .end                      ; skip receiving if its a No Energy item
    asl #4 : tax
    lda.l sm_item_table+$2, x     ; Read item flag
    sta $cc
    lda #$001e
    sta $ce
    lda.l #sm_item_table
    sta $ca
    txa : clc : adc $ca : tax
    ldy #$00cc
    jsl mw_call_receive           ; Call original item receive code (reading the item to get from $cc-ce)
.end
    plx : pla
    rts

mw_handle_queue:
    pha : phx

.loop

    lda.l !SRAM_MW_ITEMS_RECV_RPTR
    cmp.l !SRAM_MW_ITEMS_RECV_WPTR
    beq .end

    asl #2 : tax
    lda.l !SRAM_MW_ITEMS_RECV, x : sta $c3
    lda.l !SRAM_MW_ITEMS_RECV+$2, x : sta $c1
    jsr mw_receive_item

    lda.l !SRAM_MW_ITEMS_RECV_RPTR
    inc a
    sta.l !SRAM_MW_ITEMS_RECV_RPTR

    bra .loop    

.end
    plx : pla
    rts

mw_hook_main_game:
    jsl $A09169     ; Last routine of game mode 8 (main gameplay)
    lda config_multiworld
    beq +
    lda $0998
    cmp #$0008
    bne +
    jsr mw_handle_queue     ; Handle MW RECVQ only in gamemode 8 
+
    rtl

pushpc
org $828BB3
    jsl mw_hook_main_game

namespace message
org $859643
    dw !PlaceholderBig, !Big, item_sent
    dw !PlaceholderBig, !Big, item_received
    dw !EmptySmall, !Small, btn_array

table box.tbl,rtl
    ;   0                              31
item_sent:
    dw "___         YOU FOUND        ___"
    dw "___      ITEM NAME HERE      ___"
    dw "___           FOR            ___"
    dw "___          PLAYER          ___"

item_received:
    dw "___       YOU RECEIVED       ___"
    dw "___      ITEM NAME HERE      ___"
    dw "___           FROM           ___"
    dw "___          PLAYER          ___"

cleartable

btn_array:
	DW $0000, $012A, $012A, $012C, $012C, $012C, $0000, $0000, $0000, $0000, $0000, $0000, $0120, $0000, $0000
	DW $0000, $0000, $0000, $012A, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000
    DW $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000, $0000

table box_yellow.tbl,rtl
item_names:
    dw "___      AN ENERGY TANK      ___"
    dw "___         MISSILES         ___"
    dw "___       SUPER MISSILES     ___"
    dw "___        POWER BOMBS       ___"
    dw "___          BOMBS           ___"
    dw "___       CHARGE BEAM        ___"
    dw "___         ICE BEAM         ___"
    dw "___       HI-JUMP BOOTS      ___"
    dw "___       SPEED BOOSTER      ___"
    dw "___        WAVE BEAM         ___"
    dw "___       S P A Z E R        ___"
    dw "___       SPRING BALL        ___"
    dw "___        VARIA SUIT        ___"
    dw "___       GRAVITY SUIT       ___"
    dw "___       X-RAY SCOPE        ___"
    dw "___       PLASMA BEAM        ___"
    dw "___      GRAPPLING BEAM      ___"
    dw "___        SPACE JUMP        ___"
    dw "___       SCREW ATTACK       ___"
    dw "___       MORPHING BALL      ___"
    dw "___      A RESERVE TANK      ___"

    ; add 100 more entries for worst case of a different item at each location
    ; to be filled by patcher
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
    dw "________________________________"
cleartable


write_placeholders:
    phx : phy
    lda $1c1f
    cmp #$001d
    beq .adjust
    cmp #$001e
    beq .adjust
    bra .end

.adjust
    lda $c1                 ; Load item id
    asl #6 : tay
    ldx #$0000
-
    lda item_names, y       ; Write item name to box
    sta.l $7e3280, x
    inx #2 : iny #2
    cpx #$0040
    bne -

    lda $c3                 ; Load player 1
    asl #4 : tax
    ldy #$0000
-
    lda.l rando_player_table, x
    and #$00ff
    phx
    asl : tax               ; Put char table offset in X
    lda char_table-$40, x 
    tyx
    sta.l $7e3310, x        ; 16 bytes player name now instead of 12
    iny #2
    plx
    inx
    cpy #$0020              ; 16 bytes player name now instead of 12
    bne -
    rep #$30

.end
    ply : plx
    lda #$0020
    rts

char_table:
    ;  <sp>     !      "      #      $      %      %      '      (      )      *      +      ,      -      .      /
    dw $384E, $38FF, $38FD, $38FE, $38FE, $380A, $38FE, $38FD, $38FE, $38FE, $38FE, $38FE, $38FB, $38FC, $38FA, $38FE
    ;    0      1      2      3      4      5      6      7      8      9      :      ;      <      =      >      ?
    dw $3809, $3800, $3801, $3802, $3803, $3804, $3805, $3806, $3807, $3808, $38FE, $38FE, $38FE, $38FE, $38FE, $38FE
    ;    @      A      B      C      D      E      F      G      H      I      J      K      L      M      N      O 
    dw $38FE, $38E0, $38E1, $38E2, $38E3, $38E4, $38E5, $38E6, $38E7, $38E8, $38E9, $38EA, $38EB, $38EC, $38ED, $38EE
    ;    P      Q      R      S      T      U      V      W      X      Y      Z      [      \      ]      ^      _   
    dw $38EF, $38F0, $38F1, $38F2, $38F3, $38F4, $38F5, $38F6, $38F7, $38F8, $38F9, $38FE, $38FE, $38FE, $38FE, $38FE

org $858749
fix_1c1f:
    LDA $CE     ; if $CE is set, it overrides the message box
    BEQ +
    STA $1C1F
    STZ $CE     ; Clear $CE
+	LDA $1C1F
	CMP #$001D
	BPL +
	RTS
+
	ADC #$027F
	RTS
EmptyBig:
	REP #$30
    LDY #$0000
	JMP $841D
PlaceholderBig:
    REP #$30
    JSR write_placeholders
    LDY #$0000
    JMP $841D

org $858243
	JSR fix_1c1f

org $8582E5
	JSR fix_1c1f

org $858413
	DW btn_array

pullpc
namespace off
