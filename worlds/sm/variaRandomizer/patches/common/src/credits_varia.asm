// compile with xkas-plus

// custom credits
arch snes.cpu
lorom

// Defines for the script and credits data
define speed $f770
define set $9a17
define delay $9a0d
define draw $0000
define end $f6fe, $99fe
define blank $1fc0
define row $0040
define pink "table tables/pink.tbl"
define yellow "table tables/yellow.tbl"
define cyan "table tables/cyan.tbl"
define blue "table tables/blue.tbl"
define green "table tables/green.tbl"
define orange "table tables/orange.tbl"
define purple "table tables/purple.tbl"
define big "table tables/big.tbl"
// store last save slot and used saves in unused SRAM
define last_saveslot       $701dfa
define used_slots_mask     $701df8
define was_started_flag32  $701dfc
// backup RAM for timer to avoid it to get cleared at boot
define timer_backup1 $7fffe2
define timer_backup2 {timer_backup1}+2
define softreset $7fffe6
define scroll_speed $7fffe8
// RTA timer RAM updated during NMI
define timer1 $05b8
define timer2 $05ba

define stats_sram_sz_b  #$0080
define full_stats_area_sz_b  #$0300
define stats_sram_sz_w  #$0040
define tmp_area_sz      #$00df

define _stats_ram        fc00
define stats_ram         $7f{_stats_ram}
define stats_timer       {stats_ram}

define stats_sram_slot0     $1400
define stats_sram_slot1     $1700
define stats_sram_slot2     $1a00

define backup_save_data_off    #$02f8
define backup_sram_slot0       $16f8
define backup_sram_slot1       $19f8
define backup_sram_slot2       $1cf8
define last_stats_save_ok_off  #$02fc
define magic_flag 	       #$caca

define current_save_slot	$7e0952
define area_index		$079f
define load_station_index	$078b

// some scratch space in RAM for backup save system
define backup_counter	$7fff38
define backup_candidate $7fff3a

define stat_resets	#$0029

// External Routines
// routine in new_game.asm
define check_new_game   $A1F210
// routine in tracking.asm
define update_and_store_region_time $A1EC00

// Patch boot to init our stuff
org $80844B
    jml boot1
org $808490
    jml boot2

// bypass SRAM check to avoid loading 1st save at boot
org $808268
    jmp $8294

// Patch load/save/copy
org $81800d
	jsr patch_save_start
org $81807f
    jmp patch_save_end

org $81A24A
    jsl patch_load // patch load from menu only

// patch copy routine to copy SRAM stats
org $819A66
    jsr copy_stats

// patch clear routine to update used save slots bitmask in SRAM
org $819cc3
	jsr patch_clear

// hijack menu display for backup saves
org $819f13
	jsr load_menu_1st_file
org $819f46
	jsr load_menu_2nd_file
org $819f7c
	jsr load_menu_3rd_file

// Hijack loading new game to reset stats
org $82805f
    jsl clear_values

// Hijack the original credits code to read the script from bank $DF
org $8b9976
    jml scroll

org $8b999b
    jml patch1

org $8b99e5
    jml patch2

org $8b9a08
    jml patch3

org $8b9a19
    jml patch4

// Hijack when samus is in the ship and ready to leave the planet
org $a2ab13
    jsl game_end

// Patch NMI to skip resetting 05ba and instead use that as an extra time counter
org $8095e5
nmi:
    ldx #$00
    stx $05b4
    ldx $05b5
    inx
    stx $05b5
    inc $05b6
.inc:
    rep #$30
    inc $05b8
    bne +
    inc $05ba
+
    bra .end

org $809602
    bra .inc
.end:
    ply
    plx
    pla
    pld
    plb
    rti

// Patch boot to init stuff
org $80fe00
boot1:
    lda #$0000
    sta {timer_backup1}
    sta {timer_backup2}
    // check if first boot ever by checking magic 32-bit value in SRAM
    lda {was_started_flag32}
    cmp {magic_flag}
    bne .first
    lda {was_started_flag32}+2
    cmp {magic_flag}
    beq .check_reset
.first:
    // no game was ever saved:
    // init used save slots bitmask
    lda #$0000
    sta {used_slots_mask}
    // write magic number
    lda {magic_flag}
    sta {was_started_flag32}
    sta {was_started_flag32}+2
    // skip soft reset check, since it's the 1st boot
    bra .cont
.check_reset:
    // check if soft reset, if so, restore RAM timer
    lda {softreset}
    cmp #$babe
    bne .cont
    lda {timer1}
    sta {timer_backup1}
    lda {timer2}
    sta {timer_backup2}
.cont:
    // vanilla init stuff (will overwrite our timer, hence the backup)
    ldx #$1ffe
    lda #$0000
-
    stz $0000, x
    dex
    dex
    bpl -
    // restore timer
    lda {timer_backup1}
    sta {timer1}
    lda {timer_backup2}
    sta {timer2}
    // resume
    jml $808455

boot2:
    // backup the timer again, game likes to clear this area on boot
    lda {timer1}
    sta {timer_backup1}
    lda {timer2}
    sta {timer_backup2}
    // vanilla init stuff
    ldx #$1ffe
-
    stz $0000,x
    stz $2000,x
    stz $4000,x
    stz $6000,x
    stz $8000,x
    stz $a000,x
    stz $c000,x
    stz $e000,x
    dex
    dex
    bpl -
    // restore timer
    lda {timer_backup1}
    sta {timer1}
    lda {timer_backup2}
    sta {timer2}
    // clear temp variables
    ldx {tmp_area_sz}
    lda #$0000
-
    sta $7fff00, x
    dex
    dex
    bpl -

    jml $8084af

//// save related routines
// zero flag set if value in last_saveslot is valid
is_save_slot:
    // check for the 3 possible valid values
    lda {last_saveslot}
    cmp #$0010
    beq .end
    cmp #$0011
    beq .end
    cmp #$0012
    beq .end
.end:
    rtl

// assuming a valid save slot is in last_saveslot,
// stores in X the bank $70 index to stats area
// arg A: if 0 we want last stats, otherwise standard stats
save_index:
    pha
    lda {last_saveslot}
    cmp #$0010
    beq .slot0
    cmp #$0011
    beq .slot1
.slot2:
    ldx #{stats_sram_slot2}
    bra .last
.slot0:
    ldx #{stats_sram_slot0}
    bra .last
.slot1:
    ldx #{stats_sram_slot1}
.last:
    pla
    bne .end
    txa
    clc
    adc {stats_sram_sz_b}
    tax
.end:
    rtl

warnpc $80ffbf


	// Rolling backup save mechanism:
	//
	// Additional data in saves :
	//	- initial save slot ID
	//	- a player usage flag, set when a game is loaded by the user
	//	- a backup counter, incremented everytime a backup is made
	// - when loading a game (i.e. the player actually uses a file),
	//   mark the file as used with the player usage flag.
	//	- if loading an existing file without the player flag (a backup),
	//	  copy over stats from current player save (non-backup with the
	//	  closest save counter? or highest?), or directly from RAM
	//	  if possible
	// - when saving a game, and it's not the first file creating save, and save
	//   station used is different from the last one :
	//	- scan through save files to determine the best candidate to use as
	//	  backup
	//	- priority: empty save, old backup, recent backup
	//	- ignore save files with player flag set (was loaded once)
	//	- ignore backup files from different slots

