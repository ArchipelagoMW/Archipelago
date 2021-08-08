; --- new control code routine ---

; This sets up for screw attack without space jump.
; First off, we need a new control code that checks for space jump, so that we
; can gate the animation appropriately.

org $908688
control_code_routine:
    LDA $09A2           ; get item equipped info
    BIT #$0200          ; check for space jump equipped
    BNE .screw_attack   ; if space jump, branch to space jump stuff
    LDA.l config_screw_attack
    BEQ .screw_attack   ; if disabled, do regular screw attack animation (if branch taken, uses one more clock cycle)

.spin_attack:
    LDA.l $7E0A96       ; get the pose number (LDA.l here to add one more clock cycle to preserve timing)
    CLC                 ; prepare to do math
    ADC #$001B          ; skip past the old screw attack to the new stuff
    BRA .exit           ; then prepare to end subroutine

.screw_attack
    LDA $0A96           ; get the pose number
    CLC                 ; prepare to do math
    ADC #$0001          ; just add one to go to the old screw attack (instead of INC to preserves timing)
    BRA .exit           ; then prepare to end subroutine (could skip, but timing)

.exit:
    STA $0A96           ; store the new pose in the correct spot
    TAY                 ; transfer to Y because reasons
    SEC                 ; flag the carry bit because reasons
    RTS


; Hook the subroutine to control code $F5

org $90832E
    dw control_code_routine


; We want the $F5 code to run right after the $FB code. The $F5 code adds 1/27
; for space jump equipped/unequiped, but we technically want to add 0/26. This
; is solved by by having $FB add one less, and, with neither waste nor want, by
; sliding in a JMP so that return and result turns out correct.
;org $908482
;   ADC #$0015
;   STA $0A96
;   TAY
;   SEC
;   RTS

org $908482
    ADC #$0014
    STA $0A96
    JMP control_code_routine


; --- implement spin attack ---

; The control codes now need to be integrated with the screw attack and
; walljump animation sequences. We need space from bank $91. Screw attack is
; relocated into $91:812D-816E. Since much of the code is duplicated, we just
; need to move some JSR pointers.

org $918014+(11*2)
    dw $8066, $8066, $8066, $8189, $8086, $8066, $8066, $8066, $8066, $8066


; New screw attack sequence. Leaves 10 bytes to spare.

org $91812D
    db $04, $F5                                                   ; $F5 forces the decision about which sequence to draw
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01 ; old screw attack
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01
    db $FE, $18
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01 ; new spin attack
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01
    db $FE, $18
    db $08, $FF                                                   ; this gives the wall jump prompt when close to a wall


; The subroutine at $91:80BE-8109 is unreachable. The walljump sequence is
; relocate to this space. Leaves 1 byte to spare.

org $9180BE
    db $05, $05                                                   ; lead up into a jump
    db $FB                                                        ; this chooses the type of jump. we have augmented this subroutine
    db $03, $02, $03, $02, $03, $02, $03, $02                     ; spin jump
    db $FE, $08
    db $02, $01, $02, $01, $02, $01, $02, $01                     ; space jump
    db $FE, $08
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01 ; old screw attack
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01
    db $FE, $18
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01 ; new spin attack
    db $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01, $01
    db $FE, $18


; Hook the new sequences

org $91B010+(2*$81)
    dw $812D, $812D, $80BE, $80BE


; Because of this code some things need to be fixed:

; Samus green glow during spin attack
;$91:DA04    CMP #$001B

org $91DA04
    CMP #$0036

; Wall jump check
;$90:9D63    CMP #$001B

org $909D63
    CMP #$0036

; Relocate walljump prompt
;$90:9DD4    LDA #$001A

org $909DD4
    LDA #$0035


; This breaks when Samus turns mid-air, due to:
;$91:F634    LDA #$0001
;$91:F637    STA $0A9A  [$7E:0A9A]
; The value needs to be conditional based on water, screw attack, and space
; jump. With a lack of space in $91 we are doing a JSL into the space for death
; tiles since they are being relocated.

org $9B8000
conditional_pose_routine:
    LDA $09A2           ; get equipped items
    BIT #$0020          ; check for gravity suit
    BNE .equip_check    ; if gravity suit, underwater status is not important
    JSL $90EC58         ; $12 / $14 = Samus' bottom / top boundary position
    LDA $195E           ; get [FX Y position]
    BMI .acid_check     ; if [FX Y position] < 0:, need to check for acid
    CMP $14             ; check FX Y position against Samus's position
    BPL .equip_check    ; above water, so underwater status is not important
    LDA $197E           ; get physics flag
    BIT #$0004          ; if liquid physics are disabled, underwater status is not important
    BNE .equip_check
    BRA .underwater     ; ok, you're probably underwater at this point

.acid_check:
    LDA $1962
    BMI .equip_check    ; if [lava/acid Y position] < 0, then there is no acid, so underwater status is not important
    CMP $14
    BMI .underwater     ; if [lava/acid Y position] < Samus' top boundary position, then you are underwater

.equip_check:
    LDA $09A2           ; get equipped items
    BIT #$0008          ; check for screw attack equipped
    BEQ .first_pose     ; if screw attack not equipped, just do normal advance
    BIT #$0200          ; check for space jump
    BEQ .spin_attack    ; if space jump not equipped, branch out

.screw_attack:
    LDA #$0002          ; default to (new) second pose
    STA $0A9A
    RTL

.spin_attack:
    LDA.l config_screw_attack
    BEQ .screw_attack   ; if disabled, do regular screw attack animation (if branch taken, uses one more clock cycle)
    LDA #$001C          ; skip over to our new spin attack section
    STA.l $7E0A9A       ; (STA.l here to add one more clock cycle to preserve timing)
    RTL

.first_pose:
    LDA #$0001          ; default to first pose, as in classic
    STA $0A9A
    RTL

.underwater             ; figure out if Samus jumped into, or is in, the water, by checking for animation $81 or $82
    LDA $0A1C           ; get animation #
    BIT #$0080          ; check for animations $81, $82
    BEQ .first_pose     ; if not, then just do normal stuff
    BRA .equip_check    ; but if so, we have to go through all the normal checks


; Hook the subroutine
;org $91:F634
;    LDA #$0001
;    STA $0A9A  [$7E:0A9A]

org $91F634
    JSL conditional_pose_routine
    NOP
    NOP
