;
; ff5_optimize.asm
;    最強装備の改善 revision 0.3
;
; 解説
;
;    最強装備の処理を変更します:
;
;    - 最強装備のアルゴリズムを改善
;    - 装備対象から除外するアイテムを指定可能
;
; 使用領域
;
;    $C2F869-$C2F89A:   50 bytes
;    $C2F89B-$C2F8B0:   22 bytes
;    $C2F8B1-$C2F8FE:   78 bytes
;    $C2F90B-$C2F931:   39 bytes
;    $C2F932-$C2F948:   23 bytes
;    $C2F949-$C2F9CF:  135 bytes
;    $C2FA65-$C2FA74:   16 bytes
;    $C2FAAD-$C2FAD3:   39 bytes
;
; 空き領域
;
;    $C2F8FF-$C2F90A:   12 bytes
;    $C2F9D0-$C2FA64:  149 bytes
;    $C2FFF8-$C2FFFF:    8 bytes
;

;--------------------------------
; 最強装備で使用するアドレス
;--------------------------------

;--------------------------------
; 最強装備から除外するアイテムのリスト
;--------------------------------
org $C2FA65
    db $5C          ; エクスカリパー
    db $55          ; ブラッドソード
    db $36          ; リリスのロッド
    db $CE          ; ちぬられたたて
    db $CC          ; いばらのかんむり
    db $BF          ; ボーンメイル
    db $B3          ; のろいのゆびわ
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;
    db $00          ;

;--------------------------------
; 右手/左手を最強装備に変更する
;--------------------------------
org $C2F869
OPTIMIZE_WEAPONS:
    PHB
    PHP
    PEA $7E7E
    PLB
    PLB             ; DBR = $7E
    REP #$20
    STZ $2CD1       ; 最強装備: 種類[0]
    STZ $2CD3       ; 最強装備: 種類[2]
    STZ $2CD5       ; 最強装備: 攻撃力[0]
    STZ $2CD7       ; 最強装備: 攻撃力[2]
    SEP #$20
    LDA #$01        ; #$01 = "右手"
    STA $6F         ; 選択したカーソル位置
    JSR $ED87       ; 右手/左手の装備欄をセットする
    LDX $75         ; 装備できるアイテムの数
    BEQ .ret

    JSR $EE94       ; 装備欄をソートする ($7A00: 入力/出力)
    LDY $80         ; 自分アドレスへのインデックス
    LDA $0521,Y     ; アビリティフラグ2 (01: 二刀流, 02: 先制攻撃, 04: 警戒,
                    ; 08: バーサク, 10: 薬の知識, 20: 両手持ち, 40: 格闘,
                    ; 80: かばう)
    STA $F0
    JSR EQUIP_OPTIMUM_WEAPON

.ret
    PLP
    PLB
    RTS

;--------------------------------
; 最強装備に変更する
;--------------------------------
EQUIP_OPTIMUM_ITEM:
    LDY $8E         ; $8E = 0

.begin
    JSR GET_OPTIMUM
    BCS .continue

    STA $72
    JSR $FA92       ; 装備を ($72) に変更する
    BRA .ret

.continue
    INY
    CPY $75         ; 装備できるアイテムの数
    BMI .begin

.ret
    RTS

;--------------------------------
; 防具を最強装備に変更する
;--------------------------------
org $C2FAAD
OPTIMIZE_PROTECTORS:
    PHB
    PHP
    SEP #$20
    LDA #$7E
    PHA
    PLB             ; DBR = $7E
    LDA #$03        ; #$03 = "頭"
    STA $6F         ; 選択したカーソル位置

.begin
    JSR $ED5E       ; 防具の装備欄をセットする
    LDX $75         ; 装備できるアイテムの数
    BEQ .continue

    JSR $EE94       ; 装備欄をソートする ($7A00: 入力/出力)
    JSR EQUIP_OPTIMUM_ITEM
    NOP
    NOP
    NOP

.continue
    INC $6F         ; 選択したカーソル位置
    LDA $6F         ; 選択したカーソル位置
    CMP #$06
    BNE .begin

    PLP
    PLB
    RTS

;--------------------------------
; 武器の最強装備を取得する (dest: {$2CD0,$2CD4}+A, XL: フラグ(40: 両手持ち
; OK, 80: 両手装備), XH: 除外フラグ)
;--------------------------------
org $C2F8B1
GET_OPTIMUM_WEAPON:
    PHP
    SEP #$20
    STX $2CCD
    DEC
    STA $2CCF
    STZ $2CD0
    LDY $8E         ; $8E = 0
    STY $2CCB

