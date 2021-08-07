; custom credits
lorom
math pri on

; Defines for the script and credits data
!speed = $f770
!set = $9a17
!delay = $9a0d
!checkflag = checkflag&$FFFF
!draw = $0000
!end = $f6fe, $99fe
!blank = $1fc0
!row = $0040
!pink = "table tables/pink.tbl,rtl"
!yellow = "table tables/yellow.tbl,rtl"
!cyan = "table tables/cyan.tbl,rtl"
!blue = "table tables/blue.tbl,rtl"
!green = "table tables/green.tbl,rtl"
!orange = "table tables/orange.tbl,rtl"
!purple = "table tables/purple.tbl,rtl"
!big = "table tables/big.tbl,rtl"
!last_saveslot = $7fffe0
!timer_backup1 = $7fffe2
!timer_backup2 = $7fffe4
!softreset = $7fffe6
!scroll_speed = $7fffe8
!timer1 = $05b8
!timer2 = $05ba

; Patch soft reset to retain value of RTA counter
org $80844B
    jml patch_reset1
org $808490
    jml patch_reset2

; Patch loading and saving routines
org $81807f
    jmp patch_save

org $8180f7
    jmp patch_load

; Hijack loading new game to reset stats
org $828063
    jsl clear_values

; Hijack the original credits code to read the script from bank $DF
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



; Hijack when samus is in the ship and ready to leave the planet
org $a2ab13
    jsl game_end

; Patch NMI to skip resetting 05ba and instead use that as an extra time counter
org $8095e5
nmi:
    ldx #$00
    stx $05b4
    ldx $05b5
    inx
    stx $05b5
    inc $05b6
.inc:
    ;rep #$30
    ;inc $05b8
    jsl nmi_read_messages
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

; Patch soft reset to save the value of the RTA timer
org $80fe00
patch_reset1:
    lda !softreset ; Check if we're softresetting
    cmp #$babe
    beq .save
    lda #$babe
    sta !softreset
    lda #$0000
    sta !timer_backup1
    sta !timer_backup2
    sta !last_saveslot
    bra .skipsave
.save:   
    lda !timer1
    sta !timer_backup1
    lda !timer2
    sta !timer_backup2
.skipsave:
    ldx #$1ffe
    lda #$0000
-
    stz $0000, x
    dex
    dex
    bpl - 
    lda !timer_backup1
    sta !timer1
    lda !timer_backup2
    sta !timer2
    jsl init_memory
    jml $808455

patch_reset2:
    lda !timer1
    sta !timer_backup1
    lda !timer2
    sta !timer_backup2
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

    ldx #$00df          ; clear temp variables
    lda #$0000
-
    sta $7fff00, x
    dex
    dex
    bpl -

    lda !timer_backup1
    sta !timer1
    lda !timer_backup2
    sta !timer2
    jml $8084af

warnpc $80ff00

; Patch load and save routines
org $81ef20
patch_save:
    lda !timer1
    sta $7ffc00
    lda !timer2
    sta $7ffc02
    jsl save_stats
    lda config_multiworld
    beq +
    jsl mw_save_sram
+
    lda $7e0952
    clc
    adc #$0010
    sta !last_saveslot
    ply
    plx
    clc
    plb
    plp
    rtl

patch_load:
    lda $7e0952
    clc
    adc #$0010
    cmp !last_saveslot      ; If we're loading the same save that's played last
    beq +                   ; don't restore stats from SRAM, only do this if
    jsl load_stats          ; a new save slot is loaded, or loading from hard reset
    lda $7ffc00
    sta !timer1
    lda $7ffc02
    sta !timer2
+
    lda config_multiworld
    beq +
    jsl mw_load_sram
+   
    ply
    plx
    clc
    plb
    rtl

; Hijack after decompression of regular credits tilemaps
org $8be0d1
    jsl copy

; Load credits script data from bank $df instead of $8c
org $8bf770
set_scroll:
    rep #$30
    phb : pea $df00 : plb : plb
    lda $0000, y
    sta !scroll_speed
    iny
    iny
    plb
    rts

scroll:
    inc $1995
    lda $1995
    cmp !scroll_speed
    beq +
    lda $1997
    jml $8b9989
+
    stz $1995
    inc $1997
    lda $1997
    jml $8b9989


