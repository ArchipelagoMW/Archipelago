# APSudoku Setup Guide

## Required Software
- [APSudoku](https://github.com/APSudoku/APSudoku)

## General Concept

This is a HintGame client, which can connect to any multiworld slot, allowing you to play Sudoku to unlock random hints for that slot's locations.

Does not need to be added at the start of a seed, as it does not create any slots of its own, nor does it have any YAML files.

## Installation Procedures

Go to the latest release from the [APSudoku Releases page](https://github.com/APSudoku/APSudoku/releases/latest). Download and extract the appropriate file for your platform.

## Joining a MultiWorld Game

1. Run the APSudoku executable.
2. Under `Settings` &rarr; `Connection` at the top-right:
	- Enter the server address and port number
	- Enter the name of the slot you wish to connect to
	- Enter the room password (optional)
	- Select DeathLink related settings (optional)
	- Press `Connect`
4. Under the `Sudoku` tab
	- Choose puzzle difficulty
	- Click `Start` to generate a puzzle
5. Try to solve the Sudoku. Click `Check` when done
	- A correct solution rewards you with 1 hint for a location in the world you are connected to
	- An incorrect solution has no penalty, unless DeathLink is enabled (see below)

Info:
- You can set various settings under `Settings` &rarr; `Sudoku`, and can change the colors used under `Settings` &rarr; `Theme`.
- While connected, you can view the `Console` and `Hints` tabs for standard TextClient-like features
- You can also use the `Tracking` tab to view either a basic tracker or a valid [GodotAP tracker pack](https://github.com/EmilyV99/GodotAP/blob/main/tracker_packs/GET_PACKS.md)
- While connected, the number of "unhinted" locations for your slot is shown in the upper-left of the the `Sudoku` tab. (If this reads 0, no further hints can be earned for this slot, as every locations is already hinted)
- Click the various `?` buttons for information on controls/how to play
## DeathLink Support

If `DeathLink` is enabled when you click `Connect`:
- Lose a life if you check an incorrect puzzle (not an _incomplete_ puzzle- if any cells are empty, you get off with a warning), or if you quit a puzzle without solving it (including disconnecting).
- Your life count is customizable (default 0). Dying with 0 lives left kills linked players AND resets your puzzle.
- On receiving a DeathLink from another player, your puzzle resets. 
