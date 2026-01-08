;
; ff5_hp_color.asm
;    HP color の追加 revision 1.0
;
; 解説
;
;    戦闘中に表示する HP の色が残り HP の割合によって変化するようにします。
;
; 使用領域
;
;    $C130AE-$C130AF:    2 bytes
;    $C130F7-$C13107:   17 bytes
;    $C6FF2C-$C6FF5D:   50 bytes
;
; 空き領域
;
;    $C13108-$C13111:   10 bytes
;

;--------------------------------
; キャラクタの情報を表示する処理アドレス
;--------------------------------
org $C130AC
FILEPOS_DISPLAY_CHRINFO_ADDR:
    dw $327B                        ; 00: 名前を表示する
    dw DISPLAY_HIT_POINTS           ; 01: 現在ヒットポイントを表示する
    dw $3144                        ; 02: 最大ヒットポイントを表示する
    dw $3149                        ; 03: 現在マジックポイントを表示する
    dw $314E                        ; 04: 最大マジックポイントを表示する
    dw $315D                        ; 05: レベルを表示する
    dw $3177                        ; 06: 1 番目のコマンドを表示する
    dw $3182                        ; 07: 2 番目のコマンドを表示する
    dw $318D                        ; 08: 3 番目のコマンドを表示する
    dw $3198                        ; 09: 4 番目のコマンドを表示する
    dw $3112                        ; 0A: ジョブ名を表示する
    dw DISPLAY_EXPERIENCE_POINTS    ; 0B: 経験値を表示する
    dw $31A3                        ; 0C:
    dw $31AA                        ; 0D:
    dw $31B1                        ; 0E:
    dw $31B8                        ; 0F:
    dw $31BF                        ; 10:
    dw $31C6                        ; 11:
    dw $3158                        ; 12: 最大ヒットポイントを表示する
                                    ;     (suppression)
    dw $3153                        ; 13: 最大マジックポイントを表示する
                                    ;     (suppression)
    dw $30D6                        ; 14: 覚えたアビリティの数を表示する

;--------------------------------
; 拡張した現在ヒットポイントを表示する
;--------------------------------
org $C6FF2C
DISPLAY_EX_HIT_POINTS:
    REP #$20
    LDA ($78)       ; ヒットポイント
    BNE .check_hp_remaining

    LDA #$0004      ; Gray color if (HP == 0)
    BRA .hp_setattr

.check_hp_remaining
    PHY
    LDY #$0002
    LDA ($78),Y     ; 最大ヒットポイント
    PLY
    LSR
    LSR
    LSR
    CMP ($78)       ; ヒットポイント
    TDC
    BCC .hp_setattr

    LDA #$0008      ; Yellow color if (HP <= 最大HP÷8)

.hp_setattr
    SEP #$20
    STA $74         ; HP カラー

.write_char
    LDA $C4,X       ; decimal[0]
    STA ($BC),Y
    INY
    LDA $74         ; HP カラー
    STA ($BC),Y
    INY
    INX
    CPX #$0004
    BNE .write_char

    RTL

;--------------------------------
; 0Bh: 経験値を表示する
;--------------------------------
org $C130E5
DISPLAY_EXPERIENCE_POINTS:
    PHY
    LDY #$0003      ; 経験値(下位)
    LDA [$70],Y
    STA $74
    INY             ; 経験値(中位)
    LDA [$70],Y
    STA $75
    INY             ; 経験値(上位)
    LDA [$70],Y
    STA $72
    LDX $74
    STX $70
    PLY
    JMP $2EAB

;--------------------------------
; 01h: 現在ヒットポイントを表示する
;--------------------------------
DISPLAY_HIT_POINTS:
    TDC             ; ヒットポイント
    JSR $32A5       ; Read ($78),Y
    JSL DISPLAY_EX_HIT_POINTS
    RTS
