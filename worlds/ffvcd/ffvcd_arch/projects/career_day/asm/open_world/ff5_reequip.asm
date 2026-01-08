;
; ff5_reequip.asm
;    再装備の改善 revision 0.2
;
; 解説
;
;    再装備の処理を改善します。ジョブ・アビリティの変更時に装備が変わらない
;    ようにします (装備できないアイテムは自動的に外されます)。ジョブの変更時
;    に装備が変わらない「そのまま」と自動的に最強装備を行う「さいきょう」の
;    設定があります。
;
; 使用領域
;
;    $C0FA93-$C0FA96:    4 bytes
;    $C0FE67-$C0FE75:   15 bytes
;    $C0FE76-$C0FE7A:    5 bytes
;    $C2B5DD-$C2B5DF:    3 bytes
;    $C2B676-$C2B6B8:   67 bytes
;    $C2E1A6-$C2E1E1:   60 bytes
;    $C2E1E2-$C2E1FA:   25 bytes
;    $C2E211-$C2E258:   72 bytes
;    $C2E26B-$C2E285:   27 bytes
;    $C2F9F0-$C2FA64:  117 bytes
;    $C3AEC8-$C3AED8:   17 bytes
;    $C3B6CD-$C3B709:   61 bytes
;
; 空き領域
;
;    $C0FE7B-$C0FE7E:    4 bytes
;    $C2E1FB-$C2E210:   22 bytes
;    $C2E259-$C2E26A:   18 bytes
;    $C3AED9-$C3AEE9:   17 bytes
;    $C3B70A-$C3B70F:    6 bytes
;
; 依存関係
;
;    ff5_lr_menu.asm >= 1.0
;    ff5_optimize.asm
;

; incsrc ff5_labels.inc

;--------------------------------
; メニューテキストの変更
;--------------------------------
org $C0FA93
    dw MENUTEXT_86h
    dw MENUTEXT_87h

;--------------------------------
; MENUTEXT 86h: そうびが へんこうされました
;--------------------------------
org $C0FE67
MENUTEXT_86h:
    db $7D,$89,$23,$2B,$FF,$67,$B9,$73,$89,$75,$AD,$9D,$77,$7F,$00

;--------------------------------
; MENUTEXT 87h: そのまま
;--------------------------------
MENUTEXT_87h:
    db $7D,$9B,$9D,$9D,$00
    db $00,$00,$00,$00

;--------------------------------
; ("そうびが へんこうされました")
;--------------------------------
org $C3AEC8
MENUSCRIPT_REEQUIP_DIALOG:
   db $05,$00,$40
   db $06,$02,$00,$01,$14,$1E,$08
   db $04,$86,$00,$09,$17,$00
   db $00

;--------------------------------
; 未使用
;--------------------------------
org $C3AED9

;--------------------------------
; コンフィグの表示を変更
;--------------------------------
org $C3B67C
MENUSCRIPT_CONFIG_TEXT:
    db $01,$07,$04
    db $04,$0B,$00,$18,$03,$00
    db $04,$5C,$00,$04,$06,$00
    db $04,$5E,$00,$06,$08,$00
    db $04,$61,$00,$0F,$08,$80
    db $04,$60,$00,$0F,$09,$80
    db $04,$5F,$00,$06,$0A,$00
    db $04,$61,$00,$0F,$0A,$80
    db $04,$62,$00,$06,$0C,$00
    db $04,$63,$00,$06,$0E,$00
    db $04,$64,$00,$04,$10,$00
    db $04,$66,$00,$04,$12,$00
    db $04,$68,$00,$04,$14,$00
    db $04,$18,$00,$0F,$14,$00
    db $04,$87,$00,$16,$14,$00
    db $04,$69,$00,$04,$16,$00
    db $04,$6B,$00,$0F,$18,$00
    db $04,$6C,$00,$04,$1A,$00
    db $04,$6D,$00,$0F,$1A,$80
    db $04,$6E,$00,$0F,$1C,$80
    db $04,$6F,$00,$0F,$1E,$80
    db $04,$70,$00,$11,$1A,$80
    db $04,$70,$00,$11,$1C,$80
    db $04,$70,$00,$11,$1E,$80
    db $00
    db $00,$00,$00,$00,$00,$00

org $C2F9F0
;--------------------------------
; 再装備の処理
;--------------------------------
FAST_REEQUIP:
    PHB
    PHP
    SEP #$20
    LDA #$7E
    PHA
    PLB
    STZ $74         ; 装備が変更されたかどうかの判定に使用
    JSR $E178       ; キャラクタの装備を取得する ($7E050E -> $7E01E0)
    LDA #$01        ; #$01 = "右手"

