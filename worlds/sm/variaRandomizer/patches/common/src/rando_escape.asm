;;; Randomized escape sequence
;;;
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),

lorom
arch snes.cpu

;;; carry set if escape flag on, carry clear if off
macro checkEscape()
    lda #$000e : jsl $808233
endmacro

;;; see random_music.asm
!random_music_hook   = $82df3e
!random_music 	     = $a1f3f0
;;; where we are in current escapes cycle (for animals)
!current_escape      = $7fff34
!door_sz             = 12
!door_list_ptr       = $07b5

;;; external definitions
!fix_timer_gfx	     = $a1f2c0	; in new_game.asm (common routines section)
!scavenger_escape_flag = $a1f5fc ; in varia_hud.asm (option flag)

org $809E21
print "timer_value: ", pc
timer_value:
;   dw #$1030

;;; HIJACKS
org $82df38
    jml music_and_enemies

org $848c91
    jmp map_station

org $848cf3
    jmp save_station

org $84c556
    jsr super_check             ; green gate left

org $84c575
    jsr super_check             ; green gate right

org $84cee8
    jsr pb_check                ; bomb block PB reaction

org $84cf3c
    jsr pb_check                ; PB block

org $84cf75
    jsr super_check             ; super block

org $8fe896
    jsr room_setup

org $8fe8bd
    jsr room_main

;;; DATA in bank 83

;;; ASM ptr for down door at the beggining of escape
org $83aaf6
    dw escape_setup

;;; alternate flyway (= pre BT) door lists for escape animals surprise
macro FlywayDoorList()
    ;; door to parlor
    db $FD, $92, $00, $05, $3E, $26, $03, $02, $00, $80, $A2, $B9
    ;; placeholder for BT door to be filled in by randomizer
    db $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca
endmacro

org $83ADA0
print "flyway_door_lists : ", pc
flyway_door_lists:
%FlywayDoorList()
%FlywayDoorList()
%FlywayDoorList()
%FlywayDoorList()

print "bt_door_list : ", pc
bt_door_list:
	;; placeholder for inside BT door to get back from animals during escape
	db $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca, $ca

warnpc $83ae0f

;;; CODE in bank 84 (PLM)
org $84f860

;;; Disables "ammo locked" elements b/c of no ammo in escape :
;;; makes them react to hyper beam shots

;;; returns zero flag set if in the escape and projectile is hyper beam
escape_hyper_check:
    %checkEscape() : bcc .nohit
    lda $0c18,x
    bit #$0008                  ; check for plasma (hyper = wave+plasma)
    beq .nohit
    ;; avoid having actual plasma beam destroy blocks in scavenger mode escape
    lda !scavenger_escape_flag
    cmp #$0001 : beq .nohit
    lda #$0000                  ; set zero flag
    bra .end
.nohit:
    lda #$0001                  ; reset zero flag
.end:
    rts

super_check:
    cmp #$0200                  ; vanilla check for supers
    beq .end
    jsr escape_hyper_check
.end:
    rts

pb_check:
    cmp #$0300                  ; vanilla check for PBs
    beq .end
    jsr escape_hyper_check
.end:
    rts

;;; make all map stations reveal all the map
;;; we do this because only crateria map station
;;; will be opened.
map_station:
    ;; activate map stations for all regions
    lda #$ffff
    ldx #$0000
-
    sta $7ed908,x
    inx : inx
    cpx #$0008
    bcc -
    ;; resume original routine
    jmp $8c9f

;;; Disables save stations during the escape
save_station:
    %checkEscape() : bcc .resume
    ;; disable save
    jmp $8d32
.resume:
    ;; resume original routine
    lda #$0017
    jmp $8cf6

print "B84 end: ", pc
warnpc $84f8bb                  ; explicitly right there, to remember needed race mode update

;;; DATA, bank 8F. makes map stations doors in norfair/brin/maridia/ws
;;; permanently grey
org $8f8b06                     ; norfair map
    dw $C848
    db $01,$46
    dw $904C

org $8fc547                     ; maridia map
    dw $C842
    db $0E,$16
    dw $9090

org $8f84b8                     ; brinstar map
    dw $C848
    db $01,$46
    dw $9020

;;; other door tweaks
;; open Tourian grey doors to disable one way
org $8fc828
    db $0c

org $8fc836
    db $0c

;; open crateria doors to open path for animais searching
org $8f81b1
    db $10