patch1:
    phb : pea $df00 : plb : plb
    lda $0000, y    
    bpl +
    plb
    jml $8b99a0
+
    plb
    jml $8b99aa

patch2:
    sta $0014
    phb : pea $df00 : plb : plb
    lda $0002, y    
    plb
    jml $8b99eb

patch3:
    phb : pea $df00 : plb : plb
    lda $0000, y
    tay
    plb
    jml $8b9a0c

patch4:
    phb : pea $df00 : plb : plb
    lda $0000, y
    plb
    sta $19fb
    jml $8b9a1f

; Copy custom credits tilemap data from $ceb240,x to $7f2000,x
copy:
    pha
    phx
    ldx #$0000
-
    lda.l credits_rom, x
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
    sta !scroll_speed
    plx
    pla
    jsl $8b95ce
    rtl

clear_values:
    php
    rep #$30
    ; Do some checks to see that we're actually starting a new game    
    ; Make sure game mode is 1f
    lda $7e0998
    cmp.w #$001f
    bne .ret
    
    ; Check if samus saved energy is 00, if it is, run startup code
    lda $7ed7e2
    bne .ret

    ldx #$0000
    lda #$0000
-
    jsl store_stat
    inx
    cpx #$0180
    bne -

    ; Clear RTA Timer
    lda #$0000
    sta !timer1
    sta !timer2

.ret:
    plp
    jsl $809a79
    rtl

; Game has ended, save RTA timer to RAM and copy all stats to SRAM a final time
game_end:
    lda !timer1
    sta $7ffc00
    lda !timer2
    sta $7ffc02

    ; Subtract frames from pressing down at ship to this code running
    lda $7ffc00
    sec
    sbc #$013d
    sta $7ffc00
    lda #$0000  ; if carry clear this will subtract one from the high byte of timer
    sbc $7ffc02

    jsl save_stats
    lda #$000a
    jsl $90f084
    rtl

checkflag:
    rep #$30
    phb : pea $df00 : plb : plb : phx
    ldx $0000, y ; Load flag address to check
    iny #2
    lda.l config_flags&$FF0000, x ; load flag    
    bne .show
    lda $0000, y ; Load next instruction
    tay
    bra .end
.show
    iny #2
.end
    plx
    plb
    rts    


org $dfd4f0
; Draw full time as hh:mm:ss:ff
; Pointer to first byte of RAM in A
draw_full_time:
    phx
    phb
    pea $7f7f : plb : plb
    tax
    lda $0000, x
    sta $16
    lda $0002, x
    sta $14
    lda #$003c
    sta $12
    lda #$ffff
    sta $1a
    jsr div32 ; frames in $14, rest in $16
    iny : iny : iny : iny : iny : iny ; Increment Y three positions forward to write the last value    
    lda $14
    jsr draw_two
    tya
    sec
    sbc #$0010
    tay     ; Skip back 8 characters to draw the top three things
    lda $16
    jsr draw_time
    plb
    plx
    rts  

; Draw time as xx:yy:zz
draw_time:
    phx
    phb
    dey : dey : dey : dey : dey : dey ; Decrement Y by 3 characters so the time count fits
    pea $7f7f : plb : plb
    sta $004204
    sep #$20
    lda #$ff
    sta $1a
    lda #$3c
    sta $004206
    pha : pla : pha : pla : rep #$20
    lda $004216 ; Seconds or Frames
    sta $12
    lda $004214 ; First two groups (hours/minutes or minutes/seconds)
    sta $004204
    sep #$20
    lda #$3c
    sta $004206
    pha : pla : pha : pla : rep #$20
    lda $004216
    sta $14
    lda $004214 ; First group (hours or minutes)
    jsr draw_two
    iny : iny ; Skip past separator
    lda $14 ; Second group (minutes or seconds)
    jsr draw_two
    iny : iny
    lda $12 ; Last group (seconds or frames)
    jsr draw_two
    plb
    plx
    rts        

; Draw 5-digit value to credits tilemap
; A = number to draw, Y = row address
draw_value:
    phx    
    phb
    pea $7f7f : plb : plb
    sta $004204
    lda #$0000
    sta $1a     ; Leading zeroes flag
    sep #$20
    lda #$64
    sta $004206
    pha : pla : pha : pla : rep #$20
    lda $004216 ; Last two digits
    sta $12
    lda $004214 ; Top three digits
    jsr draw_three
    lda $12
    jsr draw_two
    plb
    plx
    rts