// Patch load and save routines
// a save will always be performed when starting a new game (see new_game.asm)
org $81ef20
// make optional to auto backup save, set this flag to non-zero in ROM to enable the feature
opt_backup:
	dw $0000
// put that here to have it at a fixed location (will be called from new_game)
print "new_save: ", org
new_save:
	// call save routine
	lda {current_save_slot}
	jsl $818000
	// if backup saves are disabled, return
	lda.l opt_backup
	beq .end
	// set current save slot as used in SRAM bitmask
	lda {current_save_slot}
	asl
	tax
	lda {used_slots_mask}
	ora $819af4,x	// bitmask index table in ROM
	sta {used_slots_mask}

	// init backup save data :

	// first, get offset in SRAM, using save_index routine,
	// which is based on last_saveslot value, which is correct,
	// since we juste saved stats (through patch_save_end)
	jsl save_index		// A is non-0, so get standard stats addr
	// x += backup_save_data_off
	txa
	clc
	adc {backup_save_data_off}
	tax
	// store current save slot in the save itself (useful if we reload
	// a backup save, to copy over stats from original save)
	lda {current_save_slot}
	sta $700000,x
	// store 0 + high bit set (player flag) as backup counter
	lda #$8000
	sta $700002,x
.end:
	rtl

// save slot data:
// slot ID, slot bitmask, SRAM addr for backup data, SRAM addr for load station info
// (SRAM addresses are offsets in bank $70)
slots_data:
slot0_data:
	dw $0000,$0001,{backup_sram_slot0},$0166

slot1_data:
	dw $0001,$0002,{backup_sram_slot1},$07c2

slot2_data:
	dw $0002,$0004,{backup_sram_slot2},$0e1e

// backup is needed if no existing backup of current save slot
// or last backup is at a different save station than this one
//	
// return carry set if we need to backup the save, and we can use a
// slot to do so.
// sets the most suitable save slot in backup_candidate,
// or 3 if no suitable slot found (in that case, carry is clear anyway)
is_backup_needed:
	// save DB and set it to current bank in order to
	// read slots data tables
	phb
	phk
	plb
	// save X and Y as they will be used
	phx
	phy
	// first, check if current save station is different from last save
	lda {current_save_slot}
	asl
	asl
	asl
	tay
	ldx slots_data+6,y
	lda $700000,x
	cmp {load_station_index}
	bne .check_needed
	lda $700002,x
	cmp {area_index}
	beq .no_backup
.check_needed:
	// find out our backup counter, and save it in backup_counter
	ldx slots_data+4,y
	lda $700002,x
	and #$7fff
	sta {backup_counter}
	// backup_candidate will be used to store the backup slot candidate
	// and various info as follows:
	//
	// eo------------ss
	//
	// ss: save slot usable for backup
	// e: ss is empty
	// o: ss contains an old backup
	// (e and o are only use internally by check_slot to determine ss)
	lda #$0003	// 3 is used as invalid value marker, as slots are 0 to 2
	sta {backup_candidate}
	// check all slots
	ldy #slot0_data
	jsr check_slot
	ldy #slot1_data
	jsr check_slot
	ldy #slot2_data
	jsr check_slot
	// clear all our work flags from backup_candidate
	lda {backup_candidate}
	and #$0003
	// check that we can actually backup somewhere
	cmp #$0003
	beq .no_backup
	sta {backup_candidate}
	sec
	bra .end
.no_backup:
	clc
.end:
	ply
	plx
	plb
	rts

// arg. Y: offset to slot data in bank 81 (DB is assumed 81)
// sets flags and candidate in backup_candidate
check_slot:
        // check empty save bitmask
	lda $0002,y
	and {used_slots_mask}
	// if save empty, mark as backup candidate, with high bit (e)
	// set to indicate it's an empty file
	bne .not_empty
	lda {backup_candidate}
	and #$fffc
	ora $0000,y
	ora #$8000
	sta {backup_candidate}
	bra .end
.not_empty:
	// if not our save slot, skip
	ldx $0004,y
	lda $700000,x
	cmp {current_save_slot}
	bne .end
	// if not a backup save, skip
	lda $700002,x
	bmi .end
	// if backup counter is different:
	cmp {backup_counter}
	beq .last_backup
	// mark as backup candidate, with 'old backup' (o) bit marked
	// only if no (e) flag bit marked yet
	lda {backup_candidate}
	bmi .end
	and #$fffc
	ora $0000,y
	ora #$4000
	sta {backup_candidate}
	bra .end
.last_backup:
	// we're here only if this save slot is the most recent backup
	lda {backup_candidate}
	bit #$c000 // checks both e and o flags
	bne .end
	// no better candidate yet
	and #$fffc
	ora $0000,y
	sta {backup_candidate}
.end:
	rts

backup_save:
	// increment backup counter in our save file
	lda {current_save_slot}
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700002,x
	inc
	sta $700002,x

	// direct page indirect addressing copy :
	// reuse $47/$4A used in decompression routine (according to RAM map)
	// we have to use direct page for addresses, and I'm not sure we can use
	// the start of direct page in game as it is done in original menu
	// routine ($00/$03)

	// set bank $70 as source and dest banks for copy
	lda #$0070
	sta $49
	sta $4c	
	// source slot is current one
	lda {current_save_slot}
	asl
	tax
	lda $81812b,x // get SRAM offset in bank 70 for slot
	sta $47
	// destination slot is in backup_candidate
	lda {backup_candidate}
	asl
	tax
	lda $81812b,x // get SRAM offset in bank 70 for slot
	sta $4a
	// copy save file
	ldy #$0000
-
	lda [$47],y
	sta [$4a],y
	iny
	iny
	cpy #$065c
	bmi -
	// copy checksum
	lda {current_save_slot}
	asl
	tax
	lda $701ff0,x
	pha
	lda $701ff8,x
	pha
	lda $700000,x
	pha
	lda $700008,x
	pha
	lda {backup_candidate}
	asl
	tax
	pla
	sta $700008,x
	pla
	sta $700000,x
	pla
	sta $701ff8,x
	pla
	sta $701ff0,x
	// copy stats (includes backup data)
	lda {current_save_slot}
	asl
	tax
	lda save_slots,x
	sta $47
	lda {backup_candidate}
	asl
	tax
	lda save_slots,x
	sta $4a
	ldy #$0000
-
	lda [$47],y
	sta [$4a],y
	iny
	iny
	cpy {full_stats_area_sz_b}
	bcc -
	// clear player flag in backup data area
	lda $4a		// still has destination slot SRAM offset
	clc
	adc {backup_save_data_off}
	tax
	lda $700002,x
	and #$7fff
	sta $700002,x
	// mark backup slot as used in bitmask
	lda {backup_candidate}
	asl
	tax
	lda {used_slots_mask}
	ora $819af4,x	// bitmask index table in ROM
	sta {used_slots_mask}
	rts

