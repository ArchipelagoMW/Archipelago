lorom

; RTA Timer (timer 1 is frames, and timer 2 is number of times frames rolled over)
!timer1 = $05b8
!timer2 = $05ba

; Temp variables (define here to make sure they're not reused, make sure they're 2 bytes apart)
; These variables are cleared to 0x00 on hard and soft reset
!door_timer_tmp = $7fff00
!door_adjust_tmp = $7fff02
!add_time_tmp = $7fff04
!region_timer_tmp = $7fff06
!region_tmp = $7fff08

; -------------------------------
; HIJACKS
; -------------------------------

; Samus hit a door block (Gamestate change to $09 just before hitting $0a)
org $82e176
    jml door_entered

; Samus gains control back after door (Gamestate change back to $08 after door transition)
org $82e764
    jml door_exited

; Door starts adjusting
org $82e309
    jml door_adjust_start

; Door stops adjusting
org $82e34c
    jml door_adjust_stop

; Firing charged beam
org $90b9a1
    jml charged_beam

; Firing SBAs
org $90ccde
    jmp fire_sba_local	

;Missiles/supers fired
org $90beb7
    jml missiles_fired

;Bombs/PBs laid
org $90c107
    jml bombs_laid

org $90f800
fire_sba_local:
    jml fire_sba

; -------------------------------
; CODE (using bank A1 free space)
; -------------------------------
org $a1ec00
; Helper function to add a time delta, X = stat to add to, A = value to check against
; This uses 4-bytes for each time delta
add_time:
    sta !add_time_tmp
    lda !timer1
    sec
    sbc !add_time_tmp
    sta !add_time_tmp
    txa
    jsl load_stat
    clc
    adc !add_time_tmp
    bcc +
    jsl store_stat    ; If carry set, increase the high bits
    inx
    txa
    jsl inc_stat
+
    jsl store_stat  
    rts


; Samus hit a door block (Gamestate change to $09 just before hitting $0a)
door_entered:
    lda #$0002  ; Number of door transitions
    jsl inc_stat  

    lda !timer1
    sta !door_timer_tmp ; Save RTA time to temp variable

    ; Run hijacked code and return
    plp
    inc $0998
    jml $82e1b7

; Samus gains control back after door (Gamestate change back to $08 after door transition)
door_exited:
    ; Increment saved value with time spent in door transition
    lda !door_timer_tmp
    ldx #$0003
    jsr add_time

    ; Store time spent in last room/area unless region_tmp is 0
    lda !region_tmp
    beq +
    tax
    lda !region_timer_tmp
    jsr add_time

    
+   ; Store the current frame and the current region to temp variables
    lda !timer1
    sta !region_timer_tmp
    lda $7e079f
    asl
    clc
    adc #$0007    
    sta !region_tmp    ; Store (region*2) + 7 to region_tmp (This uses stat id 7-18 for region timers)

    ; Run hijacked code and return
    lda #$0008
    sta $0998
    jml $82e76a

; Door adjust start
door_adjust_start:
    lda !timer1
    sta !door_adjust_tmp ; Save RTA time to temp variable

    ; Run hijacked code and return
    lda #$e310
    sta $099c
    jml $82e30f

; Door adjust stop
door_adjust_stop:
    lda !door_adjust_tmp
    inc ; Add extra frame to time delta so that perfect doors counts as 0
    ldx #$0005
    jsr add_time

    ; Run hijacked code and return
    lda #$e353
    sta $099c
    jml $82e352

; Charged Beam Fire
charged_beam:
    lda #$0014
    jsl inc_stat

    ; Run hijacked code and return
    LDX #$0000
    LDA $0c2c, x
    JML $90b9a7

; Firing SBAs : hijack the point where new qty of PBs is stored
fire_sba:
    ; check if SBA routine actually changed PB count: means valid beam combo selected
    cmp $09ce
    beq .end
    pha
    lda #$0015
    jsl inc_stat
    pla
    ; Run hijacked code and return
.end:
    sta $09ce
    jml $90cce1

;MissilesSupers used
missiles_fired:
    lda $09d2
    cmp #$0002
    beq .super
    dec $09c6
    lda #$0016
    jsl inc_stat
    bra .end
.super:
    dec $09ca
    lda #$0017
    jsl inc_stat
.end:
    jml $90bec7

;bombs/PBs laid
bombs_laid:
    lda $09d2			; HUD sleection index
    cmp #$0003
    beq .power_bomb
    lda #$001a
    bra .end
.power_bomb:
    lda #$0018
.end:
    jsl inc_stat
    ;run hijacked code and return
    lda $0cd2
    inc
    jml $90c10b