draw_three:
    sta $004204
    sep #$20
    lda #$64
    sta $004206
    pha : pla : pha : pla : rep #$20
    lda $004214 ; Hundreds
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0034, y
    lda.l numbers_bot, x
    sta $0074, y
    dec $1a
+
    iny : iny ; Next number
    lda $004216

draw_two:
    sta $004204
    sep #$20
    lda #$0a
    sta $004206
    pha : pla : pha : pla : rep #$20
    lda $004214
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0034, y
    lda.l numbers_bot, x
    sta $0074, y
    dec $1a
+
    lda $004216
    asl
    tax
    cmp $1a
    beq +
    lda.l numbers_top, x
    sta $0036, y
    lda.l numbers_bot, x
    sta $0076, y
    dec $1a
+
    iny : iny : iny : iny
    rts

; Loop through stat table and update RAM with numbers representing those stats
write_stats:
    phy
    phb
    php
    pea $dfdf : plb : plb
    rep #$30
    jsl load_stats      ; Copy stats back from SRAM
    ldx #$0000
    ldy #$0000

.loop:
    ; Get pointer to table
    tya
    asl : asl : asl
    tax

    ; Load stat type
    lda.l stats+4, x
    beq .end
    cmp #$0001
    beq .number
    cmp #$0002
    beq .time
    cmp #$0003
    beq .fulltime
    jmp .continue

.number:
    ; Load statistic
    lda.l stats, x
    jsl load_stat
    pha

    ; Load row address
    lda.l stats+2, x
    tyx
    tay
    pla
    jsr draw_value
    txy
    jmp .continue

.time:
    ; Load statistic
    lda.l stats, x
    jsl load_stat
    pha

    ; Load row address
    lda.l stats+2, x
    tyx
    tay
    pla
    jsr draw_time
    txy
    jmp .continue

.fulltime:    
    lda.l stats, x        ; Get stat id
    asl
    clc
    adc #$fc00          ; Get pointer to value instead of actual value
    pha

    ; Load row address
    lda.l stats+2, x
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

; 32-bit by 16-bit division routine I found somewhere
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

load_stats:
    phx
    pha
    ldx #$0000
    lda $7e0952
    bne +
-
    lda $701400, x
    sta $7ffc00, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end
+   
    cmp #$0001
    bne +
    lda $701700, x
    sta $7ffc00, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end
+   
    lda $701a00, x
    sta $7ffc00, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end

.end:
    pla
    plx
    rtl

save_stats:
    phx
    pha
    ldx #$0000
    lda $7e0952
    bne +
-
    lda $7ffc00, x
    sta $701400, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end
+   
    cmp #$0001
    bne +
    lda $7ffc00, x
    sta $701700, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end
+   
    lda $7ffc00, x
    sta $701a00, x
    inx
    inx
    cpx #$0300
    bne -
    jmp .end

.end:
    pla
    plx
    rtl

warnpc $dfd800
; Increment Statistic (in A)
org $dfd800
inc_stat:
    phx
    asl
    tax
    lda $7ffc00, x
    inc
    sta $7ffc00, x
    plx
    rtl

; Decrement Statistic (in A)
org $dfd840
dec_stat:
    phx
    asl
    tax
    lda $7ffc00, x
    dec
    sta $7ffc00, x
    plx
    rtl


; Store Statistic (value in A, stat in X)
org $dfd880
store_stat:
    phx
    pha
    txa
    asl
    tax
    pla
    sta $7ffc00, x
    plx
    rtl

; Load Statistic (stat in A, returns value in A)
org $dfd8b0
load_stat:
    phx
    asl
    tax
    lda $7ffc00, x
    plx
    rtl


