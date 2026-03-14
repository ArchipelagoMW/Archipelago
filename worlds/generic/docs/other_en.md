# Other Games and Tools

This guide provides information on additional community resources, tools, and games that function with Archipelago.

## Community Resources

The Archipelago community is active across several platforms where you can find support, new games, and tools.

### Discord Servers
Archipelago has two primary Discord servers for community interaction, game support, and hosting public games:
- **[Archipelago Official Discord](https://discord.gg/8Z65BR2)**: The main hub for the community, including general discussion, support, and public multiworld hosting.
- **[Archipelago After Dark Discord](https://discord.gg/fqvNCCRsu4)**: An adults-only server for 18+ and unrated content.

Both servers feature an **#apworld-index** channel. These channels are repositories for "APWorlds" — additional game implementations that can be easily added to your Archipelago installation to support more games.

### Documentation
- **[Archipelago Wiki](https://archipelago.miraheze.org/)**: A community-maintained wiki.

## Community Tools

These community-developed tools are frequently used alongside Archipelago to improve the player experience.

### PopTracker
**[PopTracker](https://github.com/black-sliver/PopTracker)** is a universal multi-platform tracking application designed for randomizers. It supports many Archipelago games through tracker packs, providing both manual and automatic tracking capabilities by connecting directly to an Archipelago server or a console/emulator.

## APSudoku

### What is this game?
APSudoku is a HintGame client which can connect to any multiworld slot, allowing you to play Sudoku to unlock random hints for that slot's locations.
It does not need to be added at the start of a seed, as it does not create any slots of its own, nor does it have any YAML files.

### Required Software
- [APSudoku](https://github.com/APSudoku/APSudoku)

### Installation Procedures
#### Windows / Linux
Go to the latest release from the [GitHub APSudoku Releases page](https://github.com/APSudoku/APSudoku/releases/latest). Download and extract the appropriate file for your platform.
#### Web
Go to the [GitHub pages](https://apsudoku.github.io) or [itch.io](https://emilyv99.itch.io/apsudoku) site, and play in the browser.

### Joining a MultiWorld Game
1. Run the APSudoku executable.
2. Under `Settings` &rarr; `Connection` at the top-right:
    - Enter the server address and port number
    - Enter the name of the slot you wish to connect to
    - Enter the room password (optional)
    - Select DeathLink related settings (optional)
    - Press `Connect`
3. Under the `Sudoku` tab:
    - Choose puzzle difficulty
    - Click `Start` to generate a puzzle
4. Try to solve the Sudoku. Click `Check` when done.
    - A correct solution rewards you with 1 hint for a location in the world you are connected to.
    - An incorrect solution has no penalty, unless DeathLink is enabled (see below).

### Additional Information
- You can set various settings under `Settings` &rarr; `Sudoku`, and can change the colors used under `Settings` &rarr; `Theme`.
- While connected, you can view the `Console` and `Hints` tabs for standard TextClient-like features.
- You can also use the `Tracking` tab to view either a basic tracker or a valid [GodotAP tracker pack](https://github.com/EmilyV99/GodotAP/blob/main/tracker_packs/GET_PACKS.md).
- While connected, the number of "unhinted" locations for your slot is shown in the upper-left of the `Sudoku` tab. (If this reads 0, no further hints can be earned for this slot, as every location is already hinted.)
- Click the various `?` buttons for information on controls/how to play.

### Admin Settings
By using the connected room's Admin Password on the Admin Panel tab, you can configure some settings at any time to affect the entire room.
- You can disable APSudoku for the entire room, preventing any hints from being granted.
- You can customize the reward weights for each difficulty, making progression hints more or less likely, and/or adding a chance to get "no hint" after a solve.

### DeathLink Support
If `DeathLink` is enabled when you click `Connect`:
- Lose a life if you check an incorrect puzzle (not an _incomplete_ puzzle — if any cells are empty, you get off with a warning), or if you quit a puzzle without solving it (including disconnecting).
- Your life count is customizable (default 0). Dying with 0 lives left kills linked players AND resets your puzzle.
- On receiving a DeathLink from another player, your puzzle resets.
