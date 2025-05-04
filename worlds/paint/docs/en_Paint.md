# Paint

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

Most tools are locked from the start, leaving only the Magnifier and one drawing tool, specified in the game options.
Canvas size is locked and will only expand when the Progressive Canvas Width and Progressive Canvas Height items are
obtained. Additionally, color selection is limited, starting with only 8 possible colors but gaining more options when
Progressive Color Depth items are obtained in each of the red, green, and blue components.

Location checks are sent out based on similarity to a target image, measured as a percentage. Every percentage point up
to a maximum set in the game options will send a new check, and the game will be considered done when a certain target
percentage (also set in the game options) is reached.

## What other changes are made to the game?

This project is based on [JS Paint](https://jspaint.app), an open-source remake of Microsoft Paint. Most features will
work similarly to this version but some features have also been removed. Most notably, pasting functionality has been
completely removed to prevent cheating.

With the addition of a second canvas to display the target image, there are some additional features that may not be
intuitive. There is a feature in Extras->Difference Mode (shortcut Ctrl+M) that visualizes the differences between
what has been drawn and the target image. Additionally, once unlocked, the Pick Color tool can be used on both the main
and target canvases.