patch_save_start:
	pha	// save A, it is used as arg in hijacked function
	lda.l opt_backup
	beq .end
	jsl {check_new_game}
	beq .end
	// we have backup saves enabled, and it is not the 1st save:
	// check if we shall backup the save
	jsr is_backup_needed
	bcc .end
	jsr backup_save
.end:
	pla
	and #0003	// hijacked code
	rts

patch_save_end:
    lda {timer1}
    sta {stats_timer}
    lda {timer2}
    sta {stats_timer}+2
    lda #$0001
    jsl save_stats
.end:
    ply
    plx
    clc
    plb
    plp
    rtl

print "patch_load: ", org
patch_load:
    phb
    phx
    phy
    pea $7e7e
    plb
    plb
    // call load routine
    jsl $818085
    bcc .backup_check
    // skip to end if new file or SRAM corrupt
    jmp .end
.backup_check:
	lda.l opt_backup
	beq .check
	// if backup saves are enabled:
	// check if we load a backup save, and if so, get stats
	// from original save slot, and mark this slot as non-backup
	lda {current_save_slot}
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700002,x
	bmi .check
.load_backup:
	phx
	// n flag not set, we're loading a backup
	// check if we're soft resetting: if so, will take stats from RAM
	lda {softreset}
	cmp #$babe
	beq .load_backup_end
	// load stats from original save SRAM
	lda $700000,x	// save slot in SRAM
	clc
	adc #$0010
	sta {last_saveslot}
	lda #$0000
	jsl save_index
	jsl load_stats_at
	// update live timer
	lda {stats_timer}
	sta {timer1}
	lda {stats_timer}+2
	sta {timer2}
.load_backup_end:
	// update current save slot in SRAM, and set player flag
	plx
	lda {current_save_slot}
	sta $700000,x
	clc
	adc #$0010
	sta {last_saveslot}
	lda $700002,x
	ora #$8000
	sta $700002,x
	bra .end_ok
.check:
    // check save slot
    lda {current_save_slot}
    clc
    adc #$0010
    cmp {last_saveslot}
    bne .load
    // we're loading the same save that's played last
    lda {softreset}
    cmp #$babe
    beq .end_ok     // soft reset, use stats and timer from RAM
    // TODO add menu time to pause stat and make it a general menus stat?
.load:
    // load stats from SRAM
    jsl load_stats
    // update live timer
    lda {stats_timer}
    sta {timer1}
    lda {stats_timer}+2
    sta {timer2}
.end_ok:
    // place marker for resets
    lda #$babe
    sta {softreset}
    // increment reset count
    lda {stat_resets}
    jsl inc_stat
    jsl save_last_stats
    // return carry clear
    clc
.end:
    ply
    plx
    plb
    rtl

files_tilemaps:
	dw $b436,$b456,$b476

// arg A=file
load_menu_file:
	phx
	pha
	lda.l opt_backup
	beq .nochange
.check_slot:
	pla
	pha
	asl
	tax
	lda $819af4,x	// bitmask index table in ROM
	and {used_slots_mask}
	beq .nochange
.load_slot:
	// load save slot value in SRAM
	pla
	pha
	asl
	asl
	asl
	tax
	lda.l slots_data+4,x
	tax
	lda $700000,x
	bra .load_tilemap
.nochange:
	pla
	pha
.load_tilemap:
	asl
	tax
	lda.l files_tilemaps,x
	tay
.end:
	pla
	plx
	rts

load_menu_1st_file:
	lda #$0000
	jmp load_menu_file

load_menu_2nd_file:
	lda #$0001
	jmp load_menu_file

load_menu_3rd_file:
	lda #$0002
	jmp load_menu_file

save_slots:
    dw {stats_sram_slot0}
    dw {stats_sram_slot1}
    dw {stats_sram_slot2}

print "copy_stats:", org
copy_stats:
    // src slot idx = 19b7, dst slot idx = 19b9
    lda $19b7
    asl
    tax
    lda save_slots,x
    sta $00
    lda $19b9
    asl
    tax
    lda save_slots,x
    sta $03
    ldy #$0000
    // bank part for indirect long in already setup by original
    // routine at $02 and $05
.loop:
    lda [$00],y
    sta [$03],y
    iny
    iny
    cpy {full_stats_area_sz_b}
    bcc .loop
    // disable save slot check. if data is copied we cannot rely on RAM contents
    lda #$0000
    sta {last_saveslot}
    lda $19B7   // hijacked code
    rts

// clear slot in used_slots_mask in SRAM
patch_clear:
	// $19b7 hold slot being cleared
	lda $19b7
	asl
	tax
	lda $819af4,x	// bitmask index table in ROM
	eor #$ffff
	and {used_slots_mask}
	sta {used_slots_mask}
.end:
	lda $19b7	// hijacked code
	rts

//print "b81 end: ", org
warnpc $81f29f
////////////////////////// CREDITS /////////////////////////////

// Hijack after decompression of regular credits tilemaps
org $8be0d1
    jsl copy

// Load credits script data from bank $df instead of $8c
org $8bf770
// set scroll speed routine ({speed} instruction in credits script)
set_scroll:
    rep #$30
    phb; pea $df00; plb; plb
    lda $0000, y
    sta {scroll_speed}
    iny
    iny
    plb
    rts

scroll:
    inc $1995
    lda $1995
    cmp {scroll_speed}
    beq +
    lda $1997
    jml $8b9989
+
    stz $1995
    inc $1997
    lda $1997
    jml $8b9989


patch1:
    phb; pea $df00; plb; plb
    lda $0000, y
    bpl +
    plb
    jml $8b99a0
+
    plb
    jml $8b99aa

patch2:
    sta $0014
    phb; pea $df00; plb; plb
    lda $0002, y
    plb
    jml $8b99eb

patch3:
    phb; pea $df00; plb; plb
    lda $0000, y
    tay
    plb
    jml $8b9a0c

patch4:
    phb; pea $df00; plb; plb
    lda $0000, y
    plb
    sta $19fb
    jml $8b9a1f

// Copy custom credits tilemap data from $ceb240,x to $7f2000,x
copy:
    pha
    phx
    ldx #$0000
-
    lda.l credits, x
    cmp #$0000
    beq +
    sta $7f2000, x
    inx
    inx
    jmp -
+

    ldx #$0000
-
    lda.l itemlocations, x
    cmp #$0000
    beq +
    sta $7fa000, x
    inx
    inx
    jmp -
+

    jsl write_stats
    lda #$0002
    sta {scroll_speed}
    plx
    pla
    jsl $8b95ce
    rtl

clear_values:
    php
    rep #$30
    jsl {check_new_game}
    bne .ret

    ldx #$0000
    lda #$0000
-
    jsl store_stat
    inx
    cpx {stats_sram_sz_w}
    bne -

    // Clear RTA Timer
    lda #$0000
    sta {timer1}
    sta {timer2}
    // place marker for resets
    lda #$babe
    sta {softreset}
.ret:
    plp
    jsl $80a07b	// hijacked code
    rtl