; New credits script in free space of bank $DF
org $dfd91b
script:
    dw !set, $0002 : -
    dw !draw, !blank
    dw !delay, -
    
    ; Show a compact version of the original credits so we get time to add more    
    dw !draw, !row*0      ; SUPER METROID STAFF
    dw !draw, !blank
    dw !draw, !row*4      ; PRODUCER
    dw !draw, !blank
    dw !draw, !row*7      ; MAKOTO KANOH
    dw !draw, !row*8      
    dw !draw, !blank
    dw !draw, !row*9      ; DIRECTOR
    dw !draw, !blank
    dw !draw, !row*10     ; YOSHI SAKAMOTO
    dw !draw, !row*11     
    dw !draw, !blank
    dw !draw, !row*12     ; BACK GROUND DESIGNERS
    dw !draw, !blank
    dw !draw, !row*13     ; HIROFUMI MATSUOKA
    dw !draw, !row*14     
    dw !draw, !blank
    dw !draw, !row*15     ; MASAHIKO MASHIMO
    dw !draw, !row*16     
    dw !draw, !blank
    dw !draw, !row*17     ; HIROYUKI KIMURA
    dw !draw, !row*18     
    dw !draw, !blank
    dw !draw, !row*19     ; OBJECT DESIGNERS
    dw !draw, !blank
    dw !draw, !row*20     ; TOHRU OHSAWA
    dw !draw, !row*21     
    dw !draw, !blank
    dw !draw, !row*22     ; TOMOYOSHI YAMANE
    dw !draw, !row*23    
    dw !draw, !blank
    dw !draw, !row*24     ; SAMUS ORIGINAL DESIGNERS
    dw !draw, !blank
    dw !draw, !row*25     ; HIROJI KIYOTAKE
    dw !draw, !row*26    
    dw !draw, !blank
    dw !draw, !row*27     ; SAMUS DESIGNER
    dw !draw, !blank
    dw !draw, !row*28     ; TOMOMI YAMANE
    dw !draw, !row*29    
    dw !draw, !blank
    dw !draw, !row*83     ; SOUND PROGRAM
    dw !draw, !row*107    ; AND SOUND EFFECTS
    dw !draw, !blank
    dw !draw, !row*84     ; KENJI YAMAMOTO
    dw !draw, !row*85    
    dw !draw, !blank
    dw !draw, !row*86     ; MUSIC COMPOSERS
    dw !draw, !blank
    dw !draw, !row*84     ; KENJI YAMAMOTO
    dw !draw, !row*85    
    dw !draw, !blank
    dw !draw, !row*87     ; MINAKO HAMANO
    dw !draw, !row*88    
    dw !draw, !blank
    dw !draw, !row*30     ; PROGRAM DIRECTOR
    dw !draw, !blank
    dw !draw, !row*31     ; KENJI IMAI
    dw !draw, !row*64    
    dw !draw, !blank
    dw !draw, !row*65     ; SYSTEM COORDINATOR
    dw !draw, !blank
    dw !draw, !row*66     ; KENJI NAKAJIMA
    dw !draw, !row*67    
    dw !draw, !blank
    dw !draw, !row*68     ; SYSTEM PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*69     ; YOSHIKAZU MORI
    dw !draw, !row*70    
    dw !draw, !blank
    dw !draw, !row*71     ; SAMUS PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*72     ; ISAMU KUBOTA
    dw !draw, !row*73    
    dw !draw, !blank
    dw !draw, !row*74     ; EVENT PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*75     ; MUTSURU MATSUMOTO
    dw !draw, !row*76    
    dw !draw, !blank
    dw !draw, !row*77     ; ENEMY PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*78     ; YASUHIKO FUJI
    dw !draw, !row*79    
    dw !draw, !blank
    dw !draw, !row*80     ; MAP PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*81     ; MOTOMU CHIKARAISHI
    dw !draw, !row*82    
    dw !draw, !blank
    dw !draw, !row*101    ; ASSISTANT PROGRAMMER
    dw !draw, !blank
    dw !draw, !row*102    ; KOUICHI ABE
    dw !draw, !row*103   
    dw !draw, !blank
    dw !draw, !row*104    ; COORDINATORS
    dw !draw, !blank
    dw !draw, !row*105    ; KATSUYA YAMANO
    dw !draw, !row*106   
    dw !draw, !blank
    dw !draw, !row*63     ; TSUTOMU KANESHIGE
    dw !draw, !row*96   
    dw !draw, !blank
    dw !draw, !row*89    ; PRINTED ART WORK
    dw !draw, !blank
    dw !draw, !row*90    ; MASAFUMI SAKASHITA
    dw !draw, !row*91   
    dw !draw, !blank
    dw !draw, !row*92    ; YASUO INOUE
    dw !draw, !row*93   
    dw !draw, !blank
    dw !draw, !row*94    ; MARY COCOMA
    dw !draw, !row*95   
    dw !draw, !blank
    dw !draw, !row*99    ; YUSUKE NAKANO
    dw !draw, !row*100   
    dw !draw, !blank
    dw !draw, !row*108   ; SHINYA SANO
    dw !draw, !row*109   
    dw !draw, !blank
    dw !draw, !row*110   ; NORIYUKI SATO
    dw !draw, !row*111   
    dw !draw, !blank
    dw !draw, !row*32    ; SPECIAL THANKS TO
    dw !draw, !blank
    dw !draw, !row*33    ; DAN OWSEN
    dw !draw, !row*34   
    dw !draw, !blank
    dw !draw, !row*35    ; GEORGE SINFIELD
    dw !draw, !row*36   
    dw !draw, !blank
    dw !draw, !row*39    ; MASARU OKADA
    dw !draw, !row*40   
    dw !draw, !blank
    dw !draw, !row*43    ; TAKAHIRO HARADA
    dw !draw, !row*44   
    dw !draw, !blank
    dw !draw, !row*47    ; KOHTA FUKUI
    dw !draw, !row*48   
    dw !draw, !blank
    dw !draw, !row*49    ; KEISUKE TERASAKI
    dw !draw, !row*50   
    dw !draw, !blank
    dw !draw, !row*51    ; MASARU YAMANAKA
    dw !draw, !row*52   
    dw !draw, !blank
    dw !draw, !row*53    ; HITOSHI YAMAGAMI
    dw !draw, !row*54   
    dw !draw, !blank
    dw !draw, !row*57    ; NOBUHIRO OZAKI
    dw !draw, !row*58   
    dw !draw, !blank
    dw !draw, !row*59    ; KENICHI NAKAMURA
    dw !draw, !row*60   
    dw !draw, !blank
    dw !draw, !row*61    ; TAKEHIKO HOSOKAWA
    dw !draw, !row*62   
    dw !draw, !blank
    dw !draw, !row*97    ; SATOSHI MATSUMURA
    dw !draw, !row*98   
    dw !draw, !blank
    dw !draw, !row*122   ; TAKESHI NAGAREDA
    dw !draw, !row*123  
    dw !draw, !blank
    dw !draw, !row*124   ; MASAHIRO KAWANO
    dw !draw, !row*125  
    dw !draw, !blank
    dw !draw, !row*45    ; HIRO YAMADA
    dw !draw, !row*46  
    dw !draw, !blank
    dw !draw, !row*112   ; AND ALL OF R&D1 STAFFS
    dw !draw, !row*113  
    dw !draw, !blank
    dw !draw, !row*114   ; GENERAL MANAGER
    dw !draw, !blank
    dw !draw, !row*5     ; GUMPEI YOKOI
    dw !draw, !row*6  
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank

    ; Custom item randomizer credits text        

    dw !draw, credits_start
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_randomizer
    dw !draw, !blank
    dw !draw, credits_randomizer+!row*1
    dw !draw, credits_randomizer+!row*2
    dw !draw, !blank
    dw !draw, credits_randomizer+!row*3
    dw !draw, credits_randomizer+!row*4
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_snes
    dw !draw, !blank
    dw !draw, credits_snes+!row*1
    dw !draw, credits_snes+!row*2
    dw !draw, !blank
    dw !draw, credits_snes+!row*3
    dw !draw, credits_snes+!row*4
    dw !draw, !blank
    dw !draw, credits_snes+!row*5
    dw !draw, credits_snes+!row*6
    dw !draw, !blank
    dw !draw, credits_snes+!row*7
    dw !draw, credits_snes+!row*8
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_patches
    dw !draw, !blank
    dw !draw, credits_patches+!row*1
    dw !draw, credits_patches+!row*2
    dw !draw, !blank
    dw !draw, credits_patches+!row*3
    dw !draw, credits_patches+!row*4
    dw !draw, !blank
    dw !draw, credits_patches+!row*5
    dw !draw, credits_patches+!row*6
    dw !draw, !blank
    dw !draw, !blank
    dw !checkflag, config_sprite, .after_sprite
    dw !draw, credits_custom_sprite_graphics
    dw !draw, !blank
    dw !draw, credits_custom_sprite_graphics+!row*1
    dw !draw, credits_custom_sprite_graphics+!row*2
    dw !draw, !blank
    dw !draw, !blank
