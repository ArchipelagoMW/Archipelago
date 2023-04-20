# "OOF" sound customization guide

## What does this feature do?

It replaces the sound effect when Link takes damage. The intended use case for this is custom sprites, but you can use it with any sprite, including the default one.

Due to technical restrictions resulting from limited available memory, there is a limit to how long the sound can be. Using the current method, this limit is **0.394 seconds**. This means that many ideas won't work, and any intelligible speech or anything other than a grunt or simple noise will be too long.

Some examples of what is possible: https://www.youtube.com/watch?v=TYs322kHlc0

## How do I create my own custom sound?

1. Obtain a .wav file with the following specifications: 16-bit signed PCM at 12khz, no longer than 0.394 seconds. You can do this by editing an existing sample using a program like Audacity, or by recording your own. Note that samples can be shrinked or truncated to meet the length requirement, at the expense of sound quality.
2. Use the `--encode` function of the snesbrr tool (https://github.com/boldowa/snesbrr) to encode your .wav file in the proper format (.brr). The .brr file **cannot** exceed 2673 bytes. As long as the input file meets the above specifications, the .brr file should be this size or smaller. If your file is too large, go back to step 1 and make the sample shorter.
3. When running the adjuster GUI, simply select the .brr file you wish to use after clicking the `"OOF" Sound` menu option.
4. You can also do the patch via command line: `python .\LttPAdjuster.py --baserom .\baserom.sfc --oof .\oof.brr .\romtobeadjusted.sfc`, replacing the file names with your files.

## Can I use multiple sounds for composite sprites?

No, this is not technically feasible. You can only use one sound.