.begin
    LDA $7B00,Y     ; Menu buffer
    BEQ .continue

    JSR GET_OPTIMUM
    BMI .continue   ; 武器でなければ次へ
    BCS .continue

    JSR $D9AB       ; アイテムデータを読み込む (Aレジスタ: アイテムの番号)
                    ; (-> $019B～$01A6)
    LDA $9F         ; 武器/防具データ[4]: メッセージの番号
    AND $2CCD
    EOR $2CCE
    BEQ .continue

    LDA $A2         ; 武器データ[7]: 攻撃力
    STA $2CCC
    LDA $7A00,Y     ; Menu buffer
    STA $2CCB
    BRA .break

.continue
    INY
    CPY $75         ; 装備できるアイテムの数
    BMI .begin

.break
    LDX $2CCF
    LDA $2CCB
    STA $2CD1,X     ; 最強装備: 種類
    LDA $2CCC
    STA $2CD5,X     ; 最強装備: 攻撃力
    PLP
    RTS

;--------------------------------
; 盾の最強装備を取得する (dest: {$2CD0}+A)
;--------------------------------
org $C2F90B
GET_OPTIMUM_SHIELD:
    PHP
    SEP #$20
    DEC
    STA $2CCF
    STZ $2CD0
    LDX $2CCF
    LDY $8E         ; $8E = 0

.begin
    LDA $7B00,Y     ; Menu buffer
    BEQ .continue

    JSR GET_OPTIMUM
    BPL .continue   ; 盾でなければ次へ
    BCS .continue

    STA $2CD1,X     ; 最強装備: 種類
    BRA .ret

.continue
    INY
    CPY $75         ; 装備できるアイテムの数
    BMI .begin

.ret
    PLP
    RTS

;--------------------------------
; 最強装備の対象アイテムを取得する (C=1: 除外リストに一致)
;--------------------------------
GET_OPTIMUM:
    LDA $7A00,Y     ; Menu buffer
    PHA             ; A = 装備アイテムの番号
    PHX
    LDX #$FFFF

.begin
    INX
    CLC
    LDA $C2FA65,X
    BEQ .break

    CMP $03,S       ; A = 装備アイテムの番号
    BNE .begin

.break
    PLX
    PLA
    RTS

;--------------------------------
; 武器を最強装備に変更する
;--------------------------------
EQUIP_OPTIMUM_WEAPON:
    LDX #$0080      ; #$0080 = "両手装備"
    LDA #$01        ; (dest: $7E2CD1)
    JSR GET_OPTIMUM_WEAPON
    LDA $F0
    AND #$20        ; #$20 = "両手持ち"
    BEQ .omit_two_handed

    LDX #$0040      ; #$0040 = "両手持ち OK"
    LDA #$02        ; (dest: $7E2CD2)
    JSR GET_OPTIMUM_WEAPON

.omit_two_handed
    LDX #$8080      ; #$8080 = "両手装備をスキップ"
    LDA #$03        ; (dest: $7E2CD3)
    JSR GET_OPTIMUM_WEAPON
    LDA $F0
    AND #$01        ; #$01 = "二刀流"
    BEQ .use_shield ; 二刀流でなければ、左手に盾を装備する

    LDA $7B00,Y     ; Menu buffer
    DEC
    STA $7B00,Y     ; Menu buffer
    LDX #$8080      ; #$8080 = "両手装備をスキップ"
    LDA #$04        ; (dest: $7E2CD4)
    JSR GET_OPTIMUM_WEAPON
    LDA $2CD4       ; 最強装備: 種類[3]: 左手
    BNE .omit_shield; 左手用の武器があれば、盾を装備しない

.use_shield
    LDA #$04        ; (dest: $7E2CD4)
    JSR GET_OPTIMUM_SHIELD

.omit_shield
    REP #$20
    LDA $2CD7       ; 最強装備: 攻撃力[2]: 右手
    AND #$00FF
    STA $E0
    LDA $2CD5       ; 最強装備: 攻撃力[0]: 両手装備
    AND #$00FF
    STA $E2
    LDA $2CD6       ; 最強装備: 攻撃力[1]: 両手持ち
    AND #$00FF
    ASL             ; (攻撃力を2倍にする)
    STA $E4
    LDA $2CD8       ; 最強装備: 攻撃力[3]: 左手
    AND #$00FF
	CLC
    ADC $E0
    CMP $E2
    BMI .check_both ; Branch if (二刀流 < 両手装備)

    CMP $E4
    BMI .two_handed ; Branch if (二刀流 < 両手持ち)

    LDX $2CD3       ; 最強装備: 種類[2]: 二刀流
    BRA .equip

.check_both
    LDA $E2
    CMP $E4
    BMI .two_handed ; Branch if (両手装備 < 両手持ち)

    LDA $2CD1       ; 最強装備: 種類[0]: 両手装備
    BRA .equip_without_shield

.two_handed
    LDA $2CD2       ; 最強装備: 種類[1]: 両手持ち

.equip_without_shield
    AND #$00FF
    TAX

.equip
    STX $2CD1       ; 最強装備: 種類
    JSR $FA75       ; 右手/左手の装備を ($2CD1, $2CD2) に変更する
    RTS