.after_sprite
    dw !draw, credits_original
    dw !draw, !blank
    dw !draw, credits_original+!row*1
    dw !draw, credits_original+!row*2
    dw !draw, !blank
    dw !draw, credits_special
    dw !draw, !blank
    dw !draw, credits_special+!row*1
    dw !draw, credits_special+!row*2
    dw !draw, !blank
    dw !draw, credits_special+!row*3
    dw !draw, credits_special+!row*4
    dw !draw, !blank
    dw !draw, credits_special+!row*5
    dw !draw, credits_special+!row*6
    dw !draw, !blank
    dw !draw, credits_special+!row*7
    dw !draw, credits_special+!row*8
    dw !draw, !blank
    dw !draw, credits_special+!row*9
    dw !draw, credits_special+!row*10
    dw !draw, !blank
    dw !draw, credits_special+!row*11
    dw !draw, credits_special+!row*12
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_metconst
    dw !draw, !blank
    dw !draw, credits_metconst+!row*1
    dw !draw, credits_metconst+!row*2
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_srl
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_play
    dw !draw, !blank
    dw !draw, credits_play+!row*1
    dw !draw, credits_play+!row*2
    dw !draw, !blank
    dw !draw, !blank
    

    ; Gameplay statistics
    dw !draw, !blank
    dw !draw, credits_stats
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_stats+!row*1
    dw !draw, !blank

    ; Set scroll speed to 3 frames per pixel
    dw !speed, $0003
    dw !draw, credits_stats+!row*2
    dw !draw, credits_stats+!row*3
    dw !draw, !blank
    dw !draw, credits_stats+!row*4
    dw !draw, credits_stats+!row*5
    dw !draw, !blank
    dw !draw, credits_stats+!row*6
    dw !draw, credits_stats+!row*7
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_stats+!row*8
    dw !draw, !blank
    dw !draw, credits_stats+!row*9
    dw !draw, credits_stats+!row*10
    dw !draw, !blank
    dw !draw, credits_stats+!row*11
    dw !draw, credits_stats+!row*12
    dw !draw, !blank
    dw !draw, credits_stats+!row*13
    dw !draw, credits_stats+!row*14
    dw !draw, !blank
    dw !draw, credits_stats+!row*15
    dw !draw, credits_stats+!row*16
    dw !draw, !blank
    dw !draw, credits_stats+!row*17
    dw !draw, credits_stats+!row*18
    dw !draw, !blank
    dw !draw, credits_stats+!row*19
    dw !draw, credits_stats+!row*20
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_stats+!row*21
    dw !draw, !blank
    dw !draw, credits_stats+!row*22
    dw !draw, credits_stats+!row*23
    dw !draw, !blank
    dw !draw, credits_stats+!row*24
    dw !draw, credits_stats+!row*25
    dw !draw, !blank
    dw !draw, credits_stats+!row*26
    dw !draw, credits_stats+!row*27
    dw !draw, !blank
    dw !draw, credits_stats+!row*28
    dw !draw, credits_stats+!row*29
    dw !draw, !blank
    dw !draw, credits_stats+!row*30
    dw !draw, credits_stats+!row*31
    dw !draw, !blank
    dw !draw, credits_stats+!row*32
    dw !draw, credits_stats+!row*33

   
    ; Draw item locations
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*640
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !row*641
    dw !draw, !row*642
    dw !draw, !blank
    dw !draw, !row*643
    dw !draw, !row*644
    dw !draw, !blank
    dw !draw, !row*645
    dw !draw, !row*646
    dw !draw, !blank
    dw !draw, !row*647
    dw !draw, !row*648
    dw !draw, !blank
    dw !draw, !row*649
    dw !draw, !row*650
    dw !draw, !blank
    dw !draw, !row*651
    dw !draw, !row*652
    dw !draw, !blank
    dw !draw, !row*653
    dw !draw, !row*654
    dw !draw, !blank
    dw !draw, !row*655
    dw !draw, !row*656
    dw !draw, !blank
    dw !draw, !row*657
    dw !draw, !row*658
    dw !draw, !blank
    dw !draw, !row*659
    dw !draw, !row*660
    dw !draw, !blank
    dw !draw, !row*661
    dw !draw, !row*662
    dw !draw, !blank
    dw !draw, !row*663
    dw !draw, !row*664
    dw !draw, !blank
    dw !draw, !row*665
    dw !draw, !row*666
    dw !draw, !blank
    dw !draw, !row*667
    dw !draw, !row*668
    dw !draw, !blank
    dw !draw, !row*669
    dw !draw, !row*670
    dw !draw, !blank
    dw !draw, !row*671
    dw !draw, !row*672

    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_stats_final
    dw !draw, credits_stats_final+!row*1
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, credits_stats_final+!row*2
    dw !draw, credits_stats_final+!row*3
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank
    dw !draw, !blank

    ; Set scroll speed to 4 frames per pixel
    dw !speed, $0004
   
    ; Scroll all text off and end credits
    dw !set, $0017 : -
    dw !draw, !blank
    dw !delay, -    
    dw !end