// Game has ended, save RTA timer to RAM and copy all stats to SRAM a final time
game_end:
    // update region time (will be slightly off, but avoids dealing with negative substraction result, see below)
    jsl {update_and_store_region_time}
    // Subtract frames from pressing down at ship to this code running
    lda {timer1}
    sec
    sbc #$013d
    sta {timer1}
    lda #$0000  // if carry clear this will subtract one from the high byte of timer
    sbc {timer2}

    // save timer in stats
    lda {timer1}
    sta {stats_timer}
    lda {timer2}
    sta {stats_timer}+2

    // save stats to SRAM
    lda #$0001
    jsl save_stats

    // hijacked code
    lda #$000a
    jsl $90f084
    rtl

org $dfd4f0
// Draw full time as hh:mm:ss:ff
// Pointer to first byte of RAM in A
draw_full_time:
    phx
    phb
    pea $7f7f; plb; plb
    tax
    lda $0000, x
    sta $16
    lda $0002, x
    sta $14
    lda #$003c
    sta $12
    lda #$ffff
    sta $1a
    jsr div32 // frames in $14, rest in $16
    iny; iny; iny; iny; iny; iny // Increment Y three positions forward to write the last value
    lda $14
    jsr draw_two
    tya
    sec
    sbc #$0010
    tay     // Skip back 8 characters to draw the top three things
    lda $16
    jsr draw_time
    plb
    plx
    rts

// Draw time as xx:yy:zz
draw_time:
    phx
    phb
    dey; dey; dey; dey; dey; dey // Decrement Y by 3 characters so the time count fits
    pea $7f7f; plb; plb
    sta $004204
    sep #$20
    lda #$ff
    sta $1a
    lda #$3c
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216 // Seconds or Frames
    sta $12
    lda $004214 // First two groups (hours/minutes or minutes/seconds)
    sta $004204
    sep #$20
    lda #$3c
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216
    sta $14
    lda $004214 // First group (hours or minutes)
    jsr draw_two
    iny; iny // Skip past separator
    lda $14 // Second group (minutes or seconds)
    jsr draw_two
    iny; iny
    lda $12 // Last group (seconds or frames)
    jsr draw_two
    plb
    plx
    rts

// Draw 5-digit value to credits tilemap
// A = number to draw, Y = row address
draw_value:
    phx
    phb
    pea $7f7f; plb; plb
    sta $004204
    lda #$0000
    sta $1a     // Leading zeroes flag
    sep #$20
    lda #$64
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004216 // Last two digits
    sta $12
    lda $004214 // Top three digits
    jsr draw_three
    lda $12
    jsr draw_two
.end:
    plb
    plx
    rts

draw_three:
    sta $004204
    sep #$20
    lda #$64
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004214 // Hundreds
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0034, y
    lda numbers_bot, x
    sta $0074, y
    dec $1a
+
    iny; iny // Next number
    lda $004216

draw_two:
    sta $004204
    sep #$20
    lda #$0a
    sta $004206
    pha; pla; pha; pla; rep #$20
    lda $004214
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0034, y
    lda numbers_bot, x
    sta $0074, y
    dec $1a
+
    lda $004216
    asl
    tax
    cmp $1a
    beq +
    lda numbers_top, x
    sta $0036, y
    lda numbers_bot, x
    sta $0076, y
    dec $1a
+
    iny; iny; iny; iny
    rts

// Loop through stat table and update RAM with numbers representing those stats
write_stats:
    phy
    phb
    php
    pea $dfdf; plb; plb
    rep #$30
    jsl load_stats      // Copy stats back from SRAM
    ldx #$0000
    ldy #$0000

.loop:
    // Get pointer to table
    tya
    asl; asl; asl;
    tax

    // Load stat type
    lda stats+4, x
    beq .end
    cmp #$0001
    beq .number
    cmp #$0002
    beq .time
    cmp #$0003
    beq .fulltime
    jmp .continue

.number:
    // Load statistic
    lda stats, x
    jsl load_stat
    pha

    // Load row address
    lda stats+2, x
    tyx
    tay
    pla
    jsr draw_value
    txy
    jmp .continue

.time:
    // Load statistic
    lda stats, x
    jsl load_stat
    pha

    // Load row address
    lda stats+2, x
    tyx
    tay
    pla
    jsr draw_time
    txy
    jmp .continue

.fulltime:
    lda stats, x        // Get stat id
    asl
    clc
    adc #${_stats_ram}          // Get pointer to value instead of actual value
    pha

    // Load row address
    lda stats+2, x
    tyx
    tay
    pla
    jsr draw_full_time
    txy
    jmp .continue

.continue:
    iny
    jmp .loop

.end:
    plp
    plb
    ply
    rtl

// 32-bit by 16-bit division routine I found somewhere
div32:
    phy
    phx
    php
    rep #$30
    sep #$10
    sec
    lda $14
    sbc $12
    bcs uoflo
    ldx #$11
    rep #$10

ushftl:
    rol $16
    dex
    beq umend
    rol $14
    lda #$0000
    rol
    sta $18
    sec
    lda $14
    sbc $12
    tay
    lda $18
    sbc #$0000
    bcc ushftl
    sty $14
    bra ushftl
uoflo:
    lda #$ffff
    sta $16
    sta $14
umend:
    plp
    plx
    ply
    rts

numbers_top:
    dw $0060, $0061, $0062, $0063, $0064, $0065, $0066, $0067, $0068, $0069, $006a, $006b, $006c, $006d, $006e, $006f
numbers_bot:
    dw $0070, $0071, $0072, $0073, $0074, $0075, $0076, $0077, $0078, $0079, $007a, $007b, $007c, $007d, $007e, $007f

print "load_stats: ", org
load_stats:
    phx
    phy
    lda {current_save_slot}
    clc
    adc #$0010
    sta {last_saveslot}
    // tries to load from last stats
    jsr is_last_save_flag_ok
    bcc .notok
    lda #$0000
    jsl save_index
.notok:
    jsl load_stats_at
    ply
    plx
    rtl

// arg X = index of where to load stats from in bank $70
load_stats_at:
    phx
    phb
    pea $7f7f
    plb
    plb
    ldy #$0000
.loop:
    lda $700000,x
    sta ${_stats_ram},y
    iny
    iny
    inx
    inx
    cpy {stats_sram_sz_b}
    bcc .loop
    plb
    plx
    rtl

// return carry flag set if flag ok
is_last_save_flag_ok:
    phx
    pha
    lda #$0001
    jsl save_index
    txa
    clc
    adc {last_stats_save_ok_off}
    tax
    lda {magic_flag}
    cmp $700000,x
    beq .flag_ok
    clc
    bra .end
.flag_ok:
    sec
.end:
    pla
    plx
    rts

// args: A = value to store
// X and A untouched
set_last_save_ok_flag:
    phx
    pha
    lda #$0001
    jsl save_index
    txa
    clc
    adc {last_stats_save_ok_off}
    tax
    pla
    sta $700000,x
    plx
    rts

// arg X = index of where to save stats in bank $70
save_stats_at:
    phx
    phb
    pea $7f7f
    plb
    plb
    ldy #$0000
.loop:
    lda ${_stats_ram},y
    sta $700000,x
    iny
    iny
    inx
    inx
    cpy {stats_sram_sz_b}
    bcc .loop
    plb
    plx
    rts