.begin
    STA $6F         ; 選択したカーソル位置
    JSR ITEM_GET_EQUIP
    CMP #$02        ; (Check if 0x00 or すで)
    BCC .next_equip

    LDY $80         ; 自分アドレスへのインデックス
    CMP #$80        ; (Check if 防具)
    BCS .equip_check

    XBA             ; (Save アイテムの番号)
    LDA $6F         ; 選択したカーソル位置
    CMP #$02        ; 左手以外は二刀流をチェックしない
    BNE .skip_dualwield_check

    LDA $E5         ; 右手武器を装備していなければ二刀流をチェックしない
    BEQ .skip_dualwield_check

    LDA $0521,Y     ; アビリティフラグ2 (01: 二刀流, 02: 先制攻撃, 04: 警戒,
                    ; 08: バーサク, 10: 薬の知識, 20: 両手持ち, 40: 格闘,
                    ; 80: かばう)
    AND #$01        ; (Check for 二刀流)
    BEQ .item_unequip

.skip_dualwield_check
    XBA             ; (Restore アイテムの番号)

.equip_check
    JSR $D9AB       ; アイテムデータを読み込む (Aレジスタ: アイテムの番号)
                    ; (-> $019B～$01A6)
    LDA $9D         ; 武器/防具データ[2]: 装備タイプ
    REP #$20
    AND #$003F
    ASL
    ASL
    TAX
    LDA FILEPOS_EQUIPTYPES,X
    AND $0540,Y     ; 装備できるアイテム(武器)
    BNE .item_equip

    LDA FILEPOS_EQUIPTYPES+2,X
    AND $0542,Y     ; 装備できるアイテム(防具)
.item_equip
    SEP #$20
    BNE .next_equip

.item_unequip
    INC $74         ; 装備が変更されたかどうかの判定に使用
    JSR $E211       ; 装備を外す ($73: 外したアイテム)
    LDA $73
    JSR $E286       ; そのアイテムを外せるかどうか ($90: 0: できる, 1: アイ
                    ; テム数が 100 個以上, 2: できない)
    LDA $90
    BNE .next_equip

    LDA #$01
    XBA
    LDA $73
    JSR $E2CE       ; アイテムを増やす (AL: 種類, AH: 個数)

.next_equip
    LDA $6F         ; 選択したカーソル位置
    INC
    CMP #$06
    BNE .begin

    JSR $E18F       ; キャラクタの装備を更新する ($7E01E0 -> $7E050E)
    PLP
    PLB
    RTS

;--------------------------------
; キャラクタの装備を再装備 / 各種パラメータの再設定
;--------------------------------
org $C2B676
DO_REEQUIP:
    PHP
    SEP #$20
    JSR $E6D6       ; キャラクタの(HP | MP | 能力値 | フラグ)を初期化する
    LDA $2D11       ; ジョブを変更したかどうかのフラグ (1: 変更した)
    BEQ .fast_reequip

    LDA $0973       ; コンフィグ (01: そのまま, 02: モノラル, 04: 記憶,
                    ; 80: ゲージOFF)
    AND #$01        ; (Check for そのまま)
    BNE .fast_reequip

.optimize
    JSR $DAA4       ; 装備をすべて外す
    JSR $FAAD       ; 防具を最強装備に変更する
    JSR $F869       ; 右手/左手を最強装備に変更する
    BRA .show_dialog

.fast_reequip
    JSR FAST_REEQUIP
    LDA $74         ; 装備が変更されたかどうかの判定に使用
    BEQ .skip_dialog

.show_dialog
    REP #$20
    LDA #MENUSCRIPT_REEQUIP_DIALOG
    JSR $C1B8       ; Run Menu Script
    JSR $A693       ; BG2 を更新する
                    ; /* LONGA OFF */
    LDA #$02        ; #$02 = "BG2 enable"
    TSB $7500       ; Main Screen Designation
    LDA #$04        ; #$04 = "Screen Settings"
    TSB $CA         ; DMA を実行するチャンネル
    LDX #$0028
    JSR $E65B       ; X/60 秒のウェイト

.skip_dialog
    JSR $B2BD       ; 画面表示を無効にする
    PLP
    RTS