stats:
    ; STAT ID,  ADDRESS,                        TYPE (1 = Number, 2 = Time, 3 = Full time), UNUSED
    dw 0,       credits_stats_final,            3, 0    ; Full RTA Time
    dw 2,       credits_stats_doors,            1, 0    ; Door transitions
    dw 3,       credits_stats_doors+!row*2,     3, 0    ; Time in doors
    dw 5,       credits_stats_doors+!row*4,     2, 0    ; Time adjusting doors
    dw 7,       credits_stats_spent,            3, 0    ; Crateria
    dw 9,       credits_stats_spent+!row*2,     3, 0    ; Brinstar
    dw 11,      credits_stats_spent+!row*4,     3, 0    ; Norfair
    dw 13,      credits_stats_spent+!row*6,     3, 0    ; Wrecked Ship
    dw 15,      credits_stats_spent+!row*8,     3, 0    ; Maridia
    dw 17,      credits_stats_spent+!row*10,    3, 0    ; Tourian
    dw 20,      credits_stats_ammo,             1, 0    ; Charged Shots
    dw 21,      credits_stats_ammo+!row*2,      1, 0    ; Special Beam Attacks
    dw 22,      credits_stats_ammo+!row*4,      1, 0    ; Missiles
    dw 23,      credits_stats_ammo+!row*6,      1, 0    ; Super Missiles
    dw 24,      credits_stats_ammo+!row*8,      1, 0    ; Power Bombs
    dw 26,      credits_stats_ammo+!row*10,     1, 0    ; Bombs
    dw 0,       0,                              0, 0    ; end of table