// save stats both in standard and last areas
// arg: A = 0 if we just want to save last stats
//      A != 0 save all stats (save stations)
print "save_stats: ", org
save_stats:
    phx
    phy
    pha
    lda {current_save_slot}
    clc
    adc #$0010
    sta {last_saveslot}
    pla
    beq .last   // skip standard save if A=0
    jsl save_index // A is not 0, so we ask for standard stats index
    jsr save_stats_at
    lda #$0000
.last:
    jsl save_index // A is 0, so we ask for last stats index
    lda #$0000
    jsr set_last_save_ok_flag
    jsr save_stats_at
    lda {magic_flag}
    jsr set_last_save_ok_flag
    ply
    plx
    rtl

warnpc $dfd80f
// Increment Statistic (in A)
org $dfd810
inc_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    inc
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd81f

org $dfd820
// save last stats. to be used from door transitions/menus
// keeps all registers intact
save_last_stats:
    pha
    lda {timer1}
    sta {stats_timer}
    lda {timer2}
    sta {stats_timer}+2
    lda #$0000
    jsl save_stats
    pla
    rtl

warnpc $dfd83f
// Decrement Statistic (in A)
org $dfd840
dec_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    dec
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd87f
// Store Statistic (value in A, stat in X)
org $dfd880
store_stat:
    phx
    pha
    txa
    asl
    tax
    pla
    sta {stats_ram}, x
    plx
    rtl

warnpc $dfd8af
// Load Statistic (stat in A, returns value in A)
org $dfd8b0
load_stat:
    phx
    asl
    tax
    lda {stats_ram}, x
    plx
    rtl

warnpc $dfd91a
// New credits script in free space of bank $DF
org $dfd91b
script:
    dw {set}, $0002