org $8f804f
    db $10

;; open bowling alley door to escape the room
org $8fc2fa
    db $10


;;; overwrite BT setup ASM ptr in "escape" room state
org $8f9867
    dw bt_escape_setup

;;; overwrite flyway setup ASM ptr in "escape" room state
org $8F98DC
    dw flyway_escape_setup

;;; overwrite WS main shaft setup asm ptr in "phantoon dead" state
org $8fcb3a
    dw wrecked_ship_main_setup

;; ws map door handled with PLM spawn table, as it is blue in vanilla (see plm_spawn.asm)

org $8ff500

;;; CODE (in a tiny bit of bank 8F free space)
escape_setup_l:
    ;; init possible escapes cycle (for animals)
    lda #$0000 : sta !current_escape
    ;; open all doors
    lda #$ffff
    ldx #$0000
-
    sta $7ed8b0,x
    inx : inx
    cpx #$0020
    bcc -
    ;; kill all bosses
    ldx #$0000
-
    sta $7ed828,x
    inx : inx
    cpx #$0008
    bcc -
    ;; open Maridia Tube
    lda #$000b : jsl $8081fa
.end:
    rtl

test_door_asm:
    lda #$0000 : jsl $8081fa    ; wake zebes
    lda #$000e : jsl $8081fa    ; set escape flag
;;; door ASM for MB escape door
escape_setup:
    jsl escape_setup_l
    rts

room_setup:
    jsl check_ext_escape : bcc .end
    phb                         ; do vanilla setup to call room asm
    phk
    plb
    jsr $919c                   ; sets up room shaking
    plb
    jsl !fix_timer_gfx
.end:
    ;; goes back to vanilla setup asm call
    lda $0018,x
    rts

room_main:
    jsl check_ext_escape : bcc .end
    phb                         ; do vanilla setup to call room asm
    phk
    plb
    jsr $c124                   ; explosions etc
    plb
.end:
    ;; goes back to vanilla room asm call
    ldx $07df
    rts

wrecked_ship_main_setup:
	%checkEscape() : bcc .end
	;; call asm of door from below,
	;; that sets the scroll properly
	;; (needed because of the super/hyper blocks)
	jsr $e21a
.end:
	rts

;;; stop before area rando door transition patch
warnpc $8ff5ff

;;; flyway door list pointers for escape animals (same place as animals surprise patches)
org $8ff000
flyway_door_ptrs:
macro FlywayDoorPtrs(n)
    dw flyway_door_lists+(!door_sz*2*<n>)
    dw flyway_door_lists+(!door_sz*((2*<n>)+1))
endmacro

%FlywayDoorPtrs(0)
%FlywayDoorPtrs(1)
%FlywayDoorPtrs(2)
%FlywayDoorPtrs(3)

print "flyway_escape_setup : ", pc
flyway_escape_setup:
    ;; get current door ptr list :
    ;; ptr = flyway_door_ptrs + current_escape*4
    lda !current_escape : asl : asl
    clc : adc #flyway_door_ptrs
    ;; replace it in RAM
    sta !door_list_ptr
    ;; run vanilla setup ASM
    jmp $91BB

warnpc $8ff02f

;; to call during BT door asm
org $8ff030
setup_next_escape:
    %checkEscape() : bcc .end
    ;; current_escape = (current_escape + 1) % 4
    lda !current_escape : inc : and #$0003 : sta !current_escape
.end:
    rts

bt_door_ptr:
    dw bt_door_list

bt_escape_setup:
    ;; replace door out list ptr in RAM
    lda #bt_door_ptr : sta !door_list_ptr
    ;; run vanilla setup ASM
    jmp $91B2

warnpc $8ff0ff

;;; DATA (bank A1 free space)
org $a1f000

;;; OPTIONS
print "opt_remove_enemies: ", pc
opt_remove_enemies:
    dw $0001

;;; custom enemy populations for some rooms