warnpc $dfffff

; Relocated credits tilemap to free space in bank CE
org $ceb240
credits_rom:
base $7f2000
credits:
    ; When using big text, it has to be repeated twice, first in UPPERCASE and then in lowercase since it's split into two parts
    ; Numbers are mapped in a special way as described below:
    ; 0123456789%& '´
    ; }!@#$%&/()>~.

.start    
    !pink
    dw "     ITEM RANDOMIZER STAFF      " ; 128
    !purple
.randomizer
    dw "         RANDOMIZER CODE        " ; 129
    !big
    dw "             TOTAL              " ; 130
    dw "             total              " ; 131
    dw "           HALFAREBEL           " ; 132
    dw "           halfarebel           " ; 133
    !purple
.snes
    dw "           SNES CODE            " ; 134
    !big
    dw "             TOTAL              " ; 135
    dw "             total              " ; 136
    dw "             FOOSDA             " ; 137
    dw "             foosda             " ; 138
    dw "           PERSONITIS           " ; 139
    dw "           personitis           " ; 140
    dw "            ARTHEAU             " ; 141
    dw "            artheau             " ; 142
    !purple
.patches
    dw "          ROM PATCHES           " ; 143
    !big
    dw "             TOTAL              " ; 144
    dw "             total              " ; 145
    dw "             FOOSDA             " ; 146
    dw "             foosda             " ; 147
    dw "             LEODOX             " ; 148
    dw "             leodox             " ; 149
    !purple