-
    dw {draw}, {blank}
    dw {delay}, -

    // Show a compact and sped up version of the original credits so we get time to add more
    // change scroll speed to 1 pixel per frame

    // NOTE: when adding new stuff to the credits, remove blanks from
    //	     "Last info" section, as this credits script is in sync with credits music

    dw {speed}, $0001

    dw {draw}, {row}*0      // SUPER METROID STAFF
    dw {draw}, {blank}
    dw {draw}, {row}*4      // PRODUCER
    dw {draw}, {blank}
    dw {draw}, {row}*7      // MAKOTO KANOH
    dw {draw}, {row}*8
    dw {draw}, {blank}
    dw {draw}, {row}*9      // DIRECTOR
    dw {draw}, {blank}
    dw {draw}, {row}*10     // YOSHI SAKAMOTO
    dw {draw}, {row}*11
    dw {draw}, {blank}
    dw {draw}, {row}*12     // BACK GROUND DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*13     // HIROFUMI MATSUOKA
    dw {draw}, {row}*14
    dw {draw}, {blank}
    dw {draw}, {row}*15     // MASAHIKO MASHIMO
    dw {draw}, {row}*16
    dw {draw}, {blank}
    dw {draw}, {row}*17     // HIROYUKI KIMURA
    dw {draw}, {row}*18
    dw {draw}, {blank}
    dw {draw}, {row}*19     // OBJECT DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*20     // TOHRU OHSAWA
    dw {draw}, {row}*21
    dw {draw}, {blank}
    dw {draw}, {row}*22     // TOMOYOSHI YAMANE
    dw {draw}, {row}*23
    dw {draw}, {blank}
    dw {draw}, {row}*24     // SAMUS ORIGINAL DESIGNERS
    dw {draw}, {blank}
    dw {draw}, {row}*25     // HIROJI KIYOTAKE
    dw {draw}, {row}*26
    dw {draw}, {blank}
    dw {draw}, {row}*27     // SAMUS DESIGNER
    dw {draw}, {blank}
    dw {draw}, {row}*28     // TOMOMI YAMANE
    dw {draw}, {row}*29
    dw {draw}, {blank}
    dw {draw}, {row}*83     // SOUND PROGRAM
    dw {draw}, {row}*107    // AND SOUND EFFECTS
    dw {draw}, {blank}
    dw {draw}, {row}*84     // KENJI YAMAMOTO
    dw {draw}, {row}*85
    dw {draw}, {blank}
    dw {draw}, {row}*86     // MUSIC COMPOSERS
    dw {draw}, {blank}
    dw {draw}, {row}*84     // KENJI YAMAMOTO
    dw {draw}, {row}*85
    dw {draw}, {blank}
    dw {draw}, {row}*87     // MINAKO HAMANO
    dw {draw}, {row}*88
    dw {draw}, {blank}
    dw {draw}, {row}*30     // PROGRAM DIRECTOR
    dw {draw}, {blank}
    dw {draw}, {row}*31     // KENJI IMAI
    dw {draw}, {row}*64
    dw {draw}, {blank}
    dw {draw}, {row}*65     // SYSTEM COORDINATOR
    dw {draw}, {blank}
    dw {draw}, {row}*66     // KENJI NAKAJIMA
    dw {draw}, {row}*67
    dw {draw}, {blank}
    dw {draw}, {row}*68     // SYSTEM PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*69     // YOSHIKAZU MORI
    dw {draw}, {row}*70
    dw {draw}, {blank}
    dw {draw}, {row}*71     // SAMUS PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*72     // ISAMU KUBOTA
    dw {draw}, {row}*73
    dw {draw}, {blank}
    dw {draw}, {row}*74     // EVENT PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*75     // MUTSURU MATSUMOTO
    dw {draw}, {row}*76
    dw {draw}, {blank}
    dw {draw}, {row}*77     // ENEMY PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*78     // YASUHIKO FUJI
    dw {draw}, {row}*79
    dw {draw}, {blank}
    dw {draw}, {row}*80     // MAP PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*81     // MOTOMU CHIKARAISHI
    dw {draw}, {row}*82
    dw {draw}, {blank}
    dw {draw}, {row}*101    // ASSISTANT PROGRAMMER
    dw {draw}, {blank}
    dw {draw}, {row}*102    // KOUICHI ABE
    dw {draw}, {row}*103
    dw {draw}, {blank}
    dw {draw}, {row}*104    // COORDINATORS
    dw {draw}, {blank}
    dw {draw}, {row}*105    // KATSUYA YAMANO
    dw {draw}, {row}*106
    dw {draw}, {blank}
    dw {draw}, {row}*63     // TSUTOMU KANESHIGE
    dw {draw}, {row}*96
    dw {draw}, {blank}
    dw {draw}, {row}*89    // PRINTED ART WORK
    dw {draw}, {blank}
    dw {draw}, {row}*90    // MASAFUMI SAKASHITA
    dw {draw}, {row}*91
    dw {draw}, {blank}
    dw {draw}, {row}*92    // YASUO INOUE
    dw {draw}, {row}*93
    dw {draw}, {blank}
    dw {draw}, {row}*94    // MARY COCOMA
    dw {draw}, {row}*95
    dw {draw}, {blank}
    dw {draw}, {row}*99    // YUSUKE NAKANO
    dw {draw}, {row}*100
    dw {draw}, {blank}
    dw {draw}, {row}*108   // SHINYA SANO
    dw {draw}, {row}*109
    dw {draw}, {blank}
    dw {draw}, {row}*110   // NORIYUKI SATO
    dw {draw}, {row}*111
    dw {draw}, {blank}
    dw {draw}, {row}*32    // SPECIAL THANKS TO
    dw {draw}, {blank}
    dw {draw}, {row}*33    // DAN OWSEN
    dw {draw}, {row}*34
    dw {draw}, {blank}
    dw {draw}, {row}*35    // GEORGE SINFIELD
    dw {draw}, {row}*36
    dw {draw}, {blank}
    dw {draw}, {row}*39    // MASARU OKADA
    dw {draw}, {row}*40
    dw {draw}, {blank}
    dw {draw}, {row}*43    // TAKAHIRO HARADA
    dw {draw}, {row}*44
    dw {draw}, {blank}
    dw {draw}, {row}*47    // KOHTA FUKUI
    dw {draw}, {row}*48
    dw {draw}, {blank}
    dw {draw}, {row}*49    // KEISUKE TERASAKI
    dw {draw}, {row}*50
    dw {draw}, {blank}
    dw {draw}, {row}*51    // MASARU YAMANAKA
    dw {draw}, {row}*52
    dw {draw}, {blank}
    dw {draw}, {row}*53    // HITOSHI YAMAGAMI
    dw {draw}, {row}*54
    dw {draw}, {blank}
    dw {draw}, {row}*57    // NOBUHIRO OZAKI
    dw {draw}, {row}*58
    dw {draw}, {blank}
    dw {draw}, {row}*59    // KENICHI NAKAMURA
    dw {draw}, {row}*60
    dw {draw}, {blank}
    dw {draw}, {row}*61    // TAKEHIKO HOSOKAWA
    dw {draw}, {row}*62
    dw {draw}, {blank}
    dw {draw}, {row}*97    // SATOSHI MATSUMURA
    dw {draw}, {row}*98
    dw {draw}, {blank}
    dw {draw}, {row}*122   // TAKESHI NAGAREDA
    dw {draw}, {row}*123
    dw {draw}, {blank}
    dw {draw}, {row}*124   // MASAHIRO KAWANO
    dw {draw}, {row}*125
    dw {draw}, {blank}
    dw {draw}, {row}*45    // HIRO YAMADA
    dw {draw}, {row}*46
    dw {draw}, {blank}
    dw {draw}, {row}*112   // AND ALL OF R&D1 STAFFS
    dw {draw}, {row}*113
    dw {draw}, {blank}
    dw {draw}, {row}*114   // GENERAL MANAGER
    dw {draw}, {blank}
    dw {draw}, {row}*5     // GUMPEI YOKOI
    dw {draw}, {row}*6
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    // change scroll speed to 2 pixels per frame
    dw {speed}, $0002
    // Custom item randomizer credits text
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*128 // VARIA RANDOMIZER STAFF
    dw {draw}, {blank}
    dw {draw}, {row}*129
    dw {draw}, {row}*130
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*131 // ORIGINAL ITEM RANDOMIZERS
    dw {draw}, {blank}
    dw {draw}, {row}*132
    dw {draw}, {row}*133
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*134 // CONTRIBUTORS
    dw {draw}, {blank}
    dw {draw}, {row}*135
    dw {draw}, {row}*136
    dw {draw}, {blank}
    dw {draw}, {row}*137
    dw {draw}, {row}*138
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*139 // SPECIAL THANKS TO
    dw {draw}, {blank}
    dw {draw}, {row}*140 // SMILEY SUKU
    dw {draw}, {row}*141
    dw {draw}, {blank}
    dw {draw}, {row}*154 // hackers
    dw {draw}, {row}*176
    dw {draw}, {blank}
    dw {draw}, {row}*177 // donators
    dw {draw}, {row}*178
    dw {draw}, {blank}
    dw {draw}, {row}*142 // METROID CONSTRUCTION
    dw {draw}, {blank}
    dw {draw}, {row}*143
    dw {draw}, {row}*144
    dw {draw}, {blank}
    dw {draw}, {row}*165 // SUPER METROID DISASSEMBLY
    dw {draw}, {blank}
    dw {draw}, {row}*166
    dw {draw}, {row}*167
    dw {draw}, {blank}
    dw {draw}, {row}*184 // SpriteSomething
    dw {draw}, {blank}
    dw {draw}, {row}*224
    dw {draw}, {row}*225
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*145 // RANDOMIZER PARAMETERS
    dw {draw}, {blank}
    dw {draw}, {row}*155 // PROG SPEED
    dw {draw}, {blank}
    dw {draw}, {row}*156 // PROG DIFF
    dw {draw}, {blank}
    dw {draw}, {row}*158 // SUITS RESTRICTION
    dw {draw}, {blank}
    dw {draw}, {row}*159 // MORPH PLACEMENT
    dw {draw}, {blank}

    // change scroll speed to 3 px/frame
    dw {speed}, $0003

    dw {draw}, {row}*160 // SUPER FUN COMBAT
    dw {draw}, {blank}
    dw {draw}, {row}*161 // SUPER FUN MOVEMENT
    dw {draw}, {blank}
    dw {draw}, {row}*162 // SUPER FUN SUITS
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*157 // ITEMS DISTRIBUTION
    dw {draw}, {blank}
    dw {draw}, {row}*146 // LOCATIONS
    dw {draw}, {row}*147
    dw {draw}, {blank}
    dw {draw}, {row}*148 // LOCS DETAIL
    dw {draw}, {row}*149
    dw {draw}, {blank}
    dw {draw}, {row}*168 // AVAILABLE
    dw {draw}, {row}*169
    dw {draw}, {blank}
    dw {draw}, {row}*152 // ENERGY DETAIL
    dw {draw}, {row}*153
    dw {draw}, {blank}
    dw {draw}, {row}*150 // AMMO DETAIL
    dw {draw}, {row}*151
    dw {draw}, {blank}
    dw {draw}, {row}*163 // AMMO DISTRIBUTION
    dw {draw}, {row}*164
    dw {draw}, {blank}

    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*223 // PLAY THIS RANDOMIZER AT
    dw {draw}, {blank}
    dw {draw}, {row}*179
    dw {draw}, {row}*180
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*181
    dw {draw}, {blank}
    dw {draw}, {row}*182
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*183 // GAMEPLAY STATS
    dw {draw}, {blank}
    dw {draw}, {row}*172 // DEATHS
    dw {draw}, {row}*173
    dw {draw}, {blank}
    dw {draw}, {row}*174 // RESETS
    dw {draw}, {row}*175
    dw {draw}, {blank}
    dw {draw}, {row}*185 // DOOR TRANSITIONS
    dw {draw}, {row}*186
    dw {draw}, {blank}
    dw {draw}, {row}*187 // TIME IN DOORS
    dw {draw}, {row}*188
    dw {draw}, {blank}
    dw {draw}, {row}*189 // TIME ADJUSTING DOOR
    dw {draw}, {row}*190
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*191 // TIME SPENT
    dw {draw}, {blank}
    dw {draw}, {row}*192 // CERES
    dw {draw}, {row}*193
    dw {draw}, {blank}
    dw {draw}, {row}*194 // CRATERIA
    dw {draw}, {row}*195
    dw {draw}, {blank}
    dw {draw}, {row}*196 // GREEN BRINSTAR
    dw {draw}, {row}*197
    dw {draw}, {blank}
    dw {draw}, {row}*198 // RED BRINSTAR
    dw {draw}, {row}*199
    dw {draw}, {blank}
    dw {draw}, {row}*200 // WRECKED SHIP
    dw {draw}, {row}*201
    dw {draw}, {blank}
    dw {draw}, {row}*202 // KRAID
    dw {draw}, {row}*203
    dw {draw}, {blank}
    dw {draw}, {row}*226 // UPPER NORFAIR
    dw {draw}, {row}*227
    dw {draw}, {blank}
    dw {draw}, {row}*228 // CROC
    dw {draw}, {row}*229
    dw {draw}, {blank}
    dw {draw}, {row}*230 // LOWER NORFAIR
    dw {draw}, {row}*231
    dw {draw}, {blank}
    dw {draw}, {row}*232 // WEST MARIDIA
    dw {draw}, {row}*233
    dw {draw}, {blank}
    dw {draw}, {row}*234 // EAST MARIDIA
    dw {draw}, {row}*235
    dw {draw}, {blank}
    dw {draw}, {row}*236 // TOURIAN
    dw {draw}, {row}*237
    dw {draw}, {blank}
    dw {draw}, {row}*221 // PAUSE MENU
    dw {draw}, {row}*222
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*204 // SHOTS AND AMMO
    dw {draw}, {blank}
    dw {draw}, {row}*170 // UNCHARGED
    dw {draw}, {row}*171
    dw {draw}, {blank}
    dw {draw}, {row}*205 // CHARGED
    dw {draw}, {row}*206
    dw {draw}, {blank}
    dw {draw}, {row}*207 // SBA
    dw {draw}, {row}*208
    dw {draw}, {blank}
    dw {draw}, {row}*209 // MISSILES
    dw {draw}, {row}*210
    dw {draw}, {blank}
    dw {draw}, {row}*211 // SUPERS
    dw {draw}, {row}*212
    dw {draw}, {blank}
    dw {draw}, {row}*213 // PBs
    dw {draw}, {row}*214
    dw {draw}, {blank}
    dw {draw}, {row}*215 // BOMBS
    dw {draw}, {row}*216


    // Draw item locations
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {row}*640
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*641
    dw {draw}, {row}*642
    dw {draw}, {blank}
    dw {draw}, {row}*643
    dw {draw}, {row}*644
    dw {draw}, {blank}
    dw {draw}, {row}*645
    dw {draw}, {row}*646
    dw {draw}, {blank}
    dw {draw}, {row}*647
    dw {draw}, {row}*648
    dw {draw}, {blank}
    dw {draw}, {row}*649
    dw {draw}, {row}*650
    dw {draw}, {blank}
    dw {draw}, {row}*651
    dw {draw}, {row}*652
    dw {draw}, {blank}
    dw {draw}, {row}*653
    dw {draw}, {row}*654
    dw {draw}, {blank}
    dw {draw}, {row}*655
    dw {draw}, {row}*656
    dw {draw}, {blank}
    dw {draw}, {row}*657
    dw {draw}, {row}*658
    dw {draw}, {blank}
    dw {draw}, {row}*659
    dw {draw}, {row}*660
    dw {draw}, {blank}
    dw {draw}, {row}*661
    dw {draw}, {row}*662
    dw {draw}, {blank}
    dw {draw}, {row}*663
    dw {draw}, {row}*664
    dw {draw}, {blank}
    dw {draw}, {row}*665
    dw {draw}, {row}*666
    dw {draw}, {blank}
    dw {draw}, {row}*667
    dw {draw}, {row}*668
    dw {draw}, {blank}
    dw {draw}, {row}*669
    dw {draw}, {row}*670
    dw {draw}, {blank}
    dw {draw}, {row}*671
    dw {draw}, {row}*672
    dw {draw}, {blank}
    dw {draw}, {row}*673
    dw {draw}, {row}*674
    dw {draw}, {blank}
    dw {draw}, {row}*675
    dw {draw}, {row}*676
    dw {draw}, {blank}
    dw {draw}, {row}*677
    dw {draw}, {row}*678
    dw {draw}, {blank}

    // Last info.
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*217 // Final Time
    dw {draw}, {row}*218

    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}

    dw {draw}, {row}*219 // Thanks
    dw {draw}, {row}*220

    // don't touch those blanks
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}
    dw {draw}, {blank}

    // Set scroll speed to 4 frames per pixel
    dw {speed}, $0004

    // Scroll all text off and end credits
    dw {set}, $0017
