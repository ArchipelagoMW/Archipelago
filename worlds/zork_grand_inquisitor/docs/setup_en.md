# Zork Grand Inquisitor Randomizer Setup Guide

## Requirements

- Windows OS (Hard required. Client is using memory reading / writing through Win32 API)
- A copy of Zork Grand Inquisitor. Only the GOG version is supported. The Steam version can work with some tinkering but
  is not officially supported.
- ScummVM 2.7.1 64-bit (Important: Will not work with any other version. [Direct Download](https://downloads.scummvm.org/frs/scummvm/2.7.1/scummvm-2.7.1-win32-x86_64.zip))
- Archipelago 0.4.4+

## Game Setup Instructions

No game modding is required to play Zork Grand Inquisitor with Archipelago. The client does all the work by attaching to
the game process and reading and manipulating the game state in real-time.

This being said, the game does need to be played through ScummVM 2.7.1, so some configuration is required around that.

### GOG

- Open the directory where you installed Zork Grand Inquisitor. You should see a `Launch Zork Grand Inquisitor`
  shortcut.
- Open the `scummvm` directory. Delete the entire contents of that directory.
- Still inside the `scummvm` directory, unzip the contents of the ScummVM 2.7.1 zip file you downloaded earlier.
- Go back to the directory where you installed Zork Grand Inquisitor.
- Verify that the game still launches when using the `Launch Zork Grand Inquisitor` shortcut.
- Your game is now ready to be played with Archipelago. From now on, you can use the `Launch Zork Grand Inquisitor`
  shortcut to launch the game.

## Joining a Multiworld Game

- Launch Zork Grand Inquisitor and start a new game.
- Open the Archipelago Launcher and click `Zork Grand Inquisitor Client`.
- Using the `Zork Grand Inquisitor Client`:
  - Enter the room's hostname and port number (e.g. `archipelago.gg:54321`) in the top box and press `Connect`.
  - Input your player name at the bottom when prompted and press `Enter`.
  - You should now be connected to the Archipelago room.
  - Next, input `/zork` at the bottom and press `Enter`. This will attach the client to the game process.
  - If the command is successful, you are now ready to play Zork Grand Inquisitor with Archipelago.

## Continuing a Multiworld Game

- Perform the same steps as above, but instead of starting a new game, load your latest save file.