.original
    dw "    ORIGINAL RANDOMIZER CODE    " ; 150
    !big
    dw "           DESSYREQT            " ; 151
    dw "           dessyreqt            " ; 152
    !cyan
.special
    dw "       SPECIAL THANKS TO        " ; 153
    !big
    dw "      PJBOY         KEJARDON    " ; 154
    dw "      pjboy         kejardon    " ; 155
    dw "   CROSSPRODUCT     FERAL5X     " ; 156
    dw "   crossproduct     feral%x     " ; 157
    dw "    STRAEVARAS   WILDANACONDA69 " ; 158
    dw "    straevaras   wildanaconda&) " ; 159
    dw "    BELTHASAR     KEKUMANSHOYU  " ; 160
    dw "    belthasar     kekumanshoyu  " ; 161
    dw "      TYPWO         LENOPHIS    " ; 162
    dw "      typwo         lenophis    " ; 163
    dw "      FEASEL        MITHICAL9   " ; 164
    dw "      feasel        mithical)   " ; 165
    !yellow
.metconst
    dw "      METROID CONSTRUCTION      " ; 166
    !big
    dw "     METROIDCONSTRUCTION COM    " ; 167
    dw "     metroidconstruction.com    " ; 168
    !yellow
.srl
    dw "  SUPER METROID SRL COMMUNITY   " ; 169
    !cyan
.play
    dw "     PLAY THIS RANDOMIZER AT    " ; 170
    !big
    dw "         BETA SAMUS LINK        " ; 171
    dw "         beta.samus.link        " ; 172
    !purple
.stats
    dw "      GAMEPLAY STATISTICS       " ; 173
    !orange
    dw "             DOORS              " ; 174
    !big
.stats_doors
    dw " DOOR TRANSITIONS               " ; 175
    dw " door transitions               " ; 176 
    dw " TIME IN DOORS      00'00'00^00 " ; 177
    dw " time in doors                  " ; 178 
    dw " TIME ALIGNING DOORS   00'00^00 " ; 179
    dw " time aligning doors            " ; 180 
    !blue
    dw "         TIME SPENT IN          " ; 181
    !big
.stats_spent
    dw " CRATERIA           00'00'00^00 " ; 182
    dw " crateria                       " ; 183
    dw " BRINSTAR           00'00'00^00 " ; 184
    dw " brinstar                       " ; 185
    dw " NORFAIR            00'00'00^00 " ; 186
    dw " norfair                        " ; 187
    dw " WRECKED SHIP       00'00'00^00 " ; 188
    dw " wrecked ship                   " ; 189
    dw " MARIDIA            00'00'00^00 " ; 190
    dw " maridia                        " ; 191
    dw " TOURIAN            00'00'00^00 " ; 192
    dw " tourian                        " ; 193
    !green
    dw "      SHOTS AND AMMO FIRED      " ; 194
    !big
.stats_ammo
    dw " CHARGED SHOTS                  " ; 195
    dw " charged shots                  " ; 196
    dw " SPECIAL BEAM ATTACKS           " ; 197
    dw " special beam attacks           " ; 198
    dw " MISSILES                       " ; 199
    dw " missiles                       " ; 200
    dw " SUPER MISSILES                 " ; 201
    dw " super missiles                 " ; 202
    dw " POWER BOMBS                    " ; 203
    dw " power bombs                    " ; 204
    dw " BOMBS                          " ; 205
    dw " bombs                          " ; 206
.stats_final
    dw " FINAL TIME         00'00'00^00 " ; 207
    dw " final time                     " ; 208
    dw "       THANKS FOR PLAYING       " ; 209
    dw "       thanks for playing       " ; 210
    !purple
.custom_sprite_graphics
    dw "     CUSTOM SPRITE GRAPHICS     " ; 211
    !big
    dw "                                " ; 212 // Custom sprite artist
    dw "                                " ; 213
    dw $0000                              ; End of credits tilemap

warnpc $ceff00

; Placeholder label for item locations inserted by the randomizer
org $ded200
itemlocations:
    !pink
    dw "      MAJOR ITEM LOCATIONS      " ; 640
    dw $0000

cleartable