-
    dw {draw}, {blank}
    dw {delay}, -
    dw {end}

stats:
    // STAT ID, ADDRESS,    TYPE (1 = Number, 2 = Time, 3 = Full time), UNUSED
    dw 0,       {row}*217,  3, 0    // Full RTA Time
    dw 2,       {row}*185,  1, 0    // Door transitions
    dw 3,       {row}*187,  3, 0    // Time in doors
    dw 5,       {row}*189,  2, 0    // Time adjusting doors
    dw 7,       {row}*192,  3, 0    // Ceres
    dw 9,       {row}*194,  3, 0    // Crateria/Blue brin
    dw 11,      {row}*196,  3, 0    // Green/Pink brin
    dw 13,      {row}*198,  3, 0    // Red Brin
    dw 15,      {row}*200,  3, 0    // WS
    dw 17,      {row}*202,  3, 0    // Kraid
    dw 19,      {row}*226,  3, 0    // Upper Norfair
    dw 21,      {row}*228,  3, 0    // Croc
    dw 23,      {row}*230,  3, 0    // Lower Norfair
    dw 25,      {row}*232,  3, 0    // West Maridia
    dw 27,      {row}*234,  3, 0    // East Maridia
    dw 29,      {row}*236,  3, 0    // Tourian
    dw 31,      {row}*170,  1, 0    // Uncharged Shots
    dw 32,      {row}*205,  1, 0    // Charged Shots
    dw 33,      {row}*207,  1, 0    // Special Beam Attacks
    dw 34,      {row}*209,  1, 0    // Missiles
    dw 35,      {row}*211,  1, 0    // Super Missiles
    dw 36,      {row}*213,  1, 0    // Power Bombs
    dw 37,      {row}*215,  1, 0    // Bombs
    dw 38,      {row}*221,  3, 0    // Time in pause
    dw 40,      {row}*172,  1, 0    // deaths
    dw 41,      {row}*174,  1, 0    // resets
    dw 0,               0,  0, 0    // end of table

print "credits end : ", org

warnpc $dfffff

