# Paint

## Where is the options page?

You can read through all the options and generate a YAML [here](../player-options).

## What does randomization do to this game?

Most tools are locked from the start, leaving only the Magnifier and one drawing tool, specified in the game options.
Canvas size is locked and will only expand when the Progressive Canvas Width and Progressive Canvas Height items are
obtained. Additionally, color selection is limited, starting with only a few possible colors but gaining more options
when Progressive Color Depth items are obtained in each of the red, green, and blue components.

Location checks are sent out based on similarity to a target image, measured as a percentage. Every percentage point up
to a maximum set in the game options will send a new check, and the game will be considered done when a certain target
percentage (also set in the game options) is reached.

## What other changes are made to the game?

This project is based on [JS Paint](https://jspaint.app), an open-source remake of Microsoft Paint. Most features will
work similarly to this version but some features have also been removed. Most notably, pasting functionality has been
completely removed to prevent cheating.

With the addition of a second canvas to display the target image, there are some additional features that may not be
intuitive. There are two special functions in the Extras menu to help visualize how to improve your score. Similarity
Mode (shortcut Ctrl+Shift+M) shows the similarity of each portion of the image in grayscale, with white representing
perfect similarity and black representing no similarity. Conversely, Difference Mode (shortcut Ctrl+M) visualizes the
differences between what has been drawn and the target image in full color, showing the direction both hue and
lightness need to shift to match the target. Additionally, once unlocked, the Pick Color tool can be used on both the
main and target canvases.

Custom colors have been streamlined for Archipelago play. The only starting palette options are black and white, but
additional palette slots can be unlocked as Archipelago items. Double-clicking on any palette slot will allow you to
edit the color in that slot directly and shift-clicking a palette slot will allow you to override the slot with your
currently selected color.
