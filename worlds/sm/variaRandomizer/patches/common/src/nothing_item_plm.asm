;;; plm used for nothing items
;;;
;;; compile with asar (https://www.smwcentral.net/?a=details&id=14560&p=section),
;;; or a variant of xkas that supports arch directive

lorom
arch snes.cpu

;;; use this 35 bytes unused plms space for the nothing item plm instructions lists:
;;; $BAD1: Unused. Setup ;;;

org $84BAD1
;;; Instruction list for visible/chozo nothing
visible_block_plm_start:
        dw $8724,visible_block_plm_end ; Always go to the end
visible_block_plm_end:
        dw $8724,$DFA9                 ; Go to $DFA9

;;; instruction list for nothing shot block
shot_block_plm_start:
        dw $8A2E,$E007                ; Call $E007 (item shot block)
        dw $8724,shot_block_plm_end   ; Always Go to the end
shot_block_plm_end:
        dw $8A2E,$E032                ; Call $E032 (empty item shot block reconcealing)
        dw $8724,shot_block_plm_start ; Go to start

;;; nothing PLM entries ;;;
print "nothing plm (visible block): ", pc
        dw $EE86,visible_block_plm_start ; Nothing, visible/chozo block
print "nothing plm (shot block): ", pc
        dw $EE86,shot_block_plm_start    ; Nothing, shot block

;;; end of free space
warnpc $84BAF3