;--------------------------------
; アイテムを装備する ($72: 装備したアイテム)
;--------------------------------
org $C2E1A6
ITEM_EQUIP:
    PHP
    SEP #$20
    JSR GET_EQUIP_INDEX
    CMP #$03        ; (Check if 頭, 体, アクセサリ)
    BMI .weapon

    LDA $72
    STA $E0,X       ; 装備品 (防具)
    BRA .ret

.weapon
    LDA $72
    BMI .equip_shield

    STA $E5,X       ; 装備品 (右手武器)
    STZ $E3,X       ; 装備品 (右手盾)
    BRA .arm_check

.equip_shield
    STA $E3,X       ; 装備品 (右手盾)
    STZ $E5,X       ; 装備品 (右手武器)

.arm_check
    LDA $E5,X       ; 装備品 (右手武器)
    BEQ .check_unarmed

    TYX
    LDA $E5,X       ; 装備品 (右手武器)
    CMP #$01        ; (Check if すで)
    BNE .ret

    STZ $E5,X       ; 装備品 (右手武器)
    BRA .ret

.check_unarmed
    TYX
    LDA $E5,X       ; 装備品 (右手武器)
    ORA $E3,X       ; 装備品 (右手盾)
    BNE .ret

    LDA #$01        ; #$01 = "すで"
    STA $E5,X       ; 装備品 (右手武器)
    STZ $E3,X       ; 装備品 (右手盾)

.ret
    PLP
    RTS

;--------------------------------
; 装備を取得する (Aレジスタ: アイテムの番号)
;--------------------------------
ITEM_GET_EQUIP:
    PHP
    SEP #$20
    JSR GET_EQUIP_INDEX
    CMP #$03        ; (Check if 頭, 体, アクセサリ)
    BPL .protector

    LDA $E5,X       ; 装備品 (右手武器)
    BNE .ret

    LDA $E3,X       ; 装備品 (右手盾)
    BRA .ret

.protector
    LDA $E0,X       ; 装備品 (防具)
    JSR $CBF1       ; if (A == 0x80) { A = 0x00; }

.ret
    PLP
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP

;--------------------------------
; 装備を外す ($73: 外したアイテム)
;--------------------------------
org $C2E211
ITEM_UNEQUIP:
    PHP
    SEP #$20
    STZ $73
    JSR GET_EQUIP_INDEX
    CMP #$03        ; (Check if 頭, 体, アクセサリ)
    BMI .weapon

    LDA $E0,X       ; 装備品 (防具)
    BEQ .ret

    CMP #$80
    BEQ .ret

    STA $73
    LDA #$80
    STA $E0,X       ; 装備品 (防具)
    BRA .ret

.weapon
    LDA $E5,X       ; 装備品 (右手武器)
    BNE .weapon_unequip

    LDA $E3,X       ; 装備品 (右手盾)
    BEQ .weapon_unarmed

.weapon_unequip
    CMP #$01        ; (Check if すで)
    BEQ .arm_check

    STA $73
    STZ $E3,X       ; 装備品 (右手盾)

.weapon_unarmed
    LDA #$01        ; #$01 = "すで"
    STA $E5,X       ; 装備品 (右手武器)

.arm_check
    PHX
    TYX
    LDA $E5,X       ; 装備品 (右手武器)
    CMP #$02        ; (Check if 0x00 or すで)
    BCC .check_unarmed

    PLX
    STZ $E5,X       ; 装備品 (右手武器)
    BRA .ret

.check_unarmed
    PLY
    LDA $E3,X       ; 装備品 (右手盾)
    BNE .ret

    LDA #$01        ; #$01 = "すで"
    STA $E5,X       ; 装備品 (右手武器)

.ret
    PLP
    RTS

    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP : NOP : NOP
    NOP : NOP

;--------------------------------
; 装備アイテムのインデックスを取得する (A: カーソル位置, X: インデックス,
; Y: 反対側へのインデックス(武器))
;--------------------------------
GET_EQUIP_INDEX:
    LDA #$00
    XBA
    LDA $6F         ; 選択したカーソル位置
    CMP #$01        ; (Check if 右手)
    BEQ .weapon

    CMP #$02        ; (Check if 左手)
    BEQ .weapon

    INC
    AND #$03
    BRA .ret

.weapon
    AND #$01
    TAY
    EOR #$01

.ret
    TAX
    LDA $6F         ; 選択したカーソル位置
    RTS

;--------------------------------
; ジョブ変更時に装備をすべて外す処理を削除
;--------------------------------
org $C2B5DD
    NOP
    NOP
    NOP
