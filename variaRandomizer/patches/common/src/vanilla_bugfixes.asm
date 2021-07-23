;;; Some vanilla bugfixes included in all VARIA seeds
;;; compile with asar

arch snes.cpu
lorom

;;; skips suits acquisition animation
org $848717
	rep 4 : nop

;;; fix to speed echoes bug when hell running
org $91b629
	db $01

;;; disable GT code
org $aac91c
	bra $3f

;;; Pause menu fixes :

;;; disable spacetime beam select in pause menu
org $82b174
	ldx #$0001
;;; fix screw attack select in pause menu
org $82b4c4
	cpx #$000c
;;; In inventory menu, when having only a beam and a suit you have
;;; to press right+up to go from beam to suit.
;;; It's not natural, so fix it to only require right.
org $82b000
	;; test of return of $B4B7 compare A and #$0000,
	;; when no item found A==#$ffff, which sets the carry,
	;; so when carry is clear it means that an item was found in misc.
	;; if no item was found in misc, we check in boots then in suits,
	;; so if an item is found in both boots and suits, as suits is
	;; tested last the selection will be set on suits.
	bcc $64

;;; fix morph ball in hidden chozo PLM
org $84e8ce
	db $04
org $84ee02
	db $04

;;; To allow area transition blinking doors in rooms with no enemies,
;;; fixes enemies loading so that when there are no enemies, some values
;;; are still reset
org $a08ae5
	;; hijack enemy list empty check
	jsr check_empty
org $a0f820
check_empty:
	cmp #$ffff		; original empty enemy list check
	bne .end		; it not empty: return
	stz $0e4e		; nb of enemies in the room = 0
	stz $0e52		; nb of enemies needed to clear the room = 0
.end:
	rts

warnpc $a0f830

;;; Fixes for the extra save stations in area rando/random start :

;;; allow all possible save slots (needed for area rando extra stations)
org $848d0c
	and #$001f
;;; For an unknown reason, the save station we put in main street
;;; sometimes (circumstances unclear) spawn two detection PLMs
;;; instead of one. These PLMs are supposed to precisely detect
;;; when Samus is standing on the save. When Samus does, it looks
;;; for a PLM at the same coordinates as itself, which is normally
;;; the actual save station PLM.
;;; But when two detection blocks are spawn, it detects the other detection
;;; block as being the save, and the save station doesn't work.
;;; Therefore, we add an extra check on PLM type to double check it has
;;; actually found the save station PLM.

;;; hijack in detection block PLM code when samus is
;;; positioned correctly
org $84b5d4
search_loop_start:
	jmp save_station_check
org $84b5d9
search_loop_cont:
org $84b5df
search_loop_found:
;;; some unused bank 84 space
org $84858c
save_station_check:
	cmp $1c87,x		; original block coord check
	beq .coords_ok
	jmp search_loop_cont
.coords_ok:
	pha
	lda $1c37,x : cmp #$b76f ; check if PLM ID is save station
	beq .save_ok
	pla
	jmp search_loop_cont
.save_ok:
	pla
	jmp search_loop_found

;;; end of unused space
warnpc $8485b2
