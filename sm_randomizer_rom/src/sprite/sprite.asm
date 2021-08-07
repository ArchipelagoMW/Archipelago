; Big thanks to Artheau for his vision, research, and work to realize the
; super metroid samus sprite patch through his application SpriteSomething.
; This set of changes are based on the source code at
; https://github.com/Artheau/SpriteSomething , in particular the files at:
; - https://github.com/Artheau/SpriteSomething/blob/v1.0.659/source/metroid3/rom.py
; - https://github.com/Artheau/SpriteSomething/blob/v1.0.659/source/metroid3/samus/rom_export.py

incsrc "config.asm"

incsrc "bugfixes.asm"
incsrc "improvements.asm"

incsrc "gfx.asm"
incsrc "palettes.asm"
incsrc "dmadata.asm"

incsrc "dma.asm"
incsrc "gunport.asm"
incsrc "spinjump.asm"
