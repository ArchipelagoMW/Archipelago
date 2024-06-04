# APSudoku Setup Guide

## Required Software
- [APSudoku](https://github.com/EmilyV99/APSudoku)
- Windows (most tested on Win10)
- Other platforms might be able to build from source themselves; and may be included in the future.

## General Concept

This is a HintGame client, which can connect to any multiworld slot, allowing you to play Sudoku to unlock random hints for that slot's locations.

Does not need to be added at the start of a seed, as it does not create any slots of its own, nor does it have any YAML files.

## Installation Procedures

Go to the latest release from the [APSudoku Releases page](https://github.com/EmilyV99/APSudoku/releases). Download and extract the `APSudoku.zip` file.

## Joining a MultiWorld Game

1. Run APSudoku.exe
2. Under the 'Archipelago' tab at the top-right:
	- Enter the server url & port number
	- Enter the name of the slot you wish to connect to
	- Enter the room password (optional)
	- Select DeathLink related settings (optional)
	- Press connect
3. Go back to the 'Sudoku' tab
	- Click the various '?' buttons for information on how to play / control
4. Choose puzzle difficulty
5. Try to solve the Sudoku. Click 'Check' when done.

## DeathLink Support

If 'DeathLink' is enabled when you click 'Connect':
- Lose a life if you check an incorrect puzzle (not an _incomplete_ puzzle- if any cells are empty, you get off with a warning), or quit a puzzle without solving it (including disconnecting).
- Life count customizable (default 0). Dying with 0 lives left kills linked players AND resets your puzzle.
- On receiving a DeathLink from another player, your puzzle resets. 
