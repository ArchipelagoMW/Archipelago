;
; ff5_sortplus.asm
;    「せいとん」アルゴリズムの改善 revision 1.1
;
; 解説
;
;    アイテム欄を「せいとん」するアルゴリズムを改善します。これは以下の特徴
;    があります:
;
;    - アイテム欄を種類順に並び替えます
;    - アイテム欄の先頭から 4 行は「せいとん」の影響を受けません
;
;    「せいとん」の種類順は $C6FF80～$C6FF9F で指定できます。また、「せいと
;    ん」の影響を受けないアイテムの数は $C2E019 で変更できます。
;
;    「せいとん」の影響を受けない行には、戦闘中によく使う武器/アイテムを配置
;    することができます。この「せいとん」の影響を受けない行が実装されている
;    こと以外は、ff5_sort.ips と同じです。
;
; 仕様
;
;    * 通常アイテム (0xE0～0xFF) 以外は、アイテム名の 1 文字目を使って整とん
;      します。したがって、通常アイテム以外のすべてのアイテムの名前がアイコ
;      ンで始まっていることを確認してください。1 文字目がアイコンでないアイ
;      テムには対応していません。
;    * 通常アイテム (0xE0～0xFF) のアイコンは無視します。これは「りゅうのも
;      んしょう」「オメガのくんしょう」のような 9 文字すべてを使うアイテムに
;      対応するためです。
;    * オリジナルの「せいとん」と違って、通常アイテムと装備アイテムの間に改
;      行しません。
;
; 使用領域
;
;    $C2E002-$C2E0A7:  166 bytes
;    $C6FF80-$C6FF9F:   32 bytes
;

!ITEM_NOSORT_COUNT = 8
!FILEPOS_ITEMNAME = $D11380


;--------------------------------
; 整とんの種類順を決定する配列 (アイコン)
;--------------------------------
org $C6FF80
    db $FD          ; 通常アイテム (0xE0～0xFF)
    db $E7          ; ナイフ
    db $E3          ; 剣
    db $E8          ; 槍
    db $E9          ; 斧
    db $EA          ; 刀
    db $EB          ; ロッド
    db $EC          ; つえ
    db $ED          ; 弓矢
    db $EE          ; 竪琴
    db $EF          ; むち
    db $F0          ; ベル
    db $FF          ; 空白: ツインランサー, えんげつりん, しゅりけん,
                    ;       ふうましゅりけん, すす, ライジングサン
    db $F1          ; 盾
    db $F2          ; 兜
    db $F3          ; 鎧
    db $F4          ; アクセサリ
    db $00          ; (eof)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)
    db $00          ; (empty)

;--------------------------------
; 「せいとん」の処理
;--------------------------------
org $C2E002
ITEM_SORT:
    PHB
    PHP
    PEA $7E7E
    PLB
    PLB
    REP #$20
    LDX #$0300

.init_item
    DEX
    DEX
    STZ $7F00,X     ; Init $7F00, $8000 and $8100
    BNE .init_item

    SEP #$20
    TXY             ; X and Y = 0
    LDA.b #ITEM_NOSORT_COUNT
    STA $93         ; 整とんしないアイテムの数

.do_sort
    LDA $C6FF80,X
    BEQ .transfer_items

    PHX
    STA $E0         ; 整とん中の種類 = A
    LDX $8E         ; $8E = 0

.next_item
    LDA $93         ; 整とんしないアイテムの数
    BNE .move_unsorted

    LDA $0640,X     ; アイテムの種類[0]
    BEQ .continue   ; 空欄なら、次のアイテムへ

    CMP #$01        ; #$01 = "すで"
    BEQ .continue   ; "すで" なら、次のアイテムへ

    CMP #$80        ; #$80 = "空欄"
    BEQ .continue   ; 0x80 なら、次のアイテムへ

    CMP #$E0        ; #$E0 = "ポーション"
    BCC .check_name ; 0xE0～0xFF でなければ、通常の処理を行う

    LDA #$FD        ; 整とん中の種類が 0xFD ならソートする
    BRA .check_type

.check_name
    PHX
    REP #$20
    AND #$00FF
    STA $E2
    ASL
    ASL
    ASL
    ADC $E2         ; /* CLC omitted */
    TAX             ; X = (アイテムの番号)×9
    SEP #$20
    LDA FILEPOS_ITEMNAME,X
    PLX

.check_type
    CMP $E0         ; アイテム名の一文字目と整とん中の種類を比較して、
    BNE .continue   ; アイテムの種類が異なっていれば、次のアイテムへ

    LDA $0740,X     ; アイテムの個数[0]
    BEQ .continue   ; アイテムの個数が 0 なら、次のアイテムへ

    CMP #$64
    BCC .move_sorted

    LDA #$63        ; アイテムの個数が 100 個以上なら、99 に設定
    BRA .move_sorted

.move_unsorted
    DEC $93         ; 整とんしないアイテムの数
    LDA $0740,X     ; アイテムの個数[0]

.move_sorted
    STA $8100,Y     ; (sorted item count)
    LDA $0640,X     ; アイテムの種類[0]
    STA $8000,Y     ; (sorted item type)
    STZ $0640,X     ; 一致したアイテムは以後の処理では無視する
    LDA $288A,X     ; アイテムの説明[0]
    STA $7F00,Y     ; (sorted item message)
    INY

.continue
    INX
    CPX #$0100      ; アイテム欄の終端まで繰り返す
    BNE .next_item

    PLX
    INX
    BRA .do_sort

.transfer_items
    REP #$20
    LDX #$8000      ; (sorted item type)
    LDY #$0640      ; アイテムの種類[0]
    LDA #$01FF
    MVN $7E,$7E     ; 整とんしたアイテムを転送
    LDX #$7F00      ; (sorted item message)
    LDY #$288A      ; アイテムの説明[0]
    LDA #$00FF
    MVN $7E,$7E     ; 整とんしたアイテムメッセージを転送
    PLP
    PLB
    RTS

;   NOP : NOP : NOP
