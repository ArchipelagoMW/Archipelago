# Anodyne Randomizer Setup

## Installation

The Anodyne Archipelago Client currently only supports
[the itch.io version](https://pixiecatsupreme.itch.io/anodyne-sharp) of the
game. The Steam version may be supported in the future.

1. Download the Anodyne Archipelago Randomizer from
   [the releases page](https://github.com/SephDB/AnodyneArchipelagoClient/releases).
2. Locate `AnodyneSharp.exe`.
3. Create a folder called `Mods` next to `AnodyneSharp.exe` if it does not
   already exist.
4. Unzip the randomizer into the `Mods` folder.

## Joining a Multiworld game

1. Open Anodyne.
2. Enter your connection details on the main menu. Text must be entered via
   keyboard, even if you are playing on controller.
3. Select "Connect".
4. Enjoy!

To continue an earlier game, you can perform the exact same steps as above. The
randomizer will remember the details of your last nine unique connections.

## Using Universal Tracker

Anodyne has full UT support, including yamlless so setup is minimal.

There is one extra thing you need for the full integration, and that is to download the anodyne-UniversalTracker.zip and select it when UT asks for the pack.
This zip is release-specific and needs to be updated along with the apworld.

It is separate to keep the download size for hosts low, or people who don't want to use UT.

## Frequently Asked Questions

### Will this impact the base game?

The base game can still be played normally by not selecting "Archipelago" from
the main menu. You can also safely remove the randomizer from the `Mods` folder
and add it back later. The randomizer also uses separate save files from the
main game, so your vanilla saves will not be affected either.

### Is my progress saved locally?

The randomizer generates a savefile name based on your Multiworld seed and slot
number, so you should be able to seamlessly switch between multiworlds and even
slots within a multiworld.