;;; room ID, enemy population in bank a1, enemy GFX in bank b4
enemy_table:
    dw $a7de,one_elev_list_1,$8aed  ; business center
    dw $a6a1,$98e4,$8529            ; warehouse (vanilla data)
    dw $a98d,$bb0e,$8b11            ; croc room (vanilla "croc dead" data)
    dw $962a,$89DF,$81F3            ; red brin elevator (vanilla data)
    dw $a322,one_elev_list_1,$863F  ; red tower top
    dw $94cc,$8B74,$8255            ; forgotten hiway elevator (vanilla data)
    dw $d30b,one_elev_list_2,$8d85  ; forgotten hiway
    dw $9e9f,one_elev_list_3,$83b5  ; morph room
    dw $97b5,$8b61,$824b            ; blue brin elevator (vanilla data)
    dw $9ad9,one_elev_list_1,$8541  ; green brin shaft
    dw $9938,$8573,$80d3            ; green brin elevator (vanilla data)
    dw $af3f,$a544,$873d            ; LN elevator (vanilla data)
    dw $b236,one_elev_list_4,$893d  ; LN main hall
    dw $d95e,$de5a,$9028            ; botwoon room (vanilla "botwoon dead" data)
    dw $a66a,$9081,$8333            ; G4 (G4?) (vanilla data)
    ;; table terminator
    dw $ffff

one_elev_list_1:
    dw $D73F,$0080,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_2:
    dw $D73F,$0080,$02C0,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_3:
    dw $D73F,$0580,$02C2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00

one_elev_list_4:
    dw $D73F,$0480,$02A2,$0000,$2C00,$0000,$0001,$0018,$ffff
    db $00


;;; CODE (in bank A1 free space)

;;; checks the need for "extended escape" setup
;;; return carry set if setup is needed, carry clear if not
check_ext_escape:
    %checkEscape() : bcc .end
    ;; filter out Tourian area and Crateria escape rooms
    ;; (already handled by the game)
    lda $079f                  ; current area
    cmp #$0005 : beq .filtered ; filter out Tourian
    cmp #$0000 : bne .needed   ; if not crateria, we have to do extended escape
    lda $079b                  ; current room (in crateria)
    ;; few rooms, so do a nasty "if/elseif" instead of iterating through a table
    cmp #$91f8 : beq .filtered ; Landing site
    cmp #$92fd : beq .filtered ; parlor
    cmp #$9879 : beq .filtered ; BT hallway
    cmp #$9804 : beq .filtered ; BT
    cmp #$96ba : beq .filtered ; climb
.needed:
    sec
    bra .end
.filtered:
    clc
.end:
    rtl

music_and_enemies:
    lda $0006,x                 ; common vanilla fx load
    sta $07CD
    jsl check_ext_escape : bcs .escape
    ;; vanilla
    ;; check presence of random music patch
    lda.l !random_music_hook
    and #$00ff : cmp #$005c	; JML instruction
    bne .vanilla_music
    jsl !random_music
    bra .vanilla_enemies
.vanilla_music:
    lda $0004,x ;\
    and #$00ff  ;} Music data index = [[X] + 4]
    sta $07CB   ;/
    lda $0005,x ;\
    and #$00FF  ;} Music track index = [[X] + 5]
    sta $07C9   ;/
.vanilla_enemies:
    lda $0008,x ;\
    sta $07CF   ;} Enemy population pointer = [[X] + 8]
    lda $000A,x ;\
    sta $07D1   ;} Enemy set pointer = [[X] + Ah]
    bra .end
.escape:
    stz $07CB   ;} Music data index = 0
    stz $07C9   ;} Music track index = 0
    ;; check room ID against list of custom enemy populations (elevators etc.)
    phb : phk : plb             ; data bank=program bank
    lda opt_remove_enemies
    bne .remove_enemies
    ;; vanilla enemies load
    plb
    bra .vanilla_enemies
.remove_enemies:
    ldy #$0000
.loop:
    lda enemy_table,y
    cmp #$ffff
    beq .empty_list
    lda $079B
    cmp enemy_table,y
    beq .load
    rep 6 : iny
    bra .loop
.load:
    iny : iny
    lda enemy_table,y
    sta $07CF
    iny : iny
    lda enemy_table,y
    sta $07D1
    plb
    bra .end
.empty_list:
    plb
    lda #$85a9  ;\
    sta $07CF   ;} Enemy population pointer = empty list
    lda #$80eb  ;\
    sta $07D1   ;} Enemy set pointer = empty list
.end:
    jml $82df5c

warnpc $a1f1ff

;; ;;; TEST
;; org $83AB34
;;     ;; escape door header => norfair map station
;;     dw $A7DE
;;     db $00,$04,$01,$46,$00,$04
;;     dw $8000
;;     ;; dw test_door_asm                    ; sets escape flag and triggers escape setup asm
;; ;;; END TEST