// Relocated credits tilemap to free space in bank CE
org $ceb240
credits:
    // When using big text, it has to be repeated twice, first in UPPERCASE and then in lowercase since it's split into two parts
    // Numbers are mapped in a special way as described below:
    // 0123456789%& '´
    // }!@#$%&/()>~.

    // This is not in display order
    {pink}
    dw "     VARIA RANDOMIZER STAFF     " // 128
    {big}
    dw "          DUDE AND FLO          " // 129
    dw "          dude and flo          " // 130
    {purple}
    dw "    ORIGINAL ITEM RANDOMIZERS   " // 131
    {big}
    dw "       TOTAL   DESSYREQT        " // 132
    dw "       total   dessyreqt        " // 133
    {purple}
    dw "          CONTRIBUTORS          " // 134
    {big}
    dw "         RAND 0   COUT          " // 135
    dw "         rand }   cout          " // 136
    dw "        DJLO   PRANKARD         " // 137
    dw "        djlo   prankard         " // 138
    {cyan}
    dw "       SPECIAL THANKS TO        " // 139
    {big}
    dw "         SMILEY   SUKU          " // 140
    dw "         smiley   suku          " // 141
    {yellow}
    dw "      METROID CONSTRUCTION      " // 142
    {big}
    dw "     METROIDCONSTRUCTION COM    " // 143
    dw "     metroidconstruction.com    " // 144
    {purple}
    // params title
    dw "     RANDOMIZER PARAMETERS      " // 145
    {big}
    // item distribution data start
    dw " ITEM LOCATIONS              XX " // 146
    dw " item locations............. xx " // 147
    dw "  MAJ XX EN XX AMMO XX BLANK XX " // 148
    dw "  maj xx en xx ammo XX blank XX " // 149
    dw " AMMO PACKS  MI XX SUP XX PB XX " // 150
    dw " ammo packs  mi XX sup XX pb XX " // 151
    dw " HEALTH TANKS         E XX R XX " // 152
    dw " health tanks ......  e.xx.r xx " // 153
    dw "   ALL SUPER METROID HACKERS    " // 154 : credits
    // params data start
    {yellow}
    dw " PROGRESSION SPEED .... XXXXXXX " // 155
    dw " PROGRESSION DIFFICULTY XXXXXXX " // 156
    // item distrib title
    {purple}
    dw "       ITEMS DISTRIBUTION       " // 157
    // params data end
    {yellow}
    dw " SUITS RESTRICTION ........ XXX " // 158
    dw " MORPH PLACEMENT ....... XXXXXX " // 159
    dw " SUPER FUN COMBAT ......... XXX " // 160
    dw " SUPER FUN MOVEMENT ....... XXX " // 161
    dw " SUPER FUN SUITS .......... XXX " // 162
    // item distrib data end
    {big}
    dw " AMMO DISTRIBUTION  X X X X X X " // 163
    dw " ammo distribution  x.x x.x x.x " // 164
    // credits continued
    {yellow}
    dw "   SUPER METROID DISASSEMBLY    " // 165
    {big}
    dw "        PJBOY    KEJARDON       " // 166
    dw "        pjboy    kejardon       " // 167
// stats continued
    dw " AVAILABLE AMMO XXX% ENERGY XXX%" // 168
    dw " available ammo xxx> energy xxx>" // 169
    dw " UNCHARGED SHOTS              0 " // 170
    dw " uncharged shots              } " // 171
    dw " DEATHS                       0 " // 172
    dw " deaths                       } " // 173
    dw " RESETS                       0 " // 174
    dw " resets                       } " // 175
// some more credits
    dw "   all super metroid hackers    " // 176
    dw "     OUR GENEROUS DONATORS      " // 177
    dw "     our generous donators      " // 178
// varia URLs
    {big}
    dw "            VARIA RUN           " // 179
    dw "            varia.run           " // 180
    {orange}
    dw "         BETA.VARIA.RUN         " // 181
    dw "        DISCORD.VARIA.RUN       " // 182
    {purple}
    dw "      GAMEPLAY STATISTICS       " // 183
    {yellow}
    dw "        SPRITESOMETHING         " // 184  : credits
    {big}
    dw " DOOR TRANSITIONS             0 " // 185
    dw " door transitions             } " // 186
    dw " TIME IN DOORS      00'00'00^00 " // 187
    dw " time in doors      }} }} }} }} " // 188
    dw " TIME ALIGNING DOORS   00'00^00 " // 189
    dw " time aligning doors   }} }} }} " // 190
    {blue}
    dw "         TIME SPENT IN          " // 191
    {big}
    dw " CERES              00'00'00^00 " // 192
    dw " ceres              }} }} }} }} " // 193
    dw " CRATERIA           00'00'00^00 " // 194
    dw " crateria           }} }} }} }} " // 195
    dw " GREEN BRINSTAR     00'00'00^00 " // 196
    dw " green brinstar     }} }} }} }} " // 197
    dw " RED BRINSTAR       00'00'00^00 " // 198
    dw " red brinstar       }} }} }} }} " // 199
    dw " WRECKED SHIP       00'00'00^00 " // 200
    dw " wrecked ship       }} }} }} }} " // 201
    dw " KRAID'S LAIR       00'00'00^00 " // 202
    dw " kraid s lair       }} }} }} }} " // 203
    {green}
    dw "      SHOTS AND AMMO FIRED      " // 204
    {big}
    dw " CHARGED SHOTS                0 " // 205
    dw " charged shots                } " // 206
    dw " SPECIAL BEAM ATTACKS         0 " // 207
    dw " special beam attacks         } " // 208
    dw " MISSILES                     0 " // 209
    dw " missiles                     } " // 210
    dw " SUPER MISSILES               0 " // 211
    dw " super missiles               } " // 212
    dw " POWER BOMBS                  0 " // 213
    dw " power bombs                  } " // 214
    dw " BOMBS                        0 " // 215
    dw " bombs                        } " // 216
    dw " FINAL TIME         00'00'00^00 " // 217
    dw " final time         }} }} }} }} " // 218
    dw "       THANKS FOR PLAYING       " // 219
    dw "       thanks for playing       " // 220
    dw " PAUSE MENU         00'00'00^00 " // 221
    dw " pause menu         }} }} }} }} " // 222
    {cyan}
    dw "     PLAY THIS RANDOMIZER AT    " // 223
    {big}
    // how about some more credits
    dw "    ARTHEAU   MIKE TRETHEWEY    " // 224
    dw "    artheau   mike trethewey    " // 225
    // now some more stats
    dw " UPPER NORFAIR      00'00'00^00 " // 226
    dw " upper norfair      }} }} }} }} " // 227
    dw " CROCOMIRE          00'00'00^00 " // 228
    dw " crocomire          }} }} }} }} " // 229
    dw " LOWER NORFAIR      00'00'00^00 " // 230
    dw " lower norfair      }} }} }} }} " // 231
    dw " WEST MARIDIA       00'00'00^00 " // 232
    dw " west maridia       }} }} }} }} " // 233
    dw " EAST MARIDIA       00'00'00^00 " // 234
    dw " east maridia       }} }} }} }} " // 235
    dw " TOURIAN            00'00'00^00 " // 236
    dw " tourian            }} }} }} }} " // 237

    dw $0000                              // End of credits tilemap

warnpc $ceffff

// Placeholder label for item locations inserted by the randomizer
org $ded200
itemlocations:
    {pink}
    dw "         ITEM LOCATIONS         " // 640
    padbyte $ca
    pad $dedbcf
