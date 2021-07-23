;;; VARIA new game hook: skips intro and customizes starting point
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

arch snes.cpu
lorom

;;; CONSTANTS
!GameStartState = $7ED914
!new_save	= $81ef22

;;; HIJACKS (bank 82 init routines)

org $82801d
    jsl startup

org $828067
    jsl gameplay_start

;;; This skips the intro : game state 1F instead of 1E
org $82eeda
    db $1f

;;; DATA in bank A1 (start options)

org $a1f200
print "start_location: ", pc
start_location:
    ;; start location: $0000=Zebes Landing site, $fffe=Ceres,
    ;; otherwise hi byte is area and low is save index.
    ;; (use FFFE as Ceres special value because FFFF can be mistaken
    ;; for free space by solver/tracker)
    dw $0000			; defaults to landing site
opt_doors:
    ;; optional doors to open.
    ;; door ID is low byte PLM argument when editing doors in SMILE
    ;; terminate with $00
    db $10,$32			; defaults to red tower top+construction zone
    db $00

warnpc $a1f20f

;;; CODE in bank A1
org $a1f210
;;; zero flag set if we're starting a new game
;;; called from credits_varia as well
print "check_new_game: ", pc
check_new_game:
    ;; Make sure game mode is 1f
    lda $7e0998
    cmp #$001f : bne .end
    ;; check that Game time and frames is equal zero for new game
    ;; (Thanks Smiley and P.JBoy from metconst)
    lda $09DA
    ora $09DC
    ora $09DE
    ora $09E0
.end:
    rtl

startup:
    jsl check_new_game      : bne .end
    lda.l start_location    : beq .zebes
    cmp #$fffe              : beq .ceres
    ;; custom start point on Zebes
    pha
    and #$ff00 : xba : sta $079f ; hi byte is area
    pla
    and #$00ff : sta $078b      ; low byte is save index
    lda #$0000 : jsl $8081fa    ; wake zebes
.zebes:
    lda #$0005 : bra .store_state
.ceres:
    lda #$001f
.store_state:
    sta !GameStartState
.end:
    ;; run hijacked code and return
    lda !GameStartState
    rtl

gameplay_start:
    jsl check_new_game  : bne .end
    ;; Set doors to blue if necessary
    phx
    ldx #$0000
-
    lda.l opt_doors,x : and #$00ff
    beq .save			; end list
    phx
    jsl $80818e		    ; call bit index function, returns X=byte index, $05e7=bitmask
    ;; Set door in bitfield
    lda $7ED8B0,x : ora $05E7 : sta $7ED8B0,x
    plx
    inx : bra -		    ; next
.save:
    ;; Call the save code to create a new file
    plx
    jsl !new_save		; see credits_varia
.end:
    rtl

warnpc $a1f29f

;;; since this patch is always included, we can put utility
;;; routines for other patches here (in fixed locations)

!RNG		= $808111	; RNG function
!RNG_seed	= $05e5
!RTA_timer	= $05b8		; see tracking.asm

org $a1f2a0
;;; single use (will give the same result if called several times in the same frame)
;;; random function that leaves game rng untouched
;;; result in A
rand:
    phy
    lda !RNG_seed : pha             ; save current rand seed
    eor !RTA_timer : sta !RNG_seed  ; alter seed with frame counter
    jsl !RNG : tay                  ; call RNG and save result to Y
    pla : sta !RNG_seed             ; restore current rand seed
    tya                             ; get RNG result in A
    ply
    rtl

org $a1f2c0
;;; courtesy of Smiley
fix_timer_gfx:
    PHX
    LDX $0330						;get index for the table
    LDA #$0400 : STA $D0,x  				;Size
    INX : INX						;inc X for next entry (twice because 2 bytes)
    LDA #$C000 : STA $D0,x					;source address
    INX : INX						;inc again
    SEP #$20 : LDA #$B0 : STA $D0,x : REP #$20  		;Source bank $B0
    INX							;inc once, because the bank is stored in one byte only
    ;; VRAM destination (in word addresses, basically take the byte
    ;; address from the RAM map and and devide them by 2)
    LDA #$7E00	: STA $D0,x
    INX : INX : STX $0330 					;storing index
    PLX
    RTL							;done. return

warnpc $a1f2ff

;;; patch morph+missile room state check
org $8fe652
morph_missile_check:
    ;; check that zebes is awake instead: works with both standard
    ;; start with wake_zebes.ips, and non standard start with wake
    ;; zebes forced from the start.
    lda #$0000 : jsl $808233
    bcc .not_awake
    bra .awake
org $8fe65f
.awake:
org $8fe666
.not_awake:
